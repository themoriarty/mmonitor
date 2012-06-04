import urllib2
from ofxparse import OfxParser
import config

def main():
    data = open("request").read() % (config.username, config.passwd, config.ch1, config.zch, config.s, config.c)
    request = urllib2.Request("https://ofx.firsttechfed.com", data,
                                  { "Content-type": "application/x-ofx",
                                    "Accept": "*/*, application/x-ofx"
                                  })
    response = OfxParser.parse(urllib2.urlopen(request))
    ch, zch, s, c = [a.statement.balance for a in response.accounts]
    balance = ch + c
    print "%d %d %dk" % (balance, zch, s / 1000)

if __name__ == "__main__":
    main()
