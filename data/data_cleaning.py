import json
from bs4 import BeautifulSoup
import re
import jieba
import ijson

# 停用词文件路径
STOPWORDS_PATH = 'stopwords.txt'

# 读取停用词
def load_stopwords():
    with open(STOPWORDS_PATH, 'r', encoding='utf-8') as f:
        stopwords = set(f.read().splitlines())
    return stopwords

# 清洗HTML文本，去除HTML标签
def clean_text(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    text = soup.get_text()  # 提取纯文本
    return text

# 分词并去除停用词
def tokenize_and_remove_stopwords(text, stopwords):
    words = jieba.cut(text)  # 分词
    words = [word for word in words if word not in stopwords and len(word) > 1]  # 去除停用词和单个字符的词
    return ' '.join(words)

# 处理单条数据并清洗
def process_item(item, stopwords):
    # 去除HTML标签
    text = clean_text(item['content'])
    # 分词并去除停用词
    item['content'] = tokenize_and_remove_stopwords(text, stopwords)
    return item

# 清理数据
def clean_data(input_file, output_file):
    stopwords = load_stopwords()  # 加载停用词

    with open(output_file, 'w', encoding='utf-8') as output_f:
        output_f.write('[\n')  # JSON数组开始

        first_item = True
        # 使用 ijson 逐行读取大文件
        with open(input_file, 'r', encoding='utf-8') as f:
            objects = ijson.items(f, 'item')  # 假设 JSON 数据是一个数组，根元素为 "item"
            for item in objects:
                # 处理数据
                cleaned_item = process_item(item, stopwords)

                # 写入处理后的数据到输出文件
                if first_item:
                    first_item = False
                else:
                    output_f.write(',\n')
                json.dump(cleaned_item, output_f, ensure_ascii=False, indent=4)

        output_f.write('\n]')  # JSON数组结束

if __name__ == "__main__":
    clean_data('test.json', 'test_clean.json')
