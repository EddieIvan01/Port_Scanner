#Made by Eddie_Ivan
#-*-coding:utf-8-*-
import getopt
import socket
import sys
import re
class PortScanner(object):
    def __init__(self,ip,mode):
        if not ip:
            self.usage()
            sys.exit()
        if mode == 'swift':
            self.portlist = [21,23,25,80,110,443,1521,1863,3389,5631,5632,5000]
        elif mode == 'all':
            self.portlist = range(1,65536)
        else:
            self.usage()
            sys.exit()
        self.mode = mode
        self.ip = ip
        self.formt = "|{:<6}|{:<6}|{:<5}|"
        self.lip = []
    def scan(self):
        count = 1.0
        for i in self.portlist:
            try:
                s = socket.socket()
                s.settimeout(0.1)
                host = (self.ip,i)
                s.connect(host)
                self.lip.append(i)
                progress = count*100/len(self.portlist)
                print(self.formt.format(i,"Open",str(round(progress,1))+'%'))
                print('+------+------+-----+')
                s.close()
                count += 1.0
            except KeyboardInterrupt:
                sys.exit()            
            except:
                count += 1.0
        print('[*]Scan over')
    def printua(self):
        if self.mode == 'swift':
            print('[*]Swift Mode Scanner')
            print('')
        else:
            print('[*]General Mode Scanner')
            print('')
        print('+------+------+-----+')
        print("|{:^6}|{:^6}|{:^5}|".format("Port","Status","Per"))
        print('+------+------+-----+')
    @staticmethod
    def usage():
        print('   Port Scanner')
        print('       [-h :host(ip or domain)]')
        print('       [-s :fast mode, only scan general port]')
        print('       [-w :output scan result in txt]')
        print('       E.g. port_scanner -h www.example.com -s')
        print('            port_scanner -h 127.0.0.1 -w')
    def run(self):
        print('\n[*]IP: '+ip)
        self.printua()
        self.scan()
        
def optxt(output):
    if output:
        with open('port_rst.txt','w') as fg:
            fg.writelines('Scan IP:'+ip+'\n')
            for ko in scanner.lip:
                fg.writelines('Port %s Open\n' %ko)    
        
def get_ip(domain):
    try:
        ip = socket.gethostbyname(domain)
        return ip
    except:
        print('[*]Host input error')
        sys.exit()

if __name__ == '__main__':
    ip = ''
    mode = 'all'
    output = False
    try:
        opts,args = getopt.getopt(sys.argv[1:],'h:sw')
        for ao,ou in opts:
            if ao == '-h':
                if re.findall(r'[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}',ou):
                    ip = ou
                else:
                    ip = get_ip(ou)
            elif ao == '-s':
                mode = 'swift'
            elif ao == '-w':
                output = True
    except:
        PortScanner.usage()
        sys.exit()
    scanner = PortScanner(ip,mode)
    scanner.run()  
    optxt(output)