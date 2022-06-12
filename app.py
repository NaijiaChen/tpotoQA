from flask import Flask, render_template, request, session, redirect, url_for, jsonify 
import sqlite3, hashlib, os
import httpx
from werkzeug.utils import secure_filename
from IPython.display import HTML, display, clear_output
import json

app = Flask(__name__)
app.secret_key = 'random string'


# 獲取登錄情況
def getLoginDetails():
    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        if 'uid' not in session:
            loggedIn = False
            noOfQA = 0
            firstName = ''
        else:
            loggedIn = True
            cur.execute("SELECT count(qid) FROM QA WHERE uid = ' " + str(session['uid']) +"'")
            noOfQA = cur.fetchone()[0]
            cur.execute("SELECT firstName FROM Users WHERE uid = ' " + str(session['uid']) +"'")
            firstName = cur.fetchone()
    conn.close()
    return (loggedIn, firstName, noOfQA)

# 主頁
@app.route('/')
def root():
    loggedIn, firstName, noOfQA= getLoginDetails()
    json_url = './tpotoQA/Character.json'
    json_file = open(json_url, 'r', encoding="utf-8")
    config = json.loads(json_file.read())
    json_file.close()
    return render_template("index.html", loggedIn=loggedIn, firstName=firstName, noOfQA=noOfQA, config=config)

# 問答頁面
@app.route('/question',methods=['GET','POST'])
def question():
    if request.method == "GET": 
        return render_template("question.html")
    if request.method == "POST": 
        content=request.form.get('content')
        question=request.form.get('question')
        uid = session['uid']
        url = "https://pu.ap-mic.com/qa";
        data = {"content":content[:2000], "question":question}
        r = httpx.post(url, json = data, timeout=300)
        answer = r.json()['answer']
        if answer:
            with sqlite3.connect('database.db') as con:
                try:      
                    cur = con.cursor()
                    cur.execute('SELECT COUNT(*) from QA')
                    results = cur.fetchone()[0]+1


                    cur.execute('INSERT INTO QA (qid, uid, ques, ans) VALUES (?, ?, ?, ?)', (results, uid, question, answer))
                    con.commit()
                    msg = "Save Successfully"
                except:
                    con.rollback()
                    msg = "Error occured"
            con.close()
            return jsonify({'output':answer}) 
        return jsonify({'error' : 'Missing data!'})
    return render_template("question.html")

###TODO:刪除歷史問答###
@app.route("/removeFromQA")
def removeFromQA():  
    uid = session['uid']
    qid = int(request.args.get('qid'))
    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()

        try:
            cur.execute("DELETE FROM QA WHERE uid = " + str(uid) + " AND qid = " + str(qid))
            conn.commit()
            msg = "removed successfully"
        except:
            conn.rollback()
            msg = "error occured"
    conn.close()
    return redirect(url_for('historyQA'))


# 歷史問答
@app.route("/historyQA")
def historyQA():
    loggedIn, firstName, noOfQA= getLoginDetails()
    uid = session['uid']
    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        cur.execute("SELECT qid, star, ques, ans from QA where uid = '" + str(uid)+"'")
        QA = cur.fetchall()
        
    return render_template("historyQA.html", QA = QA, loggedIn=loggedIn, firstName=firstName, noOfQA=noOfQA)

# 反饋表格？
@app.route("/feedbackForm")
def feedbackForm():
    loggedIn, firstName, noOfQA= getLoginDetails()
    uid = session['uid']
    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        cur.execute("SELECT qid, star, ques, ans from QA where uid = '" + str(uid)+"'")
        QA = cur.fetchall()
    return render_template("feedback.html", loggedIn=loggedIn, firstName=firstName, noOfQA=noOfQA)

# 反饋界面
@app.route("/feedback", methods = ['GET', 'POST'])
def feedback():
    loggedIn, firstName, noOfQA= getLoginDetails()
    
    if request.method == 'POST':
        #Parse form data    
        ftype = request.form['ftype']
        ftext = request.form['ftext']
        uid = session['uid']
        with sqlite3.connect('database.db') as con:
            try:
                cur = con.cursor()
                cur.execute('INSERT INTO  feedback (ftype, ftext, uid) VALUES (?, ?, ?)', (ftype, ftext, uid))

                con.commit()

                msg = "Feedback Successfully"
            except:
                con.rollback()
                msg = "Error occured"
        con.close()
        return render_template("feedback.html", error=msg)
    
# 跳轉登錄界面（檢查是否已經登錄）
@app.route("/loginForm")
def loginForm():
    if 'uid' in session:
        return redirect(url_for('root'))
    else:
        return render_template('login.html', error='')

# 從登錄界面返回主頁
@app.route("/goHomeFromLogin")
def goHomeFromLogin():
    return redirect(url_for('root'))
# 從註冊界面返回主頁
@app.route("/goHomeFromRegister")
def goHomeFromRegister():
    return redirect(url_for('root'))
# 登錄
@app.route("/login", methods = ['POST', 'GET'])
def login():
    if request.method == 'POST':
        uid = request.form['uid']
        password = request.form['password']
        if is_valid(uid, password):
            session['uid'] = uid
            return redirect(url_for('root'))
        else:
            error = 'Invalid UserId / Password'
            return render_template('login.html', error=error)
# 登出
@app.route("/logout")
def logout():
    session.pop('uid', None)
    return redirect(url_for('root'))

#id和密碼是否存在于資料庫中
def is_valid(email, password):
    con = sqlite3.connect('database.db')
    cur = con.cursor()
    cur.execute('SELECT uid, password FROM users')
    data = cur.fetchall()
    for row in data:
        if row[0] == str(email) and row[1] == hashlib.md5(password.encode()).hexdigest():
            return True
    return False

#註冊
@app.route("/register", methods = ['GET', 'POST'])
def register():
    if request.method == 'POST':
        #Parse form data    
        uid = request.form['uid']
        password = request.form['password']
        firstName = request.form['firstName']
        address = request.form['address']
        country = request.form['country']
        phone = request.form['phone']

        with sqlite3.connect('database.db') as con:
            try:
                cur = con.cursor()
                cur.execute('INSERT INTO users (password, uid, firstName, address, country, phone) VALUES (?, ?, ?, ?, ?, ?)', (hashlib.md5(password.encode()).hexdigest(), uid, firstName, address,  country, phone))

                con.commit()

                msg = "Registered Successfully"
            except:
                con.rollback()
                msg = "Error occured"
        con.close()
        return render_template("login.html", error=msg)

@app.route("/registerationForm")
def registrationForm():
    return render_template("register.html")

if __name__ == '__main__':
    app.run(debug=True)