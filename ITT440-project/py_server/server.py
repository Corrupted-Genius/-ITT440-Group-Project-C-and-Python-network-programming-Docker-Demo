# THIS IS PYTHON SERVER SECTION

# WHAT DOES THIS SECTION DO?
# - Connect to MySQL 
# - Each time client connected to server, increases the points of py_user by 5
# - Updates the datetime to current
# - Send back latest data to the client 
# - Logs the action 

import pymysql
import socket
import time
from datetime import datetime

# CONNECT TO MySQL WITH 10x RETRY OPTION -------------------------------------------------------------------------
def connect_db():
    retry = 10

    while retry > 0:
        try:
            db = pymysql.connect( # connect to MySQL container 
                host="mysql_db",
                user="root",
                password="",
                database="itt440"
            )
            print("STATUS : PYTHON CONNECTED TO MySQL")
            return db
        except:
            print("STATUS : PYTHON FAIL TO FIND MySQL...RETRYING")
            time.sleep(5)
            retry -= 1

    print("STATUS : MySQL LOST IN THE DESERT...RETURNING HOME") # Exit program if all 10 tries fail
    exit(1)

# ESTABLISH DATABASE CONNECTION -----------------------------------------------------------------------------------
db = connect_db()
cursor = db.cursor()

# SOCKET SERVER SETUP ---------------------------------------------------------------------------------------------
server = socket.socket()
server.bind(("0.0.0.0", 6002))
server.listen(5)
print("STATUS : PYTHON IS LISTENING ON PORT 6002...PLEASE BE QUIET")

# MAIN OPERATION INFINTE LOOP -------------------------------------------------------------------------------------
while True:  # Keep server running
    conn, addr = server.accept() # wait and accept new client connection
    print(f"STATUS : CLIENT FROM {addr} IS NOW ONLINE") #show client IP and PORT
    
# UPDATE DATABASE -------------------------------------------------------------------------------------------------
    cursor.execute("""
        UPDATE leaderboard 
        SET points = points + 5, 
            datetime_stamp = CURRENT_TIMESTAMP 
        WHERE username = 'py_user'
    """)
    db.commit() # save change to database
    
# GET LATEST DATA -------------------------------------------------------------------------------------------------
    cursor.execute("SELECT username, points, datetime_stamp FROM leaderboard LIMIT 1")
    data = cursor.fetchone()
    
# PREPARE RESPONSE MESSAGE ----------------------------------------------------------------------------------------
    if data:
        response = f"User: {data[0]}, Points: {data[1]}, Last Update: {data[2]}"
    else:
        response = "No data available"
    
# SEND RESPONSE TO CLIENT -----------------------------------------------------------------------------------------
    conn.send(response.encode())
    conn.close()
    
# LOG THE UPDATE --------------------------------------------------------------------------------------------------
    print(f"STATUS : POINTS UPDATED TO {data[1]} AT {datetime.now()}")
    time.sleep(1)  # Small delay 