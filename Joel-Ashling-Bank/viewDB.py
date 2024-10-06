import sqlite3

# Connect to the database
db = sqlite3.connect('Ashling-UserRecords.db')

# Query to select all records from userPersonalDetails
viewquery1 = "SELECT * FROM userPersonalDetails;"
viewquery2 = "SELECT * FROM userAccountDetails;"

# Remove query (if needed)
# removequery = "DELETE FROM userPersonalDetails;"

cursor = db.cursor()

# Execute the query to view records
cursor.execute(viewquery1)

# To delete the records, uncomment this line
# cursor.execute(removequery)

# Fetch and print all records using fetchall()
records = cursor.fetchall()

# If there are no records, print a message
if len(records) == 0:
    print("No records found.")
else:
    for record in records:
        # Format the CustomerID to 4 digits (e.g., 0001, 0002, ...)
        formatted_record = (
            f"{record[0]:04d}",  # Assuming CustomerID is the first column
            *record[1:]  # The rest of the record remains unchanged
        )
        print(formatted_record)

# Commit any changes and close the database
db.commit()
db.close()
