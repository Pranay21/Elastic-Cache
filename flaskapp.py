import os,time
from flask import Flask, jsonify, request, render_template, make_response, redirect,url_for
import boto3
import json
import memcache
import mysql.connector
import random

ID=[]

ACCESS_KEY = 'AKIAJYEYMPPOL7MQPI6A'
SECRET_KEY = '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'

s3 = boto3.resource('s3',aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY)
bucket=s3.Bucket('sxa0453')

app = Flask(__name__)
db = mysql.connector.connect(user='sxa0453', password='root1234',
                                 host='sxa0453.ctxfxzi2f5qr.us-west-2.rds.amazonaws.com',
                                 database='cloud')
cur = db.cursor(buffered=True)
mc = memcache.Client(['sxa0453cache.oesjvx.0001.usw2.cache.amazonaws.com:11211'], debug=1)
selectIDs = "select id from Traffic_Violations"
cur.execute(selectIDs)
rows = cur.fetchall()
for col in rows:
        ID.append(col[0])
listLength = len(ID)
@app.route('/')
def Welcome():


    return render_template('welcome.html')

@app.route('/rquery/')
def random_query():
    start_time = time.time()
    for num in range(1, 5000):
        ran = random.randint(1,listLength)
        id = ID[ran];
        query = "select * from Traffic_Violations where id=" + str(id) + ";"
        cur.execute(query)
    end_time = time.time()
    total_time = end_time - start_time
    print total_time
    return render_template('welcome.html',r_time=total_time)



@app.route('/squery/')
def specific_query():
    start_time = time.time()
    for num in range(1, 5000):
        ran = random.randint(2000, 3000)
        id = ID[ran];
        query = "select * from Traffic_Violations where id=" + str(id) + ";"
        cur.execute(query)
    end_time = time.time()
    total_time = end_time - start_time
    print total_time
    return render_template('welcome.html', s_time=total_time)

@app.route('/rcquery/')
def random_cache_query():
    start_time = time.time()
    for num in range(1, 5000):
        ran = random.randint(1, listLength)
        id = ID[ran];
        query = "select * from Traffic_Violations where id=" + str(id) + ";"
        val=mc.get((str(id)))
        if val is None:
            cur.execute(query)
            rows = cur.fetchall()
            mc.set(str(id), rows)
        else:
                rows=val;


    end_time = time.time()
    total_time = end_time - start_time
    print total_time
    return render_template('welcome.html', r_time=total_time)



@app.route('/scquery/')
def specific_cache_query():
    start_time = time.time()
    for num in range(1, 5000):
        ran = random.randint(1000, 3000)
        id = ID[ran];
        query = "select * from Traffic_Violations where id=" + str(id) + ";"
        val=mc.get((str(id)))
        if val is None:
            cur.execute(query)
            rows = cur.fetchall()
            mc.set(str(id), rows)
        else:
                rows=val;


    end_time = time.time()
    total_time = end_time - start_time
    print total_time
    return render_template('welcome.html', s_time=total_time)




port = os.getenv('PORT', '5000')
if __name__ == "__main__":
	app.run(host='0.0.0.0', port=int(port),debug=True)
