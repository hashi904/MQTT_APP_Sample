import xml.etree.ElementTree as ET
#============================================
#注意　windowsとMacOSでxpathの指定の仕方が異なる
#============================================
class MqttXpath:
    #クラス変数
    tree = ET.parse('./conf.xml')
    root = tree.getroot()

    def get_application_info(self):
        root = self.root
        self.appid = str(root.findall('.//schema/appid')[0].text)
        self.table = str(root.findall('.//schema/table')[0].text)
        self.column = str(root.findall('.//schema/columns/column')[0].text)
    
    def get_broker_connect_info(self):
        root = self.root
        self.host = str(root.findall('.//broker/host')[0].text)
        self.port = int(root.findall('.//broker/port')[0].text)
        self.mqtt_keep_alive = int(root.findall('.//broker/mqtt_keep_alive')[0].text)
        self.topic = str(root.findall('.//broker/topic')[0].text)

    def get_subscriber_conf(self):
        root = self.root
        self.commit = int(root.findall('.//subscriber/commit')[0].text)

    def get_database_connect_info(self):
        root = self.root
        self.host = str(root.findall('.//database/host')[0].text)
        self.db_port = int(root.findall('.//database/db_port')[0].text)
        self.user = str(root.findall('.//database/user')[0].text)
        self.db_name = str(root.findall('.//database/db_name')[0].text)
        self.password = str(root.findall('.//database/password')[0].text)
        self.connection_retry = int(root.findall('.//database/connection_retry')[0].text)
