# Coded in python 3
#region Imports

import socket
import sys

#endregion
#region Function to create a socket
def socket_create():
    try:
        global host
        global port
        global s
        host = ""  # Hostname (empty means localhost)
        port = 9999  # Port to listen on
        s = socket.socket()  # Create a new socket object
    except socket.error as msg:
        print("Socket creation error: " + str(msg))
#endregion

#region Function to bind the socket to a port and wait for connections from clients
def socket_bind():
    try:
        global host
        global port
        global s
        print("Binding socket to port:  " + str(port))
        s.bind((host,port))  # Bind the socket to the host and port
        s.listen(5)  # Listen for incoming connections, allowing a backlog of up to 5 connections
    except socket.error as msg:
        print("Socket binding error:  " + str(msg) + "\n" + "Retrying.....")
        socket_bind()  # Retry if there's an error
#endregion

#region Function to establish a connection with a client
def socket_accept():
    conn,address = s.accept()  # Accept a connection and get the client's socket object and address
    print("Connection has been established | " + "IP " + address[0] + " | Port " + str(address[1]))
    send_commands(conn)  # Once connected, start sending commands
    conn.close()
#endregion

#region Function to send commands to the client
def send_commands(conn):
    while True:
        cmd = input()  # Get user input for commands to send
        if cmd == "quit":
            conn.close()  # Close the connection
            s.close()  # Close the socket
            sys.exit()  # Exit the program
        if len(str.encode(cmd)) > 0:  # Check if the command is not empty
            conn.send(str.encode(cmd))  # Send the command to the client
            client_response = str(conn.recv(1024), "utf-8")  # Receive response from client
            print(client_response, end="")  # Print the response
#endregion

#region Main function to run the program
def main():
    socket_create()  # Create the socket
    socket_bind()  # Bind the socket to a port
    socket_accept()  # Accept connections from clients

main()  # Run the main function
#endregion


