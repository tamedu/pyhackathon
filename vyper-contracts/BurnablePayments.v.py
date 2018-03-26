# Events to logged
# Up to 3 parameters can be indexed https://media.consensys.net/technical-introduction-to-events-and-logs-in-ethereum-a074d65dd61e
Created: event({ _id: int128, _payer: indexed(address) })
FundsAdded: event({ _burnablePaymentId: indexed(int128), _payer: indexed(address),  _amount: wei_value, _state: int128 })
Statement: event({ _burnablePaymentId: indexed(int128), _creator: indexed(address), _statement: bytes32 })
FundsRecovered: event({ _burnablePaymentId: indexed(int128) })
Committed: event({ _burnablePaymentId: indexed(int128), _worker: indexed(address) })
FundsBurned: event({ _burnablePaymentId: indexed(int128), _amount: wei_value })
FundsReleased: event({ _burnablePaymentId: indexed(int128), _amount: wei_value })
Closed: event({ _burnablePaymentId: indexed(int128) })
Unclosed: event({ _burnablePaymentId: indexed(int128) })
AutoreleaseDelayed: event({ _burnablePaymentId: indexed(int128) })
AutoreleaseTriggered: event({ _burnablePaymentId: indexed(int128) })

# Data
burnablePayments: public({
    title: bytes <= 100,
    payer: address,
    worker: address,
    state: int128,

    _balance: wei_value,
    amountDeposited: wei_value,
    amountBurned: wei_value,
    amountReleased: wei_value,
    commitThreshold: wei_value,

    autoreleaseInterval: timedelta,
    autoreleaseTime: timestamp, # = createdTime + autoreleaseInterval

}[int128])
burnablePaymentsCount: public(int128)

State: public({
    Opened: int128,
    Committed: int128,
    Closed: int128,
    Recovered: int128
})

@public
@payable
def __init__():
    self.burnablePaymentsCount = 0
    self.State.Opened = 0
    self.State.Committed = 1
    self.State.Closed = 2
    self.State.Recovered = 3

@public
@payable
def createBurnablePayment(_title: bytes <= 100, _commitThreshold: wei_value, _autoreleaseInterval: timedelta, ) -> int128:
    _id: int128
    _id = self.burnablePaymentsCount
    self.burnablePaymentsCount += 1
    self.burnablePayments[_id].title = _title
    self.burnablePayments[_id].amountDeposited = msg.value
    self.burnablePayments[_id]._balance = msg.value
    self.burnablePayments[_id].amountBurned = 0
    self.burnablePayments[_id].amountReleased = 0
    self.burnablePayments[_id].payer = msg.sender
    self.burnablePayments[_id].commitThreshold = _commitThreshold
    self.burnablePayments[_id].autoreleaseInterval = _autoreleaseInterval
    self.burnablePayments[_id].autoreleaseTime = -1
    self.burnablePayments[_id].state = self.State.Opened
    log.Created(_id, msg.sender)
    if msg.value > 0:
        log.FundsAdded(_id, msg.sender, msg.value, self.burnablePayments[_id].state)
    return _id

@private
def onlyPayerOrWorker(_id: int128, _person: address) -> bool:
    return self.burnablePayments[_id].payer == _person or self.burnablePayments[_id].worker == _person

@public
@payable
def addFunds(_id: int128):
    assert self.burnablePayments[_id].payer == msg.sender
    assert msg.value > 0
    self.burnablePayments[_id].amountDeposited += msg.value
    self.burnablePayments[_id]._balance += msg.value
    log.FundsAdded(_id, msg.sender, msg.value, self.burnablePayments[_id].state)
    if self.burnablePayments[_id].state == self.State.Closed:
        self.burnablePayments[_id].state = self.State.Committed
        log.Unclosed(_id)

@public
@payable
def commit(_id: int128):
    assert self.burnablePayments[_id].state == self.State.Opened
    assert self.burnablePayments[_id].commitThreshold <= msg.value
    self.burnablePayments[_id].state = self.State.Committed
    self.burnablePayments[_id].worker = msg.sender
    self.burnablePayments[_id].autoreleaseTime = block.timestamp + self.burnablePayments[_id].autoreleaseInterval
    if msg.value > 0:
        self.burnablePayments[_id].amountDeposited += msg.value
        self.burnablePayments[_id]._balance += msg.value
        log.FundsAdded(_id, msg.sender, msg.value, self.burnablePayments[_id].state)

@private
def closeIfBalanceIsZero(_id: int128):
    if self.burnablePayments[_id]._balance == 0:
        self.burnablePayments[_id].state = self.State.Closed
        log.Closed(_id)

@public
def burn(_id: int128, _amount: wei_value):
    assert self.burnablePayments[_id].state == self.State.Committed
    assert self.burnablePayments[_id].payer == msg.sender
    assert self.burnablePayments[_id]._balance >= _amount
    send(0x0000000000000000000000000000000000000000, _amount)
    self.burnablePayments[_id].amountBurned += _amount
    self.burnablePayments[_id]._balance -= _amount
    log.FundsBurned(_id, _amount)
    self.closeIfBalanceIsZero(_id)

@private
def internalRelease(_id: int128, _amount: wei_value):
    assert self.burnablePayments[_id]._balance >= _amount
    send(self.burnablePayments[_id].worker, _amount)
    self.burnablePayments[_id].amountReleased += _amount
    self.burnablePayments[_id]._balance -= _amount
    log.FundsReleased(_id, _amount)
    self.closeIfBalanceIsZero(_id)

@public
def release(_id: int128, _amount: wei_value):
    assert self.burnablePayments[_id].state == self.State.Committed
    assert self.burnablePayments[_id].payer == msg.sender
    self.internalRelease(_id, _amount)

@public
def delayAutorelease(_id: int128):
    assert self.burnablePayments[_id].state == self.State.Committed
    assert self.burnablePayments[_id].payer == msg.sender
    self.burnablePayments[_id].autoreleaseTime = block.timestamp + self.burnablePayments[_id].autoreleaseInterval
    log.AutoreleaseDelayed(_id)

@public
def triggerAutorelease(_id: int128):
    assert self.burnablePayments[_id].state == self.State.Committed
    assert self.burnablePayments[_id].worker == msg.sender
    assert block.timestamp >= self.burnablePayments[_id].autoreleaseTime
    self.internalRelease(_id, self.burnablePayments[_id]._balance)
    log.AutoreleaseTriggered(_id)

@public
def recoverFunds(_id: int128):
    assert self.burnablePayments[_id].payer == msg.sender
    assert self.burnablePayments[_id].state == self.State.Opened
    send(msg.sender, self.burnablePayments[_id]._balance)
    self.burnablePayments[_id]._balance = 0
    self.burnablePayments[_id].state = self.State.Recovered
    log.FundsRecovered(_id)

# should be done via Statement contract
# @public
# def logStatement(_id: int128, _statement: bytes32):
#     assert self.onlyPayerOrWorker(_id, msg.sender)
#     log.Statement(_id, msg.sender, _statement)
