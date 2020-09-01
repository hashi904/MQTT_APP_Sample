import mqtt_xpath 
from pg import DB
from pgdb import connect, IntegrityError, InternalError
import random_func
import copy
import logger_config

class Insert_data:

    # global変数の定義
    global db_xpath
    global app_xpath
    global logger
    
    #DB接続インスタンス
    db_xpath = mqtt_xpath.MqttXpath()
    db_xpath.get_database_connect_info()

    #app情報を取得する
    app_xpath = mqtt_xpath.MqttXpath()
    app_xpath.get_application_info()

    #loggerのインポート
    logger = logger_config.Logger()
    
    #受け取ったメッセージを配列に格納してreturnする
    def sql_create_value(self, message, query_value_array):
        #受け取ったメッセージを配列に格納する
        return query_value_array.append(message)

    #SQL実行メソッド
    def sql_execute(self, query_value_array):
        # print("query_value_array"+str(query_value_array))
        logger.info("query_value_array"+str(query_value_array))
        query_value_array_commitment = copy.copy(list(query_value_array))
        #query_value_array_commitmentに格納している間にquery_value_arrayにmessageが追加された時にはquery_value_arrayを空にしない
        while True:
            #query_value_arrayとquery_value_array_commitmentの配列の長さが等しい時のみquery_value_arrayを空にする
            if len(query_value_array) == len(query_value_array_commitment):
                #print("引数配列削除前"+str(query_value_array_commitment))
                #query_value_array_commitment(DBにこれからcommitする分)だけプロセス間共有しているdelete_list_value配列を空にする
                delete_list_value = len(query_value_array_commitment)
                query_value_array[:delete_list_value] = []
                #print("引数配列削除後"+str(query_value_array_commitment))
                break
            else:
                #配列の長さが等しくなければもう一度query_value_arrayに値を入れ直す
                query_value_array_commitment = copy.copy(list(query_value_array))
        # print("queryvaluearray:::"+str(query_value_array_commitment))
        logger.info("queryvaluearray:::"+str(query_value_array_commitment))
        #IDが重複した場合xmlで設定した数だけ処理をやり直す
        for i in range(1, db_xpath.connection_retry + 1):
            try:
                #SQL VALUEを格納する空の変数を定義
                query_value_context = ''

                #SQL VALUEを作成
                for i in range(len(query_value_array_commitment)):
                    ID = random_func.Random_func.random_id_hexadecimal()
                    if i == 0:
                        query_value_context = "(" + "'" + ID +"'" + "," + "'" + query_value_array_commitment[i] + "'" + ")"
                    else:
                        query_value_context = query_value_context + "," + "(" + "'" + ID +"'" + "," + "'" + query_value_array_commitment[i] + "'" + ")"
                #DBに接続
                con = connect(database=db_xpath.db_name, host=db_xpath.host +':'+db_xpath.host, port=db_xpath.db_port, user=db_xpath.user, password=db_xpath.password)
                cursor = con.cursor()

                #SQLの発行
                query= ("""INSERT INTO "%s"."%s"("ID", "%s") VALUES %s""" % (app_xpath.appid, app_xpath.table, app_xpath.column, query_value_context))
                # print("実行SQL文:"+str(query))
                cursor.execute(str(query))
            
            except IntegrityError as e:
                # print(e)
                # print("Execute sql again.")
                logger.error(e)
                logger.error("Execute sql again.")
            
            except InternalError as e:
                #IDが重複した場合の例外処理2
                # print(e)
                # print("Execute sql again.")
                logger.error(e)
                logger.error("Execute sql again.")
            
            else: 
                #SQLcommit
                con.commit()
                # print("SQL COMMITED")
                logger.info("SQL COMMITED")
                con.close()
                # print("SQL CLOSED")
                logger.info("SQL CLOSED")
                #commitしたら終了
                break