from __future__ import division, print_function

from flask import Flask, render_template, request
import joblib
import numpy as np
import pickle
import sqlite3
import os
# Keras
from keras.applications.imagenet_utils import preprocess_input, decode_predictions
from keras.models import load_model
from keras.preprocessing import image

# Flask utils
from flask import Flask, redirect, url_for, request, render_template
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads/'

# allow files of a specific type
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

# function to check the file extension
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

model_path2 = 'models.h5' # load .h5 Model

CTS = load_model(model_path2)
from keras.preprocessing.image import load_img, img_to_array

def model_predict2(image_path,model):
    print("Predicted")
    image = load_img(image_path,target_size=(299,299))
    image = img_to_array(image)
    image = image/255
    image = np.expand_dims(image,axis=0)
    
    result = np.argmax(model.predict(image))
     
    
    if result == 0:
        return "L! Mild Sleep Apnea ","after.html"
    elif result == 1:
        return "L! Mild Sleep Apnea ","after.html"
    elif result == 2:
        return "Normal beat , No apnea","after.html"
    elif result == 3:
        return "Normal beat , No apnea","after.html"
    elif result == 4:
        return "M! MODERATE Sleep Apnea","after.html"
    elif result == 5:
        return "S! SEVERE Sleep Apnea ","after.html"

lr = joblib.load("model.pkl")

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/logon')
def logon():
	return render_template('signup.html')

@app.route('/login')
def login():
	return render_template('signin.html')

@app.route("/signup")
def signup():

    username = request.args.get('user','')
    name = request.args.get('name','')
    email = request.args.get('email','')
    number = request.args.get('mobile','')
    password = request.args.get('password','')
    con = sqlite3.connect('signup.db')
    cur = con.cursor()
    cur.execute("insert into `info` (`user`,`email`, `password`,`mobile`,`name`) VALUES (?, ?, ?, ?, ?)",(username,email,password,number,name))
    con.commit()
    con.close()
    return render_template("signin.html")

@app.route("/signin")
def signin():

    mail1 = request.args.get('user','')
    password1 = request.args.get('password','')
    con = sqlite3.connect('signup.db')
    cur = con.cursor()
    cur.execute("select `user`, `password` from info where `user` = ? AND `password` = ?",(mail1,password1,))
    data = cur.fetchone()

    if data == None:
        return render_template("signin.html")    

    elif mail1 == 'admin' and password1 == 'admin':
        return render_template("index.html")

    elif mail1 == str(data[0]) and password1 == str(data[1]):
        return render_template("index.html")
    else:
        return render_template("signup.html")




@app.route("/index")
def index():
    return render_template('index.html')

@app.route('/predict', methods = ['POST'])
def predict():
    if request.method == 'POST':
        val1, val2, val3, val4, val5, val6, val7, val8,val9,val10,val11 = float(request.form['1']), float(request.form['2']), float(request.form['3']), float(request.form['4']), float(request.form['5']), float(request.form['6']), float(request.form['7']), float(request.form['8']), float(request.form['9']), float(request.form['10']), float(request.form['11'])
        lr_pm = lr.predict([[val1, val2, val3, val4, val5, val6, val7, val8,val9,val10,val11]])

        # print(lr_pm)

    return render_template("result.html", lr_pm = np.round(lr_pm,3))

@app.route('/predict2',methods=['GET','POST'])
def predict2():
    print("Entered")
    
    print("Entered here")
    file = request.files['files'] # fet input
    filename = file.filename        
    print("@@ Input posted = ", filename)
        
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(file_path)

    print("@@ Predicting class......")
    pred, output_page = model_predict2(file_path,CTS)
              
    return render_template(output_page, pred_output = pred, img_src=UPLOAD_FOLDER + file.filename)

@app.route("/notebook")
def notebook():
    return render_template("notebook1.html")

@app.route("/notebook1")
def notebook1():
    return render_template("notebook2.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/upload")
def upload():
    return render_template("upload.html")

if __name__ == "__main__":
    app.run(debug = False)
