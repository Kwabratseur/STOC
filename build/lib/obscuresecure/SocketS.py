import socket
from main import *
import time

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)

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

def RecvMsg(HOST,PORT,Msg = "standardmsg"):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen()
        conn, addr = s.accept()
        with conn:
            print('Connected by', addr)
            while True:
                data = conn.recv(1024)
                conn.sendall(str.encode(Msg))
                if not data:
                    break
                return data

def SM_Server(step,PN,Ready,msg=""):
    data = RecvMsg(HOST,PORT,Msg=msg)
    Message = "Message_Unchanged"
    step += 1
    if step == 1:
        if data == b"ConnectDHM":
            print("{} Handshaking - 0.0 {}".format(step,data))
            Message = str(PN)
            print("{} Response - 0.0 {}".format(step,Message))
        else:
            print("Reset at step {}".format(step))
            step = 0
            PN = []
            Message = "Error - authentication"
    elif step == 2:
        print(data,type(data))
        print("{} Negotiating - 1.1 {}".format(step,data))
        if data == b"CPUB,pgB":
            print(PN)
            Message = "1.2"
        else:
            print("Reset at step {}".format(step))
            step = 0
            PN = []
        print("{} Response - 1.1 {}".format(step,Message))
    elif step == 3:
        print("Ready")
        Data = DecodeArray(data)
        print("{} Negotiating - 1.2 {}".format(step,Data))
        if Data[0] == "CPUB":
            PN.append(int(Data[4]))
            PN.append(PubKey(PN[1],PN[4],a))
            print(PN)
            Message = "Ready"
        print("{} Response - 1.2: {}".format(step,Message))
        # keys are setup, communication is secure
    elif step > 3:
        print("COM: {} - {}".format(step,data))
        Ready = True
    return [step,PN,Message,Ready]


step = 0
PN = []
print("Starting RNG and cryptographic number generation")
a = GetRand(10**4,10**1)
print("Finished getting random number")
p, g = GetPublicNumbers(10**2,10**3)
print("Finished getting public numbers")
A = PubKey(p,g,a)
print("Finished getting public key")
PN = ["SPUB,pgA",p,g,A]
Message = "Hellur"
Ready = False
print("Starting")
while True:
    step, PN, Message, Ready = SM_Server(step,PN,Ready,Message)
