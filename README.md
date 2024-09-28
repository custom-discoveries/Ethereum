## Ethereum
This TigerGraph python application will programmatically create a schema with Vertex's and Edge's and load the graph with data!
## Install and Run
### Setup Environment
- Run the installPythonEnvironment.sh first
  - This will create a Python Virtural Environment and load the needed python packages
  - **Please NOTE**: You will need to rerun the **installPythonEnvironment.sh** script each time you open up a new terminal session!
- Enter in your Database Environment Variables using Python dotenv command
    - See more information at: https://pypi.org/project/python-dotenv/
    - At terminal prompt enter:
        - **dotenv set userName** someUserName
        - **dotenv set password** somePassword
        - **dotenv set graphName** Ethereum_Graph (only a suggestion)
        - **dotenv set hostURL** (TigerGraph Network Domain vlaue)
          - (Login into TigerGraph Cloud and select the Cluster *link* to get the Network Domain value)
          - Fomat of string should be: https://tigerGraph_domain_string.i.tgcloud.io
        - **dotenv set tgVersion** (Need to login into TigerGraph Cloud and get this from the Cluster listing)
        - **dotenv set Secret** (You will fill this in later, once the program creates a graph)
        - **dotenv set Token** (You will fill this in later, once the program creates a graph)
### Run
- cd src/
- python3 EthereumMain.py
    - Make sure to write down your **Secret** and **Token** and go back and enter it into your **dotenv** environment
- Run it again, (you will need your *token* to get logged in) to see the graph statistics
  - python3 EthereumMain.py
    
