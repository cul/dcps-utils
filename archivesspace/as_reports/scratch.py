import ASFunctions as asf
import json
from pprint import pprint

asf.setServer('Prod')

x = asf.getArchivalObjectByRef(2, 'a748bf2338f1983514ca0b1c72021c99')

y = json.loads(x)

tc = y['instances'][0]['sub_container']['top_container']

print(type(tc))
print(tc)

quit()

pprint(json.loads(x))

y = asf.getResponse('repositories/2/top_containers/89920')

print(' ')

pprint(json.loads(y))
