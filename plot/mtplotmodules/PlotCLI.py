from sys import platform
import os
import readline

class PlotCLI:
    
    def __init__(self):
        self.base_path = os.getcwd()
        readline.parse_and_bind("tab:complete")
        if platform in ["linux", "linux2", "darwin"]:
            os.system("clear")
        elif platform=="windows":
            os.system("cls")
        
    
    def displayHeader(self):
        print("####################################################################")
        print("                            PLOT MODEL                              ")
        print("####################################################################")
        print("{0:17s}: {1}".format("CTRL+C or \'exit\'", "close the program"))
        print("{0:17s}: {1}".format("BASE PATH", self.base_path))
        print("####################################################################")
    
    def getInput(self):
        user_input = input(">> ")
        if user_input.lower() == "exit":
            print("Program closed")
            exit()
        else:
            return user_input