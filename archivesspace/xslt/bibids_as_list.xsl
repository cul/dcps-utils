<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema" xmlns:marc="http://www.loc.gov/MARC21/slim"
    exclude-result-prefixes="xs marc" version="2.0">
    <!--  this stylesheet will take OAI marc records from the Columbia University Libraries ArchivesSpace instance and clean them up for Voyager import.  -->

    <xsl:output indent="no" method="text"/>



    <xsl:template match="/">


        <xsl:for-each
            select="repository/record[contains(header/identifier, '/resources/')][not(header/@status = 'deleted')]">

            <xsl:value-of
                select="metadata/marc:collection/marc:record/marc:datafield[@tag = '099']/marc:subfield[@code = 'a']"/>


            <xsl:if test="position() &lt; last()">
                <xsl:text>,</xsl:text>


            </xsl:if>
        </xsl:for-each>

    </xsl:template>





</xsl:stylesheet>
