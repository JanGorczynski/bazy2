from flask import Flask, request, jsonify
import pyodbc

app = Flask(__name__)

# Establish connections to both databases
conn_db1 = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};'
                      'SERVER=DESKTOP-H61S33J\SERVERBAZY2;'
                      'DATABASE=goodBank; UID=sa; PWD=123;')
conn_db2 = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};'
                      'SERVER=DESKTOP-H61S33J\SERVERBAZY2;'
                      'DATABASE=betterBank; UID=sa; PWD=123;')





@app.route('/transfer', methods=['GET'])
def transfer_funds():

    sender_id =  request.args.get('sender_id')
    recipient_id = request.args.get('recipient_id')
    amount = request.args.get('amount')

    if sender_id==None or recipient_id==None or amount==None:
        return jsonify({
        "message": "Not enough arguments"
        }), 400
    
    amount = float(amount)


    conn_db1.autocommit = False
    conn_db2.autocommit = False
    cursor_db1 = conn_db1.cursor()
    cursor_db2 = conn_db2.cursor()



    cursors = [cursor_db1,cursor_db2]
    
    cursor1 = get_acc_cursor(cursors,sender_id)
    cursor2 = get_acc_cursor(cursors,recipient_id)

    if cursor1==None or cursor2==None:
        return jsonify({
        "message": "Account number not found"
        }), 400
    
    if sender_id==recipient_id:
        return jsonify({
        "message": "Sender and recipient numbers are identical"
        }), 400

    cursor1.execute(f"SELECT balance FROM account WHERE account_number = {sender_id}")
    balance = cursor_db1.fetchone()[0]

    if amount>balance:
        return jsonify({
        "message": "Can not wire more than in bank account"
        }), 400
    

    try:

        cursor1.execute(f"UPDATE account SET balance = balance - {amount} WHERE account_number = {sender_id}")
        cursor2.execute(f"UPDATE account SET balance = balance + {amount} WHERE account_number = {recipient_id}")

        conn_db1.commit()
        conn_db2.commit()

        return jsonify({
            "message": "Transaction successful"
        }), 200
    
    except Exception as e:

        conn_db1.rollback()
        conn_db2.rollback()
        print("Transaction rolled back due to error:", e)
        return jsonify({"error": "Transaction failed"}), 500
    
    finally:

        cursor_db1.close()
        cursor_db2.close()


def get_acc_cursor(cursors,acc_id):
    for cursor in cursors:
        try:
            cursor.execute(f"SELECT * FROM account WHERE account_number = {acc_id}")
            cursor.fetchone()[0]
            return cursor
        except:
            pass
    return None

if __name__ == '__main__':
    app.run(debug=True)

