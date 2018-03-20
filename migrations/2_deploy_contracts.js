var GrantableUpdates = artifacts.require("GrantableUpdates");

var BurnablePaymentFactory = artifacts.require("BurnablePaymentFactory");
var BurnablePayment = artifacts.require("BurnablePayment");

module.exports = function(deployer) {
  // deployer.deploy(GrantableUpdates);
  deployer.deploy(BurnablePaymentFactory);
  deployer.deploy(BurnablePayment);
};
