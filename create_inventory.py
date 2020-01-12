from string import Template
from base64 import b64encode
from http.client import HTTPSConnection

import os
import re
import ssl
import json
import ipaddress

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
c.request('GET', '/containers', headers=headers)
res = c.getresponse()
data = res.read()

json_data = json.loads(data)

template_file = open('inventory.template', 'r')
src = Template(template_file.read())

# Save the information in a dict to generate the inventory template for ansible
result_dict = {}

for container in json_data['containers']:
    service_networks = container['details']['NetworkSettings']['Networks']
    service = container['details']['Config']['Labels']['com.docker.compose.service']
    result_dict[service +
                '_hostname_id'] = container['details']['Config']['Hostname']
    key_first = list(service_networks.keys())[0]
    # Save the network of this service
    network_name = container['details']['HostConfig']['NetworkMode'].split('_')[
        1]
    result_dict[network_name + '_iprange'] = str(ipaddress.ip_network(
        service_networks[key_first]['IPAddress']+'/24', strict=False))
    # Save the ip address of this service
    result_dict[service +
                '_ip'] = container['details']['NetworkSettings']['Networks'][key_first]['IPAddress']
    if service == 'fwintern':
        for net in list(service_networks.keys()):
            name = net.split('_')[1]
            result_dict['fwintern_' + name +
                        '_ip'] = service_networks[net]['IPAddress']
    elif service == 'fwworld':
        for net in list(service_networks.keys()):
            name = net.split('_')[1]
            result_dict['fwworld_' + name +
                        '_ip'] = service_networks[net]['IPAddress']

file = open('inventory', 'w')
file.write(src.substitute(result_dict))
file.close()

print('Created inventory file...')

template_file = open('PNS1Draw.io.template.xml', 'r')
file = open('PNS1Draw.io.xml', 'w')
file.write(Template(template_file.read()).substitute(result_dict))
file.close()

# print("Created draw.io XML Template...")

file = open('servers', 'w')
for e in list(result_dict.keys()):
    if '_hostname_id' in e:
        file.write(result_dict[e] + '\n')
