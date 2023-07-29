# CS361_Microservice
Dual purpose microservice allowing for socket connectivity or local functionality

# Launching the Microservice
To launch the microservice on windows, open the containing folder in command line (cmd) and run Python3 server.py. You will be prompted to select a mode (local or socket) pick the mode that fits your needs.

# Requesting Data
## Local Mode
Local mode operates in a file called count.txt. When we request data, we need to write the filepath to the file we want the microservice to process to count.txt.
Python Example:
```Python
countfile = open("count.txt", "w")
countfile.write("test.txt") # if sharing the same directory with server.py, it can just be the file name
countfile.close()
```

## Socket Mode
To request data using the Socket mode, we need to request data to the IP address that the server is running on from a device on the same network. (to find out the ip address of the machine the server is running, open commandline and type 'ipconfig'. Look for the ipv4 address)
We will need to connect to the socket at port 60, then send a command, either read or write. For read out message must say "read", to write our message must begin with "Write:" followed by the data to be written.

Kotlin Example Read:
```Kotlin
val socket = Socket("192.168.50.95", 60)
val DOS = DataOutputStream(socket.getOutputStream())
val message = "read"
DOS.write(message.toByteArray())
```

Kotlin Example Write:
```Kotlin
val socket = Socket("192.168.50.95", 60)
val DOS = DataOutputStream(socket.getOutputStream())
val message = "Write:dataToBeWritten"
DOS.write(message.toByteArray())
```

# Receiving Data

## Local Mode
To obtain data from the local count operation, we need to 'listen' to the count.txt file. After we have send the filepath to count.txt, keep checking the file until the value has changed. 
Python Example:
```Python
  while True:
      print("Waiting...")
      countfile = open("count.txt", "r")
      content = countfile.readline()
      countfile.close()
      if "test.txt" not in content:
          print("Count Received: " + content)
          break
      time.sleep(3)
```
This example assumes we wrote test.txt to the file, then waits for that value not to be in the file any longer. It checks every 3 seconds.

## Socket Mode
Data from the microservice socket server comes in two forms, a confirmation message that the data was saved (for Write: functions) and the data we have stored (for read functions). Both will be received the same way. The client needs to listen to the input stream while the socket is still open, and after sending the command to the microservice.
Kotlin Example:
```Kotlin
//... connect to socket and send command ...
val DIS = DataInputStream(socket.getInputStream())
val inputStreamReader = InputStreamReader(DIS)
val bufferedReader = BufferedReader(inputStreamReader)
var reply: String? = ""
reply = bufferedReader.readLine()
Log.d("Data-FromServer", reply)
socket.close()
```
This example shows how to receive data from both commands, read and write. It takes the data in variable 'reply' and sends a log to the terminal with the results.

# UML Sequence Diagram
![UML](https://github.com/Jtauzin/CS361_Microservice/assets/39243613/36c96666-8423-4436-9622-903d89383a6c)
