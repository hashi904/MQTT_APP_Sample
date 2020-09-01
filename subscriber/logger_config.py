import logging
import logging.handlers
import time

class Logger: 
    def __init__(self, name=__name__):

        # ロガーを取得
        self.lg = logging.getLogger(name)
        #log level DEBUG, INFO, WARNING, ERROR, CRITICAL
        self.lg.setLevel(logging.DEBUG)

        # タイムドローテーティングファイルハンドラを作成し、ロガーに追加
        th = logging.handlers.TimedRotatingFileHandler(
            r'./logs/mqtt_system.log', encoding='utf-8',
            # 'midnight', 'S', 'M', 'H', 'D'
            when='midnight',
            # interval=10,
            # backupCount=3,
            )

        formatter = '%(levelname)s : %(asctime)s : %(message)s'
        th.setFormatter(logging.Formatter(formatter))

        #設定を適用する
        self.lg.addHandler(th)

    def debug(self, msg):
        self.lg.debug(msg)

    def info(self, msg):
        self.lg.info(msg)

    def warn(self, msg):
        self.lg.warning(msg)

    def error(self, msg):
        self.lg.error(msg)

    def critical(self, msg):
        self.lg.critical(msg)
