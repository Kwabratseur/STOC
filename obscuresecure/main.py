import random
import csv
import sys
import os
import base64
import itertools
import time
from PIL import Image

# DHM Functions
def isPrime(n):
    """"pre-condition: n is a nonnegative integer
    post-condition: return True if n is prime and False otherwise."""
    if n < 2:
        return False
    if n % 2 == 0:
         return n == 2  # return False
    k = 3
    while k*k <= n:
         if n % k == 0:
             return False
         k += 2
    return True

def reSeed():
    random.seed(os.urandom(1000))

def GetRand(Range = 10**5, LB = 10**1):
    reSeed()
    return random.randint(LB,Range)

def GetPrime(p,Pr):
    x = 0
    while isPrime(x) == False:
        x = random.randint(p,Pr)
    return x
    #return next(i for i in [random.randint(p,Pr)|1 for x in itertools.count()] if isPrime(i))

#Generate public key: A = g^a mod p, also generates secret key.
def PubKey(p,g,a):
    return (g**a)%p

# generates public numbers for pubkey
def GetPublicNumbers(Pr = 10**16,Gr = 10**3):
    reSeed()
    p = 10**1
    Prime = GetPrime(p,Pr)
    Prime2 = GetPrime(p,Pr)
    reSeed()
    Number = random.randint(p,Gr)
    return Prime*Prime2,Number
# EOF DHM Functions

# DHM Demonstration Function; Needs to be expanded
def DHM_Demonstration():
    #communication handshake (1/2) initialization
    print("This is alice")
    msg = "This is very secret and should absoluterly not be found by anyone! :o"
    print("This message needs to be sent:")
    print(msg)
    a = GetRand(10**5,10**3)
    p, g = GetPublicNumbers()
    A = PubKey(p,g,a)
    print(("Alice Generated prime p:{}, base g:{} and secret number a:{} \n which results in public key A:{}".format(p,g,a,A)))
    print(A)
    # THIS IS NOT SAFE FOR MITM! some sort of authentication needs to be added.
    # Alice has to prove with high confidence that she is alice.

    # Communication handshake (2/2)
    print("This is Bob")
    print("Bob is thankfull to receive p, g and A.")
    b = GetRand(10**5,10**3)
    #p, g = GetPublicNumbers() # received from alice!
    B = PubKey(p,g,b)
    Kbob = PubKey(p,A,b)
    print(("Bob sends his pubkey B:{} to alice, so she can calculate secret key K:{}".format(B,Kbob)))
    print("Public key:")
    print((len(bin(Kbob))))
    print((bin(Kbob)))

    # Communication setup complete, secret key is exchanged.
    print(("Alice receives Bob's B:{} and can now calculate secret key K.".format(B)))
    Kalice = PubKey(p,B,a)
    print(("The only public data is: p:{}, g:{}, A:{}, B:{}".format(p,g,A,B)))
    print(("The secret keys are: bob:{}, Alice:{}".format(Kbob,Kalice)))

    # simple communication example.
    print("Now bob and alice are the only people on the world who have the same secret key, they can encode messages with it :]")
    print(("So lets send: '{}' ".format(msg)))
    asciimsg = int(SASCII(msg))                     ###################<<----------------------- error; if we can integrate Ext_V2 at this point; use key as pass and add the files to the data; figure out a way to separate these in a subtle way
    print(("And in ascii coded: {}".format(asciimsg)))
    start = time.time()
    encodedmsg = asciimsg*Kalice
    print(("It took {} seconds to Encode message With K: {}".format((start-time.time()),encodedmsg)))
    encHex = hex(encodedmsg)
    print(("in hex format:{}".format(encHex)))

    print(("Bob now receives the msg in Hex format to further 'encode' the message: {}".format(encHex)))
    decodedLong = int(encHex,16)
    print(("Bob now returns the message to base 10:{}".format(decodedLong)))
    bobRcv = decodedLong/Kbob
    print(("And bob uses his secret key to demodulate the message: {}".format(bobRcv)))
    bobmsg = ASCIIS(bobRcv)
    print(("bob now looks up a ascii chart to restore the message. \nWhich is: '{}'.".format(bobmsg)))
# EOF DHM Demonstration Function

def Randstr(N):
    return ''.join(random.SystemRandom().choice("0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ+/") for _ in range(N))

def InitVector(Key): # initialization vector for blockchain encryption, also converts secret key.
    if type(Key)==type(""):
        Hex = Key
    else:
        Hex = hex(Key)
        Hex = Hex[2:]
        Hex = Hex[:-1]
    Chaos = Randstr(len(Hex))
    return Hex, Chaos

def xor_crypt_V2(data, key='awesomepassword',HashKey=None, encode=False, decode=False,debug = False):
    if len(data) == 0:
        return ";]"
    Klen = len(key)
    if encode:
        if HashKey == None:
            HashKey = Randstr(len(key))
        data = "{}{}".format(HashKey,data)
    if decode:
        if debug:
            print(data,type(data))
        data = data[2:-1]
        if debug:
            print(data)
        data = base64.b64decode(data).decode()
        if debug:
            print(data)
    c = 0
    xored = ""
    if debug:
        print("\n\nHkey:{}".format(HashKey))
        print("startkey:{},{}".format(key,HashKey))
        print("startdata:{}, encode:{}, decode:{}".format(data,encode,decode))
    for x in str(data):
        if c > len(key)-1:
            key = xored[len(xored)-len(key):]
            if decode:
                key = data[len(xored)-len(key):]
            if debug:
                print("Keychange:{} - Mode:{}".format(key,encode))
            c = 0
        y = key[c]
        if debug:
            print(x,y)
        xored += chr(ord(x) ^ ord(y))
        if debug:
            print(xored)
        c += 1
    #xored = ''.join(chr(ord(x) ^ ord(y)) for (x,y) in izip(data, cycle(key)))
    if debug:
        print("enddata:{}\n\n".format(xored))
    if encode:
        if debug:
            print(xored,xored.encode())
        return base64.b64encode(xored.encode()).strip()
    if decode:
        return xored[Klen:]
    return xored

def Save(File="data",pre="ponyisland",data = None,folder = None):
    if folder is not None:
        folder = folder
    else:
        folder = ""
    ext0 = ".sf"
    ext1 = ".mlp"
    if data is not None: # save data
        sf = open("{}{}_{}{}".format(folder,pre,File,ext0),'w')
        sfw = csv.writer(sf)
        sfw.writerows([[data[0]]])
        sf.close()
        kf = open("{}{}_{}{}".format(folder,pre,File,ext1),'w')
        kfw = csv.writer(kf)
        kfw.writerows([[data[1]]])
        kf.close()
        return True
    else: # open secret_data
        sf = open("{}{}_{}{}".format(folder,pre,File,ext0),'r')
        data1 = sf.readline()
        sf.close()
        kf = open("{}{}_{}{}".format(folder,pre,File,ext1),'r')
        data2 = kf.readline()
        kf.close()
        #print data1.replace("\n",""), data2
        return [data1.replace("\n","").replace("\r",""),data2.replace("\n","").replace("\r","")]

def ECCD(decrypted,arr):
    Array = decrypted[2:-1].replace('x','').split('\\')[1:]
    for i, x in enumerate(Array):
        if len(str(x)) > 2:
            if type(x) == type(10):
                Array[i] = x
            else:
                Array.insert(i+1,x[2:])
                Array[i] = x[:2]
        try:
            Array[i] = int(x,16)
            if int(x,16) > 256:
                remainder = int(x,16)
                while remainder > 256:
                    remainder = remainder/256
                    Array.insert(i,256)
                Array.insert(i,int(remainder))
        except:
            Array[i] = 0
    print("Restored {} % of original data.".format((len(Array)/len(arr[0]))*100))
    for i in range(len(arr[0]) - len(Array)):
        Array.append(0)
    return bytes(Array)

def ObfuscateImage(image):
    arr = []
    im = Image.open(image)
    #im.frombytes(StrImg)
    StrImg = im.tobytes()
    arr.append(StrImg)
    encryptord = Tofile(StrImg)
    decryptord = Fromfile()
    arr.append(encryptord)
    arr.append(decryptord)
    im.frombytes(ECCD(decryptord,arr))
    im.save("DETuxSC.ppm")
    im.frombytes(encryptord)
    im.save("ETuxSC.ppm")
    return arr

def Fromfile(file_name = "data",PreFix = "ponyisland",folder_loc = "", debug=False):
    result, Key = Save(File = file_name,pre=PreFix, folder = folder_loc)
    Decoded = xor_crypt_V2(result,key=Key, decode=True,debug = debug)
    if debug:
        print("decrypted {} to {}".format(result,Decoded))
    return Decoded

def Tofile(data,file_name = "data",PreFix = "ponyisland",folder_loc = "", debug=False):
    Key = Randstr(len(data))
    Key,Hkey = InitVector(Key)
    result = xor_crypt_V2(data, key=Key,HashKey=Hkey,encode=True,debug = debug)
    if debug:
        print("Encrypted {} to {}".format(data,result))
    Save(File = file_name, pre=PreFix, data = [result,Key], folder = folder_loc)
    return result

def main():
    print(Fromfile())
    #ObfuscateImage("IPYS/tux.png")


if __name__ == "__main__":
    print(("%s is being run directly"%__name__))
    try:
        main()
    except RuntimeError:
        print("Error!")
else:
    print("---\n{}\n---\nis being imported\n---".format(sys.argv[0]))
