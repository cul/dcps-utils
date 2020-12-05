import ASFunctions as asf
# from sheetFeeder import dataSheet
# import json


def main():
    # Main code goes here.

    asf.setServer("Test")

    print(asf.getArchivalObjectByRef(2, "fd30ef92c90442fe861683b81dd1b4e8"))


    # aoref = '21849d537360a6da5b6d900cf561f99f'
    # aoid = asf.getArchivalObjectByRef(2, aoref)
    # print(aoid)
    # deletion = asf.deleteArchivalObject(2, aoid)
    quit()


# Functions go here.

if __name__ == "__main__":
    main()
