// https://lenngro.github.io/how-to/2021/01/05/Simple-TCPIP-Server-Cpp/
#include <iostream>
#include <sys/types.h>
#include <unistd.h>
#include <sys/socket.h>
#include <netdb.h>
#include <arpa/inet.h>
#include <string.h>
#include <string>

float bytesRecv = 0.0f;
int clientSocket;

void tcp_socket() {
    std::cout << "Creating server socket..." << std::endl;
    int listening = socket(AF_INET, SOCK_STREAM, 0);
    if (listening == -1)
    {
        std::cerr << "Can't create a socket!";
        return;
    }

    struct sockaddr_in hint;
    hint.sin_family = AF_INET;
    hint.sin_port = htons(54000);
    inet_pton(AF_INET, "0.0.0.0", &hint.sin_addr);

    std::cout << "Binding socket to sockaddr..." << std::endl;
    if (bind(listening, (struct sockaddr *)&hint, sizeof(hint)) == -1) 
    {
        std::cerr << "Can't bind to IP/port";
        return;
    }

    std::cout << "Mark the socket for listening..." << std::endl;
    if (listen(listening, SOMAXCONN) == -1)
    {
        std::cerr << "Can't listen !";
        return;
    }

    sockaddr_in client;
    socklen_t clientSize = sizeof(client);

    std::cout << "Accept client call..." << std::endl;
    clientSocket = accept(listening, (struct sockaddr *)&client, &clientSize);

    std::cout << "Received call..." << std::endl;
    if (clientSocket == -1)
    {
        std::cerr << "Problem with client connecting!";
        return;
    }

    std::cout << "Client address: " << inet_ntoa(client.sin_addr) << " and port: " << client.sin_port << std::endl;

    close(listening);

    char buf[4096];
    while (true) {
        // clear buffer
        memset(buf, 0, 4096);

        // wait for a message
        bytesRecv = recv(clientSocket, buf, 4096, 0);
        if (bytesRecv == -1)
        {
            std::cerr << "There was a connection issue." << std::endl;
        }
        if (bytesRecv == 0)
        {
            std::cout << "The client disconnected" << std::endl;
        }
        
        // display message
        std::cout << "Received: " << std::stof(std::string(buf, 0, bytesRecv)) << std::endl;
        
		  // return message
        // send(clientSocket, buf, bytesRecv+1, 0);
    }
    // close socket
    // close(clientSocket);

    return;
}


int main() {
	tcp_socket();
	close(clientSocket);
	return 0;
}
