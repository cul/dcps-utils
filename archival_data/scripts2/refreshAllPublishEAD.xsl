<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet 
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform" 
  xmlns:functx="http://www.functx.com" 
  xmlns:exist="http://exist.sourceforge.net/NS/exist" 
  xmlns:xs="http://www.w3.org/2001/XMLSchema" 
  version="2.0">

  <xsl:include href="/ldpd/xml/stylesheets/functx/functx-1.0-doc-2007-01.xsl"/>

  <xsl:output encoding="UTF-8" indent="yes" method="text"/>

  <xsl:param name="xmldir">[XMLDIR]</xsl:param>
  <xsl:param name="intervalDays"><xsl:text>400</xsl:text></xsl:param>
  <xsl:param name="remoteHost" select="'http://eadrepo.cul.columbia.edu:8080/exist/rest/db/ead/'"/>
  <xsl:param name="currentDateTime" select="current-dateTime()"/>

  <xsl:template match="/">
    <xsl:message>fetching EAD modified within <xsl:value-of select="$intervalDays"/> days...</xsl:message>
    <xsl:for-each select="//collection">
      <xsl:variable name="collection" select="."/>
        <xsl:message>checking repository <xsl:value-of select="$collection"/> for updated EAD files...</xsl:message>
      <xsl:variable name="stagingDir">
        <xsl:value-of select="."/><xsl:text>_staging</xsl:text>
      </xsl:variable>
      <xsl:for-each select="document(concat($remoteHost, 'getPerms.xql?coll=', $stagingDir))//doc">
        <xsl:variable name="filename" select="child::name"/>
        <xsl:variable name="lastMod" select="child::lastModified"/>
        <xsl:variable name="duration" select="xs:dateTime($currentDateTime) - xs:dateTime($lastMod)"/>
        <xsl:choose>
          <xsl:when test="days-from-duration($duration) &lt; xs:integer($intervalDays)">
            <xsl:message>...fetching updated EAD file <xsl:value-of select="$filename"/></xsl:message>
            <xsl:result-document method="xml" href="{$xmldir}/{$collection}/{$filename}">
              <xsl:copy-of select="document(concat($remoteHost, $stagingDir, '/', $filename))"/>
            </xsl:result-document>
          </xsl:when>
        </xsl:choose>
      </xsl:for-each>
    </xsl:for-each>
  </xsl:template>
</xsl:stylesheet>

