from main import *



def mode_enc(args):
    print("encrypting {}".format(args[0]))
    if len(args[0].split(".")) > 0:
        file = open(args[0],'r')
        args[1][1] = file.read()
        file.close()
        print("File detected, content: \n{}\n---------".format(args[1][0]))
    else:
        args[1][1] = args[0]
    return args[1]

def mode_dec(args):
    print("decrypting {}".format(args[0]))
    if len(args[0].split(".")) > 0:
        file = open(args[0],'r')
        args[1][1] = file.read()
        file.close()
        print("File detected, content: \n{}\n---------".format(args[1][0]))
        args[1][3] = args[0].split(".")[0]
        args[1][0] = False
    else:
        args[1][1] = args[0]
        args[1][0] = False
    return args[1]

def Folder(args):
    print("Folder is {}".format(args[0]))
    return args[1][2]

def Name(args):
    print("Name is {}".format(args[0]))
    args[1][3] = args[0]
    return args[1]

def Output(args):
    print("Output is {}".format(args[0]))
    args[1][4] = args[0]
    return args[1]

options = {"-e":mode_enc,
           "-d":mode_dec,
           "-f":Folder,
           "-n":Name,
           "-o":Output
          }

def input_parser(argv):
    Internal_Mode = [True,"","","",False]
    for i,x in enumerate(argv):
        if x[0] == "-":
            try:
                Internal_Mode = options[x]([argv[i+1],Internal_Mode])
            except KeyError:
                print("{} is not a valid argument. Check help(STOC)")
    print("Encrypt: {}\nData: {}\nFolder: {}\nName: {}\nOutput: {}".format(Internal_Mode[0],Internal_Mode[1],Internal_Mode[2],Internal_Mode[3],Internal_Mode[4]))
    return Internal_Mode

def Run(Internal_Mode):
    if Internal_Mode[3] != "":
        # load input from name
    if Internal_Mode[0] == True:
        # Encrypt
    else:
        # Decrypt
    if Internal_Mode[4] != False:
        #Output file
        if Internal_Mode[2] != "":
            #Output to folder
    else:
        #Output on cli


Internal_Mode = input_parser(sys.argv)

def Fromfile(file_name = "data",folder_loc = ""):
    result, Key = Save(File = file_name, folder = folder_loc)
    Decoded = xor_crypt_V2(result,key=Key, decode=True,debug = False)
    print("decrypted {} to {}".format(result,Decoded))
    return Decoded

def Tofile(data,file_name = "data",folder_loc = ""):
    Key = Randstr(len(data))
    Key,Hkey = InitVector(Key)
    result = xor_crypt_V2(data, key=Key,HashKey=Hkey,encode=True,debug = False)
    print("Encrypted {} to {}".format(data,result))
    Save(File = file_name,data = [result,Key], folder = folder_loc)

# mode = sys.argv[1]
# file_name = sys.argv[2]
# folder_loc = sys.argv[3]
# if mode == "E": # encrypt
#     secret_data = sys.argv[4]
#     Tofile(secret_data,file_name=file_name,folder_loc = folder_loc)
# else: # decrypt
#     ret = Fromfile(file_name=file_name,folder_loc = folder_loc)
#     return ret
