// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

/**
 * @title VulnerableToken
 * @dev Example contract with multiple vulnerabilities for testing SolAudit
 */
contract VulnerableToken {
    mapping(address => uint256) public balances;
    address public owner;
    bool private locked;
    
    constructor() {
        owner = msg.sender;
    }
    
    // VULNERABILITY 1: Missing access control
    function mint(address to, uint256 amount) public {
        balances[to] += amount;
    }
    
    // VULNERABILITY 2: Reentrancy
    function withdraw(uint256 amount) public {
        require(balances[msg.sender] >= amount, "Insufficient balance");
        
        (bool success, ) = msg.sender.call{value: amount}("");
        require(success, "Transfer failed");
        
        balances[msg.sender] -= amount;
    }
    
    // VULNERABILITY 3: Integer overflow (if Solidity < 0.8.0)
    function transfer(address to, uint256 amount) public {
        balances[msg.sender] -= amount;
        balances[to] += amount;
    }
    
    // VULNERABILITY 4: Timestamp dependence
    function claimReward() public {
        require(block.timestamp % 10 == 0, "Not lucky");
        balances[msg.sender] += 100 ether;
    }
    
    // VULNERABILITY 5: Unprotected selfdestruct
    function destroy() public {
        selfdestruct(payable(msg.sender));
    }
    
    receive() external payable {
        balances[msg.sender] += msg.value;
    }
}
