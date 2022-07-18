<?xml version="1.0" encoding="UTF-8"?>
<!-- Stylesheet to extract idenifying information from an ArchivesSpace OAI delta file. -->
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema" exclude-result-prefixes="xs" version="2.0">

    <xsl:output method="text" indent="no"/>

    <!--  
    <xsl:param name="filename">[PLACEHOLDER: PASS NAME OF INPUT FILE AS PARAMETER filename=...]</xsl:param>
-->
    <xsl:param name="filename"
        >/Users/dwh2128/Documents/ACFA/OAI_local/20200330/20200330.asClean.xml</xsl:param>


    <xsl:variable name="cnt_updated" select="count(collection/record)"/>

    <xsl:variable name="delim">,</xsl:variable>
    <xsl:variable name="lf">
        <xsl:text>
</xsl:text>
    </xsl:variable>


    <xsl:template match="/">

        <xsl:message>Processing records in <xsl:value-of select="$filename"/> on <xsl:value-of
                select="current-dateTime()"/>. </xsl:message>



        <xsl:message>Updated records: <xsl:value-of select="$cnt_updated"/>
        </xsl:message>


        <xsl:if test="$cnt_updated > 0">


            <xsl:message> </xsl:message>

            <xsl:message>UPDATED RECORDS:</xsl:message>

            <xsl:message> --------------- </xsl:message>

        </xsl:if>

        <!-- The part that goes to the updated file list for the Rails app. -->


        <xsl:for-each select="collection/record">
            <!-- only if there is a BIBID in 099 (exclude RBMLBOOKS) -->
            <xsl:if test="normalize-space(datafield[@tag = '099']/subfield[@code = 'a'])">

                <!-- BibID -->
                <xsl:value-of select="datafield[@tag = '099']/subfield[@code = 'a']"/>

                <xsl:value-of select="$delim"/>

                <!-- Repo Code -->
                <xsl:value-of select="lower-case(datafield[@tag = '049']/subfield[@code = 'a'])"/>

                <xsl:value-of select="$lf"/>

                <!-- Output for log/notifications -->


                <xsl:message>Title: <xsl:value-of
                        select="datafield[@tag = '245']/subfield[@code = 'a']"/>
                </xsl:message>
                <!--               
                <xsl:message>Identifier: <xsl:value-of select="header/identifier"/></xsl:message>
                <xsl:message>Datestamp: <xsl:value-of select="header/datestamp"/></xsl:message>             
 -->
                <xsl:message>BibID: <xsl:value-of
                        select="datafield[@tag = '099']/subfield[@code = 'a']"/></xsl:message>
                <xsl:if test="normalize-space(datafield[@tag = '856']/subfield[@code = 'u'])">
                    <xsl:message>Finding aid: <xsl:value-of
                            select="datafield[@tag = '856']/subfield[@code = 'u']"/>
                    </xsl:message>
                </xsl:if>

                <xsl:message> --------------- </xsl:message>
            </xsl:if>
        </xsl:for-each>

    </xsl:template>




</xsl:stylesheet>
