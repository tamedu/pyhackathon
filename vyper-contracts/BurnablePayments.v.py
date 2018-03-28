# Events to log
# Up to 3 parameters can be indexed https://media.consensys.net/technical-introduction-to-events-and-logs-in-ethereum-a074d65dd61e
Created: event({ _id: int128, _payer: indexed(address) })
FundsAdded: event({ _burnablePaymentId: indexed(int128), _payer: indexed(address),  _amount: wei_value, _state: int128 })
FundsRecovered: event({ _burnablePaymentId: indexed(int128) })
Committed: event({ _burnablePaymentId: indexed(int128), _worker: indexed(address) })
FundsBurned: event({ _burnablePaymentId: indexed(int128), _amount: wei_value })
FundsReleased: event({ _burnablePaymentId: indexed(int128), _amount: wei_value })
Closed: event({ _burnablePaymentId: indexed(int128) })
Unclosed: event({ _burnablePaymentId: indexed(int128) })
AutoreleaseDelayed: event({ _burnablePaymentId: indexed(int128) })
AutoreleaseTriggered: event({ _burnablePaymentId: indexed(int128) })

# ***** Data *****
bps: public({
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
bpsCount: public(int128)

State: public({
    Opened: int128,
    Committed: int128,
    Closed: int128,
})

# ***** Constructor *****

@public
@payable
def __init__():
    self.bpsCount = 0
    self.State.Opened = 0
    self.State.Committed = 1
    self.State.Closed = 2

# ***** Helpers *****

@private
def closeIfBalanceIsZero(_id: int128):
    if self.bps[_id]._balance == 0:
        self.bps[_id].state = self.State.Closed
        log.Closed(_id)

@private
def internalRelease(_id: int128, _amount: wei_value):
    assert self.bps[_id]._balance >= _amount
    send(self.bps[_id].worker, _amount)
    self.bps[_id].amountReleased += _amount
    self.bps[_id]._balance -= _amount
    log.FundsReleased(_id, _amount)
    self.closeIfBalanceIsZero(_id)

# ***** Public *****

@public
@payable
def createBurnablePayment(_title: bytes <= 100, _commitThreshold: wei_value,
        _autoreleaseInterval: timedelta, ) -> int128:
    _id: int128
    _id = self.bpsCount
    self.bpsCount += 1
    self.bps[_id].title = _title
    self.bps[_id].amountDeposited = msg.value
    self.bps[_id]._balance = msg.value
    self.bps[_id].amountBurned = 0
    self.bps[_id].amountReleased = 0
    self.bps[_id].payer = msg.sender
    self.bps[_id].commitThreshold = _commitThreshold
    self.bps[_id].autoreleaseInterval = _autoreleaseInterval
    self.bps[_id].autoreleaseTime = -1
    self.bps[_id].state = self.State.Opened
    log.Created(_id, msg.sender)
    if msg.value > 0:
        log.FundsAdded(_id, msg.sender, msg.value, self.bps[_id].state)
    return _id

@public
@payable
def addFunds(_id: int128):
    assert self.bps[_id].payer == msg.sender
    assert msg.value > 0
    self.bps[_id].amountDeposited += msg.value
    self.bps[_id]._balance += msg.value
    log.FundsAdded(_id, msg.sender, msg.value, self.bps[_id].state)
    if self.bps[_id].state == self.State.Closed:
        self.bps[_id].state = self.State.Committed
        log.Unclosed(_id)

@public
@payable
def commit(_id: int128):
    assert self.bps[_id].state == self.State.Opened
    assert self.bps[_id].commitThreshold <= msg.value
    self.bps[_id].state = self.State.Committed
    self.bps[_id].worker = msg.sender
    self.bps[_id].autoreleaseTime = block.timestamp + self.bps[_id].autoreleaseInterval
    if msg.value > 0:
        self.bps[_id].amountDeposited += msg.value
        self.bps[_id]._balance += msg.value
        log.FundsAdded(_id, msg.sender, msg.value, self.bps[_id].state)

@public
def burn(_id: int128, _amount: wei_value):
    assert self.bps[_id].state == self.State.Committed
    assert self.bps[_id].payer == msg.sender
    assert self.bps[_id]._balance >= _amount
    send(0x0000000000000000000000000000000000000000, _amount)
    self.bps[_id].amountBurned += _amount
    self.bps[_id]._balance -= _amount
    log.FundsBurned(_id, _amount)
    self.closeIfBalanceIsZero(_id)

@public
def release(_id: int128, _amount: wei_value):
    assert self.bps[_id].state == self.State.Committed
    assert self.bps[_id].payer == msg.sender
    self.internalRelease(_id, _amount)

@public
def delayAutorelease(_id: int128):
    assert self.bps[_id].state == self.State.Committed
    assert self.bps[_id].payer == msg.sender
    self.bps[_id].autoreleaseTime = block.timestamp + self.bps[_id].autoreleaseInterval
    log.AutoreleaseDelayed(_id)

@public
def triggerAutorelease(_id: int128):
    assert self.bps[_id].state == self.State.Committed
    assert self.bps[_id].worker == msg.sender
    assert block.timestamp >= self.bps[_id].autoreleaseTime
    self.internalRelease(_id, self.bps[_id]._balance)
    log.AutoreleaseTriggered(_id)

@public
def recoverFunds(_id: int128):
    assert self.bps[_id].payer == msg.sender
    assert self.bps[_id].state == self.State.Opened
    send(msg.sender, self.bps[_id]._balance)
    self.bps[_id]._balance = 0
    log.FundsRecovered(_id)
    self.closeIfBalanceIsZero(_id)

# Should be done via Statement contract
# Simiilar to https://github.com/Bounties-Network/StandardBounties/blob/master/contracts/UserComments.sol
# Statement: event({ _burnablePaymentId: indexed(int128), _creator: indexed(address), _statement: bytes32 })
# @public
# def logStatement(_id: int128, _statement: bytes32):
#     assert self.bps[_id].payer == msg.sender or self.bps[_id].worker == msg.sender
#     log.Statement(_id, msg.sender, _statement)
