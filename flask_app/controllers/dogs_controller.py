from flask import render_template, redirect, request, session, url_for,jsonify, send_from_directory
from flask_app.models import user_model, dogs_model
from flask_app import app
from werkzeug.utils import secure_filename

path =r"D:\coding_dojo\Python\adoption\flask_app\static\uploads"
UPLOAD_FOLDER = path
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'JPG', 'PNG', 'bmp','jpeg'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/alldogs')
def dogs():
    if 'user_id' not in session:
        return redirect('/')
    user = user_model.User.get_one({'id':session['user_id']})
    context = {
        'all_dogs':dogs_model.Dog.get_all(),
    }
    return render_template('alldogs.html', **context, user=user)

@app.route('/admin/dog')
def add_dog():
    return render_template('add_dog.html')

@app.route('/dog/create', methods=['GET','POST'])
def dog_create():
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
        print(file,"*****************************************")
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(f"{app.config['UPLOAD_FOLDER']}\{filename}")
            data['pic'] = file.filename
        dogs_model.Dog.save(data)
    return redirect('/alldogs')

# @app.route('/display/<filename>')
# def display_image(filename=''):
#     return display_image(app.config["UPLOAD_FOLDER"], filename)

# @app.route('/display/<filename>')
# def display_image(filename):
#     return redirect(url_for('static', filename='uploads/' + filename), code=301)

@app.route('/dog/edit/<int:id>')
def edit_dog(id):
    context = {
        'dog':dogs_model.Dog.get_one({'id':id})
    }
    return render_template('editdog.html', **context)

@app.route('/dog/update/<int:id>', methods=['POST'])
def update(id):
    # if not dogs_model.Dog.validate_recipe(request.form):
    #     return redirect(f'/recipes/edit/{id}')
    
    data = {
        **request.form,
        'id':id
    }
    dogs_model.Dog.update(data)
    return redirect('/alldogs')

@app.route('/dog/delete/<int:id>')
def delete(id):
    data = {
        'id':id
    }
    dogs_model.Dog.delete(data)
    return redirect('/alldogs')

@app.route('/dog/view/<int:id>')
def show(id):
    data = {
        'id':id
    }
    return render_template('viewdog.html', dog=dogs_model.Dog.get_one(data))

