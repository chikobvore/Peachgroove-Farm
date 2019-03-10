import sqlite3

conn = sqlite3.connect('peachgroove_farm.db')

if conn:
	print("successfully opened peachgroove_farm database")
	print("Creating table")
	conn.execute('''CREATE TABLE CROP_DATA
						(
							Crop_id INT AUTO_INCREMENT NOT NULL PRIMARY KEY,
							Crop_name VARCHAR(255),
							DATE_OF_PURCHASE DATE,
							DEALER VARCHAR(255),
							DATE_SOWN DATE,
							Comments TEXT
						);
				''')
	print("Crop data  table successfully Created")
	conn.execute('''CREATE TABLE  FARMING_ACTIVITIES(
					Crop_id INT AUTO_INCREMENT NOT NULL PRIMARY KEY,
					Activity_id INT AUTO_INCREMENT NOT NULL,
					Activity_name varchar(255),
					Activity_date date,
					Comments TEXT);
					
						''')
	print('FARMING ACTIVITIES TABLE HAS BEEN SUCCESSFULLY CREATED')



else:
	print("Operation failed !")

