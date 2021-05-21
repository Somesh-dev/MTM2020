from flask import Flask, request, redirect, jsonify, render_template, url_for, flash
from zoautil_py import MVSCmd, Datasets
from zoautil_py.types import DDStatement
from datetime import datetime
from write1 import fun2
from send1 import read1, read2
import requests, json

app = Flask(__name__)
app.config['SECRET_KEY'] = b''


with open('config.json', 'r') as c:
    params = json.load(c)["params"]

name="Not updated"
email="Not updated"
price="Not updated"

# endpoint to choose from valid counter numbers and move to its respective page
@app.route('/', methods=['GET','POST'])
def home():
    if (request.method=='GET'):
        return render_template('home.html', l=params['counter_list'] )
    else:
        counter_no = request.form.get("counter_no")
        return render_template('feedback.html', c=counter_no )


# endpoint to put details to add to the dataset
@app.route('/feedback/<counter>', methods=['GET','POST'])
def feedback(counter):
    price="Not updated"
    counter_list=params['counter_list']
    print (type(counter))

    if (request.method=='GET'):
        return render_template('feedback.html', c=counter )
        
    for i in counter_list:
        if (int(counter) == i):   
            if (request.method=='POST'):
                now = datetime.now()
                dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
                name=request.form.get('name')
                surname=request.form.get('surname')
                phone=request.form.get('phone')
                pack=request.form.get('need')

                if (pack[:2]=="St"):
                    price="10"
                elif (pack[:2]=="Co"):
                    price="20"
                elif (pack[:2]=="En"):
                    price="35"
                elif (pack[:2]=="Cu"):
                    price="CP"

                if ((len(name)+len(surname)+1)<20):
                    name=name+" "+surname+(" "*(20-(len(name)+len(surname)+1)))
                else:
                    name=name+" "+surname
                    name=name[0:20]

                if ((len(phone))<13):
                    phone=phone+(" "*(13-len(phone)))

                str1=dt_string+"  "+counter+"  "+name+"  "+phone+"  "+price
                fun2(str1)
                return redirect(url_for('feedback', counter=counter))
            
    return "Unauthorized Access"


# to fetch the recent customer data on basis of counter number
@app.route('/getcounter/<counter>', methods=['GET']) 
def getcounter(counter):
    s = read1(counter)
    return jsonify({"date&time": s[0:19], "counter": s[21:23], "name": s[25:45], "phone": s[47:60], "pack": s[62:64]})

# to view all the details of a single customer based on phone number
@app.route('/getuser2', methods=['GET','POST']) 
def getuser2():

    if (request.method == 'GET'):
        return render_template('user.html')

    if (request.method == 'POST'):
        counter = request.form.get('phone')
        s = read2(counter) #list to send to jinja template
        return render_template('user.html', l=s) 


# to fetch all details of a customer on basis of phone number
@app.route('/getuser/<phone>', methods=['GET'])
def getuser(phone):
    result = read2(phone)
    if (len(result) == 0):
        return jsonify({"data":"no data"})
    else:
        l = []
        for s in result:
            # p =  jsonify({"date&time": s[0:19], "counter": s[21:23], "name": s[25:45], "phone": s[47:60], "pack": s[62:64]})
            l.append({"date&time": s[0:19], "counter": s[21:23], "name": s[25:45], "phone": s[47:60], "pack": s[62:64]})
        return jsonify(l)



app.run(host = '0.0.0.0', port=5000, debug=True)