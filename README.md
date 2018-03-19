[![Waffle.io - Columns and their card count](https://badge.waffle.io/tamedu/pyhackathon.png?columns=all)](https://waffle.io/tamedu/pyhackathon?utm_source=badge)
# CrytoPrimitive Python Weekend Hackathon
*   https://redd.it/83d3lz
*   [CryptoPrimitive slack invite](https://cp-hackathon-invite.herokuapp.com/). Make sure to check out #weekend-hackathon!

## Purpose
Smart contracts should, in theory, make coordination easier.

Then, with Python's strength in rapid prototyping, we could build as we use them. So as I build a given interface, I could, say, open BP with a few keystrokes, and trust that it might get seen within the dev group and taken care of within minutes.

## Todos
The focus will be on quickly building Python apps that the participants can use via command-line right away. We will begin by interfacing with the already-written contracts [here](https://github.com/cryptoprimitive/contracts): Burnable Payments, BurnChat, and CrowdServe. This should be accomplished at a basic level within the first few hours.

After that, the focus of the hackathon will be on making interaction easier and more fluid via Python command line or simple GUI.

## Python Ethereum Development

### web3py **beta** (4.x)
```
brew install python3
pip3 install --upgrade pip
pip install web3 --pre
python3 cli/burnable_payment.py
```

#### IMPORTANT !!!
cli/burnable_payment.py can be use with mainnet via quiknode a server. For the mainnet:
> Don't put a lot of money on it. Paying for very simple interfaces, some game-like.
> The current problem is you can only make calls (including withdrawing back to your own account)
> if you 'unlock' your account--and then I think
> anyone on the node has access to the funds/account until you 'lock' it again.
> Logan currently looking at handling private keys locally, but it's not necessarily going to be easy.


### Populus Development Cycle
https://populus.readthedocs.io/en/latest/dev_cycle.html
### Part 1-5: Create, compile and test Solidity contracts

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
pip install eth-utils==0.7.* # since py.test required eth-utils 0.7.* version
py.test

populus deploy --chain tester ProjectOwnership
py.test tests/test_project_ownership.py # to test selected test-cases
```

More about solidity contract testing using populus at http://populus.readthedocs.io/en/latest/testing.html#web3

#### Part 6: Deploy contract to a local chain (via geth)
http://populus.readthedocs.io/en/latest/dev_cycle.part-06.html
```
# install geth
brew tap ethereum/ethereum
brew install ethereum

# init new chain and run
populus chain new horton
chains/horton/./init_chain.sh
chains/horton/./run_chain.sh

# deploy contracts to the new chain (--no-wait-for-sync to use dummy Ether to run the transaction immediately)
populus deploy --chain horton Donator --no-wait-for-sync
populus deploy --chain horton Greeter --no-wait-for-sync
```

#### Part 7: Interacting With a Contract Instance
http://populus.readthedocs.io/en/latest/dev_cycle.part-07.html

> Populus does not ask you for the address and the ABI of the projects’ contracts: it already has the address in the registrar file at registrar.json, and the ABI in build/contracts.json

```
python3 scripts/donator.py
```

#### Part 8: Web3.py Console
http://populus.readthedocs.io/en/latest/dev_cycle.part-08.html

```
solc --abi contracts/Donator.sol
python3 cli/donator.py
```
