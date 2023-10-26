from flask import *
import mysql.connector
from datetime import datetime
import mysql.connector
from mysql.connector import pooling
import requests
import boto3
from botocore.exceptions import NoCredentialsError
import os
aws_access_key_id = "AKIAUFTPQN5O75N6A7EW"
aws_secret_access_key = "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"


app=Flask(__name__)
app.config["JSON_AS_ASCII"]=False
app.config["TEMPLATES_AUTO_RELOAD"]=True
app.config["JSONIFY_PRETTYPRINT_REGULAR"] = False
app.config["JSONIFY_MIMETYPE"] = 'application/json; charset=utf-8'
app.config ['JSON_SORT_KEYS'] = False
secret_key = "jasonkey"

def upload_text(text,filename):
	rds = boto3.client('rds',region_name='us-east-1', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
	connection = mysql.connector.connect(
    host='mydbinstance.coduydqlqucg.us-east-1.rds.amazonaws.com',
    user='myuser',
    password='mypassword',
    database='mydatabase',
    port=3306
	)
	cursor = connection.cursor()
	insert_data_sql = "INSERT INTO messages (message, filename) VALUES (%s,%s)"
	cursor.execute(insert_data_sql, (text, filename))
	connection.commit()

def get_allmsg():
    rds = boto3.client('rds',region_name='us-east-1', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
    connection = mysql.connector.connect(host='mydbinstance.coduydqlqucg.us-east-1.rds.amazonaws.com',user='myuser',password='mypassword',database='mydatabase',port=3306)
    cursor=connection.cursor()
    cursor.execute("SELECT * FROM messages ORDER BY id DESC")
    results = cursor.fetchall()
    allmsg=[]
    for i in results:
        allmsg.append([i[1],"https://d22xulnnj1fzbs.cloudfront.net/"+i[2]])
    cursor.close()
    connection.close()
    return allmsg

def get_cloudfront(filename):
	cloudfront = boto3.client('cloudfront', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
	distribution_id = "E83TZRKN3KTGV"
	#print(global_url)
	image_url="https://d22xulnnj1fzbs.cloudfront.net/"+filename
	response = requests.get(image_url)

@app.route("/")
def index():
	return render_template("index.html")


@app.route("/api/upload", methods=["POST"])
def api_upload():
	text = request.form.get('text')
	filename = request.form.get('filename')
	file = request.files['file']
	timestring=str(datetime.now().minute)+str(datetime.now().second)
	filename=timestring+filename

	upload_text(text, filename)
	s3 = boto3.client('s3',region_name='ap-southeast-2', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
	try:
		s3.upload_fileobj(file,"jasonteststage3",filename)
		s3.put_object_acl(Bucket='jasonteststage3', Key=filename, ACL='public-read') #設定成公開
	except Exception as e:
		print("error",e)
	print("upload success")
	return jsonify({"message":"success"})

@app.route("/api/display")
def api_display():
	msg = get_allmsg()
	return jsonify({"data":msg})



app.run(host="0.0.0.0", port=3000)