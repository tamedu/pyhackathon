'''
# https://github.com/pyca/cryptography
# https://github.com/andrewcooke/simple-crypt
# https://github.com/ranaroussi/pywallet BIP32 (HD) wallet creation for BTC, BTG, BCH, ETH, LTC, DASH and DOGE
# https://github.com/michailbrynard/ethereum-bip44-python

# pip3 install pywallet
from pywallet import wallet
seed = "guess tiny intact poet process segment pelican bright assume avocado view lazy"
seed = "traffic happy world clog clump cattle great toy game absurd alarm auction"
w = wallet.create_wallet(network="ETH", seed=seed, children=1)
private_key = w['xprivate_key']
private_key

# pip3 install web3==4.0.0b11
from eth_account import Account
account = Account.privateKeyToAccount(private_key)
account_address = account.address


# https://github.com/vergl4s/ethereum-mnemonic-utils
# pip3 install base58 ecdsa
from mnemonic_utils import mnemonic_to_private_key
private_key = mnemonic_to_private_key("legal winner thank year wave sausage worth useful legal winner thank yellow")

import binascii
from web3.auto import w3
account = w3.eth.account.privateKeyToAccount(private_key)
# >>> account
# <eth_account.local.LocalAccount object at 0x1114a76a0>
# json_keyfile = account.encrypt(b"any password")


from getpass import getpass
key = getpass("Enter your password: ")

# pip3 install cryptography
from cryptography.fernet import Fernet
cipher_suite = Fernet(key)
cipher_text = cipher_suite.encrypt(b"A really secret message. Not for prying eyes.")
plain_text = cipher_suite.decrypt(cipher_text)
'''

import os, sys
dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, dir_path + '/../cptools')
from init_web3 import loadABI

from web3 import Web3, IPCProvider, HTTPProvider

# ./myenv/bin/populus deploy --chain ganache Donator --no-wait-for-sync
web3 = Web3(HTTPProvider("http://127.0.0.1:8545"))
ADDRESS = "0xb87F1005FcCc76D6b9560A16085bE2c7d405332c"

ABI = loadABI("../build/contracts/Donator.json")

donator = web3.eth.contract(address=ADDRESS,abi=ABI)
print(donator)
print(donator.functions.donationsCount().call())
print(donator.functions.donationsTotal().call())

from mnemonic_utils import mnemonic_to_private_key
seed = "legal winner thank year wave sausage worth useful legal winner thank yellow"

# import binascii
# print(binascii.hexlify(mnemonic_to_private_key(seed)).decode('ascii'))
# 0xb1b314d4fedc41fa409d26eb15e4ea1b213a3e7951dd16d8701a35c783a4a594
# ganache-cli --account="<privatekey>,balance" -i chainId -l gasLimit
# ganache-cli --account="0xb1b314d4fedc41fa409d26eb15e4ea1b213a3e7951dd16d8701a35c783a4a594,999988880000000000000" -i 1 -l 10000000000

# https://ethereum.stackexchange.com/questions/43565/how-to-generate-private-public-and-ethereum-addresses-using-web3-py
from eth_account import Account
local_account = Account.privateKeyToAccount(mnemonic_to_private_key(seed))

# Donate
effective_eth_usd_rate = 5
transaction = {'value': 5000, 'from': local_account.address}
tx_hash = donator.transact(transaction).donate(effective_eth_usd_rate)
print ("Thank you for the donation! Tx hash {tx}".format(tx=tx_hash))


print(donator)
print(donator.functions.donationsCount().call())
print(donator.functions.donationsTotal().call())
