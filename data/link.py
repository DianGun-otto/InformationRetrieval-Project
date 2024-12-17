# link.py
# 用于pageRank，链接分析
import json
from bs4 import BeautifulSoup
import requests

# 加载原始JSON文件
with open('cleaned_data.json', 'r', encoding='utf-8') as f:
    webpages = json.load(f)

# 添加link字段：假设我们有一个网页的列表以及其URL，爬取链接
for page in webpages:
    url = page['url']
    try:
        # 请求页面内容
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 提取页面中的所有链接
        links = [a['href'] for a in soup.find_all('a', href=True)]
        
        # 更新当前网页的link字段
        page['link'] = links
    except Exception as e:
        print(f"Error processing {url}: {e}")
        page['link'] = []

# 将更新后的结果保存到新的JSON文件中
with open('cleaned_data_with_links.json', 'w', encoding='utf-8') as f:
    json.dump(webpages, f, ensure_ascii=False, indent=4)
