from flask import Flask, jsonify,render_template,request,redirect,flash,url_for,session
from dbconnection.datamanipulation import *

app=Flask(__name__)
app.secret_key="superadmin"

@app.route('/')
def home():
    return render_template('abc.html')

@app.route('/home_page')
def home_page():
    return render_template('home.html')

@app.route('/login')
def login():
  return render_template('login.html')


@app.route('/login_action',methods=['POST'])
def login_action():
    username=request.form['username']
    password=request.form['password']
    user=sql_query2('select * from register where username=? and password=?',(username,password))
    if len(user)>0:
        session['id']=user[0][0]
        return redirect(url_for('home_page'))
    else:
        return redirect(url_for('login'))


@app.route('/register')
def register():
    m=sql_query('select * from country' )
    return render_template('register.html',n=m)


@app.route('/register_action',methods=['POST'])
def register_action():
    name=request.form['name']
    gender=request.form['gender']
    address=request.form['address']
    country=request.form['country']
    state=request.form['state']
    phonenumber=request.form['phonenumber']
    username=request.form['username']
    password=request.form['password']
    user=sql_edit_insert('insert into register values(NULL,?,?,?,?,?,?,?,?)',(name,gender,address,country,state,phonenumber,username+'@gmail.com',password))
    flash('inserted sucessfully')
    return redirect(url_for('register'))


@app.route('/getstate')
def getstate():
    m=request.args.get('co')
    p=sql_query2('select * from state where countid=?',[m])
    return render_template('getstate.html',n=p)


@app.route('/checkuser')
def checkuser():
    m=request.args.get('user')
    p=sql_query2('select * from register where username=?',[m+'@gmail.com'])
    if len(p)>0:
        msg='user already exist'
    else:
        msg='not exist'
    return jsonify({'valid':msg})




if __name__=='__main__':
    app.run(debug=True)
    