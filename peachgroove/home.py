from flask import Flask, render_template, request
import sqlite3 as sql
app = Flask(__name__)

@app.route('/')
def home():

	return render_template('index.html')

@app.route('/calender')
def calender():
	return render_template('page-calendar.html')

@app.route('/Activity',methods = ['POST', 'GET'])
def Activity():
	pass

@app.route('/addcrop',methods = ['POST', 'GET'])
def addcrop():
	if request.method == 'POST':
		try:
			crop = request.form['crop']
			comment = request.form['comment'] 
			dealer = request.form['dealer']
			date1 = request.form['date1']
			date2 = request.form['date2']

			with sql.connect("peachgroove_farm.db") as con:
				cur = con.cursor()
				cur.execute('''INSERT INTO CROP_DATA (Crop_name,DATE_OF_PURCHASE,DEALER,DATE_SOWN,Comments) VALUES (?,?,?,?,?)",(crop,date1,dealer,date2,comment);''')

			con.commit()
			print("Record successfully added")
			
			return render_template('index.html')
		except Exception as e:
			
			con.rollback()
			print("error in insert operation")

		finally:
			return render_template('index.html')

@app.route('/list')
def list():
   con = sql.connect("peachgroove_farm.db")
   con.row_factory = sql.Row
   
   cur = con.cursor()
   cur.execute("select * from CROP_DATA")
   
   rows = cur.fetchall(); 
   return render_template("list.html",rows = rows)

if __name__ == '__main__':
	app.debug = True
	app.run() 
	app.run(debug = True)