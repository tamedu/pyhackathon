def test_grantable_updates(chain):
    grantable, _ = chain.provider.get_or_deploy_contract('GrantableUpdates')
