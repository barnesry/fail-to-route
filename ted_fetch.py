#!/usr/bin/python

from jnpr.junos import Device
from lxml import etree
import argparse, logging, getpass, sys

import json
import pprint

#
# getTed((hostname, username)): returns string in json format (use json.loads(getTed((hostname, username)) to get a Python local dictionary)
#
def getTed(login):

    host = login[0]
    user = login[1]
    # no password as we're relying on local ssh keys

    ted = None

    # setup our connection
    dev=Device(host=host, user=user)
    try:
        dev.open()
        # retrieve TED
        ted = dev.rpc.get_ted_database_information({'format': 'json'})
        #print("=== raw response ===")
        #print(ted)
        #print()
    except Exception as e:
        print ("Failed to retreive TED: {}".format(e))

    # convert ted to valid json string
    json_str = str(ted).replace("'",'"')

    #print("=== json_str ===")
    #print(json_str)
    #print()

    # converts the json string to a dictionary object (load the json into the correct types of Python variables, recursively, effectively.
    #json_dict = json.loads(json_str)

    #print("=== json in python dict ===")
    #print(json_dict)
    #print()

    # optional easy-to read recursive dict/list (json too?) printing
    #print("=== python dict pretty printing ===")
    #pprint.pprint(json_disc)

    return json_str

# execute only if called directly (not as a module)
if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--host", dest="host", help="target for connection", required=True)
    parser.add_argument("--user", dest="user", help="username to connect with", required=False)
    args = parser.parse_args()

    # Change ERROR to INFO or DEBUG for more verbosity
    logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

    # run our main program
    login = (args.host, args.user)

    #getTed(login)

    json_dict = json.loads(getTed(login))

    #print(json_dict)

    # pretty printing of json_dict
    #pprint.pprint(json_dict, indent=2)

    print()

    pprint.pprint(json_dict["ted-database-information"][0]["ted-database"], indent=2)

    #print(len(json_dict["ted-database-information"][0]["ted-database"]))

    print("===")
    for mxl in range(0,len(json_dict["ted-database-information"][0]["ted-database"])):
        print("switch: {}".format(json_dict["ted-database-information"][0]["ted-database"][mxl]["ted-database-id"][0]["data"]))
        for dest in range(0, len(json_dict["ted-database-information"][0]["ted-database"][mxl]["ted-link"])):
            print("\tconnects to: {}".format(json_dict["ted-database-information"][0]["ted-database"][mxl]["ted-link"][dest]["ted-link-to"][0]["data"]))
