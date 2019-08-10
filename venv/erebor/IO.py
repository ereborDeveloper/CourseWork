import codecs
import re


def fileToList(fileName):
    file = codecs.open(fileName, "r", "utf-8")
    lst = list(file.read().splitlines())
    for i in range (0, len(lst)):
        lst[i] = re.sub(r'[{,}]', "", lst[i]).split()
    file.close()
    return lst

def listToFile(fileName, lst):
    file = codecs.open(fileName, "w", "utf-8")
    for i in range (0, len(lst)):
        file.write("{" + re.sub(r"[\'\[\]]|","",str(lst[i])) + "}")
        if (i != len(lst) - 1):
            file.write(",\n")
    file.close()
    return lst
