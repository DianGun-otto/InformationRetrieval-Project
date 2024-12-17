import json
from elasticsearch import Elasticsearch
from sklearn.feature_extraction.text import TfidfVectorizer
from index import INDEX_NAME

es = Elasticsearch(["http://localhost:9200"])

# 读取 URL 到 HTML 路径的映射
def load_url_to_html_paths():
    with open("url_to_html_paths.json", "r", encoding="utf-8") as f:
        url_to_html_paths = json.load(f)
        # 替换反斜杠为正斜杠
        url_to_html_paths = {k: v.replace("\\", "/") for k, v in url_to_html_paths.items()}
        return url_to_html_paths


url_to_html_paths = load_url_to_html_paths()

# 查询函数，支持个性化排序
def search(query, num_results=10, user_preferences=None):
    vectorizer = TfidfVectorizer(stop_words='english')

    # 执行 Elasticsearch 查询
    res = es.search(index=INDEX_NAME, body={
        "query": {
            "multi_match": {
                "query": query,
                "fields": ["title", "content", "anchors"]
            }
        },
        "_source": ["title", "url", "content", "anchors", "pagerank"]
    })

    hits = res['hits']['hits']
    documents = [hit['_source'] for hit in hits]
    contents = [doc['content'] for doc in documents]

    # 计算 TF-IDF
    tfidf_matrix = vectorizer.fit_transform(contents)
    query_vec = vectorizer.transform([query])

    cosine_similarities = (tfidf_matrix * query_vec.T).toarray()
    page_ranks = [doc.get('pagerank', 0) for doc in documents]

    scores = []
    for i in range(len(cosine_similarities)):
        score = cosine_similarities[i][0] + page_ranks[i]

        if user_preferences and user_preferences.get('category'):
            if user_preferences['category'] in documents[i]['content']:
                score += 0.5  # 提高相关内容的分数
        scores.append((i, score))

    # 排序并返回前 N 个结果
    sorted_scores = sorted(scores, key=lambda x: x[1], reverse=True)
    ranked_documents = [documents[i] for i, _ in sorted_scores[:num_results]]

    # # 为每个搜索结果添加本地 HTML 快照路径
    # for doc in ranked_documents:
    #     url = doc.get('url')
    #     if url in url_to_html_paths:
    #         doc['snapshot_path'] = url_to_html_paths[url]
    #     else:
    #         doc['snapshot_path'] = None  # 如果没有找到对应的 HTML 快照

    # 为每个搜索结果添加本地 HTML 快照路径
    for doc in ranked_documents:
        url = doc.get('url')
        if url in url_to_html_paths:
            snapshot_path = url_to_html_paths[url]
            # 使用 flask 的 static 生成正确的路径
            doc['snapshot_path'] = f"/static/{snapshot_path}"
        else:
            doc['snapshot_path'] = None  # 如果没有找到对应的 HTML 快照

    return ranked_documents
