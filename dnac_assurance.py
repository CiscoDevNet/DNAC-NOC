#!/usr/bin/env python
from __future__ import print_function
import time
import json
import requests
# turn off warninggs
requests.packages.urllib3.disable_warnings()
from dnac_config import DNAC, DNAC_USER, DNAC_PASSWORD

from dnacentersdk import api

dnac = api.DNACenterAPI(base_url='https://{}:443'.format(DNAC),
                                username=DNAC_USER,password=DNAC_PASSWORD,verify=False)

network_health= dnac.networks.get_overall_network_health(timestamp='')
#print (json.dumps(network_health,indent=2))

timestamp = int(time.time() * 1000)
client_health= dnac.clients.get_overall_client_health(timestamp='{}'.format(timestamp))
#print(json.dumps(client_health,indent=2))

result={}
for score in network_health.response:
    result["totalscore"] = score.healthScore
    result["totalcount"] = score.totalCount
for health in network_health.healthDistirubution:
    result[health.category+".score"] = health.healthScore
    result[health.category + ".count"] = health.count
for score in client_health.response[0].scoreDetail:
    result[score.scoreCategory.value+"-client.value"] = value=score.scoreValue
    result[score.scoreCategory.value+"-client.count"]= score.clientCount

print(json.dumps(result))