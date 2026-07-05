# THIS IS THE PYTHON CLIENT SECTION

# WHAT DOES IT DO :
#- Starts the Client, then repeatedly connects to PYTHON SERVER every 5 seconds
#- Asks server the data from MySQL 
#- Close the socket after each attempts and try again

import socket
import time

print("STATUS : PYTHON IS ALIVE... STARTING SEQUENCE")
print("Will keep asking for latest data every 5 seconds...\n")

count = 0

while True: # Client will continue until manually stopped
    count += 1

    try: # better error handling
        client = socket.socket() # create new socket for each attempt
        client.connect(("py_server", 6002)) # connect to container
        
        print(f"[{count}] STATUS : PYTHON CONNECTED TO PYTHON SERVER...INITIATE OPERATION")
        
        # Receive data from server, decode it and display it
        data = client.recv(1024)
        print("FROM PY SERVER:")
        print(data.decode()) # decide bytes to string and then print the data
        print("-" * 60)
        
        client.close() # close the connection
        
    except Exception as e:
        print(f"[{count}] STATUS : PYTHON FAILED TO FIND THE SERVER...RETRYING ({e})")
    
    time.sleep(5)   # Update every 5 seconds