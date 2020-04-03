import ASFunctions as asf
import json
from pprint import pprint

asf.setServer('Test')

# x = asf.getArchivalObjectByRef(2, 'e58b4ca4a5de9917fa457ab91472b02d')

# y = json.loads(x)

# tc = y['instances'][0]['sub_container']['top_container']['ref']

# print(type(tc))
# print(tc)

# z = asf.getResponse(tc)

# pprint(json.loads(z))

repo = 2
asid = 5102

the_query = '/repositories/' + \
    str(repo) + '/resources/' + str(asid) + '/top_containers'

# list of top containers
the_refs = json.loads(asf.getResponse(the_query))


for r in the_refs:
    tc = json.loads(asf.getResponse(r['ref']))
    # print(tc)

    try:
        bibid = tc['collections'][0]['identifier']
    except:
        bibid = ''
    try:
        uri = tc['uri']
    except:
        uri = ''
    try:
        type = tc['type']
    except:
        type = ''
    try:
        display_string = tc['display_string']
    except:
        display_string = ''

    a_row = [bibid, uri, type, display_string]
    print(a_row)



quit()

pprint(json.loads(x))

y = asf.getResponse('repositories/2/top_containers/89920')

print(' ')

pprint(json.loads(y))
