//SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/utils/cryptography/MerkleProof.sol";
import "@openzeppelin/contracts/token/ERC20/IERC20.sol";

contract Airdrop is Ownable {
    bytes32 public saleMerkleRoot;
    mapping(address => bool) public claimed;
    address public token;

    event Mint(address indexed to, uint256 amount);

    constructor(address _token, bytes32 root) {
      saleMerkleRoot = root;
      token = _token;
    }

    function setSaleMerkleRoot(bytes32 merkleRoot) external onlyOwner {
        saleMerkleRoot = merkleRoot;
    }

    modifier isValidMerkleProof(bytes32[] calldata merkleProof, bytes32 root) {
        require(
            MerkleProof.verify(
                merkleProof,
                root,
                keccak256(abi.encodePacked(msg.sender))
            ),
            "Address does not exist in list"
        );
        _;
    }

    function mint(bytes32[] calldata merkleProof)
        external
        isValidMerkleProof(merkleProof, saleMerkleRoot)
    {
        require(!claimed[msg.sender], "Address already claimed");
        claimed[msg.sender] = true;
        // airdrop amount
        uint256 amount = 6944444444444444444444444444444;
        require(IERC20(token).transferFrom(token, msg.sender, amount), "Airdrop: Token transfer failed");
        emit Mint(msg.sender, amount);
    }
}