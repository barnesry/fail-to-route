#!/usr/bin/python
#
# Simple script to collect tcp_inpcb info from SRX device(s) and report results
# in tabular format. Checks for buffer exhaustion and reports TRUE if within 10%
# of limit.
#

from jnpr.junos import Device
from lxml import etree
import argparse, logging, getpass, sys

import json
import pprint

def main(args):

    host = args.host
    user = args.user
    # no password as we're relying on local ssh keys

    ted = None
    js = ""

    # setup our connection
    dev=Device(host=host, user=user)
    try:
        dev.open()

        # retrieve TED
        ted = dev.rpc.get_ted_database_information({'format': 'json'})


        print("=== raw response ===")
        print(ted)
        print()
    except Exception as e:
        print ("Failed to retreive TED: {}".format(e))
    
    # convert ted to valid json string
    json_str = str(ted).replace("'",'"')

    print("=== json_str ===")
    print(json_str)
    print()

    # converts the json string to a dictionary object (load the json into the correct types of Python variables, recursively, effectively.
    js = json.loads(json_str)

    print("=== json in python dict ===")
    print(js)
    print()

    # optional easy-to read recursive dict/list (json too?) printing
    print("=== python dict pretty printing ===")
    pprint.pprint(js)

# execute only if called directly (not as a module)
if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--host", dest="host", help="target for connection", required=True)
    parser.add_argument("--user", dest="user", help="username to connect with", required=False)
    args = parser.parse_args()

    #password = getpass.getpass()
    #args.password = password

    # Change ERROR to INFO or DEBUG for more verbosity
    logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

    # run our main program
    main(args)
