/*

THIS IS THE C CLIENT SECTION

WHAT DOES IT DO :
- Starts the Client, then repeatedly connects to C SERVER every 5 seconds
- Asks server the data from MySQL 
- Close the socket after each attempts and try again

*/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <netdb.h>

int main() {
    int sock;
    struct sockaddr_in serv_addr;
    struct hostent *server;
    char buffer[1024];

    printf("C Client started - asking every 5 seconds\n");

    while (1) {
        sock = socket(AF_INET, SOCK_STREAM, 0); //create new IPv4 TCP socket

//search hostname and find the IP address ------------------------------------------------------------
        server = gethostbyname("c_server"); 
        if (server == NULL) {
            printf("[ERROR] No such host\n");
            sleep(3);
            continue;
        }

//prepare the server address structure ----------------------------------------------------------------
        memset(&serv_addr, 0, sizeof(serv_addr));
        serv_addr.sin_family = AF_INET;
        serv_addr.sin_port = htons(6001); //set port number to 6001
        memcpy(&serv_addr.sin_addr.s_addr, server->h_addr, server->h_length);

        if (connect(sock, (struct sockaddr *)&serv_addr, sizeof(serv_addr)) == 0) {
            printf("[INFO] Connected to C server \n"); 
            
            read(sock, buffer, 1024); // Read data sent by the server into buffer
            printf("FROM C SERVER:\n%s\n", buffer); // Print the received data
            printf("--------------------------------------------------\n");
        } else {
            printf("[WARN] Server not ready...\n"); // Connection failed
        }

        close(sock); // Close the socket after each attempt
        sleep(5); // Wait 5 seconds before next connection attempt
    }
    return 0;
}