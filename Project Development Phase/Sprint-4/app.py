from flask import Flask,render_template,request,redirect,url_for,session
import ibm_db
import re

app = Flask(__name__)
app.secret_key = 'a'

conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=b0aebb68-94fa-46ec-a1fc-1c999edb6187.c3n41cmd0nqnrk39u98g.databases.appdomain.cloud;PORT=31249;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=zgf26316;PWD=zylwuzmLvUzdnjo5;","","")

@app.route('/',methods=['GET','POST'])
def login():
    global userid
    msg = " "
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        sql = "select * from users where username = ? and password = ?"
        stmt = ibm_db.prepare(conn,sql)
        ibm_db.bind_param(stmt,1,username)
        ibm_db.bind_param(stmt,2,password)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)
        print(account)
        if account:
            session['loggedin'] = True
            session['id'] = account['USERNAME']
            userid = account['USERNAME']
            session['username'] = account['USERNAME']
            msg = "Logged in successfully !"
            return render_template('premium.html')
        else:
            msg = "Incorrect username or password"
    return render_template('login.html',msg = msg)




@app.route('/premium',methods=['GET','POST'])
def premium():
    username = session['username']
    sql = "select * from premiumusers where username = ?"
    stmt = ibm_db.prepare(conn,sql)
    ibm_db.bind_param(stmt,1,username)
    ibm_db.execute(stmt)
    account = ibm_db.fetch_assoc(stmt)
    print(account)
    if account:
        return render_template('consultancy.html')
    else:
        return render_template('booking1.html')
            
            
@app.route('/registered',methods=['GET','POST'])
def registered():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form :
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        paid_on = request.form['paid_on']
        sql = "select * from users where username = ?"
        stmt = ibm_db.prepare(conn,sql)
        ibm_db.bind_param(stmt,1,username)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)
        if account:
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers !'
        elif not username or not password or not email:
            msg = 'Please fill out the form !'
        else:
            insert_sql = "Insert into premiumusers values(?,?,?,?)"
            prep_stmt = ibm_db.prepare(conn,insert_sql)
            ibm_db.bind_param(prep_stmt,1,username)
            ibm_db.bind_param(prep_stmt,2,email)
            ibm_db.bind_param(prep_stmt,3,password)
            ibm_db.bind_param(prep_stmt,4,paid_on)
            ibm_db.execute(prep_stmt)
            msg = 'You have successfully registered for premium!'
            return render_template('consultancy.html')
    
@app.route('/bookedslots',methods=['GET','POST'])
def bookedslots():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        paid_on = request.form['paid_on']
        slot = request.form['slot']
        insert_sql = "Insert into bookedslots values(?,?,?,?,?)"
        prep_stmt = ibm_db.prepare(conn,insert_sql)
        ibm_db.bind_param(prep_stmt,1,username)
        ibm_db.bind_param(prep_stmt,2,email)
        ibm_db.bind_param(prep_stmt,3,password)
        ibm_db.bind_param(prep_stmt,4,slot)
        ibm_db.bind_param(prep_stmt,5,paid_on)
        ibm_db.execute(prep_stmt)
        msg = 'You have successfully registered for premium!'
        return render_template('consultancy.html')

 
@app.route('/doc1')
def doc1():
   return render_template('doc1.html')

@app.route('/doc2')
def doc2():
   return render_template('doc2.html')

@app.route('/doc3')
def doc3():
   return render_template('doc3.html')
   
@app.route('/doc4')
def doc4():
   return render_template('doc4.html')
   
@app.route('/doc5')
def doc5():
   return render_template('doc5.html')

@app.route('/doc6')
def doc6():
   return render_template('doc6.html')
   
@app.route('/doc7')
def doc7():
   return render_template('doc7.html')
   
@app.route('/doc8')
def doc8():
   return render_template('doc8.html')
   
@app.route('/booking')
def booking():
   return render_template('booking.html')
   
@app.route('/credit')
def credit():
   return render_template('credit.html')
   
   
@app.route('/creditbooking')
def creditbooking():
   return render_template('creditbooking.html') 
   
@app.route('/debitbooking')
def debitbooking():
   return render_template('debitbooking.html') 
   
@app.route('/register',methods = ['GET','POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form :
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        sql = "select * from users where username = ?"
        stmt = ibm_db.prepare(conn,sql)
        ibm_db.bind_param(stmt,1,username)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)
        if account:
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers !'
        elif not username or not password or not email:
            msg = 'Please fill out the form !'
        else:
            insert_sql = "Insert into users values(?,?,?)"
            prep_stmt = ibm_db.prepare(conn,insert_sql)
            ibm_db.bind_param(prep_stmt,1,username)
            ibm_db.bind_param(prep_stmt,2,email)
            ibm_db.bind_param(prep_stmt,3,password)
            ibm_db.execute(prep_stmt)
            msg = 'You have successfully registered !'
            return render_template('login.html')
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('register.html', msg = msg)



if __name__ == '__main__':
   app.run()
