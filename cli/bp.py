import os, sys
dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, dir_path + '/../cptools')
from init_web3 import loadABI
from burnable_payment import *

BP_ABI = loadABI("../build/contracts/BurnablePayment.json")["abi"]

def getBP(x):
    bp_address = BPFactory.functions.BPs(x).call()
    bp_contract = web3.eth.contract(abi = BP_ABI, address = bp_address)
    state = bp_contract.functions.getFullState().call()
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

def getBPs(f, t):
    r = range(f, t)
    bps = []
    print("Loading BPs in", r, "...")
    for x in r:
        bps.append(getBP(x))
    return bps

readme = """burnable_payment functions:
getBPCount() - return number of bps
getBP(x) - return bp number x
getBPs(f, t) - return bps from number f to number t

"""

print()
print(readme)
print()

print("Number of BP contracts:", getBPCount())
print("First contract: ", getBP(0))
