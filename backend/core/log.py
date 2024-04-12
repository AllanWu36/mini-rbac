import logging
from logging import handlers

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter("[%(asctime)s] %(levelname)s %(message)s")

#往屏幕上输出
handler = logging.StreamHandler()
handler.setFormatter(formatter)
logger.addHandler(handler)

#往文件里输出
log_file = handlers.TimedRotatingFileHandler(filename="all.log",when="D",backupCount=10,encoding='utf-8')#往文件里写入#指定间隔时间自动生成文件的处理器
#实例化TimedRotatingFileHandler
        #backupCount是备份文件的个数，如果超过这个个数，就会自动删除，when是间隔的时间单位，单位有以下几种：
        # S 秒
        # M 分
        # H 小时、
        # D 天、
        # W 每星期（interval==0时代表星期一）
        # midnight 每天凌晨
log_file.setFormatter(formatter)#设置文件里写入的格式
logger.addHandler(log_file)

