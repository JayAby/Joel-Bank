import sqlite3

db = sqlite3.connect('Ashling-UserRecords.db')
try:
    cursor = db.cursor()

    # Create user personal details table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS userPersonalDetails (
        customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
        firstname TEXT NOT NULL,
        lastname TEXT NOT NULL,
        username TEXT UNIQUE NOT NULL,
        email TEXT UNIQUE NOT NULL,
        dob TEXT NOT NULL,
        password TEXT NOT NULL,
        datecreated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    ''')

    print('user personal details record table created successfully')


    # Create user account table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS userAccountDetails (
        account_id INTEGER PRIMARY KEY,
        customer_id INTEGER,
        account_number INTEGER NOT NULL UNIQUE,
        sort_code TEXT NOT NULL,
        pin INTEGER NOT NULL,
        initial_deposit REAL NOT NULL,
        balance REAL,
        datetime TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (customer_id) REFERENCES userPersonalDetails (customer_id) ON DELETE CASCADE 
    );
    ''')

    print('user account details record tables created successfully')

    # Create Transaction details table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS transactionDetails (
    transaction_id INTEGER PRIMARY KEY,
    sender_account_id INTEGER,
    recipient_account_id INTEGER,
    amount_out REAL NOT NULL,
    transaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    transaction_status TEXT NOT NULL,
    FOREIGN KEY (sender_account_id) REFERENCES userAccountDetails (account_id) ON DELETE CASCADE,
    FOREIGN KEY (recipient_account_id) REFERENCES userAccountDetails (account_id) ON DELETE CASCADE
    );
    ''')

    print('transaction details record table created successfully')

    db.commit()
    print('\n\nCustomer record tables created successfully')
except Exception as e:
    print(f'Error in customer record tables creation: {e}')
finally:
    db.close()
