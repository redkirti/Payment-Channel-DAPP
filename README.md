# Payment-Channel-DAPP
A simple DAPP that simulates a payment channel network using functions of
- registerUser(userid, username)
- createAcc(user_id1, user_id2, balance)
- sendAmount(user_id1, user_id2)
- closeAccount(user_id1, user_id2)

## Requirements:
- Ganache
- Truffle
- Python
- web3
- matplotlib
- networkx
- names

## Steps to Run:
- Run Ganache and start a new workspace with PORT as 8454 and network id as 1337. Keep high block gas limit.

- Compile the smart contract Payment.sol using the following command in the project directory.
```bash
truffle compile
```
- Deply the contract on Ganache by the following command.
```bash
truffle migrate --network development
```
- After the contract is deployed, in the same directory execute client.py to start the simulation
```bash
python client.py
```

>output.csv contains the results of the simulation  

Try changing the simulation time and the network parameters for getting more insights.
