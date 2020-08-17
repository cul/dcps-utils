<?xml version="1.0" encoding="UTF-8" ?>
<!-- 
   MARC-XML to OPDS Stylesheet for OAPen MARC-XML (http://oapen.org/content/metadata)
     Columbia University Libraries Digital Program
--> 
  
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mrc="http://www.loc.gov/MARC21/slim" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:bibframe="http://bibframe.org/vocab/" xmlns:fh="http://purl.org/syndication/history/1.0" xmlns="http://www.w3.org/2005/Atom">
  <xsl:output indent="yes" method="html" encoding="utf-8"/>
  <xsl:param name="currentTime" />
  <xsl:template match="/">
    <feed>
      <id>https://ebooks.library.columbia.edu/feeds/oapen/all/</id>
      <title>Columbia University OAPen EBooks (all)</title>
      <updated><xsl:value-of  select="$currentTime"/></updated>
      <link href="https://ebooks.library.columbia.edu/feeds/oapen/all" rel="self"/>
      <fh:complete/>
      <xsl:apply-templates select="mrc:collection/mrc:record/mrc:datafield[@tag='856'][@ind1='4'][@ind2='0']/mrc:subfield[@code='z'][text() = 'Access full text online']/../.." />
    </feed>
  </xsl:template>
  <xsl:template match="mrc:record">
    <entry>
      <id>urn:x-oapen:ebooks-app:item:<xsl:value-of select="mrc:controlfield[ @tag='001']" /></id>
      <xsl:variable name="imagePath"><xsl:call-template name="appletree"><xsl:with-param name="identifier" select="mrc:controlfield[ @tag='001']" /></xsl:call-template></xsl:variable>
      <xsl:variable name="pdfUrl"><xsl:value-of select="mrc:datafield[@tag='856'][@ind1='4'][@ind2='0']/mrc:subfield[@code='z'][text() = 'Access full text online']/../mrc:subfield[@code='u']" /></xsl:variable>
      <xsl:variable name="licenseUri"><xsl:value-of select="mrc:datafield[@tag='856'][@ind1='4'][@ind2='0']/mrc:subfield[@code='z'][text() = 'Creative Commons License']/../mrc:subfield[@code='u']" /></xsl:variable>
      <title><xsl:value-of select="normalize-space(mrc:datafield[@tag='245'][@ind1='1'][@ind2='0'])" /></title>
      <bibframe:distribution bibframe:ProviderName="OAPEN Foundation"/>
      <dcterms:identifier>doi:<xsl:value-of select="normalize-space(mrc:datafield[@tag='024'][@ind1='7']/mrc:subfield[@code='2'][text() = 'doi']/../mrc:subfield[@code='a'])" /></dcterms:identifier>
      <summary type="text"><xsl:value-of select="normalize-space(mrc:datafield[@tag='520'][@ind1=' '][@ind2=' '])" /></summary>
      <updated><xsl:call-template name="expandDate"><xsl:with-param name="date" select="mrc:controlfield[ @tag='005']" /></xsl:call-template></updated>
      <dcterms:language><xsl:value-of select="normalize-space(mrc:datafield[@tag='041'][@ind1='0'][@ind2=' ']/mrc:subfield[@code='a'])" /></dcterms:language>
      <dcterms:issued><xsl:value-of select="mrc:datafield[@tag='260']/mrc:subfield[@code='c']" /></dcterms:issued>
      <dcterms:publisher><xsl:value-of select="mrc:datafield[@tag='260']/mrc:subfield[@code='b']" />, <xsl:value-of select="mrc:datafield[@tag='260']/mrc:subfield[@code='a']" /></dcterms:publisher>
      <rights><xsl:value-of select="$licenseUri" /></rights>
      <xsl:for-each select="mrc:datafield[@tag='100'][@ind1='1']/mrc:subfield[@code='4'][text() = 'aut']/../mrc:subfield[@code='a']">
        <author>
          <name><xsl:value-of select="." /></name>
        </author>
      </xsl:for-each>
      <xsl:element name="link">
        <xsl:attribute name="rel">http://opds-spec.org/acquisition/open-access</xsl:attribute>
        <xsl:attribute name="type">application/pdf</xsl:attribute>
        <xsl:attribute name="href"><xsl:value-of disable-output-escaping="yes" select="$pdfUrl" /></xsl:attribute>
      </xsl:element>
      <xsl:element name="link">
        <xsl:attribute name="rel">http://opds-spec.org/image</xsl:attribute>
        <xsl:attribute name="type">image/jpeg</xsl:attribute>
        <xsl:attribute name="href">
          <xsl:text>http://www.oapen.org/cover</xsl:text><xsl:value-of select="$imagePath"/><xsl:text>_cover.jpg</xsl:text>
        </xsl:attribute>
      </xsl:element>
      <xsl:element name="link">
        <xsl:attribute name="rel">http://opds-spec.org/image/thumbnail</xsl:attribute>
        <xsl:attribute name="type">image/jpeg</xsl:attribute>
        <xsl:attribute name="href">
          <xsl:text>http://www.oapen.org/cover</xsl:text><xsl:value-of select="$imagePath"/><xsl:text>_cover-medium.jpg</xsl:text>
        </xsl:attribute>
      </xsl:element>
      <xsl:for-each select="mrc:datafield[@tag='653']/mrc:subfield[@code='a']">
        <xsl:element name="category">
          <xsl:attribute name="label"><xsl:value-of select="." /></xsl:attribute>
        </xsl:element>
      </xsl:for-each>
  </entry>
  </xsl:template>
  <xsl:template name="appletree"><xsl:param name="identifier"/>/<xsl:value-of select="substring($identifier,string-length($identifier) - 2, 1)"/>/<xsl:value-of select="substring($identifier,string-length($identifier) - 1, 1)"/>/<xsl:value-of select="substring($identifier,string-length($identifier), 1)"/>/<xsl:value-of select="$identifier"/>/<xsl:value-of select="$identifier"/>
  </xsl:template>
  <xsl:template name="expandDate">
    <xsl:param name="date" />
    <xsl:value-of select="substring($date,1,4)" />-<xsl:value-of select="substring($date,5,2)" />-<xsl:value-of select="substring($date,7,2)" />T00:00:00+00:00</xsl:template>
</xsl:stylesheet>