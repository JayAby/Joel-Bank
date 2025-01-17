from datetime import datetime
import sqlite3

DB_PATH = 'Ashling_UserRecords.db'

def process_pending_transactions():
    db = sqlite3.connect(DB_PATH)
    # Connect to the database
    db = sqlite3.connect(DB_PATH)
    try:
        cursor = db.cursor()

        # Get today's date
        today = datetime.now().strftime('%d-%m-%Y')

        # Fetch all scheduled transactions for today and earlier
        fetch_query = '''
        SELECT transaction_id, sender_account_id, recipient_account_id, amount_out
        FROM transactionDetails
        WHERE transaction_status = 'Scheduled' AND date(transaction_date) <= ?
        '''

        cursor.execute(fetch_query, (today,))
        transactions = cursor.fetchall()

        if not transactions:
            print("No pending transactions to process.")
            return

        # Process transaction
        for transaction in transactions:
            transaction_id, sender_id, recipient_customer_id, entered_amount = transaction

            # Add amount to recipient
            add_query = "UPDATE userAccountDetails SET balance = balance + ? WHERE customer_id = ?"
            cursor.execute(add_query, (float(entered_amount), recipient_customer_id))

            # Mark transaction as success
            update_query = "UPDATE transactionDetails SET transaction_status = 'Success' WHERE transaction_id = ?"
            cursor.execute(update_query, (transaction_id,))

            db.commit()
            print(f"{len(transactions)} pending transactions processed successfully.")
    except Exception as e:
        print(f"Error processing pending transactions: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    process_pending_transactions()