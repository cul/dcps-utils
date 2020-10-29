<?xml version="1.0" encoding="UTF-8"?>
<xsl:transform
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
  xmlns:xd="http://www.oxygenxml.com/ns/doc/xsl"
  xmlns:xs="http://www.w3.org/2001/XMLSchema"
  xmlns:saxon="http://saxon.sf.net/"
  xmlns="urn:isbn:1-931666-22-9"
  xpath-default-namespace="urn:isbn:1-931666-22-9" 
  exclude-result-prefixes="xd" 
  version="2.0">

  <xd:doc scope="stylesheet">
    <xd:desc>
      <xd:p><xd:b>Created on:</xd:b> Oct 23, 2010</xd:p>
      <xd:p><xd:b>Author:</xd:b> thc4</xd:p>
      <xd:p>Extract information from EAD instances to create SOLR index XML</xd:p>
    </xd:desc>
  </xd:doc>

  <xsl:output indent="yes" encoding="UTF-8" method="xml" exclude-result-prefixes="#all"/>

  <xsl:param name="xmldir">[XMLDIR]</xsl:param>

  <xd:doc>
    <xd:desc>
      <xd:p>Process each EAD file in $XMLDIR</xd:p>
    </xd:desc>
  </xd:doc>

  <xsl:template match="/">
    <add>
      <xsl:for-each select="for $x in collection( concat('file://', $xmldir, '?recurse=yes;?select=*ead.xml') ) return saxon:discard-document($x)">
        <xsl:sort select="normalize-space(substring-before(ead//eadid, '.'))"/>
        <xsl:call-template name="processCollection"/>
      </xsl:for-each>
    </add>
  </xsl:template>

  <xd:doc>
    <xd:desc>
      <xd:p>Create SOLR doc element for each EAD file at collection level 
        <xd:ul>
<xd:li><xd:b>id</xd:b>: a unique identifier for this record</xd:li>
<xd:li><xd:b>collection_id</xd:b>: identifer of the parent collection of the component the current record describes</xd:li>
<xd:li><xd:b>ead</xd:b>: "yes" or "no"; indicates whether the data in the current record derives from a full EAD instance</xd:li>
<xd:li><xd:b>filename</xd:b>: if applicable, filename of EAD file</xd:li>
<xd:li><xd:b>level</xd:b>: the level of the archival component described</xd:li>
<xd:li><xd:b>repository_code</xd:b>: the identifier of the repository holding the described materials</xd:li>
<xd:li><xd:b>level1</xd:b>: null</xd:li>
<xd:li><xd:b>level2</xd:b>: null</xd:li>
<xd:li><xd:b>pageName</xd:b>: the URL of the collection page of the </xd:li>
<xd:li><xd:b>audience</xd:b>: currently n/a</xd:li>
<xd:li><xd:b>collectionTitle</xd:b>: the title of the collection as a string</xd:li>
<xd:li><xd:b>collectionTitle_1st</xd:b>: the first letter of the title of the collection</xd:li>
<xd:li><xd:b>unittitle</xd:b>: the title of the archival component described by the current record</xd:li>
<xd:li><xd:b>sort_title</xd:b>: the title of the archival component described by the current record, with initial articles removed</xd:li>
<xd:li><xd:b>origination</xd:b>: the creator of the archival component described by the current record (taken from the first origination element only)</xd:li>
<xd:li><xd:b>origination_1st</xd:b>: the first letter of the name of the creator of the archival component described by the current record (taken from the first origination element only)</xd:li>
<xd:li><xd:b>unitid</xd:b>: <xd:i>repeatable</xd:i> the cataloger-assigned identifier(s) of the archival component described by the current record</xd:li>
<xd:li><xd:b>unitdate</xd:b>: the dates associated with the creation of the archival component described by the current record, in text form</xd:li>
<xd:li><xd:b>beginDate</xd:b>: the earliest date associated with the creation of the archival component described by the current record, in ISO 8601 form</xd:li>
<xd:li><xd:b>endDate</xd:b>: the latest date associated with the creation of the archival component described by the current record, in ISO 8601 form</xd:li>
<xd:li><xd:b>subject</xd:b>:<xd:i>repeatable</xd:i> subject heading describing the content of archival component described by the current record</xd:li>
<xd:li><xd:b>corpname</xd:b>:<xd:i>repeatable</xd:i> corporate name heading an entity associated with the content of archival component described by the current record</xd:li>
<xd:li><xd:b>persname</xd:b>:<xd:i>repeatable</xd:i> personal name heading of an entity associated with the content of archival component described by the current record</xd:li>
<xd:li><xd:b>genreform</xd:b>:<xd:i>repeatable</xd:i> genre or format of the content or materials of archival component described by the current record</xd:li>
<xd:li><xd:b>title</xd:b>:<xd:i>repeatable</xd:i> title heading for a work associated with the content of archival component described by the current record</xd:li>
<xd:li><xd:b>physdesc</xd:b>: statements describing the extent, form, or other physical facets of the archival component described by the current record</xd:li>
<xd:li><xd:b>bioghist</xd:b>: historical or biographical note describing the creator of the content of archival component described by the current record</xd:li>
<xd:li><xd:b>scopecontent</xd:b>: note note describing the scope and contents of the archival component described by the current record</xd:li>
<xd:li><xd:b>digcontent</xd:b>: currently empty</xd:li>
<xd:li><xd:b>component text</xd:b>: all text node descendants from the source EAD record, not including any nodes from child component descriptions</xd:li>
        </xd:ul>
      </xd:p>
    </xd:desc>
  </xd:doc>

  <xsl:template name="processCollection">
        <xsl:variable name="collection_id"
            select="normalize-space(substring-before(ead//eadid, '.'))"/>
        <xsl:variable name="filename" select="normalize-space(ead//eadid)"/>
        <xsl:variable name="repository_code"
            select="normalize-space(ead/eadheader/eadid/@mainagencycode)"/>
        <xsl:variable name="audience" select="normalize-space(ead/@audience)"/>
        <xsl:variable name="collectionTitle" select="normalize-space(ead/archdesc/did/unittitle)"/>
        <xsl:variable name="collectionOrigination" select="normalize-space(ead/archdesc/did/origination[1])"/>

        <doc>
<!--
            <xsl:message>
                <xsl:text>PROCESSING: ldpd_</xsl:text>
                <xsl:value-of select="tokenize($collection_id, '_')[2]"/>
            </xsl:message>
-->
            <field name="id">
                <xsl:text>ldpd_</xsl:text>
                <xsl:value-of select="tokenize($collection_id, '_')[2]"/>
            </field>
            <field name="ead">
                <xsl:choose>
                    <xsl:when test="//dsc/c">
                        <xsl:text>yes</xsl:text>
<!--
                        <xsl:message>
                            <xsl:text>EAD: YES</xsl:text>
                        </xsl:message>
-->
                    </xsl:when>
                    <xsl:otherwise>
                        <xsl:text>no</xsl:text>
<!--
                        <xsl:message>
                            <xsl:text>EAD: NO</xsl:text>
                        </xsl:message>
-->
                    </xsl:otherwise>
                </xsl:choose>
            </field>
            <field name="filename">
                <xsl:value-of select="$filename"/>
            </field>
            <field name="level">collection</field>
            <field name="repository_code">
                <xsl:value-of select="$repository_code"/>
            </field>
            <field name="pageName">
                <xsl:text>http://www.columbia.edu/cu/lweb/archival/collections</xsl:text>
                <xsl:text>/ldpd_</xsl:text>
                <xsl:value-of select="tokenize($collection_id, '_')[2]"/>
            </field>
            <field name="audience">
                <xsl:value-of select="$audience"/>
            </field>
            <field name="unittitle">
                <xsl:value-of select="normalize-space(ead/archdesc/did/unittitle)"/>
            </field>
            <field name="sort_title">
                <xsl:value-of select="normalize-space(ead/archdesc/did/unittitle/@altrender)"/>
            </field>
            <field name="sort_title_1st">
                <xsl:value-of select="substring(normalize-space(ead/archdesc/did/unittitle/@altrender),1, 1)"/>
            </field>
            <xsl:choose>
                <xsl:when test="ead/archdesc/did/origination">
                    <xsl:for-each select="ead/archdesc/did/origination[1]">
                        <field name="origination">
                            <xsl:value-of select="normalize-space(.)"/>
                        </field>
                    </xsl:for-each>
                </xsl:when>
                <xsl:otherwise>
                    <field name="origination"/>
                </xsl:otherwise>
            </xsl:choose>
            <xsl:choose>
                <xsl:when test="ead/archdesc/did/origination">
                    <xsl:for-each select="ead/archdesc/did/origination[1]">
                        <field name="origination_1st">
                            <xsl:value-of select="substring(normalize-space(.), 1, 1)"/>
                        </field>
                    </xsl:for-each>
                </xsl:when>
                <xsl:otherwise>
                    <field name="origination_1st"/>
                </xsl:otherwise>
            </xsl:choose>
            <xsl:choose>
                <xsl:when test="ead/archdesc/did/unitid[@type = 'call_num']">
                    <xsl:for-each select="ead/archdesc/did/unitid[@type = 'call_num']">
                        <field name="unitid">
                            <xsl:value-of select="normalize-space(.)"/>
                        </field>
                    </xsl:for-each>
                </xsl:when>
                <xsl:otherwise>
                    <field name="unitid"/>
                </xsl:otherwise>
            </xsl:choose>
            <field name="unitdate">
                <xsl:value-of select="ead/archdesc/did//unitdate[1]"/>
            </field>
            <field name="beginDate">
                <xsl:value-of
                    select="normalize-space(substring-before(ead/archdesc/did//unitdate[1]/@normal, '/'))"
                />
            </field>
            <field name="endDate">
                <xsl:value-of
                    select="normalize-space(substring-after(ead/archdesc/did//unitdate[1]/@normal, '/'))"
                />
            </field>
            <xsl:for-each select="ead/archdesc/controlaccess//subject">
                <field name="subject">
                    <xsl:value-of select="normalize-space(.)"/>
                </field>
            </xsl:for-each>
            <!-- For the purposes of the web app, fold geogname EAD field into "subject" -->
            <xsl:for-each select="ead/archdesc/controlaccess//geogname">
                <field name="subject">
                    <xsl:value-of select="normalize-space(.)"/>
                </field>
            </xsl:for-each>

            <xsl:for-each select="ead/archdesc//corpname">
                <xsl:choose>
                    <xsl:when test="@encodinganalog='610'">
                        <field name="subject">
                            <xsl:value-of select="normalize-space(.)"/>
                        </field>
                    </xsl:when>
                    <xsl:when test="@encodinganalog='611'">
                        <field name="subject">
                            <xsl:value-of select="normalize-space(.)"/>
                        </field>
                    </xsl:when>
                    <xsl:when test="@encodinganalog='710'">
                        <field name="subject">
                            <xsl:value-of select="normalize-space(.)"/>
                        </field>
                    </xsl:when>
                    <xsl:when test="@encodinganalog='711'">
                        <field name="subject">
                            <xsl:value-of select="normalize-space(.)"/>
                        </field>
                    </xsl:when>
                    <xsl:otherwise>
                        <field name="corpname">
                            <xsl:value-of select="normalize-space(.)"/>
                        </field>
                    </xsl:otherwise>
                </xsl:choose>
            </xsl:for-each>
            <xsl:for-each select="ead/archdesc//persname">
                <field name="persname">
                    <xsl:value-of select="normalize-space(.)"/>
                </field>
            </xsl:for-each>
            <xsl:for-each select="ead/archdesc/controlaccess//genreform">
                <field name="genreform">
                    <xsl:value-of select="normalize-space(.)"/>
                </field>
            </xsl:for-each>
            <xsl:for-each select="ead/archdesc/controlaccess//title">
                <field name="title">
                    <xsl:value-of select="normalize-space(.)"/>
                </field>
            </xsl:for-each>
            <field name="physdesc">
                <xsl:for-each select="/ead/archdesc/did/physdesc/*">
                    <xsl:value-of select="normalize-space(.)"/>
                    <xsl:if test="position() != last()">
                        <xsl:text>&#160;</xsl:text>
                    </xsl:if>
                </xsl:for-each>
            </field>
            <field name="scopecontent">
                <xsl:for-each select="ead/archdesc/scopecontent/p">
                    <xsl:value-of select="normalize-space(.)"/>
                    <xsl:text>
</xsl:text>
                </xsl:for-each>
            </field>
            <field name="component_text">
                <xsl:for-each select="child::*[local-name() != 'dsc']">
                    <xsl:value-of select="normalize-space(.)"/>
                </xsl:for-each>
            </field>
        </doc>

        <!-- process levels 1 and 2 dsc components -->
        <xsl:for-each select="ead/archdesc/dsc/c[@level = 'collection']">
            <xsl:call-template name="processComponent">
                <xsl:with-param name="collection_id" select="$collection_id"/>
                <xsl:with-param name="filename" select="$filename"/>
                <xsl:with-param name="repository_code" select="$repository_code"/>
                <xsl:with-param name="audience" select="$audience"/>
                <xsl:with-param name="collectionTitle" select="$collectionTitle"/>
                <xsl:with-param name="collectionOrigination" select="$collectionOrigination"/>
                <xsl:with-param name="level1" select="count(preceding-sibling::c) + 1"/>
            </xsl:call-template>
        </xsl:for-each>
        <xsl:for-each select="ead/archdesc/dsc/c/c[@level = 'collection']">
            <xsl:call-template name="processComponent">
                <xsl:with-param name="collection_id" select="$collection_id"/>
                <xsl:with-param name="filename" select="$filename"/>
                <xsl:with-param name="repository_code" select="$repository_code"/>
                <xsl:with-param name="audience" select="$audience"/>
                <xsl:with-param name="collectionTitle" select="$collectionTitle"/>
                <xsl:with-param name="collectionOrigination" select="$collectionOrigination"/>
                <xsl:with-param name="level1" select="count(parent::c/preceding-sibling::c) + 1"/>
                <xsl:with-param name="level2" select="count(preceding-sibling::c) + 1"/>
            </xsl:call-template>
        </xsl:for-each>
    </xsl:template>
    <xd:doc>
        <xd:desc>
            <xd:p><xd:b>FOR FULL EAD ONLY</xd:b>: Create a SOLR record for each level 1 and level 2
                component of archival collection; i.e., <xd:b>ead/archdesc/dsc/c</xd:b> and
                    <xd:b>ead/archdesc/dsc/c</xd:b></xd:p>
            <xd:p>
                <xd:ul>
                    <xd:li><xd:b>id</xd:b>: a unique identifier for this record in the form of
                        "ldpd_[CLIO #]/[level 1 seq #][/[level 1 seq #]]"</xd:li>
                    <xd:li><xd:b>collection_id</xd:b>: identifer of the parent collection of the
                        component the current record describes</xd:li>
                    <xd:li><xd:b>ead</xd:b>: "yes"; indicates that the data in the current record
                        derives from a full EAD instance</xd:li>
                    <xd:li><xd:b>filename</xd:b>: if applicable, filename of EAD file</xd:li>
                    <xd:li><xd:b>level</xd:b>: the level of the archival component described</xd:li>
                    <xd:li><xd:b>repository_code</xd:b>: the identifier of the repository holding
                        the described materials</xd:li>
                    <xd:li><xd:b>level1</xd:b>: integer representing the position of the current
                        component relative to the parent collection </xd:li>
                    <xd:li><xd:b>level2</xd:b>: integer representing the position of the current
                        component relative to the parent component</xd:li>
                    <xd:li><xd:b>pageName</xd:b>: the URL of the collection page of the parent
                        collection</xd:li>
                    <xd:li><xd:b>audience</xd:b>: currently n/a</xd:li>
                    <xd:li><xd:b>collectionTitle</xd:b>: the title of the collection as a
                        string</xd:li>
                    <xd:li><xd:b>unittitle</xd:b>: the title of the archival component described by
                        the current record</xd:li>
                    <xd:li><xd:b>sort_title</xd:b>: the title of the archival component described by
                        the current record, with initial articles removed</xd:li>
                    <xd:li><xd:b>origination</xd:b>: the creator of the archival component described
                        by the current record (taken from the first origination element
                        only)</xd:li>
                    <xd:li><xd:b>unitid</xd:b>: <xd:i>repeatable</xd:i> the cataloger-assigned
                        identifier(s) of the archival component described by the current
                        record</xd:li>
                    <xd:li><xd:b>unitdate</xd:b>: the dates associated with the creation of the
                        archival component described by the current record, in text form</xd:li>
                    <xd:li><xd:b>beginDate</xd:b>: the earliest date associated with the creation of
                        the archival component described by the current record, in ISO 8601
                        form</xd:li>
                    <xd:li><xd:b>endDate</xd:b>: the latest date associated with the creation of the
                        archival component described by the current record, in ISO 8601 form</xd:li>
                    <xd:li><xd:b>subject</xd:b>:<xd:i>repeatable</xd:i> subject heading describing
                        the content of archival component described by the current record</xd:li>
                    <xd:li><xd:b>corpname</xd:b>:<xd:i>repeatable</xd:i> corporate name heading an
                        entity associated with the content of archival component described by the
                        current record</xd:li>
                    <xd:li><xd:b>persname</xd:b>:<xd:i>repeatable</xd:i> personal name heading of an
                        entity associated with the content of archival component described by the
                        current record</xd:li>
                    <xd:li><xd:b>genreform</xd:b>:<xd:i>repeatable</xd:i> genre or format of the
                        content or materials of archival component described by the current
                        record</xd:li>
                    <xd:li><xd:b>title</xd:b>:<xd:i>repeatable</xd:i> title heading for a work
                        associated with the content of archival component described by the current
                        record</xd:li>
                    <xd:li><xd:b>physdesc</xd:b>: statements describing the extent, form, or other
                        physical facets of the archival component described by the current
                        record</xd:li>
                    <xd:li><xd:b>bioghist</xd:b>: historical or biographical note describing the
                        creator of the content of archival component described by the current
                        record</xd:li>
                    <xd:li><xd:b>scopecontent</xd:b>: note note describing the scope and contents of
                        the archival component described by the current record</xd:li>
                    <xd:li><xd:b>digcontent</xd:b>: currently empty</xd:li>
                    <xd:li><xd:b>component text</xd:b>: all text node descendants from the source
                        EAD record, not including any nodes from child component
                        descriptions</xd:li>
                </xd:ul>
            </xd:p>
        </xd:desc>
        <xd:param name="collection_id"/>
        <xd:param name="filename"/>
        <xd:param name="repository_code"/>
        <xd:param name="audience"/>
        <xd:param name="collectionTitle"/>
        <xd:param name="collectionOrigination"/>
        <xd:param name="level1"/>
        <xd:param name="level2"/>
    </xd:doc>
    <xsl:template name="processComponent">
        <xsl:param name="collection_id"/>
        <xsl:param name="filename"/>
        <xsl:param name="repository_code"/>
        <xsl:param name="audience"/>
        <xsl:param name="collectionTitle"/>
        <xsl:param name="collectionOrigination"/>
        <xsl:param name="level1"/>
        <xsl:param name="level2"/>
        <doc>
            <field name="id">
                <xsl:text>ldpd_</xsl:text>
                <xsl:value-of select="tokenize($collection_id, '_')[2]"/>
                <xsl:text>/dsc/</xsl:text>
                <xsl:value-of select="$level1"/>
                <xsl:if test="$level2 castable as xs:integer">
                    <xsl:text>/</xsl:text>
                    <xsl:value-of select="$level2"/>
                </xsl:if>
            </field>
<!--
            <xsl:message>
                <xsl:text>PROCESSING: </xsl:text>
                <xsl:text>ldpd_</xsl:text>
                <xsl:value-of select="tokenize($collection_id, '_')[2]"/>
                <xsl:text>/dsc/</xsl:text>
                <xsl:value-of select="$level1"/>
                <xsl:if test="$level2 castable as xs:integer">
                    <xsl:text>/</xsl:text>
                    <xsl:value-of select="$level2"/>
                </xsl:if>
            </xsl:message>
-->
            <field name="ead">yes</field>
            <field name="filename">
                <xsl:value-of select="$filename"/>
            </field>
            <field name="level">
                <xsl:value-of select="@level"/>
            </field>
            <field name="repository_code">
                <xsl:value-of select="$repository_code"/>
            </field>
            <field name="level1">
                <xsl:value-of select="$level1"/>
            </field>
            <field name="level2">
                <xsl:value-of select="$level2"/>
            </field>
            <field name="pageName">
                <xsl:text>http://findingaids.cul.columbia.edu/ead/</xsl:text>
                <xsl:value-of select="$repository_code"/>
                <xsl:text>/ldpd_</xsl:text>
                <xsl:value-of select="tokenize($collection_id, '_')[2]"/>
                <xsl:text>/dsc/</xsl:text>
                <xsl:value-of select="$level1"/>
                <xsl:if test="$level2 castable as xs:integer">
                    <xsl:text>/</xsl:text>
                    <xsl:value-of select="$level2"/>
                </xsl:if>
            </field>
            <field name="unittitle">
                <xsl:value-of select="normalize-space(did/unittitle)"/>
            </field>
            <field name="sort_title">
                <xsl:value-of select="normalize-space(did/unittitle/@altrender)"/>
            </field>
            <field name="sort_title_1st">
                <xsl:value-of select="substring(normalize-space(did/unittitle/@altrender), 1, 1)"/>
            </field>

            <xsl:choose>
                <xsl:when test="did/origination">
                    <field name="origination">
                        <xsl:value-of select="normalize-space(did/origination[1])"/>
                    </field>
                </xsl:when>
                <xsl:otherwise>
                    <field name="origination"/>
                </xsl:otherwise>
            </xsl:choose>
            <xsl:choose>
                <xsl:when test="did/origination">
                    <field name="origination_1st">
                        <xsl:value-of select="substring(normalize-space(did/origination[1]), 1, 1)"
                        />
                    </field>
                </xsl:when>
                <xsl:otherwise>
                    <field name="origination_1st"/>
                </xsl:otherwise>
            </xsl:choose>
            <xsl:choose>
                <xsl:when test="did//unitid[@type = 'call_num']">
                    <xsl:for-each select="did//unitid[@type = 'call_num']">
                        <field name="unitid">
                            <xsl:value-of select="normalize-space(.)"/>
                        </field>
                    </xsl:for-each>
                </xsl:when>
                <xsl:otherwise>
                    <field name="unitid"/>
                </xsl:otherwise>
            </xsl:choose>
            <field name="unitdate">
                <xsl:value-of select="did//unitdate[1]"/>
            </field>
            <field name="beginDate">
                <xsl:value-of select="normalize-space(substring-before(did//unitdate[@normal][1]/@normal, '/'))"
                />
            </field>
            <field name="endDate">
                <xsl:value-of select="normalize-space(substring-after(did//unitdate[@normal][1]/@normal, '/'))"
                />
            </field>
            <xsl:for-each select="controlaccess//subject | controlaccess//geogname">
                <field name="subject">
                    <xsl:value-of select="normalize-space(.)"/>
                </field>
            </xsl:for-each>
            <!-- For the purposes of the web app, fold geogname EAD field into "subject"
      <xsl:for-each select="controlaccess//geogname">
        <field name="subject">
          <xsl:value-of select="normalize-space(.)"/>
        </field>
      </xsl:for-each>
      -->
            <xsl:for-each select="descendant::corpname">
                <xsl:choose>
                    <xsl:when test="@encodinganalog='610'">
                        <field name="subject">
                            <xsl:value-of select="normalize-space(.)"/>
                        </field>
                    </xsl:when>
                    <xsl:when test="@encodinganalog='611'">
                        <field name="subject">
                            <xsl:value-of select="normalize-space(.)"/>
                        </field>
                    </xsl:when>
                    <xsl:when test="@encodinganalog='710'">
                        <field name="subject">
                            <xsl:value-of select="normalize-space(.)"/>
                        </field>
                    </xsl:when>
                    <xsl:when test="@encodinganalog='711'">
                        <field name="subject">
                            <xsl:value-of select="normalize-space(.)"/>
                        </field>
                    </xsl:when>
                    <xsl:otherwise>
                        <field name="corpname">
                            <xsl:value-of select="normalize-space(.)"/>
                        </field>
                    </xsl:otherwise>
                </xsl:choose>
            </xsl:for-each>
            <xsl:for-each select="descendant::persname">
                <field name="persname">

                    <xsl:value-of select="normalize-space(.)"/>

                </field>
            </xsl:for-each>
            <xsl:for-each select="controlaccess//genreform">
                <field name="genreform">
                    <xsl:value-of select="normalize-space(.)"/>
                </field>
            </xsl:for-each>
            <xsl:for-each select="controlaccess//title">
                <field name="title">
                    <xsl:value-of select="normalize-space(.)"/>
                </field>
            </xsl:for-each>
            <field name="physdesc">
                <xsl:for-each select="child::did/physdesc/*">
                    <xsl:value-of select="normalize-space(.)"/>
                    <xsl:if test="position() != last()">
                        <xsl:text>&#160;</xsl:text>
                    </xsl:if>
                </xsl:for-each>
            </field>
            <field name="scopecontent">
            <!-- Prevent Solr error on very large scopecontent by saving to variable and truncating to 32,000 chars. -->
                <xsl:variable name="scopecontent_data">
                    <xsl:for-each select="scopecontent/p">
                        <xsl:value-of select="normalize-space(.)"/>
                        <xsl:text>
</xsl:text>
                    </xsl:for-each>
                </xsl:variable>

                <xsl:value-of select="substring($scopecontent_data,1,32000)"></xsl:value-of>
            </field>
            <field name="component_text">
                <xsl:for-each select="child::*[local-name() != 'c']">
                    <xsl:value-of select="normalize-space(.)"/>
                </xsl:for-each>
                <xsl:if test="$level2 castable as xs:integer">
                    <xsl:for-each select="child::c">
                        <xsl:value-of select="normalize-space(.)"/>
                    </xsl:for-each>
                </xsl:if>
            </field>
        </doc>
    </xsl:template>

</xsl:transform>
