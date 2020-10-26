from socket import *
from base64 import *
import ssl

receiver = input("Enter receiver's email: ")
sender = input("Enter sender's email: ")
subject = input("Enter subject: ")
password = input("Enter sender's password: ")
body = input("Enter message: ")

msg = '{}. \r\nI love computer networks!'.format(body)
endMsg = '\r\n.\r\n'

# Choose a mail server (e.g. Google mail server) and call it mailserver
mailServer = "smtp.gmail.com"
mailPort = 587

# Create socket called clientSocket and establish a TCP connection with mailserver
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((mailServer, mailPort))
recv = clientSocket.recv(1024)
print(recv)
if recv[:3] != '220':
    print('220 reply not received from server.')

# Send HELO command and print server response.
heloCommand = 'HELO Alice\r\n'.encode()
clientSocket.send(heloCommand)
recv1 = clientSocket.recv(1024)
print(recv1)
if recv1[:3] != '250':
    print('250 reply not received from server.')

# Account Authentication
strtlscmd = "STARTTLS\r\n".encode()
clientSocket.send(strtlscmd)
recv2 = clientSocket.recv(1024)
sslClientSocket = ssl.wrap_socket(clientSocket)
EMAIL_ADDRESS = b64encode(sender.encode())
EMAIL_PASSWORD = b64encode(password.encode())
authorizationcmd = "AUTH LOGIN\r\n"
sslClientSocket.send(authorizationcmd.encode())
recv2 = sslClientSocket.recv(1024)
print(recv2)
sslClientSocket.send(EMAIL_ADDRESS + "\r\n".encode())
recv3 = sslClientSocket.recv(1024)
print(recv3)
sslClientSocket.send(EMAIL_PASSWORD + "\r\n".encode())
recv4 = sslClientSocket.recv(1024)
print(recv4)

# Send MAIL FROM command and print server response.
mailfrom = "MAIL FROM: <{}>\r\n".format(sender)
sslClientSocket.send(mailfrom.encode())
recv5 = sslClientSocket.recv(1024)
print(recv5)

# Send RCPT TO command and print server response.
rcptto = "RCPT TO: <{}>\r\n".format(receiver)
sslClientSocket.send(rcptto.encode())
recv6 = sslClientSocket.recv(1024)

# Send DATA command and print server response.
data = 'DATA\r\n'
sslClientSocket.send(data.encode())
recv7 = sslClientSocket.recv(1024)
print(recv7)

# Send message data.
sslClientSocket.send("Subject: {}\n\n{}".format(subject, msg).encode())

# Message ends with a single period.
sslClientSocket.send(endMsg.encode())
recv8 = sslClientSocket.recv(1024)
print(recv8)

# Send QUIT command and get server response.
quitcommand = 'QUIT\r\n'
sslClientSocket.send(quitcommand.encode())
recv9 = sslClientSocket.recv(1024)
print(recv9)
sslClientSocket.close()