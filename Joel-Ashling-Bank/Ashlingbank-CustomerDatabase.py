import sqlite3

db = sqlite3.connect('CustomerRecords.db')
try:
    cursor = db.cursor()

    # Create user details table
    cursor.execute('''CREATE TABLE customerRec (
        sid INTEGER PRIMARY KEY AUTOINCREMENT,
        firstname VARCHAR(30) NOT NULL,
        lastname VARCHAR(30) NOT NULL,
        email VARCHAR(50) NOT NULL,
        dob VARCHAR(10) NOT NULL,
        password VARCHAR(25) NOT NULL,
        sortcode VARCHAR(10) NOT NULL,
        accountnumber INTEGER(12) UNIQUE NOT NULL,
        datecreated VARCHAR(10) NOT NULL);''')

    db.commit()
    print('customer rec tables created successfully')
except Exception as e:
    print(f'Error in customer rec tables creation:{e}')

finally:
    db.close()
