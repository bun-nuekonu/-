import os
import sqlite3

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import LoginManager
from datetime import timedelta, date
from dateutil.relativedelta import relativedelta


app = Flask(__name__)

app.config["TEMPLATES_AUTO_RELOAD"] = True


@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config['SECRET_KEY'] = os.urandom(24)
Session(app)

db = SQL("sqlite:///birthday.db")

app.secret_key = 'abcdefghijklmn'
app.permanent_session_lifetime = timedelta(minutes=5)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(userid):
    return User(userid)


@app.route('/')
def index():
    if "user_id" in session:
        birthdays = db.execute("SELECT id, name, year, month, day FROM birthday WHERE user_id = ? ORDER BY month, day", session["user_id"])
        size = len(birthdays)
        return render_template('index.html', birthdays=birthdays, size=size)

    else:
        return render_template('login.html')


@app.route('/add', methods=["GET", "POST"])
def add():
    if "user_id" in session:
        if request.method == "POST":

            if not request.form.get("name"):
                flash("なまえが入力されてないよ！", "failed")
                return render_template("add.html")

            if not request.form.get("month"):
                flash("月が入力されてないよ！", "failed")
                return render_template("add.html")

            if not request.form.get("day"):
                flash("日が入力されてないよ！", "failed")
                return render_template("add.html")

            name = request.form.get("name")
            year = request.form.get("year")
            month = request.form.get("month")
            day = request.form.get("day")

            db.execute("INSERT INTO birthday (user_id, name, year, month, day) VALUES(?, ?, ?, ?, ?)", session["user_id"], name, year, month, day)

            flash("追加完了！", "success")
            return redirect("/")

        else:
            return render_template("add.html")
    else:
        return render_template('login.html')


@app.route('/edit', methods=["GET", "POST"])
def edit():
    if "user_id" in session:
        if request.method == "POST":

            edit_id = request.form.get("edit")
            delete = request.form.get("delete")

            if delete != None:
                return render_template('select.html', delete=delete)

            name = db.execute("SELECT name FROM birthday WHERE id = ?", edit_id)
            year = db.execute("SELECT year FROM birthday WHERE id = ?", edit_id)
            month = db.execute("SELECT month FROM birthday WHERE id = ?", edit_id)
            day = db.execute("SELECT day FROM birthday WHERE id = ?", edit_id)
            memo = db.execute("SELECT memo FROM birthday WHERE id = ?", edit_id)

            name = name[0]['name']
            year = year[0]['year']
            memo = memo[0]['memo']

            if not year == '':
                year = int(year)

            month = int(month[0]['month'])
            day = int(day[0]['day'])

            return render_template("edit.html", name=name, year=year, month=month, day=day, edit_id=edit_id, memo=memo)

        else:
            return render_template("edit.html")
    else:
        return render_template('login.html')


@app.route('/edited', methods=["GET", "POST"])
def edited():
    if "user_id" in session:
        if request.method == "POST":

            new_name = request.form.get("name")
            new_year = request.form.get("year")
            new_month = request.form.get("month")
            new_day = request.form.get("day")
            edit_id = request.form.get("edit")
            memo = request.form.get("memo")

            name = db.execute("SELECT name FROM birthday WHERE id = ?", edit_id)
            year = db.execute("SELECT year FROM birthday WHERE id = ?", edit_id)
            month = db.execute("SELECT month FROM birthday WHERE id = ?", edit_id)
            day = db.execute("SELECT day FROM birthday WHERE id = ?", edit_id)

            name = name[0]['name']
            year = year[0]['year']
            month = month[0]['month']
            day = day[0]['day']

            if not request.form.get("memo"):
                memo = 'ここにメモをいれてね'

            if not request.form.get("name") or request.form.get("name") == name:
                new_name = name

            if not request.form.get("year") and year != '':
                new_year = new_year

            elif request.form.get("year") == year:
                new_year = year

            if not request.form.get("month") or request.form.get("month") == month:
                new_month = month

            if not request.form.get("day") or request.form.get("day") == day:
                new_day = day

            db.execute("UPDATE birthday SET name = ?, year = ?, month = ?, day = ?, memo = ? WHERE id = ?", new_name, new_year, new_month, new_day, memo, edit_id)

            detail_id = edit_id

            name = db.execute("SELECT name FROM birthday WHERE id = ?", detail_id)
            year = db.execute("SELECT year FROM birthday WHERE id = ?", detail_id)
            month = db.execute("SELECT month FROM birthday WHERE id = ?", detail_id)
            day = db.execute("SELECT day FROM birthday WHERE id = ?", detail_id)
            memo = db.execute("SELECT memo FROM birthday WHERE id = ?", detail_id)

            name = name[0]['name']
            year = year[0]['year']
            month = month[0]['month']
            day = day[0]['day']
            memo = memo[0]['memo']

            age = 0

            today = date.today()
            days = 0
            conpare = 0

            if not year == '':

                birthday = date(year, month, day)
                age = relativedelta(today, birthday)

            if today < date(today.year, month, day):
                conpare = date(today.year, month, day)
                days = conpare - today
            else:
                next_year = today.year + 1
                conpare = date(next_year, month, day)
                days = conpare - today

            flash("変更完了！", "success")
            return render_template("detail.html", name=name, year=year, month=month, day=day, age=age, detail_id=detail_id, memo=memo, days=days)

        else:
            return render_template("edit.html")
    else:
        return render_template('login.html')


@app.route("/detail", methods=["GET", "POST"])
def detail():
    if "user_id" in session:
        if request.method == "POST":

            detail_id = request.form.get("detail")

            name = db.execute("SELECT name FROM birthday WHERE id = ?", detail_id)
            year = db.execute("SELECT year FROM birthday WHERE id = ?", detail_id)
            month = db.execute("SELECT month FROM birthday WHERE id = ?", detail_id)
            day = db.execute("SELECT day FROM birthday WHERE id = ?", detail_id)
            memo = db.execute("SELECT memo FROM birthday WHERE id = ?", detail_id)

            name = name[0]['name']
            year = year[0]['year']
            month = month[0]['month']
            day = day[0]['day']
            memo = memo[0]['memo']

            age = 0

            today = date.today()
            days = 0
            conpare = 0

            if not year == '':
                birthday = date(year, month, day)
                age = relativedelta(today, birthday)

            if today < date(today.year, month, day):
                conpare = date(today.year, month, day)
                days = conpare - today
            else:
                next_year = today.year + 1
                conpare = date(next_year, month, day)
                days = conpare - today

            return render_template("detail.html", name=name, year=year, month=month, day=day, age=age, detail_id=detail_id, memo=memo, days=days)

        else:
            return render_template("detail.html")
    else:
        return render_template('login.html')


@app.route('/delete', methods=["GET", "POST"])
def delete():
    if "user_id" in session:
        if request.method == "POST":

            if request.form.get("yes") != None:
                yes = request.form.get("yes")

                db.execute("DELETE FROM birthday WHERE user_id = ? AND id = ?", session["user_id"], yes)

                flash("削除しました！", "success")
                return redirect("/")

            detail_id = request.form.get("no")

            name = db.execute("SELECT name FROM birthday WHERE id = ?", detail_id)
            year = db.execute("SELECT year FROM birthday WHERE id = ?", detail_id)
            month = db.execute("SELECT month FROM birthday WHERE id = ?", detail_id)
            day = db.execute("SELECT day FROM birthday WHERE id = ?", detail_id)
            memo = db.execute("SELECT memo FROM birthday WHERE id = ?", detail_id)

            name = name[0]['name']
            year = year[0]['year']
            month = month[0]['month']
            day = day[0]['day']
            memo = memo[0]['memo']

            age = 0

            today = date.today()
            days = 0
            conpare = 0

            if not year == '':

                birthday = date(year, month, day)
                age = relativedelta(today, birthday)

            if today < date(today.year, month, day):
                conpare = date(today.year, month, day)
                days = conpare - today
            else:
                next_year = today.year + 1
                conpare = date(next_year, month, day)
                days = conpare - today

            return render_template("detail.html", name=name, year=year, month=month, day=day, age=age, detail_id=detail_id, memo=memo, days=days)

        else:
            return render_template("detail.html")
    else:
        return render_template('login.html')

@app.route('/setting', methods=["GET", "POST"])
def setting():
    if "user_id" in session:
        if request.method == "POST":

            username = db.execute("SELECT username FROM users WHERE id = ?", session["user_id"])

            username = username[0]['username']

            if request.form.get("usage") != None:
                return render_template("usage.html")

            if request.form.get("birthdelete") != None:
                return render_template("birthday_delete.html")

            elif request.form.get("change") != None:
                return render_template("change.html", username=username)

            elif request.form.get("delete") != None:
                return render_template("important_select.html")

        else:
            return render_template("setting.html")
    else:
        return render_template('login.html')


@app.route('/change', methods=["GET", "POST"])
def change():
    if "user_id" in session:
        if request.method == "POST":

            username = request.form.get("change")
            old_name = db.execute("SELECT username FROM users WHERE id = ?", session["user_id"])

            old_name = old_name[0]['username']

            if not request.form.get("change") or username == old_name:
                flash("なまえの変更をキャンセルしました！", "failed")
                return render_template("setting.html")

            for i in range(len(username)):
                if username[i].isspace():
                    flash("入力できない文字が含まれています", "failed")
                    return render_template("change.html", username=username)

            db.execute("UPDATE users SET username = ? WHERE id = ?", username, session["user_id"])

            flash(f"なまえを変更しました、{username}さん！", "success")
            return render_template("setting.html")

        else:
            return render_template("setting.html")
    else:
        return render_template('login.html')


@app.route('/birthday_delete', methods=["GET", "POST"])
def birthday_delete():
    if "user_id" in session:
        if request.method == "POST":

            if request.form.get("yes") != None:
                db.execute("DELETE FROM birthday WHERE user_id = ?", session["user_id"])
                flash("誕生日を全削除しました！", "success")
                return redirect("/")

            else:
                return render_template("setting.html")
        else:
            return render_template("setting.html")
    else:
        return render_template('login.html')


@app.route('/account_delete', methods=["GET", "POST"])
def account_delete():
    if "user_id" in session:
        if request.method == "POST":

            if request.form.get("yes") != None:
                yes = request.form.get("yes")

                db.execute("DELETE FROM birthday WHERE user_id = ?", session["user_id"])
                db.execute("DELETE FROM users WHERE id =?", session["user_id"])

                session.clear()
                flash("アカウントを削除しました", "failed")
                return redirect("/")

            else:
                return render_template("setting.html")

        else:
            return render_template("setting.html")
    else:
        return render_template('login.html')


@app.route("/login", methods=["GET", "POST"])
def login():

    session.clear()

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        if not request.form.get("username"):
            flash("なまえが入力されてないよ！", "failed")
            return render_template("login.html", username=username)

        elif not request.form.get("password"):
            flash("パスワードが入力されてないよ！", "failed")
            return render_template("login.html", username=username)

        for i in range(len(username)):
            if username[i].isspace():
                flash("入力できない文字が含まれています", "failed")
                return render_template("login.html", username=username)

        for i in range(len(password)):
            if password[i].isspace():
                flash("入力できない文字が含まれています", "failed")
                return render_template("login.html", username=username)

        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            flash("入力が正しくないよ！", "failed")
            return render_template("login.html", username=username)

        session["user_id"] = rows[0]["id"]

        flash(f"{username}さん、おかえりなさい！", "success")
        return redirect("/")

    else:
        return render_template("login.html")


@app.route("/logout")
def logout():

    session.clear()

    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        if not request.form.get("username"):
            flash("なまえが入力されてないよ！", "failed")
            return render_template("register.html", username=username)

        elif not request.form.get("password"):
            flash("パスワードが入力されてないよ！", "failed")
            return render_template("register.html", username=username)

        elif request.form.get("password") != request.form.get("confirmation"):
            flash("パスワードが一致しないよ！", "failed")
            return render_template("register.html", username=username)

        for i in range(len(username)):
            if username[i].isspace():
                flash("入力できない文字が含まれています", "failed")
                return render_template("register.html", username=username)

        for i in range(len(password)):
            if password[i].isspace():
                flash("入力できない文字が含まれています", "failed")
                return render_template("register.html", username=username)

        password = generate_password_hash(request.form.get("password"))

        registered = db.execute("SELECT username FROM users")
        name_list = []
        for i in range(len(registered)):
            name_list.append(registered[i]['username'])

        if username in name_list:
            flash("このなまえは使用されているよ！", "failed")
            return render_template("register.html", username=username)

        db.execute("INSERT INTO users(username, hash) VALUES(?, ?)", username, password)
        rows = db.execute("SELECT * FROM users WHERE username = ?", username)

        session["user_id"] = rows[0]["id"]

        flash(f"{username}さん、ようこそ！", "success")
        return redirect("/")

    else:
        return render_template("register.html")


if __name__ == "__main__":
    app.run(debug=True)