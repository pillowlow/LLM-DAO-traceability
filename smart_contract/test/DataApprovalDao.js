const { expect } = require("chai");
const { ethers } = require("hardhat");

describe("DataApprovalDAO", function () {
  let dao;
  let owner, user;

  beforeEach(async function () {
    [owner, user] = await ethers.getSigners();

    const DAOFactory = await ethers.getContractFactory("DataApprovalDAO");
    dao = await DAOFactory.deploy();
    await dao.waitForDeployment();
  });

  it("should allow proposing and approving a dataset", async function () {
    const cid = "a9682d2d2f0c3760cf3bfda81421a4babb37f8def6b89029aa09fc5c93fabad3";

    // user proposes
    await dao.connect(user).proposeDataset(cid);
    expect(await dao.isApproved(cid)).to.equal(false);

    // owner approves
    await dao.connect(owner).approveDataset(cid);
    expect(await dao.isApproved(cid)).to.equal(true);
  });
});
