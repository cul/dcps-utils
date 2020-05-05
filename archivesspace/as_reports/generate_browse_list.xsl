<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema" xmlns:marc="http://www.loc.gov/MARC21/slim"
    exclude-result-prefixes="xs marc" version="2.0">

    <!-- Stylesheet to output html snippets for the finding aid application. One output file per repo. Set the output folder in param $output_dir. See ACFA-213. -->
    
    <xsl:output method="html" indent="yes"/>

    <!-- provide directory to place output files -->
    <xsl:param name="output_dir"
        >/Users/dwh2128/Documents/ACFA/TEST/ACFA-133-generate-browse-list</xsl:param>




    <xsl:template match="/">

        <!--  For each repo, run template to save an html snippet to location in $output_dir  -->

        <xsl:call-template name="list_records">
            <xsl:with-param name="repo">nnc-ccoh</xsl:with-param>
        </xsl:call-template>

        <xsl:call-template name="list_records">
            <xsl:with-param name="repo">nnc-a</xsl:with-param>
        </xsl:call-template>

        <xsl:call-template name="list_records">
            <xsl:with-param name="repo">nnc-rb</xsl:with-param>
        </xsl:call-template>

        <xsl:call-template name="list_records">
            <xsl:with-param name="repo">nnc-ut</xsl:with-param>
        </xsl:call-template>

        <xsl:call-template name="list_records">
            <xsl:with-param name="repo">nnc-ua</xsl:with-param>
        </xsl:call-template>

        <xsl:call-template name="list_records">
            <xsl:with-param name="repo">nnc-ea</xsl:with-param>
        </xsl:call-template>

    </xsl:template>




    <xsl:template name="list_records">
        <xsl:param name="repo"/>

        <!-- The name of the output file. -->
        <xsl:result-document href="{$output_dir}/{$repo}_fa_list.html" method="html">

            <ul>
                <xsl:for-each
                    select="repository/record/metadata/marc:collection/marc:record[contains( marc:datafield[@tag='856']/marc:subfield[@code='u'], $repo) ]">
                    <!-- sort alphabetically by title string -->
                    <xsl:sort
                        select="marc:datafield[@tag='245']/marc:subfield[@code='a']/lower-case( translate(.,'&quot;',''))"/>

                    <li>
                        <a
                            href="/ead/{$repo}/ldpd_{ marc:datafield[@tag='099']/marc:subfield[@code='a']}">
                            <xsl:apply-templates select="marc:datafield[@tag='245']"/>
                        </a>

                    </li>
                </xsl:for-each>

            </ul>

        </xsl:result-document>
    </xsl:template>

    <!-- Process title and unitdates -->
    <xsl:template match="marc:datafield[@tag='245']">
        <!-- Normalize ampersands to unescaped character.  -->
        <xsl:analyze-string select="marc:subfield[@code='a']" regex="&amp;amp;">
            <xsl:matching-substring>
                <xsl:text>&amp;</xsl:text>
            </xsl:matching-substring>
            <!-- Convert apostrophes to curly single quotes, to avoid terminating yml value.  -->
            <xsl:non-matching-substring>
                <xsl:value-of select='translate(.,"&apos;", "’")'/>
            </xsl:non-matching-substring>
        </xsl:analyze-string>

        <xsl:text> </xsl:text>
        <xsl:value-of select="normalize-space(marc:subfield[@code='f'])"/>
        <xsl:for-each select="marc:subfield[not(@code='a' or @code='f')]">
            <xsl:text> (bulk </xsl:text>
            <xsl:value-of select="."/>
            <xsl:text>)</xsl:text>
        </xsl:for-each>
    </xsl:template>


</xsl:stylesheet>
