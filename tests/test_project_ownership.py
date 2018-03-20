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
    assert project.call().getMyOwnershipPercent() == 100

    title = "My first task"
    project.transact().createTodo(title);
    chain.wait.for_receipt(set_txn_hash)
    t = project.call().getTodoInfo(0)
    assert t[0] == title
    assert t[1] == owner
    assert t[2] == 0
    assert t[3] == False

    project.transact().approveTodo(0);
    chain.wait.for_receipt(set_txn_hash)

    assert project.call().getTotalTime() == 1001
    t = project.call().getTodoInfo(0)
    assert t[0] == title
    assert t[1] == owner
    assert t[2] == 1
    assert t[3] == True

'''
def test_another_participant(chain):
    project, _ = chain.provider.get_or_deploy_contract('ProjectOwnership')
    w3 = chain.web3
    owner = w3.eth.coinbase

    passphrase = 'test'
    another_account = w3.personal.newAccount(password=passphrase)
    assert another_account != owner
    assert w3.personal.unlockAccount(account=another_account,passphrase=passphrase) == True
    assert w3.eth.defaultAccount != another_account

    # set_txn_hash = w3.eth.sendTransaction({'value':ONE_ETH_IN_WEI,'to':another_account,'from':w3.eth.coinbase})
    # chain.wait.for_receipt(set_txn_hash)
    #
    # set_txn_hash = project.transact({"from": another_account}).join()
    # chain.wait.for_receipt(set_txn_hash)
    # assert project.call().getParticipantsCount() == 2
'''
