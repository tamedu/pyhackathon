def test_defaultUsdRate(chain):
    donator, deploy_tx_hash = chain.provider.get_or_deploy_contract('Donator')
    defaultUsdRate = donator.call().defaultUsdRate()
    assert defaultUsdRate == 350
