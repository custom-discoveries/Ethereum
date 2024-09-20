#******************************************************************************
# Copyright (c) 2024, Custom Discoveries Inc.
# All rights reserved.
# EthereumMain.py: Python Class to programmatically create a simple schema with 
# Vertex and Edges and load the graph with sample data
#******************************************************************************
import os 
from pathlib import Path
import sys
import csv
import traceback

from TigerGraphConsole import TigerGraphConsole
from pyTigerGraph.schema import Graph, Vertex, Edge
from pyTigerGraph.pyTigerGraphException import TigerGraphException
from datetime import datetime
from typing import List, Dict, Optional, Union
from dataclasses import dataclass, fields


#color: #4b72f0, icon: person
@dataclass
class Subscriber(Vertex):
    firstName: str
    lastName: str
    dob: datetime
    primary_id: str = "id"
    primary_id_as_attribute: bool = True

#color: #1d9f0f, icon: book
@dataclass
class Account(Vertex):
    firstName: str
    lastName: str
    accountNumber: str
    primary_id: str = "id"
    primary_id_as_attribute: bool = True

#color: #f33008, icon: management
@dataclass
class AccountHolder(Vertex):
    name: str
    address: str
    dob: datetime
    primary_id: str = "id"  # always of type string, corresponds to the desired primary ID attribute.
    primary_id_as_attribute: bool = True

@dataclass
class hasAccount(Edge):
    from_vertex: Subscriber
    to_vertex: Account
    is_directed: bool = False

@dataclass
class holds_Account(Edge):
    accountNumber: str
#    from_vertex: Union[AccountHolder, g.vertex_types["Account"]]
    from_vertex: AccountHolder
    to_vertex: Account
    is_directed: bool = True
    reverse_edge: str = "account_Held_By"
    discriminator: str = "accountNumber"

class Ethereum:

    def __init__(self):
        self.conn = None
        self._projectDir=os.getcwd()


    def getGraphDataDir(self):

        self._projectDir=Path(Path.cwd().resolve().parent).as_posix()+"/GraphData/"
        return (self._projectDir)
    
    def getConnection(self):
        return self.conn
    
    def setConnection(self, connection):
        self.conn = connection

    def buildVertexs(self,g):
        try:
            g.add_vertex_type(Subscriber)
            g.add_vertex_type(Account)
            g.add_vertex_type(AccountHolder)
            g.commit_changes()
            print("Added Vertexs: Subscriber, Account, AccountHolder...")
        except TigerGraphException as e:
            print("Error in Adding Vertexs: ",e)

    def buildEdges(self,g):
        try:
            g.add_edge_type(hasAccount)
            g.add_edge_type(holds_Account)
            g.commit_changes()
            print("Added holds_Account Edge...")
        except TigerGraphException as e:
            print("Error adding Edges: ", e)
            traceback.print_exc()

    def buildSchema(self,g):
        if (len(self.getConnection().getVertexCount()) < 1):
            self.buildVertexs(g)
            self.buildEdges(g)
            self.readDataFile(buid_schema=True)
            # Need to build out and load schema before you can load
            # Accounts into Account Holder and set the holds_Account edge
            self.loadAccountHolder()
        else:
            results =  self.getConnection().getVertexCount()
            print(f"\n# of Verticies: {results}")
            results =  self.getConnection().getEdgeTypes()
            print(f"Edges: {results}")


    def readDataFile(self,buid_schema,skipHeader=True):

        inFile = open(self.getGraphDataDir() + "Person.csv")
        csvReader = csv.reader(inFile)
        #
        # read file and skip header
        #
        for line in csvReader:
            if (skipHeader):
                skipHeader = False
            else:
                # read persons name, getting only the First and Lastname and if suffix exists
                id = line[0]
                xx = line[2].split(" ")
                match (len(xx)):
                    case 1: 
                        break
                    case 2:
                        firstName = xx[0]
                        lastName = xx[1]
                    case 3:
                        firstName = xx[0]
                        lastName = xx[2]
                    case 4:
                        firstName = xx[0]
                        lastName = xx[2]+" "+xx[3]
                accountNumber = line[8]
                dob = line[5]
                if (buid_schema == True):
                    self.createAccountHolder(id, firstName, lastName, accountNumber,dob)
                
                self.loadSchema(id, firstName, lastName, accountNumber, dob)

    def loadSchema(self, id, firstName, lastName, accountNumber,dob):

        if len(accountNumber) > 0:
            print("Loading " + firstName + " " + lastName)
            self.getConnection().upsertVertex("Subscriber", id, {"firstName": firstName,"lastName":lastName,"dob":dob})
            self.getConnection().upsertVertex("Account", (int(id)*100), {"firstName": firstName,"lastName":lastName,"accountNumber":accountNumber})
            #
            #Setup Edge between Subscriber & Account
            #
            self.getConnection().upsertEdge("Subscriber",id,"hasAccount","Account",(int(id)*100))

    def createAccountHolder(self, id, firstName, lastName, accountNumber, dob):
        if (firstName == "John" and accountNumber == "1839-0001"):
            #Create Account Holder
            #print(firstName+" "+lastName+" "+accountNumber, results)
            print("Creating Account Holder")
            address = "999 Main St. Somewhere, NY"
            self.getConnection().upsertVertex("AccountHolder", (int(id)*1000+999), {"name":firstName+" "+lastName,"address":address, "dob":dob})


    def loadAccountHolder(self):

        accounts = self.getConnection().getVertices("Account", select="accountNumber", fmt="py")
        for dic in accounts:
            id = dic.get("v_id")
            accId = dic.get("attributes").get("accountNumber")
            print(id,accId)
            self.getConnection().upsertEdge("AccountHolder",5999,"holds_Account","Account",id, attributes={"accountNumber":accId})          
        #print(f"Updating Account Holder Accounts {accounts}")
        print("Updated Account Holder Accounts")


    def main(self, argv):

        adminConsole = TigerGraphConsole()
        self.setConnection(adminConsole.commonLoginMenu(displayMenu=True))
        found = self.getConnection().check_exist_graphs(self.getConnection().graphname)
    
        if found:
            g = Graph(adminConsole.getConnection())    
            print ("Found Graph: " + g.graphname)
        else:
            try:
                adminConsole.crateGraph()
                g = Graph(self.getConnection())
                print ("Created Graph: " +g.graphname)
            
            except TigerGraphException as e:
                print("Error Creating Graph: ", e)
                traceback.print_exc()                    

        self.buildSchema(g)


if __name__ == "__main__":
   ethereum = Ethereum()
   ethereum.main(sys.argv[1:])