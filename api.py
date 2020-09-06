import flask
from flask import request, jsonify,  Flask, flash, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
from fastai.vision.all import *
import os



UPLOAD_FOLDER = '/mnt/c/Users/13058/Documents/Work/FastAI/ROOM/backend'
ALLOWED_EXTENSIONS = {'png','jpg','jpeg'}
app = flask.Flask(__name__)
app.config["DEBUG"] = True
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
learn = load_learner('./export.pkl')
# Some random data, we'll use fastai somehow here
'''
books = [
    {'id': 0,
     'title': 'A Fire Upon the Deep',
     'author': 'Vernor Vinge',
     'first_sentence': 'The coldsleep itself was dreamless.',
     'year_published': '1992'},
    {'id': 1,
     'title': 'The Ones Who Walk Away From Omelas',
     'author': 'Ursula K. Le Guin',
     'first_sentence': 'With a clamor of bells that set the swallows soaring, the Festival of Summer came to the city Omelas, bright-towered by the sea.',
     'published': '1973'},
    {'id': 2,
     'title': 'Dhalgren',
     'author': 'Samuel R. Delany',
     'first_sentence': 'to wound the autumnal city.',
     'published': '1975'}
]

@app.route('/', methods=['GET'])
def home():
    return "<h1>Hello this is where we return our fast ai bs</h1>"


# a route to return all t he available entries in our catalog
@app.route('/api/v1/resources/books/all', methods=['GET'])
def api_all():
    return jsonify(books)

@app.route('/api/v1/resources/books',methods=['GET'])
def api_id():
    # Check if an ID was provided as part of the URL
    # if ID is provided assign it to avariable
    # if no ID is provided, display an error in the browser.
    if 'id' in request.args:
        id = int(request.args['id'])
    else:
        return "Error: No id field provided. please specify and id."

    results = []

    for book in books:
        if book['id'] == id:
            results.append(book)
    
    return jsonify(results)
'''
def predict(learn, image):
    return learn.predict(image)



def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/',methods=['GET','POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)

        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            file = file.read()
            result = predict(learn,file)
            print(result)
            return redirect(url_for('prediction',result=result))
            '''filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file',filename=filename))'''
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''
@app.route('/images/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],filename)

@app.route('/prediction/<result>')
def prediction(result):
    return result
# NEED a GET request to send Fastai result to user
# NEED a POST request to receive data from user
if __name__ == '__main__':
    app.run()
