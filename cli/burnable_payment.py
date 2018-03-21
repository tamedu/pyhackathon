# import pprint
import json
from web3 import Web3, HTTPProvider
from web3.contract import ConciseContract

import os
import sys
dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, dir_path + '/../cptools')
import cptools

# use cptools.web3
w3 = cptools.web3

with open(dir_path + '/../build/contracts.json', 'r') as infile:
    contracts_json = json.load(infile)
BP_FACTORY_ABI = contracts_json["BurnablePaymentFactory"]["abi"]
BP_ABI = contracts_json["BurnablePayment"]["abi"]

bp_factory_contract = w3.eth.contract(abi = BP_FACTORY_ABI, address = cptools.BPFactoryAddress)

def getBPCount():
    bp_count = bp_factory_contract.call().getBPCount()
    print("Number of BPs:", bp_count)

def getBPNumber(x):
    bp_address = bp_factory_contract.call().BPs(x)
    bp_contract = w3.eth.contract(abi = BP_ABI, address = bp_address)
    state = bp_contract.call().getFullState()
    bp = {
        "address": bp_address,
        "state": state[0],
        "payer": state[1],
        "worker": state[2],
        "title": state[3],
        "balance": state[4],
        "service_deposit": state[5],
        "amount_deposited": state[6],
        "amount_burned": state[7],
        "amount_released": state[8],
        "autorelease_interval": state[9],
        "autorelease_time": state[10]
    }
    return bp

def getBPFromTo(f, t):
    r = range(f, t)
    bps = []
    print("Loading BPs in", r, "...")
    for x in r:
        bps.append(getBPNumber(x))
    return bps

readme = """burnable_payment functions:
getBPCount() - return number of bps
getBPNumber(x) - return bp number x
getBPFromTo(f, t) - return bps from number f to number t

"""

print()
print(readme)
print()

getBPCount()
