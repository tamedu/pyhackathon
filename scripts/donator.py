from populus.project import Project
import random

p = Project(project_dir="./")
with p.get_chain('horton') as chain:
    donator, deploy_tx_hash = chain.provider.get_or_deploy_contract('Donator')

print("Donator address on horton is {address}".format(address=donator.address))
if deploy_tx_hash is None:
    print("The contract is already deployed on the chain")
else:
    print("Deploy Transaction {tx}".format(tx=deploy_tx_hash))

# Get contract state with calls
donationsCount = donator.call().donationsCount()
donationsTotal = donator.call().donationsTotal()

# Client side
ONE_ETH_IN_WEI = 10**18  # 1 ETH == 1,000,000,000,000,000,000 Wei
total_ether = donationsTotal/ONE_ETH_IN_WEI
avg_donation = donationsTotal/donationsCount if donationsCount > 0 else 0
status_msg = (
    "Total of {:,.2f} Ether accepted in {:,} donations, "
    "an avergage of {:,.2f} Wei per donation."
    )

print (status_msg.format(total_ether, donationsCount, avg_donation))

# Donate
donation = ONE_ETH_IN_WEI * random.randint(1,10)
effective_eth_usd_rate = 5
transaction = {'value': donation, 'from': chain.web3.eth.coinbase}
tx_hash = donator.transact(transaction).donate(effective_eth_usd_rate)
print ("Thank you for the donation! Tx hash {tx}".format(tx=tx_hash))
