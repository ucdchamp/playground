"""
A simple password generator, using basic python.
"""

import argparse, random, string


def genpass(args):
    """
    Generate the password!
    """

    match args.no_num:
        case True:
            text= string.ascii_letters
        case False:
            text= string.ascii_letters + string.digits
        case _:
            text= string.ascii_letters + string.digits

    if args.s: text+="".join(args.s)

    passwd = "".join(random.choices(text, k=args.l))
    
    return passwd,text

def proc_args():
    """
    Process the commandline arguments and return them to main()
    """
    
    parser = argparse.ArgumentParser(description="generate a password")
    
    parser.add_argument(
        "-l",
        type=int,
        default=8,
        nargs='?',
        help="password length"
    )

    parser.add_argument(
        "-s",
        type=str,
        nargs='+',
        help="specify atleast one special character to include within password"
    )

    parser.add_argument(
        "-b",
        type=str,
        nargs='+',
        help="specify a basewords for the password"
    )

    parser.add_argument(
        "--no-num",
        action='store_true',
        dest='no_num',
        help="specify if numbers should be included within the password"
    )

    return parser.parse_args()

def main():
    """
    This is the main function where the program's logic resides.
    """
    
    #get cmd line args
    args=proc_args()

    #debug flags
    #print(args.no_num)

    #generate password
    passwd,text=genpass(args)

    #display password
    print(passwd)
    

if __name__ == "__main__":
    main()