#!/usr/bin/env python
import ruamel.yaml
import json
import sys

in_file = sys.argv[1]
out_file = sys.argv[2]

#in_file = 'singleturb.yaml'
#out_file = 'output.json'

yaml = ruamel.yaml.YAML(typ='safe')
with open(in_file) as fpi:
    data = yaml.load(fpi)
with open(out_file, 'w') as fpo:
    json.dump(data, fpo, indent=2)
