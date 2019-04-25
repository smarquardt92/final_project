import os
from flask import Flask, request, render_template, redirect, jsonify
from flask_mysqldb import MySQL
import pickle
mysql = MySQL()
from time import sleep
from ML import classify
app = Flask(__name__)

app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Snowihop^9'
app.config['MYSQL_DB'] = 'Recipes'
app.config['MYSQL_HOST'] = 'localhost'
#mysql.init_app(app)


mysql = MySQL(app)


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        print(request)

        if request.files.get('file'):
            # read the file
            file = request.files['file']

            # read the filename, this is part of the image file you uplaod
            filename = file.filename 
            file.save(os.path.join("../uploads/", filename))
            predict=classify.classifier(f"../uploads/{filename}")
            print(predict)
            cur = mysql.connection.cursor()
            cur.execute("SELECT * From allrecipes WHERE Ingredients LIKE '%Apple%'")
            data = cur.fetchall()
            
           
        
            return render_template('index.html', object_list=data)
            #other_data= jsonify({'data': 'data'})
    
       
    return render_template('index.html')  
 
    
            

if __name__ == "__main__":
    app.run(debug=True)