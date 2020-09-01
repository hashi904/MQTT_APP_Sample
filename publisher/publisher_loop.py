import paho.mqtt.client as mqtt
from time import sleep
import mqtt_xpath 

#==================
#送信側 (loop)
#==================

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

#ブローカーが切断した時の処理
def on_disconnect(client, userdata, flag, rc):
    #接続時はrc==0
    if rc != 0:
        print("Unexpected disconnection.")

#publishが完了した時の処理
def on_publish(client, userdata, mid):
    print("publish: {0} Completed!".format(mid))

def main():
    #インスタンスの生成
    client = mqtt.Client()
    #接続
    client.on_connect = on_connect
    #切断
    client.on_disconnect = on_disconnect
    #メッセージ送信
    client.on_publish = on_publish
    #接続先の指定 
    client.connect(MQTT_HOST, MQTT_PORT, MQTT_KEEP_ALIVE)
    #通信処理のスタート
    client.loop_start()

    #永遠に繰り返す
    #client.publishの第一引数がtopcsとなる。topicsはsubscriberに合わせること
    #テスト用 iを無限大にincrement
    i=0
    while True:
        #publish_message = "数値を送信::"
        client.publish(MQTT_TOPIC, str(i))
        #0.5秒まつ
        i+=1
        sleep(0.1)

if __name__ == '__main__':
    main()
