# settings.py

LOG_ENABLED = False
BOT_NAME = 'nankai_search_engine'

SPIDER_MODULES = ['nankai_search_engine.spiders']
NEWSPIDER_MODULE = 'nankai_search_engine.spiders'

USER_AGENT = 'nankai_search_engine (+http://www.yourdomain.com)'

ROBOTSTXT_OBEY = False  # 不遵守 robots.txt 文件

# 下载延迟设置，避免过于频繁的请求
DOWNLOAD_DELAY = 0.5

# 存储抓取的 JSON 数据
FEED_FORMAT = 'json'

FEED_URI = '../data/data.json'  # 数据存储路径，按时间自动生成文件名

FEED_EXPORT_ENCODING = 'utf-8'  # 设置输出文件的编码格式为 UTF-8

DEFAULT_REQUEST_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.9',  # 如果目标网站主要使用中文内容
}

# 最大并发请求数
CONCURRENT_REQUESTS = 128

# 防止程序崩溃丢失数据
AUTOTHROTTLE_ENABLED = True  # 开启自动调节下载速度
AUTOTHROTTLE_START_DELAY = 1
AUTOTHROTTLE_MAX_DELAY = 10
AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0

# 防止 IP 被封禁
DOWNLOAD_TIMEOUT = 10  # 设置请求超时
RETRY_ENABLED = True
RETRY_TIMES = 3  # 设置最大重试次数
