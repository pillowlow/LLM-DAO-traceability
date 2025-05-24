// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

/// @title DataApprovalDAO
/// @notice A minimal DAO-style smart contract for approving datasets before use in an LLM training pipeline.
/// @dev This contract simulates DAO governance over dataset usage by tracking approved CIDs (e.g., IPFS or SHA256 hashes).

contract DataApprovalDAO {
    /// @notice The owner of the contract (can approve datasets)
    address public owner;

    /// @notice Structure to hold each dataset's proposal data
    struct DatasetProposal {
        string cid;        // Dataset identifier (e.g., IPFS CID or SHA256 hash)
        address proposer;  // Address of the user who proposed the dataset
        bool approved;     // Whether the dataset has been approved for use
    }

    /// @notice Mapping from CID to proposal data
    mapping(string => DatasetProposal) public proposals;

    /// @notice Emitted when a dataset is proposed
    event DatasetProposed(string cid, address proposer);

    /// @notice Emitted when a dataset is approved
    event DatasetApproved(string cid, address approver);

    /// @notice Restricts certain functions to only the contract owner
    modifier onlyOwner() {
        require(msg.sender == owner, "Not authorized");
        _;
    }

    /// @notice Constructor sets the contract deployer as the owner
    constructor() {
        owner = msg.sender;
    }

    /// @notice Allows any user to propose a dataset for approval
    /// @param cid A unique identifier for the dataset (e.g., IPFS CID or hash)
    function proposeDataset(string memory cid) public {
        // Ensure this CID hasn't already been proposed
        require(bytes(proposals[cid].cid).length == 0, "CID already proposed");

        // Save the proposal to the mapping
        proposals[cid] = DatasetProposal({
            cid: cid,
            proposer: msg.sender,
            approved: false
        });

        emit DatasetProposed(cid, msg.sender);
    }

    /// @notice Allows the contract owner to approve a proposed dataset
    /// @param cid The identifier of the dataset to approve
    function approveDataset(string memory cid) public onlyOwner {
        // Make sure the dataset was previously proposed
        require(bytes(proposals[cid].cid).length != 0, "CID not found");

        // Ensure the dataset hasn't already been approved
        require(!proposals[cid].approved, "Already approved");

        // Mark the dataset as approved
        proposals[cid].approved = true;

        emit DatasetApproved(cid, msg.sender);
    }

    /// @notice Checks if a dataset is approved
    /// @param cid The dataset identifier to check
    /// @return True if approved, false otherwise
    function isApproved(string memory cid) public view returns (bool) {
        return proposals[cid].approved;
    }
}
