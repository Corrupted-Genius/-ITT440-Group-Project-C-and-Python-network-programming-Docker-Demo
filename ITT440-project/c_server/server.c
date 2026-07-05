/*

THIS IS THE C SERVER SECTION

WHAT DOES IT DO?
- Runs inside docker container
- Connects to MySQL database
- Listen for clients on port 6001 (port number already set in C CLIENT)
- Everytime C CLIENT connects, it update the leaderboard record 
- Send the latest data back to the C CLIENT for next chain execution

*/


#include <mysql/mysql.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>

int main() {
    int server_fd, new_socket;
    struct sockaddr_in address;
    int addrlen = sizeof(address);
    MYSQL *conn;

    printf("Starting C Server...\n");

    // INITIALIZE MySQL CONNECTION ------------------------------------------------------------------------------------
    conn = mysql_init(NULL);
    if (conn == NULL) {
        printf(" mysql_init failed\n");
        return 1;
    }

    // CONNECT TO MySQL WITH 10x RETRY OPTION -------------------------------------------------------------------------
    int retry = 10;
    while (retry > 0) {
        if (mysql_real_connect(conn, "mysql_db", "root", "", "itt440", 3306, NULL, 0)) {
            printf(" C Server connected to MySQL successfully\n");
            break;
        }
        printf("[WARN] MySQL not ready, retrying... (%d left)\n", retry);
        sleep(3);
        retry--;
    }

    if (retry == 0) {
        printf(" Failed to connect to MySQL\n");
        return 1;
    }

    // CREATE TCP SOCKET AND SERVER ADDRESS CONFIGURATION --------------------------------------------------------------
    server_fd = socket(AF_INET, SOCK_STREAM, 0);
    address.sin_family = AF_INET;
    address.sin_addr.s_addr = INADDR_ANY;
    address.sin_port = htons(6001);

    // BIND SOCKET -----------------------------------------------------------------------------------------------------
    if (bind(server_fd, (struct sockaddr *)&address, sizeof(address)) < 0) {
        printf(" Bind failed\n");
        return 1;
    }

    listen(server_fd, 5); 
    printf(" C Server listening on port 6001...\n");

    // MAIN SECTION, APPLY INFINITE LOOP --------------------------------------------------------------------------------
    while (1) {

        // Accept new client connection
        new_socket = accept(server_fd, (struct sockaddr *)&address, (socklen_t*)&addrlen);
        if (new_socket < 0) {
            printf(" Accept failed\n");
            sleep(1);
            continue;
        }

        printf(" CLIENT STATUS : CONNECTED TO C SERVER\n");

        // BEGIN THE DATABASE OPERATION
        // Try to create row
        if (mysql_query(conn, "INSERT IGNORE INTO leaderboard (username, points) VALUES ('c_user', 5)")) {
            printf(" Insert failed: %s\n", mysql_error(conn));
        } else {
            printf(" Row ensured\n");
        }

        // Update points and timestamp
        if (mysql_query(conn, "UPDATE leaderboard SET points = points + 5, datetime_stamp = CURRENT_TIMESTAMP WHERE username = 'c_user'")) {
            printf(" Update failed: %s\n", mysql_error(conn));
        } else {
            printf(" Update successful! Rows affected: %lu\n", (unsigned long)mysql_affected_rows(conn));
        }

        // Get current value
        MYSQL_RES *res; // To hold query result set
        MYSQL_ROW row; // To hold one row of data
        mysql_query(conn, "SELECT username, points, datetime_stamp FROM leaderboard WHERE username = 'c_user' ORDER BY id DESC LIMIT 1");
        res = mysql_store_result(conn); // Store the result of the query
        row = mysql_fetch_row(res); // Fetch the first (and only) row

        // RESPONSE MESSAGE -----------------------------------------------------------------------------------------------
        char response[256];
        if (row) {
            snprintf(response, sizeof(response), "User: %s, Points: %s, Last Update: %s", row[0], row[1], row[2]);
            printf("Current c_user: %s points\n", row[1]);
        } else {
            strcpy(response, "No data available");
            printf(" No row found for c_user\n");
        }

        send(new_socket, response, strlen(response), 0); // send response back to client
        close(new_socket);
        mysql_free_result(res);
    }

    mysql_close(conn);
    return 0;
}