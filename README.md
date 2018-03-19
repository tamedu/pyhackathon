# CrytoPrimitive Python Weekend Hackathon
* https://redd.it/83d3lz
* https://cryptoprimitive.slack.com/messages

## Purpose
Smart contracts should, in theory, make coordination easier.

Then, with Python's strength in rapid prototyping, we could build as we use them. So as I build a given interface, I could, say, open BP with a few keystrokes, and trust that it might get seen within the dev group and taken care of within minutes.

## Todos
The focus will be on quickly building Python apps that the participants can use via command-line right away. We will begin by interfacing with the already-written contracts [here](https://github.com/cryptoprimitive/contracts): Burnable Payments, BurnChat, and CrowdServe. This should be accomplished at a basic level within the first few hours.

After that, the focus of the hackathon will be on making interaction easier and more fluid via Python command line or simple GUI.

## Python Ethereum Development

### web3py
```
brew install python3
pip3 install --upgrade pip
pip install web3
python3 burnable_payment.py
```

### Populus Development Cycle
https://populus.readthedocs.io/en/latest/dev_cycle.html

```
brew install pkg-config libffi autoconf automake libtool openssl # to complie https://github.com/ludbb/secp256k1-py
sudo touch /usr/local/LICENSE
sudo chown "Alex Nguyen" /usr/local/LICENSE

pip install populus
# - OR -
git clone https://github.com/ethereum/populus.git
pip install -e . -r requirements-dev.txt

populus init
brew tap ethereum/ethereum && brew install solidity # http://solidity.readthedocs.io/en/develop/installing-solidity.html
populus compile

populus deploy --chain tester Donator
pip install eth-utils==0.7.*
py.test
```

#### new chain via geth
```
# install geth
brew tap ethereum/ethereum
brew install ethereum

populus chain new horton
chains/horton/./init_chain.sh
```
