//Grantable Updates

pragma solidity ^0.4.21;

contract GrantableUpdates {
    mapping (address => bool) public agentCanUpdate;
    
    event Update(address agent, string data);
    
    modifier onlyApprovedSender() {
        require(agentCanUpdate[msg.sender] == true);
        _;
    }
    
    function test(address addr)
    public 
    returns (bool) {
        return (msg.sender == addr);
    }
    
    function GrantableUpdates(address initialAgent)
    public {
        agentCanUpdate[initialAgent] = true;
    }
    
    function grantUpdatePermissionTo(address newAgent)
    onlyApprovedSender()
    public {
        agentCanUpdate[newAgent] = true;
    }
    
    function postUpdate(string data)
    onlyApprovedSender()
    public {
        emit Update(msg.sender, data);
    }
}