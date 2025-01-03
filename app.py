from flask import Flask, render_template,request,redirect,url_for,flash,session
import bcrypt
from flask_mysqldb import MySQL
app=Flask(__name__)

app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']=''
app.config['MYSQL_DB']='mydatabase'
app.secret_key='your_secret_key_here'

mysql=MySQL(app)



@app.route('/')
def homepage():
    return render_template('homepage.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/investor_dashboard',methods=['GET'])       
def investor_dashboard():
    cursor=mysql.connection.cursor()
    cursor.execute("SELECT * FROM usersideas")
    data=cursor.fetchall()
    cursor.close()
    return render_template('investor-dashboard.html',data=data)


@app.route("/loginsubmit",methods=['POST'])
def loginsubmit():
    username=request.form['username']
    password=request.form['password']
    cursor=mysql.connection.cursor()
    cursor.execute("SELECT * FROM users where username=%s",[username])
    user=cursor.fetchone()
    cursor.close()
    print(user)
    if user==None:
        flash("Username doesn't exist")
        return redirect(url_for('login'))
    else:
        cursor=mysql.connection.cursor()
        cursor.execute("SELECT * FROM users where username=%s",[username])
        user=cursor.fetchone()
        cursor.close()
        print(user[3])
        if user and bcrypt.checkpw(password.encode('utf-8'),user[2].encode('utf-8')):
            session['user_id']=user[0]
            session['user_name']=user[1]
            session['email']=user[4]
            if user[3]=="investor":
                return redirect(url_for('investor_dashboard'))
            elif user[3]=="user":
                return render_template('user-dashboard.html')
        else:
            flash("incorrect password")
            return redirect(url_for('login'))



        


@app.route("/usersubmit",methods=['POST'])
def usersubmit():
    
    title=request.form['title']
    description=request.form['description']
    categories=request.form['categories']
    cursor=mysql.connection.cursor()
    cursor.execute("INSERT INTO usersideas (title,description,categories,username,email) VALUES (%s,%s,%s,%s,%s)",(title,description,categories,session['user_name'],session['email']))
    mysql.connection.commit()
    cursor.close()
    return render_template('user-dashboard.html')



@app.route("/feedback",methods=['POST'])
def feedback():
    
    name=request.form['name']
    email=request.form['email']
    feedbackdata=request.form['feedbackdata']
    cursor=mysql.connection.cursor()
    cursor.execute("INSERT INTO feedback (name,email,feedbackdata) VALUES (%s,%s,%s)",(name,email,feedbackdata))
    mysql.connection.commit()
    cursor.close()
    return render_template('homepage.html')






@app.route("/individualuserideas",methods=['GET'])
def individualuserideas():
    cursor=mysql.connection.cursor()
    cursor.execute("SELECT * FROM usersideas where username=%s",[session['user_name']])
    data=cursor.fetchall()
    cursor.close()
    return render_template('individualuser-dashboard.html',data=data)






@app.route("/registersubmit",methods=['POST'])
def registersubmit():
    usernamee=request.form['username']
    password=request.form['password']
    emaill=request.form['email']
    typee=request.form['category']
    hased_password=bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt())
    cursor=mysql.connection.cursor()
    cursor.execute("SELECT * FROM users where username=%s",[usernamee])
    user=cursor.fetchone()
    cursor.close()
    if user:
        flash("Username already Exist")
        return redirect(url_for('register'))
    else:
        cursor=mysql.connection.cursor()
        cursor.execute("INSERT INTO users (username,password,type,email) VALUES (%s,%s,%s,%s)",(usernamee,hased_password,typee,emaill))
        mysql.connection.commit()
        cursor.close()
        flash("Registerion successfull")
        return redirect(url_for('login'))
    
@app.route("/logout")
def logout():
    session.pop('user_id',None)
    session.pop('user_name',None)
    session.pop('user_name',None)
    return redirect(url_for('homepage'))




if __name__=='__main__':
    app.run(debug=True)