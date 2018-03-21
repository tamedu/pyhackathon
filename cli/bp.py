import os, sys
dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, dir_path + '/../cptools')
import init_web3
import burnable_payment

BP_ABI = init_web3.loadABI("../build/contracts/BurnablePayment.json")

def getBPNumber(x):
    bp_address = BPFactory.call().BPs(x)
    bp_contract = web3.eth.contract(abi = BP_ABI, address = bp_address)
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
burnable_payment.getBPCount() - return number of bps
getBPNumber(x) - return bp number x
getBPFromTo(f, t) - return bps from number f to number t

"""

print()
print(readme)
print()

burnable_payment.getBPCount()
