pragma solidity ^0.4.11;

/// TUTORIAL CONTRACT DO NOT USE IN PRODUCTION
/// @title Donations collecting contract


contract Donator {

    uint public donationsTotal;
    uint public donationsUsd;
    uint public donationsCount;
    uint public defaultUsdRate;

    function Donator()  public {
        defaultUsdRate = 350;
    }

    // fallback function
    function () payable  public {
        donate(defaultUsdRate);
    }

    modifier nonZeroValue() { if (!(msg.value > 0)) revert(); _; }

    function donate(uint usd_rate) public payable nonZeroValue {
        donationsTotal += msg.value;
        donationsCount += 1;
        defaultUsdRate = usd_rate;
        uint inUsd = msg.value * usd_rate;
        donationsUsd += inUsd;
    }
}
