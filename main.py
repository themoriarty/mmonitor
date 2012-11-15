import pycurl
from StringIO import StringIO as SIO

from ofxparse import OfxParser
import config

def post(url, data, headers):
    c = pycurl.Curl()
    c.setopt(pycurl.URL, url)
    real_headers = {"Expect": ""}
    real_headers.update(headers)
    c.setopt(pycurl.HTTPHEADER, [": ".join(x) for x in real_headers.items()])
    c.setopt(pycurl.CONNECTTIMEOUT, 5)
    c.setopt(pycurl.TIMEOUT, 30)
    c.setopt(pycurl.POSTFIELDS, data)
    c.setopt(pycurl.FAILONERROR, True)
    b = SIO()
    c.setopt(pycurl.WRITEFUNCTION, b.write)
    c.perform()
    b.seek(0)
    return b

def main():
    balances = {}
    for request in config.requests:
        data = open(request["file"]).read() % request
        response_data = post(request["url"], data, { "Content-type": "application/x-ofx",
                                                     "Accept": "*/*, application/x-ofx"
                                                     })
        response = OfxParser.parse(response_data)
        groups = dict([(request[k], v) for k, v in request.get("groups", {}).items()])
        for account in response.accounts:
            group = groups.get(account.number, "")
            balances[group] = balances.get(group, 0) + account.statement.balance
        #balances.append(sum([float(x.statement.balance) for x in response.accounts]))
        #for label, k in request.get("special", {}).items():
        #    balance = [a.statement.balance for a in response.accounts if a.number == request[k]]
        #    if balance:
        #        specials.append("%s: %d" % (label, balance[0]))
#         positive_accounts = set([request[x.strip()] for x in request.get("positive", "").split(", ") if x.strip()])
#         positive = sum([float(x.statement.balance) for x in response.accounts if x.number in positive_accounts])
#         negative = sum([float(x.statement.balance) for x in response.accounts if x.number not in positive_accounts])
#         print positive, negative
        #print [x.statement for x in response.accounts]
        #ch, zch, s, c = [a.statement.balance for a in response.accounts]
        #balance = ch + c
        #print "%d %d %dk" % (balance, zch, s / 1000)
        #print "%d %d" % (balance, zch)
    print "%d %s" % (balances[""] - 10000, ", ".join(["%s: %d" % (k, v) for k, v in balances.items() if k]))
if __name__ == "__main__":
    main()
