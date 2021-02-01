import argparse
from main import *

my_parser = argparse.ArgumentParser()
my_parser.add_argument('input', action='store', type=str, help='input file or data, will be used as suffix if supplied. Otherwise data is suffix.')
my_parser.add_argument('-encode', action='store_true', help='Encode input')
my_parser.add_argument('-decode', action='store_true', help='Decode input')
my_parser.add_argument('-folder', action='store', default = '', help='Give folder to load/store data')
my_parser.add_argument('-prefix', action='store',default="ponyisland", type=str, help='prefix for encrypted files')

args = my_parser.parse_args()
Folder = args.folder
prefix = args.prefix
suffix = "data"
Decode = True
try:
    file = open(args.input)
    Name = args.input.split('/')[-1]
    if len(args.input.split('/')) > 1:
        Folder = "/".join(args.input.split('/')[:-1]) + "/"
    if len(Name.split("_")) == 2:
        suffix=Name.split(".")[0].split("_")[1]
        prefix=Name.split(".")[0].split("_")[0]
    else:
        prefix=Name.split(".")[0]
    Data = file.read()
    file.close()
except:
    Data=args.input

if args.encode:
    Decode = False

if Decode:
    Fromfile(file_name=suffix,PreFix=prefix,folder_loc=Folder)
else: # encode
    Tofile(data=Data,file_name = suffix,PreFix = prefix,folder_loc = Folder)
