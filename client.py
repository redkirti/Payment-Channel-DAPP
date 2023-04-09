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
provider = Web3.HTTPProvider('http://127.0.0.1:8545')
w3 = Web3(provider)
#check if ethereum is connected
print(w3.is_connected())

#replace the address with your contract address (!very important)
deployed_contract_address = '0x909ba23ab8aCF1fdB61892Efa826C69802A1e9e0'

#path of the contract json file. edit it with your contract json file
compiled_contract_path ="build/contracts/Payment.json"
with open(compiled_contract_path) as file:
    contract_json = json.load(file)
    contract_abi = contract_json['abi']
contract = w3.eth.contract(address = deployed_contract_address, abi = contract_abi)



def createAcc(node1, node2):
    amount = int(rnd.exponential(scale=10))
    txn_receipt = contract.functions.createAcc(node1, node2, amount).transact({
        "chainId": w3.eth.chain_id,
        "from": w3.eth.accounts[0],
        "gasPrice": w3.eth.gas_price,
    })
    # txn_receipt_json = json.loads(w3.to_json(txn_receipt))
    # print(txn_receipt_json) # print transaction hash

    # print block info that has the transaction)
    # print(w3.eth.get_transaction(txn_receipt_json)) 

def sendTxns():
    global count
    sender = random.randrange(1, 101)
    receiver = random.randrange(1, 101)
    while(sender==receiver):
        receiver = random.randrange(1, 101)
    txn_receipt = contract.functions.sendAmount(sender, receiver).transact({
        "chainId": w3.eth.chain_id,
        "from": w3.eth.accounts[0],
        "gasPrice": w3.eth.gas_price,
    })
    # txn_receipt_json = json.loads(w3.to_json(txn_receipt))
    # print(txn_receipt_json) # print transaction hash
    # print block info that has the transaction)
    # print(w3.eth.get_transaction(txn_receipt_json))
    tx_receipt = w3.eth.get_transaction_receipt(txn_receipt)
    processed_logs = contract.events.myEvent().process_receipt(tx_receipt)

    if processed_logs[0]['args']['found'] == True:
        count += 1
        # print("Hello" + str(count))
    # print(processed_logs)
    # print(txn_receipt_json)



# Create 100 users
for i in range(1,101):
    name = names.get_full_name()
    txn_receipt = contract.functions.registerUser(i, name).transact({
        "chainId": w3.eth.chain_id,
        "from": w3.eth.accounts[0],
        "gasPrice": w3.eth.gas_price,
    })
    # txn_receipt_json = json.loads(w3.to_json(txn_receipt))
    # print(txn_receipt_json) # print transaction hash
    # print block info that has the transaction)
    # print(w3.eth.get_transaction(txn_receipt_json)) 

# Make graph
G= nx.barabasi_albert_graph(101,3)
G.remove_node(0)

rows, cols = (101, 101)
visited = [[False for i in range(cols)] for j in range(rows)]

for i in list(G.nodes):
    adj = list(G.adj[i])
    for j in adj:
        if visited[i][j] == False:
            visited[i][j] = True
            visited[j][i] = True
            createAcc(i,j)

# nx.draw(G, with_labels=True)
# plt.show()

# Send 1000 random txns
for i in range(1000):
    sendTxns()
    if (((i+1) % 100) == 0):
        with open('output.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([i+1, count])
        print(count/100)
        count = 0




# print(contract.functions.network(1,2).call())
