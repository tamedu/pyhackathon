import json
from web3 import Web3, IPCProvider
w3 = Web3(IPCProvider(ipc_path="./chains/horton/chain_data/geth.ipc"))

# pilot info
print("blockNumber:", w3.eth.blockNumber)
print("Accounts:", w3.eth.accounts)

ADDRESS = "0x9f0dbc1e416d244184966935967741832715f1a4"
ABI = json.loads('[{"constant":true,"inputs":[],"name":"donationsTotal","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"donationsCount","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"defaultUsdRate","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"donationsUsd","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"usd_rate","type":"uint256"}],"name":"donate","outputs":[],"payable":true,"stateMutability":"payable","type":"function"},{"inputs":[],"payable":false,"stateMutability":"nonpayable","type":"constructor"},{"payable":true,"stateMutability":"payable","type":"fallback"}]')

donator = w3.eth.contract(address=ADDRESS,abi=ABI)
print(donator)
print(donator.call().donationsCount())
print(donator.call().donationsTotal())

transaction = {'value':5*(10**18),'from':w3.eth.coinbase}
donator.transact(transaction).donate(7)

transaction = {'value':100*(10**18),'from':w3.eth.coinbase,'to':donator.address}
w3.eth.sendTransaction(transaction)


# create new account
DEMO = "demo"
print("Note: use '{}' as passphrase".format(DEMO))
w3.personal.newAccount()
print(w3.eth.accounts)
last_account = w3.eth.accounts[-1]
print("Just created:", last_account)
w3.personal.unlockAccount(account=last_account,passphrase=DEMO)
