from steemapi.steemnoderpc import SteemNodeRPC
from pprint import pprint
import time

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
last_block = 864000

"""
   Witness account to monitor
"""
watch_account = "delegate.lafona"


if __name__ == '__main__':
    # Let's find out how often blocks are generated!
    config = rpc.get_config()
    block_interval = config["STEEMIT_BLOCK_INTERVAL"]

    # We are going to loop indefinitely
    count = 0
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
                      
            if block["witness"] == watch_account:
                count = count + 1
                print("Produced Blocks for",watch_account,":", count)
                witness_info = rpc.get_witness(watch_account)
                missed_count = witness_info["total_missed"]
                print("Missed:",missed_count)
                reliability = count/(count + missed_count)*100
                print("Reliability:",reliability)


            # Process block
            #process_block(block, last_block)

        # Sleep for one block

        time.sleep(block_interval)
