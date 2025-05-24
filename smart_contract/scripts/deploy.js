const hre = require("hardhat");

async function main() {
  const Dao = await hre.ethers.getContractFactory("DataApprovalDAO");
  const dao = await Dao.deploy();
  await dao.waitForDeployment();

  console.log("✅ DataApprovalDAO deployed to:", await dao.getAddress());
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
