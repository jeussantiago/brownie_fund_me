from brownie import FundMe, MockV3Aggregator, network, config
from scripts.helpful_scripts import (
    get_account,
    deploy_mocks,
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
)


def deploy_fund_me():
    account = get_account()
    # If we are on a  persistent network like rinkeby,use the associated address
    # otherwise, deploy mocks ---- network.show_active() tells what network we are on (ex: rinkeby)
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        price_feed_address = config["networks"][network.show_active()][
            "eth_usd_price_feed"
        ]
    else:
        deploy_mocks()
        price_feed_address = MockV3Aggregator[-1].address

    # publish_source=True => added ETHERSCAN api key to .env file -> meaning that brownie will publish our code to etherscan without manually having to do it
    # FundMe requires parameters for constructor
    fund_me = FundMe.deploy(
        price_feed_address,
        {"from": account},
        publish_source=config["networks"][network.show_active()].get(
            "verify"
        ),  # publih source(verify) added to .yaml depending on if we're on development or not -> .get('verify') == ['verify'], just incase you forget to add 'verify to .yaml file
    )
    print(f"Contract deployed to {fund_me.address}")
    return fund_me


def main():
    deploy_fund_me()
