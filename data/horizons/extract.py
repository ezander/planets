#!/usr/bin/env python

import json
import sys

import subprocess
p = subprocess.Popen(['./hor-extract'], 
                     stdout=subprocess.PIPE, 
                     stderr=subprocess.PIPE)
out, err = p.communicate()

data = json.loads(out)
#print json.dumps(data, indent=2)
fp=open("../../src/solarsys_dyndata.json", "w")
json.dump(data, fp, indent=2)



