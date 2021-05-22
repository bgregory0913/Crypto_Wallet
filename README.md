# Multi-Blockchain Wallet in Python </h1>

![Coin_Cradle](https://github.com/bgregory0913/Crypto_Wallet/blob/master/Images/newtons-coin-cradle.jpg)


## Purpose

Example: The main focus of a startup company is to build a portfolio management system (PMS) that supports both, traditional assets
(gold, silver, stocks, etc) and crypto-assets! With so many coins being used and the understanding of how HD wallets work, they would need to build a system that can create the portfolios.

Unfortunately there aren't as many tools available in Python for this sort of thing (yet), but this is an advantage that allows early market entry for this sort of system.

There is a command line tool, `hd-wallet-derive`, that supports not only BIP32, BIP39, and BIP44, but also supports non-standard derivation paths for today's most popular wallets.

Once we integrate the "universal" wallet, it can be used to manage hundreds of thousands of addresses across 300+ coins, giving a huge advantage over the competition.

In this project, we only need 2 coins working to prove the point: Ethereum (ETH) & Bitcoin Testnet (BTCTEST).
Ethereum keys are the same format on any network, so the Ethereum keys work with custom networks or testnets.


## Overview:

### Instructions for Replication (step-by-step):

#### Dependencies:

1. PHP must be installed on your operating system (any version, 5 or 7); __you will *not* need to know any PHP for this.__
2. We have to clone the [hd-wallet-derive](https://github.com/dan-da/hd-wallet-derive) tool.
3. pip install [`bit`](https://ofek.github.io/bit/)  - the Python Bitcoin library.
4. pip install [`web3.py`](https://github.com/ethereum/web3.py) the - Python Ethereum library.

#### Setting up the Project:

1. Create a project directory called `wallet` and `cd` into it.
2. Clone the `hd-wallet-derive` tool into this folder and install it using the instructions on its `README.md`.
3. Create a symlink called `derive` for the `hd-wallet-derive/hd-wallet-derive.php` script into the top level project
  directory like so: `ln -s hd-wallet-derive/hd-wallet-derive.php derive`
  * This will clean up the command needed to run the script in our code, as we can call `./derive`
    instead of `./hd-wallet-derive/hd-wallet-derive.php`.
4. Test that you can run the `./derive` script properly, use one of the examples on the repo's `README.md`.
  4.1 __NOTE: If one get an error running `./derive`, as it can happen on windows machine then use: `php ./hd-wallet-derive/hd-wallet-derive.php`.__

5. Create a file called `wallet.py`; this will be the universal wallet script.

__The directory tree should look like this:__

![Dir_Tree](https://github.com/bgregory0913/Crypto_Wallet/blob/master/Images/tree.png)

#### Setup Constants File to Manage Coins:

1. In a separate file, `constants.py`, set the following constants:
  - `BTC = 'btc'`
  - `ETH = 'eth'`
  - `BTCTEST = 'btc-test'`
1. In `wallet.py`, import all constants: `from constants import *`
  - Use this to reference these strings in function calls and setting object keys.

#### Generate a Mnemonic Phrase:

1. Generate a new 12 word mnemonic using `hd-wallet-derive` or by using [this tool](https://iancoleman.io/bip39/).
2. Set this mnemonic as an environment variable, and include the one you generated as a fallback using:
  `mnemonic = os.getenv('MNEMONIC', 'insert mnemonic here')`

#### Derive a Wallet:

1. Pass as variables Mnemonic (--mnemonic), Coin (--coin) and Numderive (--numderive), then set the --format=json flag,  parse the output   into a JSON object using json.loads(output).And finally pass all into one function, called 'derive_wallets'.
- If done properly the final object should look like this:
- Accounts used in the project are marked for BTC Test and ETH
