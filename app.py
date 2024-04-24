
from cs50 import SQL
from flask import Flask, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime


app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)




db = SQL("sqlite:///haksulang.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login", methods = ["GET", "POST"])
def login():
    
    session.clear()
    
    if request.method == "POST":
        # 로그인 할때 user_id 가 없다면 403오류
        if not request.form.get("user_id"): 
            return render_template("error.html") 

        # password가 없다면 403오류
        elif not request.form.get("password"): 
            return render_template("error.html")

        # 로그인 할려는 db 정보를 긁어 옴 user_id를
        rows = db.execute(
            "SELECT * FROM user WHERE user_id = ?", request.form.get("user_id")
        )
        # 해시 확인해서 맞으면 로그인 ㄱㄱ
        if len(rows) != 1 or not check_password_hash(
            rows[0]["password"], request.form.get("password")
        ):
            return render_template("error.html")

        # 세션에 user_id에 id를 집어넣음
        session["user_id"] = rows[0]["id"]

        # 로그인 성공하면 메인 페이지로 ㄱㄱ
        return redirect("/")

    # get으로 요청보내오면 바로 홈페이지로 ㄱㄱ
    else:
        return render_template("login.html")
    
#db.execute("insert")
#return render_template("login.html")


# 회원가입 로직
@app.route("/register", methods = ["GET", "POST"])
def register():
    if request.method == "POST":
        user_name = request.form.get("user_name")
        user_id = request.form.get("user_id")
        user_password_1 = request.form.get("user_password_1")
        user_password_2 = request.form.get("user_password_2")
        
        if user_name and user_id and user_password_1 and user_password_2: # 이름, ID, password1, password2 칸이 비어있다면 에러 발생
            if user_password_1 == user_password_2:# password1 , password2 가 다르다면 에러 발생
               hash_password = generate_password_hash(user_password_1) # password1 password2 가 같다면 password 를 해시값으로 변경함
               db.execute("insert into user (name, user_id, password) values (?,?,?)", user_name,user_id,hash_password) # db에 집어넣음
               print(user_name)
               return render_template("index.html")
            else:
                return render_template("register.html")
        else:
            return render_template("register.html")       
    else:
        return render_template("register.html")


