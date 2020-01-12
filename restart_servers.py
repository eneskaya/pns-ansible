import ssl
import os
from base64 import b64encode
from http.client import HTTPSConnection

username = os.environ["HAW_USER"]
password = os.environ["HAW_PASSWORD"]

userpass_string = username + ":" + password
userpass_string = userpass_string.encode()

# Crawl the Container Harbor to get the current containers.
# Only works, when there is just one set of PNS containers.
c = HTTPSConnection("pnskss.informatik.haw-hamburg.de",
                    context=ssl._create_unverified_context())
userAndPass = b64encode(userpass_string).decode("ascii")
headers = {'Authorization': 'Basic %s' % userAndPass,
           'Accept': 'application/json'}

with open('servers') as file:
    content = file.readlines()
    content = [x.strip() for x in content]

    for server in content:
        request_url = '/containers/{}/execution'.format(server)
        print(request_url)
        r = c.request('POST', request_url, headers=headers)
        res = c.getresponse()
        print(res.read())
        c.close()
