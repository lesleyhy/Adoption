from flask import render_template, redirect, request, session
from flask_app.models import user_model
from flask_app import app, bcrypt

@app.route('/')
def index():
    if 'user_id' not in session:
        return redirect('/firstpage')
    return render_template('index.html')

@app.route('/firstpage')
def firstpage():
    if 'user_id' in session:
        return redirect('/')
    return render_template('firstpage.html')

# @app.route('/')
# def index():
#     if 'user_id' not in session:
#         return render_template('index.html')
#     user = user_model.User.get_one({'id':session['user_id']})
#     return render_template('index.html',user=user)

@app.route('/home/login')
def new():
    return render_template('login.html')

@app.route('/create', methods=['POST'])
def create():
    is_valid = user_model.User.validate(request.form)
    if not is_valid:
        return redirect('/home/login')
    
    hash_pw = bcrypt.generate_password_hash(request.form['password'])
    data = {
        **request.form,
        'password':hash_pw
    }

    user_id = user_model.User.save(data)
    session['user_id'] = user_id
    print(session,'here')
    return redirect('/')

@app.route('/login', methods = ['POST'])
def login():
    is_valid =user_model.User.validate_login(request.form)
    if not is_valid:
        return redirect("/home/login")
    user = user_model.User.get_one_by_email({'email':request.form['email']})
    session['user_id'] = user.id
    return redirect('/')

@app.route('/user/logout', methods = ['GET'])
def logout():
    del session['user_id']
    return redirect('/home/login')

