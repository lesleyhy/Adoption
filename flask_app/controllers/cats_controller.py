from flask import render_template, redirect, request, session, url_for,jsonify
from flask_app.models import user_model, cats_model
from flask_app import app
from werkzeug.utils import secure_filename

path =r"C:\Users\lesle\OneDrive\桌面\Python\adoption\flask_app\static\uploads"
UPLOAD_FOLDER = path
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'JPG', 'PNG', 'bmp','jpeg'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/allcats')
def cats():
    if 'user_id' not in session:
        return redirect('/')
    user = user_model.User.get_one({'id':session['user_id']})
    context = {
        'all_cats':cats_model.Cat.get_all(),
    }
    return render_template('allcats.html',**context, user=user)

@app.route('/admin/cat')
def add_cat():
    return render_template('add_cat.html')

@app.route('/cat/create', methods=['GET','POST'])
def cat_create():
    data = {
        'name' : request.form['name'],
        'age' : request.form['age'],
        'sex' : request.form['sex'],
        'color' : request.form['color'],
        'breed' : request.form['breed'],
        'health' : request.form['health'],
        'other_info' : request.form['other_info'],
        'location' : request.form['location'],
        'user_id':session['user_id'],
        'pic' : "",
    }
    if request.method == 'POST':
        file = request.files['pic']
        print(file)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(f"{app.config['UPLOAD_FOLDER']}\{filename}")
            data['pic'] = file.filename
        cats_model.Cat.save(data)
    return redirect('/allcats')

# @app.route("/display/<filename>")
# def display_img(filename):
#     return redirect(url_for('static',filename='uploads/'+filename), code=301)

@app.route('/cat/edit/<int:id>')
def edit_cat(id):
    context = {
        'cat':cats_model.Cat.get_one({'id':id})
    }
    return render_template('editcat.html', **context)

@app.route('/cat/update/<int:id>', methods=['POST'])
def update_cat(id):
    # if not cats_model.cat.validate_recipe(request.form):
    #     return redirect(f'/recipes/edit/{id}')
    
    data = {
        **request.form,
        'id':id
    }
    cats_model.Cat.update(data)
    return redirect('/allcats')

@app.route('/cat/delete/<int:id>')
def delete_cat(id):
    data = {
        'id':id
    }
    cats_model.Cat.delete(data)
    return redirect('/allcats')

@app.route('/cat/view/<int:id>')
def show_cat(id):
    data = {
        'id':id
    }
    return render_template('viewcat.html', cat=cats_model.Cat.get_one(data))

