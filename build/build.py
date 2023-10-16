# requires python 3.12
import os
import tomli
def find_version(curr_item):
    string=str(curr_item)
    pos=string.find("version")
    if pos!=-1:
        version=string[pos:]
        char=version[0]
        counter=0
        while char!=":":
            counter+=1
            char=version[counter]
        return version[counter:].split("'")[1]
def build():
    if os.path.isfile("pyproject.toml") :
        with open("pyproject.toml", "rb") as toml:
            values=tomli.load(toml)
            

            x=input(f"Current version is {find_version(dict(values))}. Please enter the new version! ")
if __name__=="__main__":
    build()