from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from search import search  # 引入搜索功能
import json
import os
import time

app = Flask(__name__, static_folder='/', static_url_path='/static')

app.secret_key = os.urandom(24)  # 用于 Flask session 的密钥

USER_DATA_FILE = "user_data.json"

# 加载用户数据
def load_user_data():
    if os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

# 保存用户数据
def save_user_data(data):
    with open(USER_DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

# 个性化推荐函数
def get_recommendations(query, user_data, username):
    user_history = user_data.get(username, {}).get("history", [])
    recommendations = []

    # 根据历史记录匹配关键词
    for history in user_history:
        if query.lower() in history['query'].lower():
            # 根据历史记录查询中包含的关键词，返回相关文档
            results = search(history['query'], num_results=5, user_preferences={})
            recommendations.extend(results)

    # 去重并返回推荐的文档
    unique_recommendations = {rec['title']: rec for rec in recommendations}.values()
    return list(unique_recommendations)

# 搜索界面
@app.route("/", methods=["GET", "POST"])
def index():
    if "username" not in session:
        return redirect(url_for("login"))

    user_data = load_user_data()
    username = session["username"]
    user_preferences = user_data.get(username, {}).get("preferences", {})
    query_history = user_data.get(username, {}).get("history", [])

    if request.method == "POST":
        query = request.form["query"]
        user_preferences = {"category": request.form.get("category", "")}
        user_data[username]["preferences"] = user_preferences
        save_user_data(user_data)

        results = search(query, num_results=15, user_preferences=user_preferences)

        # 保存查询历史
        query_history.append({
            "query": query,
            "timestamp": time.time()
        })
        user_data[username]["history"] = query_history
        save_user_data(user_data)

        return render_template("index.html", results=results, user_preferences=user_preferences, query_history=query_history, enumerate=enumerate)

    return render_template("index.html", query_history=query_history, user_preferences=user_preferences, enumerate=enumerate)

# 推荐功能
@app.route("/recommend", methods=["GET"])
def recommend():
    query = request.args.get('query', '')
    if 'username' not in session:
        return jsonify({'recommendations': []})
    
    user_data = load_user_data()
    username = session['username']
    
    recommendations = get_recommendations(query, user_data, username)
    return jsonify({'recommendations': recommendations})

# 登录页面
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        
        user_data = load_user_data()
        
        if username in user_data and user_data[username]["password"] == password:
            session["username"] = username
            return redirect(url_for("index"))
        else:
            flash("用户名或密码错误！")
    
    return render_template("login.html")

# 注册页面
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        preferences = request.form["preferences"]

        user_data = load_user_data()
        
        if username not in user_data:
            user_data[username] = {
                "password": password,
                "preferences": {"category": preferences},
                "history": []
            }
            save_user_data(user_data)
            flash("注册成功！请登录。")
            return redirect(url_for("login"))
        else:
            flash("用户名已存在！")
    
    return render_template("register.html")

# 退出登录
@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("login"))

# 删除查询历史
@app.route("/delete_history/<int:index>")
def delete_history(index):
    if "username" not in session:
        return redirect(url_for("login"))
    
    user_data = load_user_data()
    username = session["username"]
    user_data[username]["history"].pop(index)
    save_user_data(user_data)
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
