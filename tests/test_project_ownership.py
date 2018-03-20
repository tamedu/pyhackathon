ONE_ETH_IN_WEI = 10**18

def test_project_ownership(chain):
    project, _ = chain.provider.get_or_deploy_contract('ProjectOwnership')

    assert project.call().version() == '0.0.1'
    assert project.call().getParticipantsCount() == 0
    assert project.call().getTotalTime() == 0


def test_just_joined_participant(chain):
    project, _ = chain.provider.get_or_deploy_contract('ProjectOwnership')
    owner = chain.web3.eth.coinbase

    set_txn_hash = project.transact().join()
    chain.wait.for_receipt(set_txn_hash)

    assert project.call().getParticipantsCount() == 1
    assert project.call().getTotalTime() == 1
    assert project.call().getMyOwnershipPercent() == [100, 0, 1, 1]

    title = "My first task"
    set_txn_hash = project.transact().createTodo(title);
    chain.wait.for_receipt(set_txn_hash)
    t = project.call().getTodoInfo(0)
    assert t[0] == title
    assert t[1] == owner
    assert t[2] == 0
    assert t[3] == False

    set_txn_hash = project.transact().approveTodo(0);
    chain.wait.for_receipt(set_txn_hash)

    set_txn_hash = project.transact().approveTodo(0);
    chain.wait.for_receipt(set_txn_hash)

    assert project.call().getTotalTime() == 1001
    t = project.call().getTodoInfo(0)
    assert t[0] == title
    assert t[1] == owner
    assert t[2] == 1
    assert t[3] == True

def test_another_participant(chain):
    project, _ = chain.provider.get_or_deploy_contract('ProjectOwnership')
    w3 = chain.web3
    owner = chain.web3.eth.coinbase

    set_txn_hash = project.transact().join()
    chain.wait.for_receipt(set_txn_hash)
    set_txn_hash = project.transact().createTodo("account 1 todo");
    chain.wait.for_receipt(set_txn_hash)

    # create another account to call from
    passphrase = 'test'
    another_account = w3.personal.newAccount(password=passphrase)
    assert another_account != owner
    assert w3.personal.unlockAccount(account=another_account,passphrase=passphrase) == True
    assert owner != another_account
    # send 1 ether to new account
    set_txn_hash = w3.eth.sendTransaction({'value':ONE_ETH_IN_WEI,'to':another_account,'from':w3.eth.coinbase})
    chain.wait.for_receipt(set_txn_hash)

    #  call contract from new account
    set_txn_hash = project.transact({"from": another_account}).join()
    chain.wait.for_receipt(set_txn_hash)
    # should have two participants, 50% ownership for each
    assert project.call().getParticipantsCount() == 2
    assert project.call().getTotalTime() == 2
    assert project.call().getMyOwnershipPercent() == [50, 0, 1, 2]
    assert project.call({'from': another_account}).getMyOwnershipPercent() == [50, 1, 1, 2]

    # owner approve first todo
    set_txn_hash = project.transact().approveTodo(0);
    chain.wait.for_receipt(set_txn_hash)

    assert project.call().getTotalTime() == 2
    t = project.call().getTodoInfo(0)
    assert t[1] == owner
    assert t[2] == 1
    assert t[3] == False

    # the other participant approve first todo
    set_txn_hash = project.transact({'from': another_account}).approveTodo(0);
    chain.wait.for_receipt(set_txn_hash)

    t = project.call().getTodoInfo(0)
    assert t[2] == 2
    assert t[3] == True

    assert project.call().getTotalTime() == 1002
    assert project.call().getParticipantOwnedTime(0) == 1001
    assert project.call().getParticipantOwnedTime(1) == 1

    assert project.call({'from': owner}).getMyOwnershipPercent() == [100, 0, 1001, 1002]
    assert project.call({'from': another_account}).getMyOwnershipPercent() == [0, 1, 1, 1002]
