# Import dependencies
import subprocess
import json
from dotenv import load_dotenv
import os

# Load and set environment variables
load_dotenv()
mnemonic = os.getenv("mnemonic")


# Import constants.py and necessary functions from bit and web3
from Constants import *
from bit import PrivateKeyTestnet
from bit.network import NetworkAPI
from web3 import Web3 as w3
from web3.middleware import geth_poa_middleware

# w3.middleware_onion.inject(geth_poa_middleware, layer=0)


# Create a function called `derive_wallets`
def derive_wallets(mnemonic, coin, numderive):
    cmd = f"php ../derive -g --mnemonic='{mnemonic}'' --coin={coin} --numderive={numderive} --format=json"
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    output, err = p.communicate()
    p_status = p.wait()
    return json.loads(output)


# Create a dictionary object called coins to store the output from `derive_wallets`:
coins = {ETH: derive_wallets(mnemonic=mnemonic, coin=ETH, numderive=3), BTCTEST: derive_wallets(mnemonic=mnemonic, coin=BTCTEST, numderive=3)}


# Create a function that converts privkey strings to account objects:
def priv_key_to_account(coin, priv_key):
    print(coin)
    if coin == ETH:
        return Account.privateKeyToAccount(priv_key)
    elif coin == BTCTEST:
        return PrivateKeyTestnet(priv_key)
    
    
# Create child accounts from the coins dictionary:
eth_acct = priv_key_to_account(ETH, derive_wallets(mnemonic, ETH,3)[0]['privkey'])
btctest_acct = priv_key_to_account(BTCTEST, derive_wallets(mnemonic, BTCTEST, 3)[0]['privkey'])


# Function that creates an unsigned transaction with the appropriate metadata:
def create_tx(coin, account, to, amount):
    if coin == ETH: 
        gas_estimate = w3.eth.estimateGas(
            {"from": account.address, "to": to, "value": amount}
        )
        return {
            "to": to,
            "from": account.address,
            "value": amount,
            "gas": gas_estimate,
            "gasPrice": w3.eth.gasPrice,
            "nonce": w3.eth.getTransactionCount(account.address)
            "chainID": w3.net.chainId
        }
    elif coin == BTCTEST:
        return PrivateKeyTestnet.prepare_transaction(account.address, [(to, amount, BTC)])
    
    

# Create a function called `send_tx` that calls `create_tx`, signs and sends the transaction:
def send_tx(coin, account, to, amount):
    raw_tx = create_tx(coin, account, to, amount)
    if coin == ETH:
        signed = account.sign_transaction(raw_tx)
        result = w3.eth.sendRawTransaction(signed.rawTransaction)
        return result#.hex()
    
    elif coin == BTCTEST:
        raw_tx = create_tx(coin, account, recipient, amount)
        signed = account.sign_transaction(raw_tx)
        return NetworkAPI.broadcast_tx_testnet(signed)