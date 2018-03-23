# Ethereum Virtual Machine Security

**Table of Content**
<!-- TOC START min:2 max:4 link:true update:true -->
  - [Talks](#talks)
    - [A brief history of smart contract security](#a-brief-history-of-smart-contract-security)
    - [Automatic bugfinding for the blockchain](#automatic-bugfinding-for-the-blockchain)
  - [Tutorials](#tutorials)
    - [Manticore](#manticore)
  - [List of Tools](#list-of-tools)
    - [trailofbits](#trailofbits)
    - [Solium Linter](#solium-linter)
    - [MAIAN: finding trace vulnerabilities](#maian-finding-trace-vulnerabilities)

<!-- TOC END -->

## Talks
* https://blog.trailofbits.com/2017/12/22/videos-from-ethereum-focused-empire-hacking
* [https://github.com/trailofbits/presentations/tree/master/Automatic Bug-Finding for the Blockchain](https://github.com/trailofbits/presentations/tree/master/Automatic%20Bug-Finding%20for%20the%20Blockchain)
### A brief history of smart contract security
* Gas https://youtu.be/8LAThtT7euA?t=672
* Reentry https://youtu.be/8LAThtT7euA?t=795
* the DAO https://youtu.be/8LAThtT7euA?t=864
* Parity multisign hack https://youtu.be/8LAThtT7euA?t=942
* Secure reuse code (DappHub, OpenZeppelin) https://youtu.be/8LAThtT7euA?t=1057
* Static Analysis Tool (Mythirl) https://youtu.be/8LAThtT7euA?t=1070

### Automatic bugfinding for the blockchain
* Blockchain = Distributed data + Decentralized consensus https://youtu.be/r0cvQhBBw1w?t=121
    - Distributed data: all participants store all the data
    - Decentralized consensus: everyone agree on the data
    - 2009 Bitcoin: the first blockchain $, solved double-spending problem
    - 2015 Ethereum: extended blockchain to run app, store & exec code
    - Bitcoin:distributed-database => Ethereum:distributed-virtual-machine
    - Smart Contracts: apps run on Ethereum - everyone exec & verify it, no-one can stop or secretly modify data
* EVM https://youtu.be/r0cvQhBBw1w?t=312
    - `contract = balance + code + storage[key:value]`
    - `calling a function = making a transaction`
    - `state = contract variables + balance`
* Transaction https://youtu.be/r0cvQhBBw1w?t=460
    - transfer(from,to)=data
    - data: function name (4 byte of keccak256())
* Vulnerabilities https://youtu.be/r0cvQhBBw1w?t=566
* Reentry https://youtu.be/r0cvQhBBw1w?t=718
    - the DAO `withDrawBalance() { ... msg.sender.call.value(userBalance[msg.sender])() ... }`
    - call withdrawBalance() from a malicious contract
    - withdrawBalance() calls the fallback function of the malicious contract
    - the fallback calls a second time withdrawBalance()
    - repeat n times => withdraw n times the original deposit
* Logic vuls hard to find https://youtu.be/r0cvQhBBw1w?t=909
* Manticore analyze EVM code https://youtu.be/r0cvQhBBw1w?t=993
    - Transaction https://youtu.be/r0cvQhBBw1w?t=1471

## Tutorials
### Manticore
```
brew install python3
pip3 install --upgrade pip
pip install manticore
git clone https://github.com/trailofbits/manticore.git && cd manticore
make
#pip install --no-binary capstone .

```

## List of Tools
### trailofbits
https://blog.trailofbits.com/2018/03/23/use-our-suite-of-ethereum-security-tools
* https://github.com/trailofbits/manticore
* https://github.com/trailofbits/echidna
* https://github.com/trailofbits/ethersplay
* https://github.com/trailofbits/not-so-smart-contracts

### Solium Linter
https://github.com/duaraghav8/Solium
```
npm install -g solium
cd pyhackathon
solium --init
solium -f contracts/ProjectOwnership.sol
solium -d contracts/
solium -d contracts --fix # auto-fix codes

#Atom Solium Linter https://github.com/travs/linter-solium
apm install linter-solium
npm i -g solium
solium --init #in your project dir
```

### MAIAN: finding trace vulnerabilities
https://github.com/MAIAN-tool/MAIAN
```
python3 maian.py -s ParityWalletLibrary.sol WalletLibrary -c 0
```
