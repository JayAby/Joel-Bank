import sqlite3

# Connect to the database
db = sqlite3.connect('Ashling-UserRecords.db')

# Query to select all records
viewquery = "SELECT * FROM userRecords;"
removequery = "DELETE FROM userRecords;"

cursor = db.cursor()

# Execute the query
cursor.execute(viewquery)

# To delete the records!
# cursor.execute(removequery)

# Fetch and print all records using fetchall()
records = cursor.fetchall()

# If there are no records, print a message
if len(records) == 0:
    print("No records found.")
else:
    for record in records:
        print(record)

# Commit any changes and close the database
db.commit()
db.close()
