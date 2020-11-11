<?xml version="1.0" encoding="UTF-8" ?>
<!-- 
   MARC-XML to EAD Stylesheet (Single Record Conversion)
     Prepared by Terry Catapano, 
     Columbia University Libraries Digital Program
     thc4@columbia.edu
     2007-02-16
--> 
  
<xsl:stylesheet version="2.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:xlink="http://www.w3.org/1999/xlink"
    xpath-default-namespace="http://www.loc.gov/MARC21/slim">

    <xsl:import href="nnc-rb_eadheader.xsl"/>
    <xsl:import href="nnc-a_eadheader.xsl"/>
    <xsl:import href="nnc-m_eadheader.xsl"/>
    <xsl:import href="nnc-ua_eadheader.xsl"/>
    <xsl:import href="nnc-ut_eadheader.xsl"/>
    <xsl:import href="nnc-ea_eadheader.xsl"/>

    <xsl:output indent="yes" method="xml" encoding="utf-8"/>

    <xsl:key name="other_coll_data" match="*[local-name() = 'Sheet1']" use="*[local-name() = 'CLIO']"/>

    <xsl:param name="pdf_path">
        <xsl:text>http://www.columbia.edu/cu/libraries/inside/projects/findingaids/scans/pdfs/</xsl:text>
    </xsl:param>

    <xsl:param name="fa_path">
        <xsl:text>http://www.columbia.edu/cu/lweb/eresources/archives/rbml/</xsl:text>
    </xsl:param>

    <xsl:param name="xmldir">[XMLDIR]</xsl:param>

    <xsl:param name="today">
        <!-- get name of month, two digit day, and year -->
        <xsl:value-of select="format-date(current-date(), '[MNn] [D], [Y]')"/>
        <xsl:text> </xsl:text>
    </xsl:param>

    <xsl:param name="audience">
        <xsl:text>external</xsl:text>
    </xsl:param>

    <xsl:param name="isotoday" select="format-date(current-date(), '[Y]-[M01]-[D01]')"/>

    <xsl:param name="repository"/>

    <xsl:param name="coll_data_file">
        <xsl:choose>
            <xsl:when test="$repository = 'nnc-rb'">
                <xsl:text>RB_collections.xml</xsl:text>
            </xsl:when>
            <xsl:when test="$repository = 'nnc-a'">
                <xsl:text>AV_collections.xml</xsl:text>
            </xsl:when>
            <xsl:when test="$repository = 'nnc-m'">
                <xsl:text>HS_collections.xml</xsl:text>
            </xsl:when>
            <xsl:when test="$repository = 'nnc-ua'">
                <xsl:text>UA_collections.xml</xsl:text>
            </xsl:when>
            <xsl:when test="$repository = 'nnc-ut'">
                <xsl:text>UT_collections.xml</xsl:text>
            </xsl:when>
            <xsl:when test="$repository = 'nnc-oh'">
                <xsl:text>OH_collections.xml</xsl:text>
            </xsl:when>
            <xsl:when test="$repository = 'nnc-ea'">
                <xsl:text>EA_collections.xml</xsl:text>
            </xsl:when>
            <xsl:otherwise>
                <xsl:message>WARNING - REPOSITORY PARAMETER INCORRECT OR MISSING</xsl:message>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:param>

    <xsl:template match="/">
        <xsl:apply-templates select="collection/record"/>
    </xsl:template>

    <xsl:template match="record[substring(child::leader, 8, 1) = 'c']">
        <!--
        <xsl:message><xsl:text>LEADER 7 is: </xsl:text><xsl:value-of select="substring(child::leader, 8, 1)"/></xsl:message> 
-->
        <xsl:variable name="ID" select="child::controlfield[@tag = '001']"/>

        <xsl:variable name="unittitle">
          <!-- <xsl:for-each select="document($coll_data_file)">
                <xsl:value-of select="key('other_coll_data', $ID)//*[local-name() = 'PREFERRED_TITLE']"/>
            </xsl:for-each>
          -->
            <!-- 2010-03-30 removed lookup of preferred title -->
            <xsl:text/>
        </xsl:variable>


        <xsl:variable name="pdf_url">
            <xsl:for-each select="document($coll_data_file)">
                <xsl:value-of select="key('other_coll_data', $ID)//*[local-name() = 'PDF_FINDAID_FILENAME']"/>
            </xsl:for-each>
        </xsl:variable>

        <xsl:variable name="other_fa_url">
            <xsl:variable name="lookup_url">
                <xsl:for-each select="document($coll_data_file)">
                    <xsl:value-of select="key('other_coll_data', $ID)//*[local-name() = 'OTHER_FINDAID_URL']"/>
                </xsl:for-each>
            </xsl:variable>
            <!-- get falink value -->
           <xsl:choose xmlns="urn:isbn:1-931666-22-9" >
                <!-- when subfield u -->
                <xsl:when test="string-length(//datafield[@tag = '555']/subfield[@code = 'u']) &gt; 1">
                    <p>
                        <extref xlink:type="simple" xlink:href="{//datafield[@tag = '555']/subfield[@code = 'u']}">Online finding aid
                        available.</extref>
                    </p>
                </xsl:when>
                <!-- otherwise -->
                <xsl:otherwise>
                    <xsl:choose>
                        <!-- when 856 3 = 'Finding aid'-->
                        <xsl:when
                            test="descendant::datafield[@tag = '856'][starts-with(subfield[@code = '3'], 'Finding aid')]">
                            <xsl:message>
                                <xsl:text>WARNING: Finding Aid link moved from 856 to otherfindaid/555 </xsl:text>
                            </xsl:message>
                            <p>
                                <extref
                                    xlink:type="simple" xlink:href="{descendant::datafield[@tag = '856'][subfield[@code = '3']/text() = 'Finding aid']/subfield[@code = 'u']}"
                                    >Online finding aid available.</extref>
                            </p>
                        </xsl:when>
                        <xsl:otherwise>
                            <xsl:choose>
                                <!-- when $lookup_url &gt; 1 -->
                                <xsl:when test="string-length($lookup_url) &gt; 1">
                                    <xsl:message>
                                        <xsl:text>WARNING: Finding Aid link added from other collection info file</xsl:text>
                                    </xsl:message>
                                    <p>
                                        <extref xlink:type="simple" xlink:href="{$fa_path}{$lookup_url}/">Online finding aid available.</extref>
                                    </p>
                                </xsl:when>
                                <!-- otherwise -->
                                <xsl:otherwise></xsl:otherwise>
                            </xsl:choose>
                        </xsl:otherwise>
                    </xsl:choose>
                </xsl:otherwise>
            </xsl:choose>
        </xsl:variable>

        <xsl:variable name="digital_content">
            <xsl:for-each select="document($coll_data_file)">
                <xsl:value-of select="key('other_coll_data', $ID)//*[local-name() = 'RELATED_RESOURCE_URL']"/>
            </xsl:for-each>
        </xsl:variable>
        <xsl:message>
            <xsl:text>DIGITAL CONTENT: </xsl:text>
            <xsl:value-of select="$digital_content"/>
        </xsl:message>
        
        <xsl:processing-instruction name="oxygen">
          <xsl:text>NVDLSchema="http://eadrepo.cul.columbia.edu:8080/exist/rest/db/ead/</xsl:text><xsl:value-of select="$repository"/><xsl:text>_staging/schema/ead_cul.nvdl" </xsl:text>
          <xsl:text>type="xml"</xsl:text>
        </xsl:processing-instruction>
        <ead audience="{$audience}" xmlns="urn:isbn:1-931666-22-9" xmlns:xlink="http://www.w3.org/1999/xlink">
            <eadheader findaidstatus="unedited" countryencoding="iso3166-1" dateencoding="iso8601" langencoding="iso639-2b" relatedencoding="DC" repositoryencoding="iso15511" scriptencoding="iso15924">
                <eadid countrycode="US" encodinganalog="Identifier"
                    publicid="-//us::{$repository}//TEXT us::{$repository}::ldpd_{$ID}_ead//EN"
                    mainagencycode="{$repository}">ldpd_<xsl:value-of select="$ID"/>_ead.xml</eadid>
                <filedesc>
                    <xsl:choose>
                        <xsl:when test="$repository = 'nnc-rb'">
                            <xsl:call-template name="nnc-rb_eadheader">
                                <xsl:with-param name="unittitle">
                                    <xsl:call-template name="get_unittitle">
                                        <xsl:with-param name="title">
                                            <xsl:value-of select="$unittitle"/>
                                        </xsl:with-param>
                                    </xsl:call-template>
                                </xsl:with-param>
                                <xsl:with-param name="isotoday" select="$isotoday"/>
                                <xsl:with-param name="today" select="$today"/>
                            </xsl:call-template>
                        </xsl:when>
                        <xsl:when test="$repository = 'nnc-a'">
                            <xsl:call-template name="nnc-a_eadheader">
                                <xsl:with-param name="unittitle">
                                    <xsl:call-template name="get_unittitle">
                                        <xsl:with-param name="title">
                                            <xsl:value-of select="$unittitle"/>
                                        </xsl:with-param>
                                    </xsl:call-template>
                                </xsl:with-param>
                                <xsl:with-param name="isotoday" select="$isotoday"/>
                                <xsl:with-param name="today" select="$today"/>
                            </xsl:call-template>
                        </xsl:when>
                        <xsl:when test="$repository = 'nnc-ea'">
                            <xsl:call-template name="nnc-ea_eadheader">
                                <xsl:with-param name="isotoday" select="$isotoday"/>
                                <xsl:with-param name="today" select="$today"/>
                            </xsl:call-template>
                        </xsl:when>
                        <xsl:when test="$repository = 'nnc-m'">
                            <xsl:call-template name="nnc-m_eadheader">
                                <xsl:with-param name="isotoday" select="$isotoday"/>
                                <xsl:with-param name="today" select="$today"/>
                            </xsl:call-template>
                        </xsl:when>
                        <xsl:when test="$repository = 'nnc-ua'">
                            <xsl:call-template name="nnc-ua_eadheader">
                                <xsl:with-param name="isotoday" select="$isotoday"/>
                                <xsl:with-param name="today" select="$today"/>
                            </xsl:call-template>
                        </xsl:when>
                        <xsl:when test="$repository = 'nnc-ut'">
                            <xsl:call-template name="nnc-ut_eadheader">
                                <xsl:with-param name="isotoday" select="$isotoday"/>
                                <xsl:with-param name="today" select="$today"/>
                            </xsl:call-template>
                        </xsl:when>
                    </xsl:choose>
                </filedesc>
                <profiledesc>
                    <creation>Machine readable finding aid generated from MARC-AMC source via XSLT conversion <date
                            normal="{$isotoday}">
                            <xsl:value-of select="$today"/>
                        </date>
                    </creation>
                    <langusage>Finding aid written in <language encodinganalog="Language" scriptcode="Latn"
                            langcode="eng">English.</language>
                    </langusage>
                </profiledesc>
                <revisiondesc>
                    <change>
                        <date normal="{$isotoday}">
                            <xsl:value-of select="$isotoday"/>
                        </date>
                        <item>File created.</item>
                    </change>
                </revisiondesc>
            </eadheader>
            <archdesc level="collection" relatedencoding="MARC21">
                <did>
                    <xsl:choose>
                        <xsl:when test=".//datafield[@tag = '100']">
                            <origination>
                                <persname encodinganalog="100">
                                    <xsl:for-each select=".//datafield[@tag = '100']/subfield[(@code != '0') and (@code != '2')]">
                                        <xsl:call-template name="subelements-inline"/>
                                    </xsl:for-each>
                                </persname>
                            </origination>
                        </xsl:when>
                        <xsl:when test=".//datafield[@tag = '110']">
                            <origination>
                                <corpname encodinganalog="110">
                                    <xsl:for-each select=".//datafield[@tag = '110']/subfield[(@code != '0') and (@code != '2')]">
                                        <xsl:call-template name="subelements-inline"/>
                                    </xsl:for-each>
                                </corpname>
                            </origination>
                        </xsl:when>
                        <xsl:when test=".//datafield[@tag = '111']">
                            <origination>
                                <corpname encodinganalog="111">
                                    <xsl:for-each select=".//datafield[@tag = '111']/subfield[(@code != '0') and (@code != '2')]">
                                        <xsl:call-template name="subelements-inline"/>
                                    </xsl:for-each>
                                </corpname>
                            </origination>
                        </xsl:when>
                        <xsl:when test=".//datafield[@tag = '130']">
                            <origination>
                                <title encodinganalog="130">
                                    <xsl:for-each select=".//datafield[@tag = '130']/subfield[(@code != '0') and (@code != '2')]">
                                        <xsl:call-template name="subelements-inline"/>
                                    </xsl:for-each>
                                </title>
                            </origination>
                        </xsl:when>
                    </xsl:choose>
                    <xsl:element name="unittitle">
                        <xsl:attribute name="encodinganalog">
                            <xsl:text>245$a</xsl:text>
                        </xsl:attribute>
                        <xsl:attribute name="altrender">
                            <xsl:call-template name="get_sort_title">
                                <xsl:with-param name="title">
                                    <xsl:value-of select="$unittitle"/>
                                </xsl:with-param>
                            </xsl:call-template>
                        </xsl:attribute>
                        <xsl:call-template name="get_unittitle">
                            <xsl:with-param name="title">
                                <xsl:value-of select="$unittitle"/>
                            </xsl:with-param>
                        </xsl:call-template>
                    </xsl:element>
                    <!--
                      <xsl:message>
                        <xsl:text>UNITTITLE IS: </xsl:text><xsl:value-of select="$unittitle"/>
                      </xsl:message>
-->

                    <xsl:variable name="bedate">
                        <xsl:value-of select="substring(.//controlfield[@tag = '008'], 8, 4)"/>
                        <xsl:if test="not(contains(substring(.//controlfield[@tag = '008'], 12, 1), ' '))"><xsl:text>/</xsl:text>
                        <xsl:value-of select="substring(.//controlfield[@tag = '008'], 12, 4)"/></xsl:if>
                    </xsl:variable>
                    <unitdate encodinganalog="245$f" normal="{$bedate}" type="inclusive">
                      <xsl:value-of select=".//datafield[@tag = '245']/subfield[@code = 'f']"/>
                    </unitdate>
                    <xsl:for-each select=".//datafield[@tag = '245']/subfield[@code = 'g']">
                        <unitdate encodinganalog="245$g" type="bulk">
                            <xsl:value-of select="."/>
                        </unitdate>
                    </xsl:for-each>
                    <physdesc>
                        <extent encodinganalog="300">
                            <xsl:for-each select=".//datafield[@tag = '300']">
                                <xsl:value-of select="normalize-space(.)"/>
                                <xsl:if test="position() != last()">
                                    <xsl:text>; </xsl:text>
                                </xsl:if>
                            </xsl:for-each>
                        </extent>
                    </physdesc>
                    <repository encodinganalog="852">
                        <xsl:choose>
                            <xsl:when test=".//datafield[@tag = '852']">
                                <corpname>
                                    <xsl:value-of select=".//datafield[@tag = '852']/subfield[@code = 'a']"/>
                                    <subarea>
                                        <xsl:value-of select=".//datafield[@tag = '852']/subfield[@code = 'b']"/>
                                    </subarea>
                                </corpname>
                                <address>
                            <addressline>
                                <xsl:value-of select=".//datafield[@tag = '852']/subfield[@code = 'e']"/>
                            </addressline>
                        </address>
                            </xsl:when>
                            <xsl:otherwise>
                                <xsl:choose>
                                    <xsl:when test="$repository = 'nnc-rb'">
                                        <corpname>Columbia University. <subarea>Rare Book and Manuscript
                                            Library.</subarea>
                                        </corpname>
                                        <address>
                                  <addressline>New York, NY.</addressline> 
                                </address>
                                    </xsl:when>
                                    <xsl:when test="$repository = 'nnc-a'">
                                        <corpname>Columbia University. <subarea>Avery Architecture and Fine Arts
                                                Library. Department of Drawings and Archives.</subarea>
                                        </corpname>
                                        <address>
                                  <addressline>New York, NY.</addressline> 
                                </address>
                                    </xsl:when>
                                    <xsl:when test="$repository = 'nnc-ea'">
                                        <corpname>Columbia University. <subarea>C.V. Starr East Asian Library.</subarea>
                                        </corpname>
                                        <address>
                                  <addressline>New York, NY.</addressline> 
                                </address>
                                    </xsl:when>
                                    <xsl:when test="$repository = 'nnc-m'">
                                        <corpname>Columbia University. <subarea>Health Sciences Library. Archives and
                                                Special Collections.</subarea>
                                        </corpname>
                                        <address>
                                  <addressline>New York, NY.</addressline> 
                                </address>
                                    </xsl:when>
                                    <xsl:when test="$repository = 'nnc-ua'">
                                        <corpname>Columbia University. <subarea>Columbia University Archives.</subarea>
                                        </corpname>
                                        <address>
                                  <addressline>New York, NY.</addressline> 
                                </address>
                                    </xsl:when>
                                    <xsl:when test="$repository = 'nnc-ut'">
                                        <corpname>Columbia University. <subarea>Burke Library Archives.</subarea>
                                        </corpname>
                                        <address>
                                  <addressline>New York, NY.</addressline> 
                                </address>
                                    </xsl:when>
                                    <xsl:otherwise> </xsl:otherwise>
                                </xsl:choose>
                            </xsl:otherwise>
                        </xsl:choose>
                    </repository>
                    <xsl:for-each select=".//datafield[@tag = '090']">
                        <unitid encodinganalog="090$b" countrycode="US" repositorycode="{$repository}" type="call_num">
                          <xsl:value-of select="normalize-space(subfield[@code = 'b'])"/>
                        </unitid>
                    </xsl:for-each>
                    <xsl:for-each select=".//datafield[@tag = '852']">
                        <unitid encodinganalog="090$b" countrycode="US" repositorycode="{$repository}" type="call_num">
                          <xsl:value-of select="normalize-space(subfield[@code = 'j'])"/>
                        </unitid>
                    </xsl:for-each>
                    <unitid encodinganalog="001" countrycode="US" repositorycode="{$repository}" type="clio">
                        <xsl:value-of select="normalize-space(.//controlfield[@tag = '001'])"/>
                    </unitid>
                    <langmaterial encodinganalog="546">
                        <xsl:element name="language">
                            <xsl:attribute name="langcode">
                                <xsl:choose>
                                    <xsl:when test=".//datafield[@tag = '041']">
                                        <xsl:value-of select=".//datafield[@tag = '041']"/>
                                    </xsl:when>
                                    <xsl:otherwise>eng</xsl:otherwise>
                                </xsl:choose>
                            </xsl:attribute>
                            <xsl:choose>
                                <xsl:when test=".//datafield[@tag = '546']">
                                    <xsl:value-of select=".//datafield[@tag = '546']"/>
                                </xsl:when>
                                <xsl:otherwise>In English</xsl:otherwise>
                            </xsl:choose>
                        </xsl:element>
                    </langmaterial>
                </did>

                <bioghist encodinganalog="545">
                    <head>History</head>
                    <xsl:for-each select=".//datafield[@tag = '545']">
                        <p>
                            <xsl:comment> BIOGHIST REQUIRED </xsl:comment>
                            <xsl:call-template name="subelements-inline"/>
                        </p>
                    </xsl:for-each>
                    <p/>
                </bioghist>
                <scopecontent encodinganalog="520">
                    <head>Scope and Content</head>
                    <xsl:for-each select=".//datafield[@tag = '520']">
                        <p>
                            <xsl:call-template name="subelements-inline"/>
                        </p>
                    </xsl:for-each>
                    <p/>
                </scopecontent>
                <xsl:if test=".//datafield[@tag = '351']">
                    <arrangement encodinganalog="351">
                        <head>Arrangement</head>
                        <xsl:for-each select=".//datafield[@tag = '351']">
                            <p>
                                <xsl:call-template name="subelements-inline"/>
                            </p>


                        </xsl:for-each>
                    </arrangement>
                </xsl:if>
                <controlaccess>
                    <head>Subjects</head>
                    <!--For each -->
                    <xsl:for-each select=".//datafield[@tag = '610']">
                        <corpname encodinganalog="610">
                            <xsl:for-each select="child::subfield[(@code != '0') and (@code != '2')]">
                                <xsl:call-template name="subelements-inline"/>
                            </xsl:for-each>
                        </corpname>
                    </xsl:for-each>
                    <xsl:for-each select=".//datafield[@tag = '611']">
                        <corpname encodinganalog="611">
                            <xsl:for-each select="child::subfield[(@code != '0') and (@code != '2')]">
                                <xsl:call-template name="subelements-inline"/>
                            </xsl:for-each>
                        </corpname>
                    </xsl:for-each>
                    <xsl:for-each select=".//datafield[@tag = '710']">
                        <corpname encodinganalog="710">
                            <xsl:for-each select="child::subfield[(@code != '0') and (@code != '2')]">
                                <xsl:call-template name="subelements-inline"/>
                            </xsl:for-each>
                        </corpname>
                    </xsl:for-each>
                    <xsl:for-each select=".//datafield[@tag = '711']">
                        <corpname encodinganalog="711">
                            <xsl:for-each select="child::subfield[(@code != '0') and (@code != '2')]">
                                <xsl:call-template name="subelements-inline"/>
                            </xsl:for-each>
                        </corpname>
                    </xsl:for-each>
                    <xsl:for-each select=".//datafield[@tag = '600']">
                        <persname encodinganalog="600">
                            <xsl:for-each select="child::subfield[(@code != '0') and (@code != '2')]">
                                <xsl:call-template name="subelements-inline"/>
                            </xsl:for-each>
                        </persname>
                    </xsl:for-each>
                    <xsl:for-each select=".//datafield[@tag = '700'] ">
                        <persname encodinganalog="700">
                            <xsl:for-each select="child::subfield[(@code != '0') and (@code != '2')]">
                                <xsl:call-template name="subelements-inline"/>
                            </xsl:for-each>
                        </persname>
                    </xsl:for-each>
                    <xsl:for-each select=".//datafield[@tag = '651']">
                        <xsl:element name="geogname">
                            <xsl:attribute name="encodinganalog">651</xsl:attribute>
                            <xsl:call-template name="source"/>
                            <xsl:for-each select="child::subfield[(@code != '0') and (@code != '2')]">
                                <xsl:call-template name="subelements-inline"/>
                            </xsl:for-each>
                        </xsl:element>
                    </xsl:for-each>
                    <xsl:for-each select=".//datafield[@tag = '650']">
                        <xsl:element name="subject">
                            <xsl:attribute name="encodinganalog">650</xsl:attribute>
                            <xsl:call-template name="source"/>
                            <xsl:for-each select="child::subfield[(@code != '0') and (@code != '2')]">
                                <xsl:call-template name="subelements-inline"/>
                            </xsl:for-each>
                        </xsl:element>
                    </xsl:for-each>
                    <xsl:for-each select=".//datafield[@tag = '655']">
                        <xsl:element name="genreform">
                            <xsl:attribute name="encodinganalog">655</xsl:attribute>
                            <xsl:call-template name="source"/>
                            <xsl:for-each select="child::subfield[(@code != '0') and (@code != '2')]">
                                <xsl:call-template name="subelements-inline"/>
                            </xsl:for-each>
                        </xsl:element>
                    </xsl:for-each>
                    <xsl:for-each select=".//datafield[@tag = '697']">
                        <xsl:element name="corpname">
                            <xsl:attribute name="encodinganalog">697</xsl:attribute>
                            <xsl:call-template name="source"/>
                            <xsl:for-each select="child::subfield[(@code != '0') and (@code != '2')]">
                                <xsl:call-template name="subelements-inline"/>
                            </xsl:for-each>
                        </xsl:element>
                    </xsl:for-each>
                    <xsl:for-each select=".//datafield[@tag = '656']">
                        <xsl:element name="occupation">
                            <xsl:attribute name="encodinganalog">656</xsl:attribute>
                            <xsl:call-template name="source"/>
                            <xsl:for-each select="child::subfield[@code != '2']">
                                <xsl:call-template name="subelements-inline"/>
                            </xsl:for-each>
                        </xsl:element>
                    </xsl:for-each>
                    <xsl:for-each select=".//datafield[@tag = '657']">
                        <function encodinganalog="657">
                            <xsl:call-template name="subelements-foreach"/>
                        </function>
                    </xsl:for-each>
                    <xsl:for-each select=".//datafield[@tag = '630']">
                        <title encodinganalog="630">
                            <xsl:call-template name="subelements-foreach"/>
                        </title>
                    </xsl:for-each>
                    <xsl:for-each select=".//datafield[@tag = '730']">
                        <title encodinganalog="730">
                            <xsl:for-each select="child::subfield">
                                <xsl:call-template name="subelements-inline"/>
                            </xsl:for-each>
                        </title>
                    </xsl:for-each>
                </controlaccess>
                <xsl:if test=".//datafield[@tag = '506']">
                    <accessrestrict encodinganalog="506">
                        <head>Access Restrictions</head>
                        <xsl:for-each select=".//datafield[@tag = '506']">

                            <p>
                                <!-- ACCESSRESTRICT REQUIRED IF APPLICABLE -->
                                <xsl:call-template name="subelements-inline"/>
                            </p>
                        </xsl:for-each>
                    </accessrestrict>
                </xsl:if>
                <xsl:if test=".//datafield[@tag = '541']">
                    <acqinfo encodinganalog="541">
                        <head>Acquisition</head>
                        <xsl:for-each select=".//datafield[@tag = '541']">
                            <p>
                                <xsl:call-template name="subelements-inline"/>
                            </p>
                        </xsl:for-each>
                    </acqinfo>
                </xsl:if>
                <xsl:if test=".//datafield[@tag = '530']">
                    <altformavail encodinganalog="530">
                        <head>Alternate Formats</head>
                        <xsl:for-each select=".//datafield[@tag = '530']">
                            <p>
                                <xsl:call-template name="subelements-inline"/>
                            </p>
                        </xsl:for-each>
                    </altformavail>
                </xsl:if>
                <xsl:if test=".//datafield[@tag = '561']">


                    <custodhist encodinganalog="561">
                        <xsl:for-each select=".//datafield[@tag = '561']">
                            <p>
                                <xsl:call-template name="subelements-inline"/>
                            </p>
                        </xsl:for-each>
                    </custodhist>
                </xsl:if>
                <xsl:choose>
                    <xsl:when test=".//datafield[@tag = '524']">
                        <prefercite encodinganalog="524">
                            <head>Preferred Citation</head>
                            <xsl:for-each select=".//datafield[@tag = '524']">
                                <p>
                                    <xsl:call-template name="subelements-inline"/>
                                </p>
                            </xsl:for-each>
                        </prefercite>
                    </xsl:when>
                    <xsl:otherwise>
                        <prefercite encodinganalog="524">
                            <head>Preferred Citation</head>
                            <p>
                                <xsl:if test="$repository = 'nnc-rb'">[Collection Name]. Rare Book and Manuscript
                                    Library. Columbia University.</xsl:if>
                                <xsl:if test="$repository = 'nnc-les'">[Collection Name]. Herbert H. Lehman Suite
                                    &amp; Papers. Columbia University.</xsl:if>

                            </p>
                        </prefercite>
                    </xsl:otherwise>
                </xsl:choose>
                <xsl:if test=".//datafield[@tag = '583']">
                    <processinfo encodinganalog="583">
                        <head>Processing Information</head>
                        <xsl:for-each select=".//datafield[@tag = '583']">
                            <p>
                                <xsl:call-template name="subelements-inline"/>
                            </p>
                        </xsl:for-each>
                    </processinfo>

                </xsl:if>
                <xsl:if
                    test=".//datafield[@tag = '540'] | .//datafield[@tag ='856']/subfield[@code = '3'][starts-with(., 'For additional')]">


                    <userestrict encodinganalog="540">
                        <head>Restrictions on Use</head>
                        <xsl:for-each select=".//datafield[@tag = '540']">
                            <p>
                                <xsl:call-template name="subelements-inline"/>
                            </p>
                        </xsl:for-each>
                        <xsl:for-each
                            select=".//datafield[@tag ='856'][subfield[@code = '3'][starts-with(., 'For additional')]]">
                            <xsl:message>
                                <xsl:text>WARNING: 856 FIELD MOVED TO USERESTRICT</xsl:text>
                            </xsl:message>
                            <p>
                                <xsl:value-of select="child::subfield[@code = '3']"/>
                                <xsl:text> </xsl:text>
                                <extref xlink:type="simple" xlink:href="{child::subfield[@code = 'u']}"/>
                            </p>
                        </xsl:for-each>
                    </userestrict>
                </xsl:if>
                <xsl:if test=".//datafield[@tag = '544']">

                    <relatedmaterial encodinganalog="544">
                        <head>Related Material</head>
                        <xsl:for-each select=".//datafield[@tag = '544']">
                            <p>
                                <xsl:call-template name="subelements-inline"/>
                            </p>
                        </xsl:for-each>
                    </relatedmaterial>
                </xsl:if>

                <xsl:choose>
                    <xsl:when test=".//datafield[@tag = '555']">
                        <otherfindaid encodinganalog="555">
                            <xsl:for-each select=".//datafield[@tag = '555']">
                                <p>
                                    <xsl:call-template name="subelements-inline"/>
                                </p>
                            </xsl:for-each>
                            <xsl:choose>
                                <xsl:when test="string-length($other_fa_url) &gt; 1">
                                    <xsl:copy-of select="$other_fa_url"/>
                                </xsl:when>
                                <xsl:otherwise>
                                    <xsl:if test="string-length($pdf_url) &gt; 1">
                                        <p>
                                            <extref xlink:type="simple" xlink:href="{$pdf_path}{$pdf_url}">PDF available.</extref>
                                        </p>
                                    </xsl:if>
                                </xsl:otherwise>
                            </xsl:choose>

                        </otherfindaid>
                    </xsl:when>
                    <xsl:otherwise>
                        <xsl:choose>
                            <xsl:when test="string-length($other_fa_url) &gt; 1">
                                <otherfindaid encodinganalog="555">
                                    <xsl:copy-of select="$other_fa_url"/>
                                </otherfindaid>
                            </xsl:when>
                            <xsl:otherwise>
                                <xsl:if test="string-length($pdf_url) &gt; 1">
                                    <otherfindaid encodinganalog="555">
                                        <p>
                                            <extref xlink:type="simple" xlink:href="{$pdf_path}{$pdf_url}">PDF available.</extref>
                                        </p>
                                    </otherfindaid>
                                </xsl:if>
                            </xsl:otherwise>
                        </xsl:choose>
                    </xsl:otherwise>
                </xsl:choose>

                <!-- dao/856 -->
                <xsl:choose>
                    <xsl:when test=".//datafield[@tag = '856']">
                        <xsl:for-each select=".//datafield[@tag = '856']">
                            <xsl:choose>
                                <xsl:when test="starts-with(child::subfield[@code = '3'], 'For additional')"> </xsl:when>
                                <xsl:when test="starts-with(child::subfield[@code = '3'], 'Finding aid')"> </xsl:when>
                                <xsl:otherwise>
                                    <dao encodinganalog="856" xlink:type="simple" xlink:href="{child::subfield[@code = 'u']}">
                                        <daodesc>
                                            <p>
                                                <xsl:value-of select="child::subfield[@code = '3']"/>
                                                <xsl:text> </xsl:text>
                                                <xsl:value-of select="child::subfield[@code = 'z']"/>
                                            </p>
                                        </daodesc>
                                    </dao>
                                </xsl:otherwise>
                            </xsl:choose>
                        </xsl:for-each>
                    </xsl:when>
                    <xsl:otherwise>
                        <xsl:if test="string-length($digital_content) &gt; 1">
                            <dao encodinganalog="856" xlink:type="simple" xlink:href="{$digital_content}">
                                <daodesc>
                                    <p>Digital content available.</p>
                                </daodesc>
                            </dao>
                        </xsl:if>
                    </xsl:otherwise>
                </xsl:choose>
            </archdesc>
        </ead>
    </xsl:template>

    <xsl:template name="subelements-inline">
        <xsl:value-of select="normalize-space(.)"/>
        <xsl:if test="position() != last()">
            <xsl:choose>
                <xsl:when test="ancestor::datafield/@tag = '300'">
                    <xsl:text>; </xsl:text>
                </xsl:when>
                <xsl:when test="starts-with(ancestor::datafield/@tag, '6')">
                    <xsl:choose>
                        <xsl:when
                            test="following-sibling::subfield/@code =  'd' or following-sibling::subfield/@code =  'q'">
                            <xsl:text> </xsl:text>
                        </xsl:when>
                        <xsl:otherwise>
                            <xsl:text>--</xsl:text>
                        </xsl:otherwise>
                    </xsl:choose>
                </xsl:when>
                <xsl:when test="starts-with(ancestor::datafield/@tag, '7')">
                    <xsl:choose>
                        <xsl:when
                            test="following-sibling::subfield/@code =  'd' or following-sibling::subfield/@code =  'q'">
                            <xsl:text> </xsl:text>
                        </xsl:when>
                        <xsl:otherwise>
                            <xsl:text>--</xsl:text>
                        </xsl:otherwise>
                    </xsl:choose>
                </xsl:when>
                <xsl:when test="@code = 'u'">
                    <xsl:text> </xsl:text>
                    <extref xlink:type="simple" xlink:href="{.}"/>
                </xsl:when>
                <xsl:otherwise>
                    <xsl:text> </xsl:text>
                </xsl:otherwise>
            </xsl:choose>
        </xsl:if>
        <xsl:if test="@code = 'u'">
            <xsl:text> </xsl:text>
            <extref xlink:type="simple" xlink:href="{.}"/>
        </xsl:if>
    </xsl:template>

    <xsl:template name="subelements-block">
        <xsl:for-each select="./*"/>
        <p>
            <xsl:value-of select="normalize-space(.)"/>
        </p>
    </xsl:template>

    <xsl:template name="subelements-foreach">
        <xsl:for-each select="child::*">
            <xsl:call-template name="subelements-inline"/>
        </xsl:for-each>
    </xsl:template>

    <xsl:template name="get_unittitle">
        <xsl:param name="title"/>
        <xsl:choose>
            <xsl:when test="string-length($title) &gt; 1">
                <xsl:value-of select="$title"/>
            </xsl:when>
            <xsl:otherwise>
                <xsl:value-of select="descendant::datafield[@tag = '245']/subfield[@code = 'a']"/>
                <xsl:value-of select="descendant::datafield[@tag = '245']/subfield[@code = 'k']"/>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>

    <xsl:template name="get_sort_title">
        <xsl:param name="title"/>
        <xsl:choose>
            <xsl:when test="string-length($title) &gt; 1">
                <xsl:value-of select="$title"/>
            </xsl:when>
            <xsl:otherwise>
                <xsl:variable name="nonSort">
                    <xsl:choose>
                        <!-- test to see if 245 ind2 is a number; if not coerce to zero. -->
                        <xsl:when test="number(descendant::datafield[@tag = '245']/@ind2)">
                            <xsl:value-of select="descendant::datafield[@tag = '245']/@ind2"/>
                        </xsl:when>
                        <xsl:otherwise>0</xsl:otherwise>
                    </xsl:choose>
                </xsl:variable>
                
                <xsl:value-of select="substring(descendant::datafield[@tag = '245']/subfield[@code = 'a'], $nonSort)"/>
                <xsl:value-of select="descendant::datafield[@tag = '245']/subfield[@code = 'k']"/>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
    <xsl:template name="source">
        <xsl:choose>
            <xsl:when test="child::subfield[@code = '2']">
                <xsl:attribute name="source">
                    <xsl:value-of select="child::subfield[@code = '2']"/>
                </xsl:attribute>
            </xsl:when>
            <xsl:otherwise/>
        </xsl:choose>
    </xsl:template>


</xsl:stylesheet>
