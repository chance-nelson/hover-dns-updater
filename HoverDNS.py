"""
Desc: Simple DNS updater for hover domains

Authors:
    -Chance Nelson <chance-nelson@nau.edu>
"""


import sys
import requests


class HoverDNS:
    def __init__(self, username, password, dns_id):
        self.dns_id   = dns_id
        self.__cookie = self.__login(username, password)

    
    def __login(self, username, password):
        login = requests.post('https://www.hover.com/api/login', json={'username': username, 'password': password})
 
        if login.status_code != 200:
            return None
       
        else:
            return login.cookies


    def updateDNS(self, ip=None):
        if not ip:
            ip = requests.get('https://api.ipify.org?format=text').text
        
        update = requests.put('https://www.hover.com/api/dns/' + self.dns_id, {'content': ip}, cookies=self.__cookie)

        return update


def main():
    if '-h' in sys.argv or '--help' in sys.argv:
        helpstr = 'Usage: ' + sys.argv[0] + ' <username> <password> <dnsid>'
        helpstr += '<args> \n'
        helpstr += 'Update a hover DNS record\'s IP address\n'
        helpstr += '-h, --help   print this help string\n'
        helpstr += '--ip         manually set an ip'
        print(helpstr)
        return

    IP = None
    if '--ip' in sys.argv:
        IP = sys.argv[sys.argv.index('--ip') + 1]

    hover = HoverDNS(sys.argv[1], sys.argv[2], sys.argv[3])
    resp  = hover.updateDNS(IP)

    if resp.status_code != 200:
        print("Error:", resp.text)


if __name__ == '__main__':
    main()
