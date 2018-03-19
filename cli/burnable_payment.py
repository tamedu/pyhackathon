import pprint
import json
from web3 import Web3, HTTPProvider
from web3.contract import ConciseContract

# ropsten testnet
# w3 = Web3(HTTPProvider('https://ropsten.infura.io'))
# ADDRESS = "0xA981e23E9Ff17357dE2a13a9CA36E728322016f0"

# mainnet
w3 = Web3(HTTPProvider('https://gladly-golden-parrot.quiknode.io/8959339e-f0ab-4403-876f-1aed9422a44f/xh9aJBYpYQHEhu6q8jQrkA==/'))
ADDRESS = "0x38B394cD27C3b0D865F58a4512b65c7b0ab6DB66"
''' IMPORTANT !!!
Don't put a lot of money on it. Paying for very simple interfaces, some game-like.
The current problem is you can only make calls (including withdrawing back to your own account)
if you 'unlock' your account--and then I think
anyone on the node has access to the funds/account until you 'lock' it again.
Logan currently looking at handling private keys locally, but it's not necessarily going to be easy.
'''


# pilot info
print("blockNumber:", w3.eth.blockNumber)
print("Accounts:", w3.eth.accounts)

FACTORY_ABI = json.loads(' [{"constant":true,"inputs":[{"name":"","type":"uint256"}],"name":"BOPs","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"getBOPCount","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"payer","type":"address"},{"name":"serviceDeposit","type":"uint256"},{"name":"autoreleaseInterval","type":"uint256"},{"name":"title","type":"string"},{"name":"initialStatement","type":"string"}],"name":"newBurnableOpenPayment","outputs":[{"name":"","type":"address"}],"payable":true,"stateMutability":"payable","type":"function"},{"anonymous":false,"inputs":[{"indexed":true,"name":"newBOPAddress","type":"address"},{"indexed":false,"name":"payer","type":"address"},{"indexed":false,"name":"serviceDeposit","type":"uint256"},{"indexed":false,"name":"autoreleaseTime","type":"uint256"},{"indexed":false,"name":"title","type":"string"},{"indexed":false,"name":"initialStatement","type":"string"}],"name":"NewBOP","type":"event"}]')

BP_ABI = json.loads(' [{"constant":true,"inputs":[],"name":"payer","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[],"name":"delayAutorelease","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"amount","type":"uint256"}],"name":"release","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[],"name":"commit","outputs":[],"payable":true,"stateMutability":"payable","type":"function"},{"constant":false,"inputs":[{"name":"amount","type":"uint256"}],"name":"burn","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"title","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"worker","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"amountBurned","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"autoreleaseInterval","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"statement","type":"string"}],"name":"logPayerStatement","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[],"name":"triggerAutorelease","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"serviceDeposit","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"getFullState","outputs":[{"name":"","type":"address"},{"name":"","type":"string"},{"name":"","type":"uint8"},{"name":"","type":"address"},{"name":"","type":"uint256"},{"name":"","type":"uint256"},{"name":"","type":"uint256"},{"name":"","type":"uint256"},{"name":"","type":"uint256"},{"name":"","type":"uint256"},{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[],"name":"addFunds","outputs":[],"payable":true,"stateMutability":"payable","type":"function"},{"constant":false,"inputs":[],"name":"recoverFunds","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"autoreleaseTime","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"state","outputs":[{"name":"","type":"uint8"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"amountReleased","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"statement","type":"string"}],"name":"logWorkerStatement","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"amountDeposited","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"inputs":[{"name":"_payer","type":"address"},{"name":"_serviceDeposit","type":"uint256"},{"name":"_autoreleaseInterval","type":"uint256"},{"name":"_title","type":"string"},{"name":"initialStatement","type":"string"}],"payable":true,"stateMutability":"payable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"name":"contractAddress","type":"address"},{"indexed":false,"name":"payer","type":"address"},{"indexed":false,"name":"serviceDeposit","type":"uint256"},{"indexed":false,"name":"autoreleaseInterval","type":"uint256"},{"indexed":false,"name":"title","type":"string"}],"name":"Created","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"name":"from","type":"address"},{"indexed":false,"name":"amount","type":"uint256"}],"name":"FundsAdded","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"name":"statement","type":"string"}],"name":"PayerStatement","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"name":"statement","type":"string"}],"name":"WorkerStatement","type":"event"},{"anonymous":false,"inputs":[],"name":"FundsRecovered","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"name":"worker","type":"address"}],"name":"Committed","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"name":"amount","type":"uint256"}],"name":"FundsBurned","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"name":"amount","type":"uint256"}],"name":"FundsReleased","type":"event"},{"anonymous":false,"inputs":[],"name":"Closed","type":"event"},{"anonymous":false,"inputs":[],"name":"Unclosed","type":"event"},{"anonymous":false,"inputs":[],"name":"AutoreleaseDelayed","type":"event"},{"anonymous":false,"inputs":[],"name":"AutoreleaseTriggered","type":"event"}]')

print("Loading BP contracts ...")
factory_contract = w3.eth.contract(FACTORY_ABI, ADDRESS)

bp_count = factory_contract.call().getBOPCount()
print("Number of BPs:", bp_count)

print("Loading 10 BPs ...")
for x in range(0, 10):
    bp_address = factory_contract.call().BOPs(x)
    print("\nBP #%d:" % (x))
    bp_contract = w3.eth.contract(BP_ABI, bp_address)
    state = bp_contract.call().getFullState()
    bp = {
        "address": bp_address,
        "payer": state[0],
        "title": state[1],
        "state": state[2],
        "worker": state[3],
        "balance": state[4],
        "service_deposit": state[5],
        "amount_deposited": state[6],
        "amount_burned": state[7],
        "amount_released": state[8],
        "autorelease_interval": state[9],
        "autorelease_time": state[10]
    }
    pprint.pprint(bp)
