from steemapi.steemnoderpc import SteemNodeRPC
from pprint import pprint
import time
import os

"""
   Requires installation of xeroc's python-steemlib
   Adapted from monitor.py
   
   Connection Parameters to steemd daemon.
   Start the steemd daemon with the rpc-endpoint parameter:
      ./programs/steemd/steemd --rpc-endpoint=127.0.0.1:8092
    This opens up a RPC port (e.g. at 8092). Currently, authentication
    is not yet available, thus, we recommend to restrict access to
    localhost. Later we will allow authentication via username and
    passpword (both empty now).
"""
rpc = SteemNodeRPC("ws://localhost:8090", "", "")

"""
    Last Block that you have process in your backend.
    Processing will continue at `last_block + 1`
"""
last_block = 1

"""
   Witness accounts to monitor
"""
watch_accounts = ["roadscape", "kushed", "smooth.witness", "abit", "pharesim", "dele-puppy", "steemed", "nextgencrypto", "clayop", "au1nethyb1", "steempty", "riverhead", "arhag", "complexring", "bitcube", "silversteem", "xeldal", "witness.svk", "wackou", "bhuz", "steemychicken1", "datasecuritynode", "cyrano.witness", "delegate.lafona", "boatymcboatface", "jabbasteem", "bue", "ihashfury", "masteryoda", "joseph", "pumpkin", "blocktrades", "steem-id", "liondani", "salvation", "modprobe", "dantheman", "mrs.agsexplorer", "fminerten", "lafona", "pfunk", "summon", "randaletouri", "rainman", "itsascam", "steemroller", "hello", "lxcteem", "steemit", "idol", "bittrexrichie", "testzcrypto", "moon", "drsteem", "afew", "phantas", "healthcare", "felekas1", "abka", "neonminer", "silkroad", "signalandnoise", "stephanie", "stesting1", "drifter1", "support1", "alittle", "zisis1", "miltos1"]


if __name__ == '__main__':
    # Let's find out how often blocks are generated!
    config = rpc.get_config()
    block_interval = config["STEEMIT_BLOCK_INTERVAL"]

    # We are going to loop indefinitely
    
    #Initialize count to store blocks produced for each witness
    count={}
    for witness in watch_accounts:
        count[witness] = 0
    while True:

        # Get chain properies to identify the 
        # head/last reversible block
        props = rpc.get_dynamic_global_properties()

        # Get block number
        block_number = props['head_block_number']


        # We loop through all blocks we may have missed since the last
        # block defined above
        while (block_number - last_block) > 0:
            last_block += 1

            # Get full block
            block = rpc.get_block(last_block)
            
            #Match witness from block to witness from list and increase block production count of that witness
            for witness in watch_accounts:
                if block["witness"] == witness:
                    count[witness] = count[witness] + 1
       
        os.system('clear')
        
        print("{:^17} {:^17} {:^17} {:^17}".format("witness","produced","missed","reliability"))
        for witness in watch_accounts:
            
            #Gets missed block count from blockchain(for each witness)
            witness_info = rpc.get_witness_by_account(witness)
            missed_count = witness_info["total_missed"]            
            
            #outputs statistics if produced more than 50 blocks
            if count[witness]>50:
                reliability = count[witness]/(count[witness] + missed_count)*100
                print("{:^17} {:^17} {:^17} {:^17}".format(witness,count[witness],missed_count,reliability))

        # Sleep for one block
        time.sleep(block_interval)
