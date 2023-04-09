import networkx as nx
import matplotlib.pyplot as plt
G= nx.barabasi_albert_graph(50,3)
nx.draw(G, with_labels=True)
plt.show()



rows, cols = (100, 100)
visited = [[False for i in range(cols)] for j in range(rows)]

for i in list(G.nodes):
    adj = list(G.adj[i])
    for j in adj:
        if visited[i][j] == False:
            visited[i][j] = True
            visited[j][i] = True
            createAcc(i,j)


def createAcc(node1, node2):
    amount = random.exponential(scale=10)
    txn_receipt = contract.functions.createAcc(node1, node2, amount).transact({
        "chainId": w3.eth.chain_id,
        "from": w3.eth.accounts[0],
        "gasPrice": w3.eth.gas_price,
    })
    txn_receipt_json = json.loads(w3.to_json(txn_receipt))
    print(txn_receipt_json) # print transaction hash

    # print block info that has the transaction)
    print(w3.eth.get_transaction(txn_receipt_json)) 



