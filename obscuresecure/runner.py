from main import *

def input_parser(argv),pattern=["*.sf","*.mlp","e"]:
    for i in argv:


mode = sys.argv[1]
file_name = sys.argv[2]
folder_loc = sys.argv[3]
if mode == "E": # encrypt
    secret_data = sys.argv[4]
    Tofile(secret_data,file_name=file_name,folder_loc = folder_loc)
else: # decrypt
    ret = Fromfile(file_name=file_name,folder_loc = folder_loc)
    return ret
