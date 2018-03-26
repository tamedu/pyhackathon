# https://github.com/ethereum/pyethereum/blob/develop/ethereum/tools/tester.py

import unittest

from ethereum.tools import tester
import ethereum.utils as utils


def assert_tx_failed(ballot_tester, function_to_test, exception=tester.TransactionFailed):
    """ Ensure that transaction fails, reverting state (to prevent gas exhaustion) """
    initial_state = ballot_tester.s.snapshot()
    ballot_tester.assertRaises(exception, function_to_test)
    ballot_tester.s.revert(initial_state)


class Testbps(unittest.TestCase):
    def setUp(self):
        # Initialize tester, contract and expose relevant objects
        self.t = tester
        self.s = self.t.Chain()
        self.s.head_state.gas_limit = 10**7
        from vyper import compiler
        self.t.languages['vyper'] = compiler.Compiler()
        contract_code = open('BurnablePayments.v.py').read()
        self.c = self.s.contract(contract_code, language='vyper', args=[])

    def test_createBurnablePayment(self):
        id = self.c.createBurnablePayment("need help !!!", 100, 1000,  sender=self.t.k0, value=2)
        assert self.c.bpsCount() == 1
        assert self.c.bps__title(id) == b'need help !!!'
        assert utils.remove_0x_head(self.c.bps__payer(id)) == self.t.a0.hex()
        assert self.c.bps__worker(id) == '0x0000000000000000000000000000000000000000'
        assert self.c.bps__amountBurned(id) == 0
        assert self.c.bps__amountReleased(id) == 0
        assert self.c.bps___balance(id) == 2
        assert self.c.bps__state(id) == 0
        assert self.c.bps__commitThreshold(id) == 100
        assert self.c.bps__autoreleaseInterval(id) == 1000
        assert self.c.bps__amountDeposited(id) == 2
        # assert self.c.bps__autoreleaseTime(id) ==

        self.c.addFunds(id, sender=self.t.k0, value=8)
        assert self.c.bps___balance(id) == 10

        self.c.recoverFunds(id)
        assert self.c.bps___balance(id) == 0

if __name__ == '__main__':
    unittest.main()
