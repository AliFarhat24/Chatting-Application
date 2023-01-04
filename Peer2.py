import socket
import threading
import time

global seq, ack, msg, seq_rec 

seq=0
ack=1
ack_rec=0
seq_rec=0
file_number=0
Hussam = ('127.0.0.1', 12000)


def request_image():
    # Create a TCP socket and Bind it to the port
    c2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
    c2.bind(('127.0.0.100', 12000))
    # Now wait for Peer connection.
    c2.listen(5)                    
    print ("I am listening..")

    # Establish connection with another peer.
    conn, addr = c2.accept()    
    print ("Got connection from", addr)
    data = conn.recv(1024)
    print('I received:', repr(data))

    #In the same folder or path is this file running
    # must the file you want to tranfser to be
    filename=input("Enter the name of the file you want to send: ") 
    f = open(filename,'rb')
    l = f.read(1024)

    while (l):
        conn.send(l)
        l = f.read(1024)
    f.close()
    print('Done sending')
    conn.close()

def recive_image():
    global file_number
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
    client.connect(('127.0.0.100', 12000))
    client.send(b"Hello Peer!")
    file_number=str(file_number)

    with open('Received File'+file_number+'.jpeg', 'wb') as f:
        print ('file opened')
        print('receiving data...')
        data = client.recv(1024)
        f.write(data)

    f.close()
    print('Successfully get the file')
    client.close()
    print('connection closed')
    file_number=int(file_number)
    file_number=file_number+1


def requestf():
    # Create a TCP socket and Bind it to the port
    c2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
    c2.bind(('127.0.0.1', 12000))
    # Now wait for Peer connection.
    c2.listen(5)                    
    print ("I am listening..")

    # Establish connection with another peer.
    conn, addr = c2.accept()    
    print ("Got connection from", addr)
    data = conn.recv(1024)
    print('I received:', repr(data))

    #In the same folder or path is this file running
    #must the file you want to tranfser to be
    filename=input("Enter the name of the file you want to send: ")
    f = open(filename,'rb')
    l = f.read(1024)

    while (l):
        conn.send(l)
        #print('Sent: ',repr(l))
        l = f.read(1024)
    f.close()
    print('Done sending')
    conn.close()

def recivef():
    global file_number
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
    client.connect(('127.0.0.1', 12000))
    client.send(b"Hello Peer!")
    file_number=str(file_number)
    with open('Received_File'+file_number+'.txt', 'wb') as f:
        print ('file opened')
        while True:
            print('receiving data...')
            data = client.recv(1024)
            #print('data=%s', (data))
            if not data:
                break
            # write data to a file
            f.write(data)

    f.close()
    print('Successfully get the file')
    client.close()
    print('connection closed')
    file_number=int(file_number)
    file_number=file_number+1

# Connect to Hussam
print('connecting to Hussam server')

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('127.0.0.11', 12011))
sock.sendto(b'0', Hussam)

while True:
    data = sock.recv(1024).decode()

    if data.strip() == 'ready':
        print('checked in with server, waiting')
        break

data = sock.recv(1024).decode()
ip, sport, dport = data.split(' ')
sport = int(sport)
dport = int(dport)

print('\ngot peer')
print('  ip:          {}'.format(ip))
print('  source port: {}'.format(sport))
print('  dest port:   {}\n'.format(dport))
print("To request sending a file, write /file")
print("To request sending an image, write /image\n")

# punch hole

print('punching hole')
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('127.0.0.11', sport))
sock.sendto(b'0', (ip, dport))
print('ready to exchange messages\n')

# listen for
def listen():
    global ack_rec
    global seq_rec
    global ack
    global var

    while True:
        data = sock.recv(1024)
        data = data.decode()

        if len(data)==1:
            ack_rec=data
            var=0
            #print("ack_rec is: ", data)
        else:
            if seq_rec==data[0]:
                pass
            else:
                seq_rec=data[0]
                #print("seq_rec is: " , seq_rec)
                if data[1:]=="/file":
                    recivef()
                if data[1:]=="/image":
                    recive_image()
                print('\rpeer2: {}\n> '.format(data[1:]), end='')
                sock.sendto(((seq_rec).encode()), (ip, dport))
                #print("ack sent is: ",seq_rec )

listener = threading.Thread(target=listen, daemon=True);
listener.start()

# send messages
while True:
    msg = input('> ')
    seq=str(seq)
    sock.sendto(((seq+msg).encode()), (ip, dport))
    seq=int(not(bool(int(seq))))
    var=1
    if msg=="/file":
        requestf()
    if msg=="/image":
        request_image()
    t=time.process_time()
    while(True):
        if var==0:
            break
        if ((time.process_time()-t) >1):
            seq=str(seq)
            sock.sendto(((seq+msg).encode()), (ip, dport))
            t=time.process_time()
    




    