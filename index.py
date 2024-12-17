# index.py
# Elasticsearch 索引构建和数据上传

from elasticsearch import Elasticsearch, helpers
import json

es = Elasticsearch(["http://localhost:9200"])
INDEX_NAME = "nankai_pages"

# 删除现有索引并重新创建索引
def create_index():
    if es.indices.exists(index=INDEX_NAME):
        print(f"Index {INDEX_NAME} exists. Deleting and recreating...")
        es.indices.delete(index=INDEX_NAME)
    
    mappings = {
        "mappings": {
            "properties": {
                "title": {"type": "text", "analyzer": "standard"},  # 页面标题，使用标准分词器
                "url": {"type": "keyword"},  # URL，使用 keyword 类型以提高精确匹配
                "content": {"type": "text", "analyzer": "standard"},  # 页面内容，使用标准分词器
                "anchors": {"type": "text", "analyzer": "standard"},  # 锚文本，使用标准分词器
                "pagerank": {"type": "float"}  # PageRank 权重，浮动类型
            }
        }
    }

    es.indices.create(index=INDEX_NAME, body=mappings)
    print(f"Index {INDEX_NAME} created successfully.")

# 批量上传数据到 Elasticsearch
def bulk_index_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    actions = [
        {
            "_op_type": "index",
            "_index": INDEX_NAME,
            "_source": item
        }
        for item in data
    ]

    helpers.bulk(es, actions)
    print("Data indexed successfully.")

if __name__ == "__main__":
    create_index()
    bulk_index_data('data/cleaned_data.json')
