# transform.py
import sys
import os
import datetime
import lxml.etree as etree

def main():
	dom = etree.parse("oapen.marc.xml")
	xslt = etree.parse("transform.xsl")
	transform = etree.XSLT(xslt)
	newdom = transform(dom, **{'currentTime' : datetime.datetime.utcnow().strftime("'%Y-%m-%dT%H:%M:%S+00:00'")})
	f = open('oapen.opds.xml', 'wb')
	f.write(etree.tostring(newdom, pretty_print=True))
	f.close()
if __name__ == '__main__':
    main()