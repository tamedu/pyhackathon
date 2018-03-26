# https://github.com/ethereum/pyethereum/blob/develop/ethereum/tools/tester.py

import unittest

from ethereum.tools import tester
import ethereum.utils as utils


def assert_tx_failed(ballot_tester, function_to_test, exception=tester.TransactionFailed):
    """ Ensure that transaction fails, reverting state (to prevent gas exhaustion) """
    initial_state = ballot_tester.s.snapshot()
    ballot_tester.assertRaises(exception, function_to_test)
    ballot_tester.s.revert(initial_state)


class TestBurnablePayments(unittest.TestCase):
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

    def test_commit(self):
        id = self.c.createBurnablePayment("need help !!!", 100, 1000,  sender=self.t.k2, value=20)
        assert_tx_failed(self, lambda: self.c.commit(id, sender=self.t.k0, value=1))
        self.c.commit(id, sender=self.t.k0, value=100)
        assert utils.remove_0x_head(self.c.bps__worker(id)) == self.t.a0.hex()
        assert self.c.bps__state(id) == self.c.State__Committed()
        assert self.c.bps___balance(id) == 120
        self.c.burn(id, 20, sender=self.t.k2)
        assert self.c.bps___balance(id) == 100
        assert self.c.bps__amountBurned(id) == 20
        self.c.release(id, 50, sender=self.t.k2)
        assert self.c.bps___balance(id) == 50
        assert self.c.bps__amountReleased(id) == 50


        assert_tx_failed(self, lambda: self.c.triggerAutorelease(id, sender=self.t.k0))
        assert_tx_failed(self, lambda: self.c.burn(id, 45, sender=self.t.k1))
        assert_tx_failed(self, lambda: self.c.release(id, 63, sender=self.t.k1))

    def test_triggerAutorelease(self):
        id = self.c.createBurnablePayment("need help !!!", 100, 0,  sender=self.t.k2, value=20)
        self.c.commit(id, sender=self.t.k0, value=200)
        assert self.c.bps___balance(id) == 220
        assert self.c.bps__amountReleased(id) == 0
        self.c.triggerAutorelease(id, sender=self.t.k0)
        assert self.c.bps___balance(id) == 0
        assert self.c.bps__amountReleased(id) == 220


if __name__ == '__main__':
    unittest.main()
