import paho.mqtt.client as mqtt
from time import sleep
import mqtt_xpath 
import argparse
import logger_config

#==================
#　送信側
#==================


#loggerのインポート
logger = logger_config.Logger()

# コマンドライン引数の受け取り
parser = argparse.ArgumentParser()
parser.add_argument("--msg",help="message[Type:str or int]")
args = parser.parse_args()
message = args.msg

#messageはstrに変換
if type(args.msg) != str:
    message = str(message)

#xpath　インスタンスを生成
broker_xpath = mqtt_xpath.MqttXpath()
broker_xpath.get_broker_connect_info()

#初期設定
MQTT_HOST = broker_xpath.host
MQTT_PORT = broker_xpath.port
MQTT_TOPIC = broker_xpath.topic

if broker_xpath.mqtt_keep_alive:
    MQTT_KEEP_ALIVE = broker_xpath.mqtt_keep_alive

#ブローカーに接続できたときの処理
def on_connect(client, userdata, flag, rc):
    print("Connected with result code" + str(rc))
    #logger.info("Connected with result code" + str(rc))

#ブローカーが切断した時の処理
def on_disconnect(client, userdata, flag, rc):
    if rc != 0:
        print("Unexpected disconnection.")
        #logger.info("Unexpected disconnection.")

#publishが完了した時の処理
def on_publish(client, userdata, mid):
    print("publish: {0} Completed!".format(mid))
    #logger.info("publish: {0} Completed!".format(mid))

def main():
    #インスタンスの生成
    client = mqtt.Client()
    #接続時
    client.on_connect = on_connect
    #切断時
    client.on_disconnect = on_disconnect
    #メッセージ送信
    client.on_publish = on_publish
    #接続先の指定
    client.connect(MQTT_HOST, MQTT_PORT, MQTT_KEEP_ALIVE)
    #通信スタート
    client.loop_start()
    #メッセージの送信
    client.publish(MQTT_TOPIC, message)
    client.disconnect()

if __name__ == '__main__':
    main()
