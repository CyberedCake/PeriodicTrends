# PercentageToEmpiricalFormula.py
#
# This file was created by and modified by CyberedCake
# Last Modified: December 13th, 2022 at 1:10PM
# Version: 1.0.0
#
# Please do not modify or distribute without first
# acknowledging you did not create this and including
# the github page for this project... which can be found
# here: https://github.com/CyberedCake/PeriodicTrends
# (or you could just fork it on GitHub)
#
# I, the creator of this file, am aware the code is not
# the best and not quite as efficient as it could be, but
# oh well. This project isn't suppose to be maintained or
# made as efficient as possible as it's just a small script
# running on my school computer!
#
# Created by CyberedCake

print("Loading program... please wait!")
import os
os.system("title Periodic Trends - Loading...")
def title(titleWhat=""):
    if(titleWhat.strip() == ""):
        os.system("title Periodic Trends")
        return
    os.system("title Periodic Trends - " + titleWhat)

import time, sys, math, subprocess, ctypes
from os.path import exists
import urllib.request

title("Loading program... please wait!")

def setup():
    # yes i know this function code sucks but oh well it works and
    # the main reason it exist is because i'm used3 to minecraft
    # color codes lol
    global printF
    def printF(string):
        string = str(string)
        string = string.replace("&0", "\u001b[30m")
        string = string.replace("&1", "\u001b[34m")
        string = string.replace("&2", "\u001b[32m")
        string = string.replace("&3", "\u001b[36m")
        string = string.replace("&4", "\u001b[31m")
        string = string.replace("&5", "\u001b[35m")
        string = string.replace("&6", "\u001b[33m")
        string = string.replace("&7", "\u001b[37m")
        string = string.replace("&8", "\u001b[30;1m")
        string = string.replace("&9", "\u001b[34;1m")
        string = string.replace("&a", "\u001b[32;1m")
        string = string.replace("&b", "\u001b[36;1m")
        string = string.replace("&c", "\u001b[31;1m")
        string = string.replace("&d", "\u001b[35;1m")
        string = string.replace("&e", "\u001b[33;1m")
        string = string.replace("&f", "\u001b[37;1m")
        string = string.replace("&l", "\u001b[1m")
        string = string.replace("&n", "\u001b[4m")
        string = string.replace("&h", "\u001b[7m")
        string = string.replace("&r", "\u001b[0m")
        print(string + "\u001b[0m")

    alreadyHaveTrends = exists('trends.txt')
    if alreadyHaveTrends == False:
        import requests
        title("Downloading 'trends.txt' (required)...")
        print("Downloading 'trends.txt' (required)...")
        url = "https://pastebin.com/raw/Xzcv9S4d"
        try:
            time.sleep(4)
            request = requests.get(url)

            with open('trends.txt', 'wb') as file:
                file.write(request.content)

            print("Successfully downloaded 'trends.txt'... launching program!")
            title()
        except Exception as err:
            exception = str(err)
            printF("&cAn exception occurred: &8" + exception)
            printF(" ")
            input("Press enter to close")
            exit()

    file = open('trends.txt', 'r')
    if("PERIODIC TRENDS" not in file.readline()):
        printF("&cAn error occurred!")
        printF("&8Failed to properly read 'trends.txt'!")
        printF(" ")
        input("Press enter to exit!")
        exit()

    global elementsOnFile
    elementsOnFile = []
    for line in file:
        if(line.strip() == "" or line.startswith("#")):
            continue
        elementsOnFile.append(line)

    file.close()

    os.system("cls")
    title()

    printF("&6PERIODIC TRENDS")
    printF("&8Comparisons and more!")
    printF(" ")
    printF("Please enter an element &7(full name or symbol) &falong with other elements &7(full name or symbol) &fseparated by commas in the following format:")
    printF("&a%element or symbol%, %element or symbol%, ...")
    printF("&eEX: carbon, F, Fe, tennessine")
    printF(" ")

def main():
    printF(" ")
    ending = "\u001b[36;1m"
    title()
    form = input("Enter format: " + ending)
    if("restart" in form.lower()):
        os.startfile(__file__)
        exit()
        return
    if("exit" in form.lower()):
        exit()
        return
    title("Comparing elements... please wait!")
    timing = epoch()
    printF("&r")

    if(form.strip() == ""):
        throwParseException("INPUT_REQUIRED")

    elementsBeingCompared = []
    elementInformation = {}

    # Step 1 >> obtain the element name and information
    elementsProvided, alreadyUsed = form.split(", "), []
    for inputtedElement in elementsProvided:
        if(inputtedElement.strip() == ""):
            throwParseException("FOUND_EMPTY_ELEMENT_SELECTOR")
        if(inputtedElement[-1] == ","):
            throwParseException("FOUND_COMMA_WITH_NO_ELEMENT")
        validElement = False
        for element in elementsOnFile:
            if(element.strip() == "" or element.startswith("#")):
                continue
            symbol = element[element.find("[")+1:element.find("]")]
            element = element.strip().lower()
            start = element.find("-")+2
            if(inputtedElement.lower() == element[start:element.find("[")-1].lower() or inputtedElement.lower() == element[element.find("[")+1:element.find("]")].lower()):
                validElement = True
                end = element.find("[")-1
                substring = element[start:end]
                if(substring in elementsBeingCompared):
                    throwParseException("FOUND_DUPLICATE_ELEMENTS")

                elementInformation[substring] = [
                    element[0:element.find("-")-1],
                    symbol,
                    element[element.find("(")+1:element.find(")")],
                    element[element.find("{")+1:element.find("}")],
                    element[element.find("<")+1:element.find(">")]
                ]
                elementsBeingCompared.append(substring)
        if(validElement == False):
            throwParseException("FOUND_INVALID_ELEMENT")

    # sorted(x.items(), key=lambda item: item[1])
    # Step 2 >> Compare elements (and get sorted list)
    comparisons = ""
    atomicNumSorted = {}
    atomicRadSorted = {}
    electNegSorted = {}
    ionizationSorted = {}
    for element in elementInformation.keys():
        # Atomic Number
        info = elementInformation[element][0]
        if(info == "none"):
            atomicNumSorted[element] = 0
        else:
            atomicNumSorted[element] = (int(info))

        # Atomic Radius
        info = elementInformation[element][2]
        if(info == "none"):
            atomicRadSorted[element] = 0
        else:
            atomicRadSorted[element] = (float(info))

        # Electronegativity
        info = elementInformation[element][3]
        if(info == "none"):
            electNegSorted[element] = 0
        else:
            electNegSorted[element] = (float(info))

        # Ionization Energy
        info = elementInformation[element][3]
        if(info == "none"):
            ionizationSorted[element] = 0
        else:
            ionizationSorted[element] = (float(info))

    # Get sorted list, you must reverse it because if you don't it'll be from least to greatest rather than greatest to least
    atomicNumSorted = reverse({k: v for k, v in sorted(atomicNumSorted.items(), key=lambda item: item[1])})
    atomicRadSorted = reverse({k: v for k, v in sorted(atomicRadSorted.items(), key=lambda item: item[1])})
    electNegSorted = reverse({k: v for k, v in sorted(electNegSorted.items(), key=lambda item: item[1])})
    ionizationSorted = reverse({k: v for k, v in sorted(ionizationSorted.items(), key=lambda item: item[1])})


        #atomicNum = atomicNum + value.capitalize() +
        #" (" + elementInformation[value][1] + " " +
        #str(elementInformation[value][2]) + ") " +
        #str(atomicNumSorted[value]) + ", "
    #print(atomicNum)

    # Finally, print the text out so the user can see it
    seperator = "&e&l&h----------------------------------------------------------------------------------------------"
    thingsToPrint = []
    thingsToPrint.append(seperator)
    thingsToPrint.append(" ")
    thingsToPrint.append("&fYou are comparing &b" + str(len(elementInformation.keys())) + " &felements all at once!")
    thingsToPrint.append("rep_time_ms")
    thingsToPrint.append(" ")
    IF_NO_VALUE = "Value unknown or does not exist"
    
    thingsToPrint.append("&c&l&hATOMIC NUMBER:")
    index = 1
    for value in atomicNumSorted:
        thingsToPrint.append("&c" + str(index) + "&c. &e" + value.capitalize() + " &a(" + elementInformation[value][1] + "&a) &f> " + str(atomicNumSorted[value]))
        index += 1

    thingsToPrint.append(" ")
    thingsToPrint.append("&c&l&hATOMIC RADIUS:")
    index = 1
    for value in atomicRadSorted:
        printthis = "&c" + str(index) + "&c. &e" + value.capitalize() + " &a(" + elementInformation[value][1] + "&a) &f> " + str(atomicRadSorted[value])
        if(atomicRadSorted[value] == 0):
            printthis = "&c" + str(index) + "&c. &4" + value.capitalize() + " &a(" + elementInformation[value][1] + "&a) &f> " + IF_NO_VALUE
        else:
            index += 1
        thingsToPrint.append(printthis)

    thingsToPrint.append(" ")
    thingsToPrint.append("&c&l&hELECTRONEGATIVITY:")
    index = 1
    for value in electNegSorted:
        printthis = "&c" + str(index) + "&c. &e" + value.capitalize() + " &a(" + elementInformation[value][1] + "&a) &f> " + str(electNegSorted[value])
        if(electNegSorted[value] == 0):
            printthis = "&c" + str(index) + "&c. &4" + value.capitalize() + " &a(" + elementInformation[value][1] + "&a) &f> " + IF_NO_VALUE
        else:
            index += 1
        thingsToPrint.append(printthis)

    thingsToPrint.append(" ")
    thingsToPrint.append("&c&l&hIONIZATION ENERGY:")
    index = 1
    for value in ionizationSorted:
        printthis = "&c" + str(index) + "&c. &e" + value.capitalize() + " &a(" + elementInformation[value][1] + "&a) &f> " + str(ionizationSorted[value])
        if(ionizationSorted[value] == 0):
            printthis = "&c" + str(index) + "&c. &4" + value.capitalize() + " &a(" + elementInformation[value][1] + "&a) &f> " + IF_NO_VALUE
        else:
            index += 1
        thingsToPrint.append(printthis)

    thingsToPrint.append(" ")
    thingsToPrint.append(seperator)

    for item in thingsToPrint:
        if("rep_time_ms" in item):
            printF("&fIt took &b" + str(epoch() - timing) + "&bms &fto complete the operation!")
            continue
        printF(item)

    title()
    main()

def epoch():
    return round(time.time() * 1000)

def reverse(dictionary):
    keys = list(dictionary.keys())
    returned = {}
    keys.reverse()
    for key in keys:
        returned[key] = dictionary[key]
    return returned

def exception(exception, button=" "):
    printF("&cAn exception occurred: &8" + exception)
    returned = ctypes.windll.user32.MessageBoxW(0, str(exception), "An exception occurred!", 0x10 | 0x05)
    if(returned == 4):
        main()
    elif(returned == 2):
        exit()

def throwParseException(why):
    exception("Could not parse your format correctly!\n(" + why + ")", "Restart program")

def boolToString(boolean):
    return "True" if boolean == True else "False"

if __name__ == "__main__":
    def execute():
        try:
            setup() #setup
            main() # init
        except Exception as err:
            printF("&b---------------------------------------------------------")
            printF("&cA fatal exception occurred within the program, going to restart!")
            printF("&8" + str(err))
            printF("&7Please contact a developer if this error persists.")
            printF("&b---------------------------------------------------------")
            execute()
    execute()
