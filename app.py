from flask import Flask, render_template, request, session, redirect, url_for
import sqlite3, hashlib, os
import httpx
from werkzeug.utils import secure_filename
from IPython.display import HTML, display, clear_output

app = Flask(__name__)
app.secret_key = 'random string'


def getLoginDetails():
    with sqlite3.connect('database.db') as conn:
        uid = 1
        session['uid'] = 1
        cur = conn.cursor()
        """
        if 'email' not in session:
            loggedIn = False
            firstName = ''
            noOfItems = 0
        else:
        """
        loggedIn = True
        cur.execute("SELECT count(qid) FROM QA WHERE uid = " + "1")
        noOfQA = cur.fetchone()[0]
    conn.close()
    return (loggedIn, uid, noOfQA)

@app.route('/')
def root():
    loggedIn, uid, noOfQA= getLoginDetails()
    return render_template("index.html", loggedIn=loggedIn, uid=uid, noOfQA=noOfQA)
# 問答頁面
@app.route('/question')
def question():
    return render_template("question.html")
# 答案頁面
@app.route('/anser', methods=['POST'])
def anser():
    content=request.form.get('content')
    question=request.form.get('question')
    url = "https://pu.ap-mic.com/qa"
    data = {"content":content[:2000], "question":question}
    r = httpx.post(url, json = data, timeout=300)
    answer = r.json()['answer']
    return answer


###TODO:刪除歷史問答###
@app.route("/removeFromQA")
def removeFromQA():  
    uid = session['uid']
    qid = int(request.args.get('qid'))
    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
#        cur.execute("SELECT uid FROM users WHERE email = '" + email + "'")
#        userId = cur.fetchone()[0]
        try:
            cur.execute("DELETE FROM QA WHERE uid = " + str(uid) + " AND qid = " + str(qid))
            conn.commit()
            msg = "removed successfully"
        except:
            conn.rollback()
            msg = "error occured"
    conn.close()
    return redirect(url_for('historyQA'))

###TODO:收藏歷史問答 考虑是否进行功能删减
@app.route("/starFromQA")
def starFromQA():
    uid = session['uid']
    qid = int(request.args.get('qid'))
    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
#        cur.execute("SELECT uid FROM users WHERE email = '" + email + "'")
#        userId = cur.fetchone()[0]
        try:
            if 'star' == True:
                cur.execute("UPDATE QA SET star = true WHERE uid = " + str(uid) + " AND qid = " + str(qid))
                conn.commit()
                msg = "removed successfully"
            else:
                cur.execute("UPDATE QA SET star = false WHERE uid = " + str(uid) + " AND qid = " + str(qid))
                conn.commit()
                msg = "removed successfully"
        except:
            conn.rollback()
            msg = "error occured"
    conn.close()
    return redirect(url_for('historyQA'))

@app.route("/historyQA")
def historyQA():
    loggedIn, uid, noOfQA= getLoginDetails()
    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        cur.execute("SELECT qid, star, ques, ans from QA where uid = " + str(uid))
        QA = cur.fetchall()
    return render_template("historyQA.html", QA = QA, loggedIn=loggedIn, uid=uid, noOfQA=noOfQA)

@app.route("/feedbackForm")
def feedbackForm():
    loggedIn, uid, noOfQA= getLoginDetails()
    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        cur.execute("SELECT qid, star, ques, ans from QA where uid = " + str(uid))
        QA = cur.fetchall()
    return render_template("feedback.html", loggedIn=loggedIn, uid=uid, noOfQA=noOfQA)

@app.route("/feedback", methods = ['GET', 'POST'])
def feedback():
    loggedIn, uid, noOfQA= getLoginDetails()
    if request.method == 'POST':
        #Parse form data    
        ftype = request.form['ftype']
        ftext = request.form['ftext']

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
if __name__ == '__main__':
    app.run(debug=True)
