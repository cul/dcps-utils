import ASFunctions as asf
import json
from pprint import pprint

asf.setServer('Test')

x = asf.getArchivalObjectByRef(2, 'e58b4ca4a5de9917fa457ab91472b02d')

y = json.loads(x)

tc = y['instances'][0]['sub_container']['top_container']['ref']

print(type(tc))
print(tc)

z = asf.getResponse(tc)

pprint(json.loads(z))

x = asf.getResponse('/repositories/2/resources/5435/top_containers')

pprint(json.loads(x))

quit()

pprint(json.loads(x))

y = asf.getResponse('repositories/2/top_containers/89920')

print(' ')

pprint(json.loads(y))
