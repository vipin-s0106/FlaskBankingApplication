import configparser
import os

def getInstance():
    reader = configparser.ConfigParser()
    path = os.path.dirname(__file__)
    path = path.split("\\")
    path = "\\".join(path[:len(path)-1])
    reader.read(path+"\\input\\Config.ini")
    return reader
