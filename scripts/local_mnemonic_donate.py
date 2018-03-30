'''
# https://github.com/pyca/cryptography
# https://github.com/andrewcooke/simple-crypt
# https://github.com/ranaroussi/pywallet BIP32 (HD) wallet creation for BTC, BTG, BCH, ETH, LTC, DASH and DOGE
# https://github.com/michailbrynard/ethereum-bip44-python
# https://github.com/vergl4s/ethereum-mnemonic-utils # Finally it works! :D

# pip3 install base58 ecdsa
from mnemonic_utils import mnemonic_to_private_key
private_key = mnemonic_to_private_key("legal winner thank year wave sausage worth useful legal winner thank yellow")

# pip3 install web3==4.0.0b13
import binascii
from web3.auto import w3
account = w3.eth.account.privateKeyToAccount(private_key)
# >>> account
# <eth_account.local.LocalAccount object at 0x1114a76a0>
# json_keyfile = account.encrypt(b"any password")
'''

import os, sys
dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, dir_path + '/../cptools')
from utils import loadABI
from accounts import buildSignSendTx, initLocalAccount, LOCAL_STORAGE

from web3 import Web3, IPCProvider, HTTPProvider

'''
seed = "legal winner thank year wave sausage worth useful legal winner thank yellow"
ganache-cli --account="0xb1b314d4fedc41fa409d26eb15e4ea1b213a3e7951dd16d8701a35c783a4a594,999988880000000000000" -i 1 -l 90732000000000
999988880000000000000
90732000000000
21464000000000
1000000000 * 21464 + 500000000
./myenv/bin/populus deploy --chain ganache Donator --no-wait-for-sync
'''
import binascii
initLocalAccount()
print(binascii.hexlify(LOCAL_STORAGE['private_key']).decode('ascii'))
print(LOCAL_STORAGE['account'].address)

web3 = Web3(HTTPProvider("http://127.0.0.1:8545"))
ADDRESS = "0xb87F1005FcCc76D6b9560A16085bE2c7d405332c"

ABI = loadABI("../build/contracts/Donator.json")

donator = web3.eth.contract(address=ADDRESS,abi=ABI)
print(donator)
print(donator.functions.donationsCount().call())
print(donator.functions.donationsTotal().call())


buildSignSendTx(donator.functions.donate, 3, value=5*(10**8))

print(donator)
print(donator.functions.donationsCount().call())
print(donator.functions.donationsTotal().call())
