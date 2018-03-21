import pprint
import json
from web3 import Web3, HTTPProvider
from web3.contract import ConciseContract

# mainnet
w3 = Web3(HTTPProvider('https://gladly-golden-parrot.quiknode.io/8959339e-f0ab-4403-876f-1aed9422a44f/xh9aJBYpYQHEhu6q8jQrkA==/'))
ADDRESS = "0xA225EbE73347dd87492868332F9B746bEb8499bb"

# pilot info
print("blockNumber:", w3.eth.blockNumber)
print("Accounts:", w3.eth.accounts)

import os
dir_path = os.path.dirname(os.path.realpath(__file__))
with open(dir_path + '/../build/contracts.json', 'r') as infile:
    contracts_json = json.load(infile)
BP_FACTORY_ABI = contracts_json["BurnablePaymentFactory"]["abi"]
BP_ABI = contracts_json["BurnablePayment"]["abi"]


print("Loading BP contracts ...")
bp_factory_contract = w3.eth.contract(abi = BP_FACTORY_ABI, address = ADDRESS)

bp_count = bp_factory_contract.call().getBPCount()
print("Number of BPs:", bp_count)

print("Loading 3 BPs ...")
for x in range(0, 3):
    bp_address = bp_factory_contract.call().BPs(x)
    print("\nBP #%d:" % (x))
    bp_contract = w3.eth.contract(abi = BP_ABI, address = bp_address)
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
