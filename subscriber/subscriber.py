import paho.mqtt.client as mqtt
import mqtt_xpath
import insert_data
import time
from multiprocessing import Manager, Process
import logger_config

#==================================
#受信側
#broker start 
#command line: mosquitto -v
#==================================

#subscriber 設定　インスタンス
subscriber_xpath = mqtt_xpath.MqttXpath()
subscriber_xpath.get_subscriber_conf()

#broker_connect_xpath　インスタンスを生成
broker_xpath = mqtt_xpath.MqttXpath()
broker_xpath.get_broker_connect_info()

#初期設定
MQTT_HOST = broker_xpath.host
MQTT_PORT = broker_xpath.port
MQTT_TOPIC = broker_xpath.topic
MQTT_KEEP_ALIVE = broker_xpath.mqtt_keep_alive

#schema app情報インスタンス
app_xpath = mqtt_xpath.MqttXpath()
app_xpath.get_application_info()

#DB Insertインスタンス
db_insert = insert_data.Insert_data()

#loggerのインポート
logger = logger_config.Logger()

#ブローカーに接続できた時の処理
def on_connect(client, userdata, flag, rc):
    logger.info("Connected broker with result code" + str(rc))
    # print("Connected broker with result code" + str(rc))
    client.subscribe(MQTT_TOPIC)

#ブローカーが切断したときの処理
def on_disconnect(client, userdata, flag, rc):
    if rc != 0:
        logger.info("Unexpected disconnection.")
        # print("Unexpected disconnection.")

#メッセージが届いたときの処理
def on_message(client, userdata, msg):
    topic = msg.topic
    message = msg.payload.decode("UTF-8")
    # print("Recieved::" + "' on topic '" + topic + "' with message '" + message)
    logger.info("Recieved::" + "' on topic '" + topic + "' with message '" + message)
    #受け取ったmessageを配列に格納して返す
    return db_insert.sql_create_value(message, query_value_array_global)

#subscriber実行
def subscriber_execute(no_value_dict, query_value_array):
    global query_value_array_global
    query_value_array_global = query_value_array
    client = mqtt.Client()
    #接続時のコールバック関数の作成
    client.on_connect = on_connect
    #切断時のコールバック関数を作成
    client.on_disconnect = on_disconnect
    #メッセージ到着時のコールバック関数
    client.on_message = on_message
    #接続先のbrokerの指定 (windows app mosquittoに合わせている)
    client.connect(MQTT_HOST, MQTT_PORT, MQTT_KEEP_ALIVE)
    #ループして立ち上げたままにする
    client.loop_forever()

#DBに保存するための処理(別スレッドで実行)実行間隔はconf.xmlで指定
def db_execute(no_value_dict, query_value_array):
    while True:
        if len(query_value_array) > 0:
            logger.info("DB commit前のvalue配列:::" + str(query_value_array))
            # print("DB commit前のvalue配列:::" + str(query_value_array))
            db_insert.sql_execute(query_value_array)
            logger.info("DB commit後のvalue配列:::" + str(query_value_array))
            # print("DB commit後のvalue配列:::" + str(query_value_array))
        time.sleep(subscriber_xpath.commit)

if __name__ == '__main__':
    #プロセス間で変数を共有するためにmanagerオブジェクトからインスタンスを生成
    manager = Manager()
    #空の辞書を定義(multiprocessing libraryの仕様上必要)
    no_value_dict = manager.dict()
    #受け取ったメッセージを格納する配列
    query_value_array = manager.list()
    p1=Process(target=subscriber_execute,args=(no_value_dict, query_value_array))
    p2=Process(target=db_execute,args=(no_value_dict, query_value_array))
    #プロセスの実行
    p1.start()
    p2.start()
    p1.join()
    p2.join()