# Events to logged
# Up to 3 parameters can be indexed https://media.consensys.net/technical-introduction-to-events-and-logs-in-ethereum-a074d65dd61e
Created: event({ _payer: indexed(address), _title: bytes32, })
FundsAdded: event({ _burnablePaymentId: indexed(int128), _payer: indexed(address),  _amount: int128 })
Statement: event({ _burnablePaymentId: indexed(int128), _creator: indexed(address), _statement: bytes32 })
FundsRecovered: event({ _burnablePaymentId: indexed(int128) })
Committed: event({ _burnablePaymentId: indexed(int128), _worker: indexed(address) })
FundsBurned: event({ _burnablePaymentId: indexed(int128), _amount: int128 })
FundsReleased: event({ _burnablePaymentId: indexed(int128), _amount: int128 })
Closed: event({ _burnablePaymentId: indexed(int128) })
Unclosed: event({ _burnablePaymentId: indexed(int128) })
AutoreleaseDelayded: event({ _burnablePaymentId: indexed(int128) })
AutoreleaseTriggered: event({ _burnablePaymentId: indexed(int128) })

# Data
burnablePayments: public({
    title: bytes32,
    payer: address,
    worker: address,
    recovered: bool,
    state: int128,

    amountDeposited: wei_value,
    amountBurned: wei_value,
    amountReleased: wei_value,
    commitThreshold: wei_value,

    autoreleaseInterval: timedelta,
    autoreleaseTime: timestamp, # = createdTime + autoreleaseInterval

}[int128])
burnablePaymentsCount: public(int128)

@public
@payable
def __init__():
    self.burnablePaymentsCount = 0

@public
@payable
def createBurnablePayment(_title: bytes32, _initialStatement: bytes32,
        _commitThreshold: wei_value, _autoreleaseInterval: timedelta, ) -> int128:
    _id: int128
    _id = self.burnablePaymentsCount
    self.burnablePaymentsCount += 1
    self.burnablePayments[_id].title = _title
    self.burnablePayments[_id].amountDeposited = msg.value
    self.burnablePayments[_id].amountBurned = 0
    self.burnablePayments[_id].amountReleased = 0
    self.burnablePayments[_id].payer = msg.sender
    self.burnablePayments[_id].commitThreshold = _commitThreshold
    self.burnablePayments[_id].autoreleaseInterval = _autoreleaseInterval
    self.burnablePayments[_id].autoreleaseTime = block.timestamp + _autoreleaseInterval
    self.burnablePayments[_id].state = 0
    log.Created(msg.sender, _title)
    log.Statement(_id, msg.sender, _initialStatement)
    return _id
