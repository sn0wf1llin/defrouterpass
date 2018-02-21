import argparse
import urllib.request as ur

from bs4 import BeautifulSoup


def exec_interactive(raddr):
    """
        Login / Password Pairs will be chosen from default: http://www.phenoelit.org/dpl/dpl.html
    :param raddr:
    :return:
    """
    html_defaults = ur.urlopen("http://www.phenoelit.org/dpl/dpl.html")

    if html_defaults.code != 200:
        print("Smth gone bad. Host [ {http://www.phenoelit.org/dpl/dpl.html} ] is unreachable. \nExiting...\n")

    soup = BeautifulSoup(html_defaults.read(), 'lxml')


    # print(soup)


def exec_from_file(raddr):
    pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('-r', '--router-ip', action='store', dest='raddr', help='Router IP Address')
    parser.add_argument('-i', '--interactive', action='store_true', dest='interactive',
                        help='Interactive Mode (Login / Password Pairs will be taken from site)')
    parser.add_argument('-f', '--file', action='store', dest='file',
                        help='Path-to-file with Login / Password Pairs; \nPair per line:\nLogin Password')

    args = parser.parse_args()

    if args.raddr is None:
        print("Destination Router IP Address can't be empty. Fill it in :)")
        exit()

    if not (args.interactive or args.file):
        print("Interactive or File Mode should be chosen. Correct it and we can go!")
        exit()

    if args.interactive:
        exec_interactive(args.raddr)

    elif args.file:
        exec_from_file(args.raddr)