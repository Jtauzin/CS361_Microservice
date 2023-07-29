import socket
import time

# On launch, figure out what mode we need to be in
mode = input("Enter mode: (socket or local) ")
while True:
    if mode.lower() == "socket" or mode.lower() == "local":
        break
    else:
        mode = input("Try again - Enter mode: (socket or local) ")

# Activate socket mode, listening on the correct port / ip address
if mode.lower() == "socket":
    active_socket = socket.socket()
    active_socket.bind(("0.0.0.0", 60))  # Automatically sets to local ipv4
    active_socket.listen(10)
    print("server activated...")

    while True:
        sock, addr = active_socket.accept()
        rec = sock.recv(1024).decode("utf-8")
        # If Write command, save the data to a local file by appending its contents
        if "Write:" in rec:
            print(f"Received {rec!r}")
            savedata = open("gym.txt", 'a')
            rec = rec.replace("Write:", "")
            savedata.write(rec)
            savedata.close()
            response = ("Data saved to server!").encode("utf-8")
            sock.sendall(response)
            sock.close()
        # If read command, read the current saved data and send back to the client
        elif rec == "read":
            savedata = open("gym.txt", 'r')
            savetext = savedata.readline()
            response = savetext.encode("utf-8")
            sock.sendall(response)
            print("Data sent to client")
            savedata.close()
            sock.close()
        # Anything else is a command to close the server
        else:
            sock.close()
            break
    # shutdown
    print("closing server...")
    active_socket.close()

# If local, check count.txt for commands
elif mode.lower() == "local":
    while True:
        countfile = open("count.txt", 'r')
        response = str(countfile.readline())
        countfile.close()
        if response == "quit":
            break
        # if there is a txt file path or csv file path in count.txt, count the entries in the file
        #  separated by commas and write that to the count file
        elif ".txt" in response or ".csv" in response:
            csv_to_process = open(response, 'r')
            file_data = csv_to_process.read()
            data_array = file_data.split(",")
            countfile = open("count.txt", 'w')
            response = str(len(data_array))
            countfile.write(response)
            print("count is " + response)
            countfile.close()
        else:
            print("waiting for command...")
            time.sleep(3)

# loop to count csv file items
