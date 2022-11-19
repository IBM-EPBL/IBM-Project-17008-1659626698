from flask import Flask, render_template, request, redirect, url_for, session
import ibm_db
import re

app = Flask(__name__)
  
app.secret_key = 'a'

# conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=b70af05b-76e4-4bca-a1f5-23dbb4c6a74e.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud;PORT=32716;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=jzc43091;PWD=PI8VtGRvZlSVT65A",'','')
conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=19af6446-6171-4641-8aba-9dcff8e1b6ff.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud;PORT=30699;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=hcq89801;PWD=usAygURNqa4m1FSR", '', '')


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

@app.route('/',methods =['GET', 'POST'])
def login():
    global userid
    msg = ''
   
  
    if request.method == 'POST' :
        username = request.form['username']
        password = request.form['password']
        sql = "SELECT * FROM users WHERE username =? AND password=?"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt,1,username)
        ibm_db.bind_param(stmt,2,password)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)
        print (account)
        if account:
            session['loggedin'] = True
            session['id'] = account['USERNAME']
            userid=  account['USERNAME']
            session['username'] = account['USERNAME']
            print(session)
            msg = 'Logged in successfully !'
            return render_template('home.html', msg = msg)
        else:
            msg = 'Incorrect username / password !'
    return render_template('login.html', msg = msg)

        
@app.route('/registered',methods=['GET','POST'])
def registered():
    msg = ''
    if request.method == 'POST':
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

@app.route('/register', methods =['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' :
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        sql = "SELECT * FROM users WHERE username =?"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt,1,username)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)
        print(account)
        
        if account:
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'name must contain only characters and numbers !'
        else:
            insert_sql = "INSERT INTO  users VALUES (?, ?, ?)"
            prep_stmt = ibm_db.prepare(conn, insert_sql)
            ibm_db.bind_param(prep_stmt, 1, username)
            ibm_db.bind_param(prep_stmt, 2, email)
            ibm_db.bind_param(prep_stmt, 3, password)
            ibm_db.execute(prep_stmt)
            msg = 'You have successfully registered !'
            return render_template('login.html', msg = msg)
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('register.html', msg = msg)

@app.route('/payment')
def payment():
    return render_template('payment.html')

@app.route('/home')
def home():
    return render_template('home.html')
    
@app.route('/daily_update', methods =['GET', 'POST'])
def daily_update():
    msg=""
    if request.method == 'POST':
        protein = request.form['protein1']
        calo = request.form['calories1']
        carbo = request.form['carbohydrates1']
        fat= request.form['fat1']
        calci = request.form['calcium1']
        print(protein, calo, carbo, fat, calci)
        sql = "SELECT * FROM dietplan WHERE username =?"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt,1,session['username'])
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)
        print(account)
        if account:
            protein = round(float(account['PROTEINS']) - float(protein), 2)
            calo = round(float(account['CALORIES']) - float(calo), 2)
            carbo = round(float(account['CARBOHYDRATES']) - float(carbo), 2)
            fat = round(float(account['FAT'])- float(fat), 2)
            calci = round(float(account['CALCIUM']) - float(calci), 2)
            if protein<0: protein = 0
            if calo<0: calo = 0
            if carbo<0: carbo = 0
            if fat<0: fat = 0
            if calci<0: calci = 0

            msg = ['Calories', str(calo) , 'Proteins', str(protein) + " g", 'Carbohydrates', str(carbo) + " g", 'Fat', str(fat) + " g", 'Calcium', str(calci) + " g"]
            update_sql = "UPDATE dietplan SET calories=?, proteins=?, carbohydrates=?, fat=?, calcium=? WHERE username=?"
            prep_stmt = ibm_db.prepare(conn, update_sql)
            ibm_db.bind_param(prep_stmt, 1, calo)
            ibm_db.bind_param(prep_stmt, 2, protein)
            ibm_db.bind_param(prep_stmt, 3, carbo)
            ibm_db.bind_param(prep_stmt, 4, fat)
            ibm_db.bind_param(prep_stmt, 5, calci)
            ibm_db.bind_param(prep_stmt, 6, session['username'])
            ibm_db.execute(prep_stmt)


    return render_template('daily_update.html',msg=msg)
    

@app.route('/uploadimage')
def uploadimage():
    return render_template('upload_image.html')

@app.route('/consultancy')
def consultancy():
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

 

@app.route('/booking')
def booking():
   return render_template('booking.html')
   
@app.route('/credit')
def credit():
   return render_template('credit.html')
   
@app.route('/debit')
def debit():
   return render_template('debit.html') 
   
@app.route('/creditbooking')
def creditbooking():
   return render_template('creditbooking.html') 
   
@app.route('/debitbooking')
def debitbooking():
   return render_template('debitbooking.html') 

@app.route('/user_diet_info', methods =['GET', 'POST'])
def user_diet_info():
    msg = ""
    if request.method == 'POST' :
        protein = request.form['protein1']
        calo = request.form['calories1']
        carbo = request.form['carbohydrates1']
        fat= request.form['fat1']
        calci = request.form['calcium1']

        protein = protein.split('-')[0]
        carbo = carbo.split('-')[0]
        fat = fat.split('-')[0]
        calci = ''.join(filter(str.isdigit, calci))

        sql = "SELECT * FROM dietplan WHERE username =?"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt,1,session['username'])
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)
        print(account)
        if account:
            update_sql = "UPDATE dietplan SET calories=?, proteins=?, carbohydrates=?, fat=?, calcium=? WHERE username=?"
            prep_stmt = ibm_db.prepare(conn, update_sql)
            ibm_db.bind_param(prep_stmt, 1, calo)
            ibm_db.bind_param(prep_stmt, 2, protein)
            ibm_db.bind_param(prep_stmt, 3, carbo)
            ibm_db.bind_param(prep_stmt, 4, fat)
            ibm_db.bind_param(prep_stmt, 5, calci)
            ibm_db.bind_param(prep_stmt, 6, session['username'])
            ibm_db.execute(prep_stmt)
            msg = 'Details Updated !'
            print(msg)
            return render_template('home.html', msg = msg)
        else:
            insert_sql = "INSERT INTO dietplan VALUES (?, ?, ?, ?, ?, ?)"
            prep_stmt = ibm_db.prepare(conn, insert_sql)
            ibm_db.bind_param(prep_stmt, 1, session['username'])
            ibm_db.bind_param(prep_stmt, 2, calo)
            ibm_db.bind_param(prep_stmt, 3, protein)
            ibm_db.bind_param(prep_stmt, 4, carbo)
            ibm_db.bind_param(prep_stmt, 5, fat)
            ibm_db.bind_param(prep_stmt, 6, calci)
            ibm_db.execute(prep_stmt)
            print(msg)
            msg = "Details Saved !"
            return render_template('home.html', msg = msg)
    return render_template('user_diet_info.html', msg = msg)

@app.route('/logout')

def logout():
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   return render_template('login.html')

# @app.route('/apply',methods =['GET', 'POST'])
# def apply():
#      msg = ''
#      if request.method == 'POST' :
#          username = request.form['username']
#          email = request.form['email']
         
#          qualification= request.form['qualification']
#          skills = request.form['skills']
#          jobs = request.form['s']
#          sql = "SELECT * FROM job WHERE username =?"
#          stmt = ibm_db.prepare(conn, sql)
#          ibm_db.bind_param(stmt,1,username)
#          ibm_db.execute(stmt)
#          account = ibm_db.fetch_assoc(stmt)
#          print(account)
#          if account:
#             msg = 'there is only 1 job position! for you'
#             return render_template('apply.html', msg = msg)

         
         
#          insert_sql = "INSERT INTO  job VALUES (?, ?, ?, ?, ?)"
#          prep_stmt = ibm_db.prepare(conn, insert_sql)
#          ibm_db.bind_param(prep_stmt, 1, username)
#          ibm_db.bind_param(prep_stmt, 2, email)
#          ibm_db.bind_param(prep_stmt, 3, qualification)
#          ibm_db.bind_param(prep_stmt, 4, skills)
#          ibm_db.bind_param(prep_stmt, 5, jobs)
#          ibm_db.execute(prep_stmt)
#          msg = 'You have successfully applied for job !'
#          session['loggedin'] = True
#          TEXT = "Hello,a new application for job position" +jobs+"is requested"
         
        
         
         
         
#      elif request.method == 'POST':
#          msg = 'Please fill out the form !'
#      return render_template('apply.html', msg = msg)

# @app.route('/display')
# def display():
#     print(session["username"],session['id'])
    
#     cursor = mysql.connection.cursor()
#     cursor.execute('SELECT * FROM job WHERE userid = % s', (session['id'],))
#     account = cursor.fetchone()
#     print("accountdislay",account)

    
#     return render_template('display.html',account = account)

# @app.route('/logout')

# def logout():
#    session.pop('loggedin', None)
#    session.pop('id', None)
#    session.pop('username', None)
#    return render_template('home.html')

if __name__ == '__main__':
   app.run(host='0.0.0.0')
