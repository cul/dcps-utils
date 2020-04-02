import ASFunctions as asf
import json
from pprint import pprint

asf.setServer('Prod')

x = asf.getArchivalObjectByRef(2, 'a748bf2338f1983514ca0b1c72021c99')

pprint(json.loads(x))
