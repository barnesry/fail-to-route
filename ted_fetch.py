#!/usr/bin/python
#
# Simple script to collect tcp_inpcb info from SRX device(s) and report results
# in tabular format. Checks for buffer exhaustion and reports TRUE if within 10%
# of limit.
#

from jnpr.junos import Device
from lxml import etree
import argparse, logging, getpass, sys


def main(args):

    host = args.host
    user = args.user
    # no password as we're relying on local ssh keys

    # setup our connection
    dev=Device(host=host, user=user, password=password)
    try:
        dev.open()

        # retrieve TED
        ted = dev.rpc.get_ted_database_information({'format': 'json'})

        print(ted)

    except:
        print "Failed to retreive TED"


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
