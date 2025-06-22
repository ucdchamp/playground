"""
Example on how to store credentials in the keyring

Requirements:
apt-get update && apt-get install -y python3-keyring gnome-keyring dbus-x11
to start a dbus session execute dbus-launch --sh-syntax

Tested on ubuntu 24.04 container
"""

import keyring, secretstorage, argparse
from keyring.backends import SecretService


SVC='rrr'
USER='rrrr'
PASSWD='rrrr'

class kr:

    def __init__(self,**kwargs):
        self.svc=kwargs['service']
        self.user=kwargs['user']
        self.passwd=kwargs['password']

    def store(self):
        try:
            #see if entry exists in keyring already
            lookup=self.__lookup()
            if lookup is None:
                #set the password in keyring
                self.__setpasswd()
            else:
                print(f"Retrieved password: {lookup}")
        except Exception as e:
            print(f"Error: {e}")

    def __lookup(self):
        password = keyring.get_password(self.svc, self.user)
        return password
    
    def __setpasswd(self):
        keyring.set_password(self.svc, self.user, self.passwd)
        print("Password set.")

    def get_kritems(self):
        #connect to the default keyring
        bus = secretstorage.dbus_init()
        collection = secretstorage.get_default_collection(bus)
        
        keys = collection.get_all_items()

        for i in keys:
            attrs = i.get_attributes()
            print(f'service: {attrs['service']} user: {attrs['username']}')


def proc_args():
    """
    Process the cmd-line arguments and return them to main()
    """
    
    parser = argparse.ArgumentParser(description="keyring management cmd-line tool")
    
    parser.add_argument(
        "-l", "--list",
        action="store_true",
        help="List all keyring items"
    )

    parser.add_argument(
        "-p", "--pwd",
        type=str,
        nargs='?',
        help="specify password"
    )

    parser.add_argument(
        "-u", "--user",
        type=str,
        nargs='?',
        help="specify a user"
    )

    parser.add_argument(
        "-s","--svc",
        type=str,
        nargs='?',
        help="specify a service"
    )


    return parser.parse_args()

def main():
    
    #get cmd line args
    args=proc_args()

    if args:
        #set the keyring backend that the keyring module will use for storing and retrieving secrets.
        keyring.set_keyring(SecretService.Keyring())

        new_kr = kr(service=args.svc,user=args.user,password=args.pwd)

        #store password in keyring
        new_kr.store()

        if args.list:
            #display all items in keyring
            new_kr.get_kritems()

if __name__ == "__main__":
    main()