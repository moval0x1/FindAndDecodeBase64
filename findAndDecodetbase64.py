#-------------------------------------------------------------------------------
# Name:        Find&Decode Base64
# Purpose:     Search default base64 strings in powershell files and decode :)
#
# Author:      Charles Lomboni
#
# Created:     05/11/2018
# Copyright:   (c) Charles Lomboni 2018
# Licence:     MIT
#-------------------------------------------------------------------------------
from termcolor import colored
import base64
import pyfiglet
import shutil
import argparse

def banner():
    result = pyfiglet.figlet_format("Find&Decode Base64")
    print(result)


def getargs():
    # script name
    parser = argparse.ArgumentParser("findAndDecodetbase64")

    # needed args
    parser.add_argument("EncodedFile", help="Path + name to encrypted file.")

    return parser.parse_args()


def findAndReplace(fileName, textToSearch, textToReplace):
    # Read in the file
    with open(fileName, 'r') as file :
      filedata = file.read()

    # Replace the target string
    filedata = filedata.replace(textToSearch, textToReplace)

    # Write the file out again
    with open(fileName, 'w') as file:
      file.write(filedata)


def backupFile(originalFile, bkpFile):
    shutil.copyfile(originalFile, bkpFile)


def renameFile(originalFile, newFile):
    shutil.move(originalFile, newFile)


def main():

    stringSearch = 'FromBase64String'

    args = getargs()

    # open encoded file
    fileRead = open(args.EncodedFile)

    backupFile(args.EncodedFile, args.EncodedFile + '.bkp')

    try:
        # sweep each line from file
        for line in fileRead:

            # if match
            if line.find(stringSearch) != -1:
                # split by separator '::'
                splitedString = line.split('::')

                # sweep itens splited
                for splitLine in splitedString:
                    # if match
                    if splitLine.find(stringSearch) != -1:
                        # FromBase64String('VABoAG==')))
                        base64SplitedLine = splitLine.split('\'')
                        encoded = base64SplitedLine[1]
                        print (colored('Encoded string found: ' + encoded, 'cyan'))

                        data = base64.b64decode(str(encoded)).replace('\x00','')
                        print (colored('Replaced by: '+ data, 'green'))

                        # Replace the target string
                        findAndReplace(args.EncodedFile + '.bkp', encoded, data)
    except Exception as ex:
        print ex
    finally:
        fileRead.close()

    renameFile(args.EncodedFile, args.EncodedFile + '_old')
    renameFile(args.EncodedFile + '.bkp', args.EncodedFile)

    pass

if __name__ == '__main__':
    banner()
    main()
