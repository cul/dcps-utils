import ASFunctions as asf
from pprint import pprint

asf.setServer('Prod')

x = asf.getArchivalObjectByRef('a748bf2338f1983514ca0b1c72021c99')

pprint(x)
