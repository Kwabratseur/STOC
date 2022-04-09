import socket
from main import *
import time

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 65432        # The port used by the server
def decoder(Data):
    try:
        Data = Data.split(",")
        Data[0] = Data[0].split('[')[1]
        Data[0] = Data[0].split("'")[1]
        Data[1] = Data[1].split("'")[0]
        Data[-1] = Data[-1].split(']')[0]
        return Data
    except:
        return [0,0,0,0]

def DecodeArray(Data):
    a2 = Data.decode("utf-8")
    return decoder(a2)



def SendMsg(HOST,PORT,msg):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            s.sendall(msg)
            data = s.recv(1024)
            while not data:

                data = s.recv(1024)
            return data
    except:
        print("Oopsie")

def SM_Client(step,PN, Ready,Message):
    step += 1
    if step == 1:
        print("{} Handshaking - 0.1 {}".format(step,b"ConnectDHM"))
        data = SendMsg(HOST,PORT,b"ConnectDHM")
        if data and data == b'Hellur':
            print("{} Response - 0.1: {}".format(step,data))
        else:
            print("{} Error - 0.1: {}".format(step,data))
            step = 0
    if step == 2:
        data = SendMsg(HOST,PORT,b"CPUB,pgB")
        print("{} Negotiating - 1.1 {}".format(step,b"CPUB,pgB"))
        Data = DecodeArray(data)
        print(Data)
        if Data[0] == "SPUB":
            print("{} Response - 1.1: {}".format(step,Data))
            PN = ["CPUB,pgB",int(Data[2]),int(Data[3]),int(Data[4])]
            B = PubKey(PN[1],PN[2],b)
            PN.insert(3,B)
            print("Generating Public Key:{}".format(PN))
        else:
            print("{} Error - 1.1: {}".format(step,data))
            step = 1

    if step == 3:
        print("{} Negotiating - 1.2 {}".format(step,PN))
        data = SendMsg(HOST,PORT,str.encode(str(PN[:-1])))
        if data and data == b"1.2":
            PN.append(PubKey(PN[1],PN[4],b))
            print("{} Response - 1.2: {}".format(step,data))
        else:
            step = 2
            print("{} ERROR - 1.2: {}".format(step,data))
    elif step > 3:
        Ready = True
        data = SendMsg(HOST,PORT,str.encode(Message))
        print("COM:{} - {}".format(step,data))
    return [step,PN,Message,Ready]



step = 0
PN = []
Message = ""
Ready = False
b = GetRand(10**4,10**1)
while True:
    step, PN, Message, Ready = SM_Client(step,PN, Ready,Message)
    time.sleep(5)




def SM_Server(step,PN,msg=""):
    conn,data = RecvMsg(HOST,PORT)
    Message = ""
    step += 1
    if step == 1:
        if Data[0] == "SPUB,pgA":
            print("Handshaking - 0.0", Data)
            a = GetRand(10**5,10**3)
            p, g = GetPublicNumbers()
            A = PubKey(p,g,a)
            PN = ["SPUB,pgA",p,g,A]
            conn.sendall(PN)
        else:
            step = 0
            PN = []
        # generate p,g,a
        # calculate A
        # send p,g,A
    elif step == 2:
        if Data[0] == "CPUB,pgB":
            PN.append(Data[1])
            PN.append(PubKey(Data[1],PN[3],PN[4]))
            conn.sendall("OK!")
        else:
            step = 0
            PN = []
    elif step > 2:
        print("Ready")
        # keys are setup, communication is secure

    return [step,PN,Message]
