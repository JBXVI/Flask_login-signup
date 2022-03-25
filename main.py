from flask import Flask, render_template as render, request as req
from flask_pymongo import PyMongo
import time


class Login:
    def __init__(self):
        pass

    def flask_app(self):
        app = Flask(__name__)
        app.config["MONGO_URI"] = "mongodb://localhost:27017/users"
        mongo = PyMongo(app)
        f = mongo.db.users

        @app.route("/", methods=["GET", "POST"])
        def home():
            return render("index.html", message="sign up or login")

        @app.route("/signup", methods=["GET", "POST"])
        def signup():
            if req.method == "POST":
                t = time.localtime()
                current_date = time.strftime("%y:%m:%d")
                current_time = time.strftime("%I:%M:%S:%p")
                username = req.form.get("uname")
                password = req.form.get("pwd")
                signature = req.form.get("msg")
                f.insert_one({"name": username, "password": password, "sign": signature, "date": current_date,
                              "time": current_time})
                if True:
                    return render("index.html", message="Signup completed please Login")
            return render("signup.html")

        @app.route('/login', methods={"GET", "POST"})
        def login():
            if req.method == "POST":
                username = req.form.get("uname")
                password = req.form.get("pwd")
                print(f"username {username} password {password}")
                status = f.find_one({"name": username, "password": password})
                if status != None:
                    message=status["sign"]
                    date = status['time']
                    time=status['date']
                    return render("welcome.html", message=message, date=date,time=time)
                else:
                    return render("index.html", message="no user found please sign up")
            return render("login.html")

        if __name__ == "__main__":
            app.run(debug=False)


login = Login()
login.flask_app()
