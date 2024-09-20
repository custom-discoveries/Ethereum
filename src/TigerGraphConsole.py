#******************************************************************************
# Copyright (c) 2024, Custom Discoveries Inc.
# All rights reserved.
# TigerGraphConsole.py: Python Class to create a TigerGraph session and perform
# some administrative functions.
#******************************************************************************
import os, sys
import warnings
import subprocess
import pyTigerGraph as tg

from dotenv import load_dotenv
from prompt_toolkit import prompt
#
# You can store environmet variables by using
# the dotenv command in your terminal window
# Ex: > dotenv set userName JohnDoe
#
# The below code will read the dotenv variables
# into your runtime environment
# More information, see https://pypi.org/project/python-dotenv/
#
load_dotenv('../.env', override=True)
warnings.filterwarnings('ignore')

class TigerGraphConsole:


    def __init__(self):
        self.userName = os.getenv('userName') 
        self._passWord = os.getenv('password')
        self.graphName = os.getenv('graphName')
        self.hostURL = os.getenv("hostURL")
        self.version = os.getenv("tgVersion")
        self._secret = os.getenv("Secret")
        self._token = os.getenv("Token")
        self._conn = None
        self.tgCloud = False

    def commonLoginMenu(self,displayMenu=False):

        subprocess.run('clear',shell=True)
        print(f"Initinalizing Connction to Graph: {self.graphName}")
        if displayMenu == True:
            if self.userName == None: self.userName = ''
            self.userName = prompt("Enter Your User Name: ", default=self.userName)
            
            if self._passWord == None: self._passWord = ''
            self._passWord = prompt("Enter Your Password: ", is_password=True, default=self._passWord)

            if self.graphName == None: self.graphName = ''
            self.graphName = prompt("Enter Your Graph Name: ", default=self.graphName)

            if self.hostURL == None: self.hostURL = ''
            self.hostURL = prompt("Enter Your Remote Host URL: ", default=self.hostURL)
            
            if self._token == None: self._token = ''
            self._token = prompt("Enter Remote Host Token: ",default=self._token)
        #
        # Make sure to initinalize the connection
        #
        return self.initConnection()        

    def initConnection(self):

        try:
            if (self._conn == None):

                self._conn = tg.TigerGraphConnection(host = self.hostURL,
                                                graphname = self.graphName,
                                                username = self.userName, 
                                                password = self._passWord, 
                                                apiToken = self._token,
                                                gsqlVersion = self.version,
                                                tgCloud = self.tgCloud)
            else:
                return self._conn 
        except Exception as error:
            print(f"Error Count = {error.args.count()}")
            print("initConnection Error:",repr(error))
            print("Check to see if the server is up and Running...")
            if error.args[0].find("exists.") >0 :
                #self._conn.gsql("DROP GRAPH "+ self.graphName)
                print("Your Config File is out of Sync with your Secrets for Graph:", self.graphName,"\nPlease login to your database a delete your secrets under Admin Portal -> Management -> Users")
                raise LookupError("\nYour Config File is out of Sync with your Secrets for Graph "+self.graphName)
            
        return self._conn

    def getConnection(self):
        return self._conn
    
    def getSecretAlias(self):
        return self.userName +"_"+ self.graphName
    
    #
    # Create a Secret and Token for remote connection
    #   
    def createSecret(self, aliasName, expirationDate=2592000):

        update_Flag = False
        try:
            if (len(aliasName) > 0):
                    self._secret = self.getConnection().createSecret(alias=aliasName)
                    update_Flag=True
                    self._token = ""
                    print("Secret =",self._secret)
            #
            # Create a token with default of 30 day expiration
            #
            if (len(self._secret) > 0):
                tokenTuple = self.getConnection().getToken(None,lifetime=int(expirationDate))
                update_Flag=True
                self._token = tokenTuple[0]
                self._token = tokenTuple             
                print("New Token =", tokenTuple)
            else:
                self.getConnection().apiToken = self._token
        
            if (update_Flag == True):
                print("\n******* Warining *******")
                print("Make sure to store these values in a safe plase, Once you hit enter, you will not be able to retrieve these values")
                input("\nPress Enter to continue: ")          

        except LookupError as error:
            print("Error:",repr(error))
            input("\nPress Enter to continue: ")
            return False

        except Exception as error:
            print("createSecret/Token Error:",repr(error))
            #traceback.print_exc()
            input("\nPress Enter to continue: ")
            return False

        return True

    def crateGraph(self) -> bool:
        self.initConnection()
        rs = self.getConnection().gsql("CREATE GRAPH "+ self.graphName + "(*)")
        print(rs)
        if rs.find("created") >=0:
            self._secret = ''
            self._token = ''
            self.createSecret(self.getSecretAlias())
        else:
            return False
        
        return True
    
    def main(self, argv):
        self.commonLoginMenu()


if __name__ == "__main__":
   ethereum = TigerGraphConsole()
   ethereum.main(sys.argv[1:])