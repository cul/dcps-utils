<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" 
    xmlns:saxon="http://saxon.sf.net/" 
    xmlns:xlink="http://www.w3.org/1999/xlink" 
    xmlns:xs="http://www.w3.org/2001/XMLSchema" version="2.0">

    <!-- Generate delimited text file of bibid and repository code, as represented in Solr (Archives Portal). 
    Run against itself with directory of solr files as $source_dir param. -->


    <xsl:output method="text" indent="no"/>

    <xsl:param name="source_dir">/Users/dwh2128/Documents/ACFA/TEST/SOLR%20MIGRATION/Output/20200205/solr</xsl:param>

    <xsl:variable name="file_list">
        <file>nnc-a_solr.xml</file>
        <file>nnc-ea_solr.xml</file>
        <file>nnc-m_solr.xml</file>
        <file>nnc-rb_solr.xml</file>
        <file>nnc-ua_solr.xml</file>
        <file>nnc-ut_solr.xml</file>
        <file>nnc-ccoh_solr.xml</file>
    </xsl:variable>

    <xsl:variable name="lf">
        <xsl:text>&#x0A;</xsl:text>
    </xsl:variable>

    <xsl:variable name="delim1">|</xsl:variable>

    <xsl:template match="/">
        <xsl:for-each select="$file_list/file">
            <xsl:call-template name="process_solr">
                <xsl:with-param name="file_path" select="concat($source_dir, '/', .)"/>
            </xsl:call-template>
        </xsl:for-each>

    </xsl:template>


    <xsl:template name="process_solr">
        <xsl:param name="file_path"/>


        <xsl:for-each select="document($file_path)/add/doc">
            <xsl:value-of select="substring-after(field[@name='id'],'ldpd_')"/>
            <xsl:value-of select="$delim1"/>
            <xsl:value-of select="field[@name='repository_code']"/>
            <xsl:value-of select="$lf"/>

        </xsl:for-each>

    </xsl:template>

</xsl:stylesheet>