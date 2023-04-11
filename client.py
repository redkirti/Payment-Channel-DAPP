import json
from web3 import Web3
from numpy import random as rnd
import networkx as nx
import matplotlib.pyplot as plt
import names
import csv
import random

count = 0

#connect to the local ethereum blockchain
provider = Web3.HTTPProvider('http://127.0.0.1:8545', request_kwargs={'timeout': 60})
w3 = Web3(provider)
#check if ethereum is connected
print(w3.is_connected())

#replace the address with your contract address (!very important)
deployed_contract_address = '0xf83db10363A5BD5fB1D0f748F110F983b37C3391'

#path of the contract json file. edit it with your contract json file
compiled_contract_path ="build/contracts/Payment.json"
with open(compiled_contract_path) as file:
    contract_json = json.load(file)
    contract_abi = contract_json['abi']
contract = w3.eth.contract(address = deployed_contract_address, abi = contract_abi)


# Function to create payment channel
def createAcc(node1, node2):
    amount = int(rnd.exponential(scale=10))
    txn_receipt = contract.functions.createAcc(node1, node2, amount).transact({
        "chainId": w3.eth.chain_id,
        "from": w3.eth.accounts[0],
        "gasPrice": w3.eth.gas_price,
    })

# Function to send transctions
def sendTxns():
    global count
    # Selecting random sender and receiver
    sender = random.randrange(1, 101)
    receiver = random.randrange(1, 101)
    while(sender==receiver):
        receiver = random.randrange(1, 101)
    print("Sender: " + str(sender) + ", Receiver: "+ str(receiver))
    txn_receipt = contract.functions.sendAmount(sender, receiver).transact({
        "chainId": w3.eth.chain_id,
        "from": w3.eth.accounts[0],
        "gas": 1000000000,
        "gasPrice": w3.eth.gas_price,
    })
    tx_receipt = w3.eth.get_transaction_receipt(txn_receipt)
    processed_logs = contract.events.myEvent().process_receipt(tx_receipt)
    # Finding if the transaction finished successfully
    print(processed_logs[0]['args']['found'])
    if processed_logs[0]['args']['found'] == True:
        count += 1


# Using library to generate a graph following power law distribution
G= nx.barabasi_albert_graph(101,2)
G.remove_node(0)
nx.draw(G, with_labels=True)
plt.show()


# Create 100 users
for i in range(1,101):
    # Generating a random name
    name = names.get_full_name()
    txn_receipt = contract.functions.registerUser(i, name).transact({
        "chainId": w3.eth.chain_id,
        "from": w3.eth.accounts[0],
        "gasPrice": w3.eth.gas_price,
    })

# Creating payment channel network based on graph
rows, cols = (101, 101)
visited = [[False for i in range(cols)] for j in range(rows)]

for i in list(G.nodes):
    adj = list(G.adj[i])
    for j in adj:
        if visited[i][j] == False:
            visited[i][j] = True
            visited[j][i] = True
            createAcc(i,j)

# Send 1000 random txns
for i in range(1000):
    print("This is txn: " + str(i+1) )
    sendTxns()
    # Output to a file every 100 transactions
    if (((i+1) % 100) == 0):
        with open('output.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([i+1, count])
        print(count/100)
        count = 0
