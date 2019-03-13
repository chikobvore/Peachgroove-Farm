from flask import Flask, render_template, request,url_for,redirect,session
import pymongo
import os

app = Flask(__name__)
client = pymongo.MongoClient('localhost', 27017)
db = client['PeachGroove']

@app.route('/')
def home():
	if 'Name' in session:
		crops = []
		for crop in db['Crop_data'].find():
			crops.append(crop)
		return render_template('index.html',crops = crops)
	else:
		print("User not logged in")
		return render_template('page-login.html')

@app.route('/login')
def login():
	return render_template('page-login.html')

@app.route('/logging',methods =['GET','POST'])
def logging():

	if request.method == 'POST':
		name = request.form['Name']
		password = request.form['Password']
		print("credentials provided")

		for Admin in db['Administrators'].find():
			print("validating credentials")
			if Admin['Email'] == name:
				print("Username found")
				if Admin['Password'] == password:
					print("Password validation Passed")
					session['Name'] = Admin['Name']
					session['Surname'] = Admin['Surname']
					return render_template('index.html')
				else:
					name = 'Sorry you password did not match your email'
					print(name)
					return render_template('page-login.html', name = name)
			else:
				print("invalid username")
				return render_template('page-signup.html')
	else:
		return render_template('page-signup.html')
	print("we are now here")
	return "Sytem validation error, contact Programmer"

@app.route('/logout')
def logout():	
	session.pop('Name', None)
	session.pop('Surname', None)
	session.pop('message',None)
	print("Sessions successfully deleted")
	return render_template('page-login.html')

@app.route('/signup',methods = ['GET','POST'])
def signup():
	if request.method == 'POST':
		name = request.form['name']
		surname = request.form['surname']
		email = request.form['email']
		password = request.form['pass1']
		Admin = {
			'Name': name,
			'Surname':surname,
			'Email': email,
			'Password': password
		}
		Transaction = db['Administrators'].insert_one(Admin)
		print("Successfully signed in new Admin.Transaction id is " + str(Transaction.inserted_id))
		return redirect(url_for('login'))
	else:
		return render_template('page-signup.html')

@app.route('/gallery',methods = ['GET','POST'])
def gallery():
	if request.method == 'POST':
		print('Trying to upload a file')
		app.config['UPLOAD_FOLDER'] = 'static/images'
		f = request.files['file']
		f.save(os.path.join(app.config['UPLOAD_FOLDER'],f.filename))
		print("file successfully uploaded" + f.filename)
    
		ProductName = request.form['Name']
		ProductDescription = request.form['Description']
		image = {
			"Image_Name": ProductName,
			"Image_Description": ProductDescription,
			"Image_url": 'static/images/'+f.filename
		}
		transaction = db['Images'].insert_one(image)
		print("image details successfuly saved with id "+str(transaction.inserted_id))
		gallery = []
		for image in db['Images'].find():
			gallery.append(image)
		return render_template('gallery.html',gallery = gallery)
	else:
		gallery = []
		for image in db['Images'].find():
			gallery.append(image)
		return render_template('gallery.html',gallery = gallery)

@app.route('/calender')
def calender():
	return render_template('page-calendar.html')

@app.route('/Activity',methods = ['POST', 'GET'])
def Activity():
	if request.method == 'POST':
		try:
			print("let me try that")
			crop_name = request.form['crop']
			activity_date = request.form['activity_date']
			Activity = request.form['Activity']

			if Activity == 'watering':
				mode = request.form['watering_mode']
				amount = request.form['watering_amount']
				Watering = {
					"crop_name": crop_name,
					"activity_date": activity_date,
					"activity": Activity,
					"Mode": mode,
					"amount": amount
				}
				transaction = db['Activities'].insert_one(Watering)
				print("New Activity successfully added with id: "+str(transaction.inserted_id))
			elif Activity == 'weeding':
				mode = request.form['weeding_mode']
				if mode == 'Other':
					print(mode)
					mode = request.form['other_weeding']
				Weeding = {
					"crop_name": crop_name,
					"activity_date": activity_date,
					"activity": Activity,
					"Mode": mode
				}
				transaction = db['Activities'].insert_one(Weeding)
				print("New Activity successfully added with id: "+str(transaction.inserted_id))
			elif Activity == 'fertilisation':
				Fertliser = request.form['Fertiliser']
				Application_rate = request.form['rate']
				fertilisation = {
					"crop_name": crop_name,
					"activity_date": activity_date,
					"activity": Activity,
					"Fertiliser": Fertliser,
					"Application_rate": Application_rate
				}
				transaction = db['Activities'].insert_one(fertilisation)
				print("New Activity successfully added with id: "+str(transaction.inserted_id))
			elif Activity == 'spraying':
				spray = request.form['spraying']
				Application_rate = request.form['rate']
				spraying = {
					"crop_name": crop_name,
					"activity_date": activity_date,
					"activity": Activity,
					"Spray": spray,
					"Application_rate": Application_rate
				}
				transaction = db['Activities'].insert_one(spraying)
				print("New Activity successfully added with id: "+str(transaction.inserted_id))
			else:
				pass
		except Exception as e:
			print("We handled an Exception for you but however your last transaction did not complete")
		finally:
			return records()


@app.route('/records')
def records():
	records = []
	for record in db['Crop_data'].find():
		"""if record['Transplanted_rate'] == '':
			record['Transplanted_rate'] = 'Not nursed'"""
		records.append(record)
	return render_template('Records.html',records =records)

@app.route('/watering')
def watering():
	records = []
	for record in db['Activities'].find():
		record.pop('_id')
		if record['activity'] == 'watering':
			records.append(record)
	return render_template('Activity.html',records = records)

@app.route('/weeding')
def weeding():
	records = []
	for record in db['Activities'].find():
		record.pop('_id')
		if record['activity'] == 'weeding':
			records.append(record)
	return render_template('Activity.html',records = records)

@app.route('/spraying')
def spraying():
	records = []
	for record in db['Activities'].find():
		record.pop('_id')
		if record['activity'] == 'spraying':
			records.append(record)
	return render_template('Activity.html',records = records)

@app.route('/fertilisation')
def fertilisation():
	records = []
	for record in db['Activities'].find():
		record.pop('_id')
		if record['activity'] == 'fertilisation':
			records.append(record)
	return render_template('Activity.html',records = records)

@app.route('/other')
def other():
	records = []
	for record in db['Activities'].find():
		record.pop('_id')
		if record['activity'] == 'other':
			records.append(record)
	return render_template('Activity.html',records = records)

@app.route('/addcrop',methods = ['POST', 'GET'])
def addcrop():
	if request.method == 'POST':
		try:
			crop = request.form['crop']
			variety = request.form['Variety']
			location = request.form['Location']
			nurse = request.form['nurse']
			sown = request.form['Sown']
			Quantity = request.form['Quantity']
			Germinated = request.form['Germinated']
			Germination_rate = request.form['Germination_rate']
			comment = request.form['comment']
			if nurse == 'yes':
				transplanted_date = request.form['transplanted']
				crop = {
						"crop_name": crop,
						"Variety": variety,
						"Location": location,
						"Nursed": nurse,
						"Sown": sown,
						"Quantity": Quantity,
						"Germinated_date": Germinated,
						"Germination_rate": Germination_rate,
						"Transplanted_rate": transplanted_date,
						"comment":comment
						}
				transaction = db['Crop_data'].insert_one(crop)
				print("New crop successfully added with id: "+str(transaction.inserted_id))
			else:

				crop = {
					"crop_name": crop,
					"Variety": variety,
					"Location": location,
					"Nursed": nurse,
					"Sown": sown,
					"Quantity": Quantity,
					"Germinated_date": Germinated,
					"Germination_rate": Germination_rate,
					"comment":comment
					}
				transaction = db['Crop_data'].insert_one(crop)
				print("New crop successfully added with id: "+str(transaction.inserted_id))

		except Exception as e:
			print("We handled an error for you but however your last transaction did not complete")
		finally:
			return render_template('index.html')

if __name__ == '__main__':
	import os
	os.system('start mongod')
	os.system('rundll32 url.dll,FileProtocolHandler http://127.0.0.1:5000/')
	app.secret_key = 'super secret key'
	app.config['SESSION_TYPE'] = 'filesystem'
	app.run(debug = True)
	