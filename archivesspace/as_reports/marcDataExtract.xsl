<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema" xmlns:marc="http://www.loc.gov/MARC21/slim"
    exclude-result-prefixes="xs marc" version="2.0">
    <!-- Run this against a full OAI harvest -->

    <xsl:output indent="no" method="text"/>

    <!--  This is where the column heads are drawn from. Should match process below.   -->
<!--    TODO: FIX-->
    <xsl:variable name="myHead">BIBID|REPO|CALLNO|TITLE|CREATOR|REPO_ID|RESOURCE_ID|MODIFIED|FA_LINK</xsl:variable>

    <xsl:variable name="lf">
        <xsl:text>
</xsl:text>
    </xsl:variable>

    <xsl:variable name="delim1">|</xsl:variable>


    <xsl:template match="/">
        <xsl:value-of select="$myHead"/>
        <xsl:value-of select="$lf"/>

        <xsl:apply-templates select="repository/record[contains(header/identifier, '/resources/')]"
        />
    </xsl:template>
    
    


    <xsl:template match="record">
        <!-- BIBID       -->
        <xsl:value-of
            select="metadata/marc:collection/marc:record/marc:datafield[@tag='099']/marc:subfield[@code='a']"/>
        
        <xsl:value-of select="$delim1"/>
        <!-- REPO       -->
        <xsl:apply-templates
            select="metadata/marc:collection/marc:record/marc:datafield[@tag='040']/marc:subfield[@code='a']"/>

        <xsl:value-of select="$delim1"/>

        <!-- CALL NO       -->
        <xsl:value-of
            select="metadata/marc:collection/marc:record/marc:datafield[@tag='852']/marc:subfield[@code='j']"/>
        
        <xsl:value-of select="$delim1"/>
        
        <!-- TITLE       -->
        <xsl:for-each select="metadata/marc:collection/marc:record/marc:datafield[@tag='245']/marc:subfield">
            <xsl:value-of select="."/>
            <xsl:text> </xsl:text>
        </xsl:for-each>
        
        <xsl:value-of select="$delim1"/>



        <!-- CREATOR       -->
        <xsl:value-of select="metadata/marc:collection/marc:record/marc:datafield[@tag='100']/marc:subfield[@code='a']"/>
            <xsl:text> </xsl:text>
        <xsl:value-of select="metadata/marc:collection/marc:record/marc:datafield[@tag='100']/marc:subfield[@code='q']"/>    
        <xsl:text> </xsl:text>
        <xsl:value-of select="metadata/marc:collection/marc:record/marc:datafield[@tag='100']/marc:subfield[@code='d']"/>
        
            
        <xsl:value-of select="$delim1"/>
        
        
        
        <!-- AS IDentifiers -->
            <xsl:analyze-string select="header/identifier" regex="^.*repositories/(.*)/resources/(.*)$">
                <xsl:matching-substring>
                    <!-- repo id -->
                    <xsl:value-of select="regex-group(1)"/>
                    <xsl:value-of select="$delim1"/>
                    
                    <!-- asid -->
                    <xsl:value-of select="regex-group(2)"/>
                </xsl:matching-substring>
            </xsl:analyze-string>
            <xsl:value-of select="$delim1"/>
           
            
        
       

        <!-- MODIFIED DATE       -->
        <xsl:value-of
            select="header/datestamp"/>
        
        <xsl:value-of select="$delim1"/>
        

        <!-- FA LINK       -->
        
        <xsl:value-of
            select="metadata/marc:collection/marc:record/marc:datafield[@tag='856']/marc:subfield[@code='u']"/>
        
        
        <xsl:value-of select="$lf"/>
        

    </xsl:template>


    <xsl:template match="marc:datafield[@tag='040']/marc:subfield[@code='a']">
        <xsl:choose>
            <xsl:when test="../../marc:datafield[@tag='035']/marc:subfield[@code='a'][contains(.,'NNC-UA')]">
                <xsl:text>nnc-ua</xsl:text>
            </xsl:when>
            <xsl:when test="text()='NNC-AV'">
                <xsl:text>nnc-a</xsl:text>
            </xsl:when>
            <xsl:otherwise>
                <xsl:value-of select="lower-case(.)"/>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>

</xsl:stylesheet>
