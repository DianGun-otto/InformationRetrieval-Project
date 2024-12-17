# getpage.py
# 爬取网页快照（html文件）
import json
import requests
import re
from pathlib import Path

# 读取 JSON 文件
def load_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

# 获取网页内容
def fetch_webpage(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # 如果请求失败，会抛出异常
        response.encoding = response.apparent_encoding  # 根据内容自动调整编码方式
        return response.text  # 返回网页的 HTML 内容
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None

# 将 URL 转换为合法的文件名
def sanitize_filename(url):
    # 使用正则表达式移除 URL 中的不合法字符
    filename = re.sub(r'[\\/*?:"<>|]', '_', url)
    # 如果 URL 最后是斜杠 /，则默认文件名为 index.html
    if filename.endswith('/'):
        filename += 'index'
    return filename

# 保存为 HTML 文件
def save_as_html(url, content, output_dir):
    # 获取清理后的 URL 文件名
    filename = sanitize_filename(url) + '.html'
    file_path = Path(output_dir) / filename
    
    try:
        # 在文件内容的 <head> 中加入基本的 meta 信息，确保网页编码正确
        head = '''<head>
                    <meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <title>Web Snapshot</title>
                  </head>'''
        # 合并网页内容和 head 部分
        full_content = f'<!DOCTYPE html>\n<html>{head}\n<body>{content}</body></html>'
        
        # 保存网页内容为 HTML 文件
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(full_content)
        return str(file_path)  # 返回保存的文件路径
    except Exception as e:
        print(f"Error saving {url} as HTML: {e}")
        return None

# 主函数
def main(json_file, output_dir, output_json):
    data = load_json(json_file)
    
    # 存储 URL 与文件路径的映射
    url_to_html_path = {}
    
    for item in data:
        url = item.get('url')
        if url:
            # 获取网页内容
            webpage_content = fetch_webpage(url)
            if webpage_content:
                # 保存为 HTML 文件并获取路径
                html_file_path = save_as_html(url, webpage_content, output_dir)
                if html_file_path:
                    # 将 URL 和对应的 HTML 文件路径存储在字典中x
                    url_to_html_path[url] = html_file_path
    
    # 将 URL 与 HTML 文件路径映射保存为 JSON 文件
    try:
        with open(output_json, 'w', encoding='utf-8') as f:
            json.dump(url_to_html_path, f, ensure_ascii=False, indent=4)
        print(f"URLs and HTML file paths have been saved to {output_json}")
    except Exception as e:
        print(f"Error saving URL to HTML path mapping: {e}")

if __name__ == "__main__":
    # 设置 JSON 文件路径和输出目录
    json_file = "cleaned_data.json"  # 假设你的 JSON 文件名为 'webpages.json'
    output_dir = "../output_html_files"  # 输出 HTML 文件的目录
    output_json = "../url_to_html_paths.json"  # 保存 URL 和 HTML 文件路径映射的 JSON 文件

    # 确保输出目录存在
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    # 执行主函数
    main(json_file, output_dir, output_json)
