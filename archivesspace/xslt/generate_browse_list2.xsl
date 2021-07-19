<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema" xmlns:marc="http://www.loc.gov/MARC21/slim"
    exclude-result-prefixes="xs marc" version="2.0">

    <!-- Stylesheet to output bibid and title from OAI file, to be composed into html snippets for the finding aid application. Run once per $repo. . -->

    <xsl:output method="text" indent="no"/>

    <!-- Params -->
    <!-- repos: nnc-a | nnc-ea | nnc-rb | nnc-ua | nnc-ut -->
    <xsl:param name="repo">nnc-ea</xsl:param> 

    <!-- Can change these when running if desired. Used by Python script to decode results into structured data. -->
    <xsl:param name="delim1">|</xsl:param>
    <xsl:param name="delim2">¶</xsl:param>


    <xsl:template match="/">

        <xsl:for-each
            select="repository/record[not(header/@status = 'deleted')]/metadata/marc:collection/marc:record[contains(marc:datafield[@tag = '856']/marc:subfield[@code = 'u'], $repo)]">
            <!-- sort alphabetically by title string -->
            <xsl:sort
                select="marc:datafield[@tag = '245']/marc:subfield[@code = 'a']/lower-case(translate(., '&quot;', ''))"/>
            <!-- Return tuples of bibid | title -->
            <xsl:value-of select="marc:datafield[@tag = '099']/marc:subfield[@code = 'a']"/>
            <xsl:value-of select="$delim1"/>
            <xsl:apply-templates select="marc:datafield[@tag = '245']"/>
            <xsl:if test="position() &lt; last()">
                <xsl:value-of select="$delim2"/>
            </xsl:if>

        </xsl:for-each>



    </xsl:template>

    <!-- Process title and unitdates -->
    <xsl:template match="marc:datafield[@tag = '245']">
        <!-- Normalize ampersands to unescaped character.  -->
        <xsl:analyze-string select="marc:subfield[@code = 'a']" regex="&amp;amp;">
            <xsl:matching-substring>
                <xsl:text>&amp;</xsl:text>
            </xsl:matching-substring>
            <!-- Convert apostrophes to curly single quotes, to avoid terminating yml value.  -->
            <xsl:non-matching-substring>
                <xsl:value-of select='translate(., "&apos;", "’")'/>
            </xsl:non-matching-substring>
        </xsl:analyze-string>

        <xsl:text> </xsl:text>
        <xsl:value-of select="normalize-space(marc:subfield[@code = 'f'])"/>
        <xsl:for-each select="marc:subfield[not(@code = 'a' or @code = 'f')]">
            <xsl:text> (bulk </xsl:text>
            <xsl:value-of select="."/>
            <xsl:text>)</xsl:text>
        </xsl:for-each>
    </xsl:template>


</xsl:stylesheet>
