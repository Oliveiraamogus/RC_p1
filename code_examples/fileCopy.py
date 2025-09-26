#!/usr/bin/env python3

SIZE = 1024

def main():
    fName = input("File to copy: ")
    try:
        f = open(fName, "rb")
    except:
        data = "File " + fName + " not found"
        exit(1)

    fName2 = "Copy"
    fC = open(fName2, "wb")
    data = f.read(SIZE)
    print("Copying ")
    print(".",end='')
    while (data):
        fC.write(data)
        print(".",end='')
        data = f.read(SIZE)
    f.close()
    fC.close()
    print("\nFile",fName,"has been copied")

main()
