import argparse
import urllib.request as ur
import os
from subprocess import Popen, PIPE
import re

from bs4 import BeautifulSoup

DEFPASSHOST = "http://www.phenoelit.org/dpl/dpl.html"
VENDORHOST = 'http://api.macvendors.com/'


def is_alive(raddr):
    HOST_UP = True if os.system("ping -c 1 " + raddr) is 0 else False

    return HOST_UP


def get_vendor(raddr):
    Popen(["ping", "-c 1", raddr], stdout=PIPE)
    pid = Popen(["arp", "-n", raddr], stdout=PIPE)
    s = pid.communicate()[0].decode('utf-8')

    MAC = re.search(r"(([a-f\d]{1,2}\:){5}[a-f\d]{1,2})", s).groups()[0]

    vendor = ur.urlopen(VENDORHOST + MAC).read().decode("utf-8")

    print('MAC \t{} \tvendor \t{}'.format(MAC, vendor))

    return vendor


def exec_interactive(raddr):
    """
        Login / Password Pairs will be chosen from default: http://www.phenoelit.org/dpl/dpl.html
    :param raddr:
    :return:
    """

    if not is_alive(raddr):
        print('{} is unreachable.\nExiting...\n'.format(raddr))
        exit()

    print('IP {} ...'.format(raddr))
    vendor = get_vendor(raddr)

    get_pass_table()


def get_pass_table(url=DEFPASSHOST):
    html_defaults = ur.urlopen(url)

    if html_defaults.code != 200:
        print("Smth gone bad. Host [ {} ] is unreachable. \nExiting...\n".format(url))

    soup = BeautifulSoup(html_defaults.read(), 'lxml')
    table = soup.find('table')
    table_body = table.find('tbody')

    columns = []
    for i, tr_tag in enumerate(table_body.find_all('tr')):
        print([i for i in tr_tag.text.split('\n') if len(i) != 0])
        exit()
        if i == 0:
            columns.extend(tr_tag.text)



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
