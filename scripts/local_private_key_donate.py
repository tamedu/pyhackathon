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


acct_pub_key = acct_priv_key.public_key
print('Account Master Public Key (Hex): ' + acct_pub_key.to_hex())
print('XPUB format: ' + acct_pub_key.to_b58check())


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

# web3 = Web3(IPCProvider(ipc_path="chains/horton/chain_data/geth.ipc"))
# ADDRESS = "0x0c1afbd0e19a225202e80d07c38632105fb0718f"

# ./myenv/bin/populus deploy --chain ganache Donator --no-wait-for-sync
web3 = Web3(HTTPProvider("http://127.0.0.1:8545"))
ADDRESS = "0x0C1afBd0E19a225202E80d07c38632105FB0718f"

ABI = loadABI("../build/contracts/Donator.json")

donator = web3.eth.contract(address=ADDRESS,abi=ABI)
print(donator)
print(donator.functions.donationsCount().call())
print(donator.functions.donationsTotal().call())

with open('../chains/horton/chain_data/keystore/UTC--2018-03-20T08-11-38.682616898Z--f26f97d14c56260fa935d16e18984de6d3c8ae5b') as keyfile:
    keyfile_json = keyfile.read()
private_key = web3.eth.account.decrypt(keyfile_json, 'this-is-not-a-secure-password')
import binascii
print(binascii.hexlify(private_key).decode('ascii'))
# 0x5ec5f57652661e8081b3ada11e4a77281bfd83375f3a3fb9c14331a6d2b1cefd

# https://ethereum.stackexchange.com/questions/43565/how-to-generate-private-public-and-ethereum-addresses-using-web3-py
from eth_account import Account
account = Account.privateKeyToAccount(private_key)
account_address = account.address
# 0xf26f97d14c56260fa935d16e18984de6d3c8ae5b

# ganache-cli --account="<privatekey>,balance" -i chainId -l gasLimit
# ganache-cli --account="0x5ec5f57652661e8081b3ada11e4a77281bfd83375f3a3fb9c14331a6d2b1cefd,999988880000000000000" -i 1 -l 10000000000

# http://web3py.readthedocs.io/en/latest/web3.eth.account.html#sign-a-contract-transaction
nonce = web3.eth.getTransactionCount(account_address)
txn = donator.functions.donate(
    7,
).buildTransaction({
    'value': 5*(10**18),
    'chainId': 1,
    'gas': 990000,
    'gasPrice': web3.toWei('1', 'gwei'),
    'nonce': nonce,
})

print(txn)

signed_txn = web3.eth.account.signTransaction(txn, private_key=private_key)
print(binascii.hexlify(signed_txn.hash))
signed_txn.rawTransaction
print(binascii.hexlify(signed_txn.rawTransaction))
print(signed_txn.r)
print(signed_txn.s)
print(signed_txn.v)

web3.eth.sendRawTransaction(signed_txn.rawTransaction)
print(web3.toHex(web3.sha3(signed_txn.rawTransaction)))

print(donator)
print(donator.functions.donationsCount().call())
print(donator.functions.donationsTotal().call())
