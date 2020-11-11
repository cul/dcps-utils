<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:saxon="http://saxon.sf.net/"
    xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mrc="http://www.loc.gov/MARC21/slim"
    xmlns:xs="http://www.w3.org/2001/XMLSchema" version="2.0"
    xpath-default-namespace="urn:isbn:1-931666-22-9">

    <xsl:output indent="yes" encoding="UTF-8" method="xml" exclude-result-prefixes="#all"/>

    <xsl:param name="xmldir">[XMLDIR]</xsl:param>

    <xsl:template match="/">
        <add>
            <xsl:for-each select="//mrc:record">
                <xsl:variable name="collection_id"
                    select="descendant::mrc:controlfield[@tag = '001']"/>
                <xsl:variable name="filename"/>
                <xsl:variable name="repository_code">
                    <xsl:text>nnc-oh</xsl:text>
                </xsl:variable>
                <xsl:variable name="collectionTitle">
                    <xsl:for-each select="descendant::mrc:datafield[@tag = '245']">
                        <xsl:call-template name="processSubfields"/>
                    </xsl:for-each>
                </xsl:variable>
                <xsl:variable name="creator">
                    <xsl:for-each
                        select="descendant::mrc:datafield[@tag = '100'] | descendant::mrc:datafield[@tag = '110']">
                        <xsl:value-of select="child::mrc:subfield[@code = 'a']"/>
                        <xsl:if test="child::mrc:subfield[@code = 'd']">
                            <xsl:text> </xsl:text>
                            <xsl:value-of select="child::mrc:subfield[@code = 'd']"/>
                        </xsl:if>
                    </xsl:for-each>
                </xsl:variable>

		
		<!-- set levelCode -  evaluate biblevel code from leader -->
                <xsl:variable name="levelCode" select="substring(descendant::mrc:leader, 8, 1)"/>

		<!-- What is the project-title for this interview?  Or is it blank?
			Should be blank for project-level records.    -->
                <xsl:variable name="projectTitle">
                      <xsl:choose>
                        <!-- This is an interview, with a 773 pointer to the project  -->
                        <xsl:when test="descendant::mrc:datafield[@tag = '773']">
                        <xsl:for-each
                             select="descendant::mrc:datafield[@tag = '773']/mrc:subfield[@code = 'a'] | descendant::mrc:datafield[@tag = '773']/mrc:subfield[@code = 't']">
                            <xsl:value-of select="normalize-space(.)"/>
                        </xsl:for-each>   
                        </xsl:when>
                        <!--  Otherwise (no 773), either a proj. or a project-less interview -->
                        <xsl:otherwise>
<!-- marquis, 6/11 - no, don't use collectionTitle ( = all 245 fields clumped together),
     instead take only 245$a and munge punctuation
                          <xsl:value-of select="$collectionTitle"/>
-->

                      <xsl:choose>
                    <!-- if the biblevel is 'm' or 'd', it's an interview -->
                        <xsl:when test="$levelCode = 'm'">
                          <xsl:text></xsl:text>
                        </xsl:when>
                        <xsl:when test="$levelCode = 'd'">
                          <xsl:text></xsl:text>
                        </xsl:when>
                        <xsl:otherwise>
                          <!-- otherwise, it's a project -->
                          <xsl:value-of select="replace(descendant::mrc:datafield[@tag = '245']/mrc:subfield[@code = 'a'], ' :', '.')"/>
                        </xsl:otherwise>
                      </xsl:choose>


                        </xsl:otherwise>
                      </xsl:choose>
                </xsl:variable>
                <xsl:variable name="level">
<!-- marquis, 6/11 - no, collectionTitle does not string-equal projectTitle for 
     project-level records.  instead, test for presence of the 773.

                    <xsl:when test="$collectionTitle = $projectTitle">
-->
<!-- thc, 2011-06-06 changed code to evaluate biblevel code from leader -->

                  <xsl:choose>
                <!-- when there is a 773, it's an interview -->
                    <xsl:when test="descendant::mrc:datafield[@tag = '773']">
                      <xsl:text>interview</xsl:text>
                    </xsl:when>
                    <xsl:otherwise>
                      <!-- if no 773, then... -->
                      <xsl:choose>
                    <!-- if the biblevel is 'm' or 'd', it's an interview -->
                        <xsl:when test="$levelCode = 'm'">
                          <xsl:text>interview</xsl:text>
                        </xsl:when>
                        <xsl:when test="$levelCode = 'd'">
                          <xsl:text>interview</xsl:text>
                        </xsl:when>
                        <xsl:otherwise>
                          <!-- otherwise, it's a project -->
                          <xsl:text>project</xsl:text>
                        </xsl:otherwise>
                      </xsl:choose>
                    </xsl:otherwise>
                  </xsl:choose>
                </xsl:variable>
<!--
                <xsl:message>
                  <xsl:text>LEVEL = </xsl:text>
                  <xsl:value-of select="$level"/>
                </xsl:message>
                <xsl:message>
                  <xsl:text>TITLE = </xsl:text>
                  <xsl:value-of select="$collectionTitle"/>
                </xsl:message>
-->
                <doc>
                  <!-- id -->
                    <field name="id">
                        <xsl:text>ldpd_</xsl:text>
                        <xsl:value-of select="$collection_id"/>
                    </field>
                    <!-- filename -->
                    <field name="filename">
                        <xsl:value-of select="$filename"/>
                    </field>
                    <!-- level -->
                    <field name="level">
                      <xsl:value-of select="$level"/>
                    </field>
                    <!-- ead -->
                    <field name="ead">
                        <xsl:text>no</xsl:text>
                    </field>
                    <!-- repository_code -->
                    <field name="repository_code">
                        <xsl:value-of select="$repository_code"/>
                    </field>
                    <!-- pageName -->
                    <field name="pageName"/>
                    <!-- unittitle -->
                    <field name="unittitle">
                        <xsl:value-of select="$collectionTitle"/>
                    </field>
                    <!-- unitid -->
                    <field name="unitid"/>
                    <!-- sort_title -->
                    <field name="sort_title">
                        <xsl:value-of select="$collectionTitle"/>
                    </field>
                    <!-- sort_title_1st -->
                    <field name="sort_title_1st">
                        <xsl:value-of select="substring($collectionTitle, 1, 1)"/>
                    </field>
                    <!-- origination -->
                    <field name="origination">
                        <xsl:variable name="lastChar"
                            select="substring($creator, string-length($creator))"/>
                        <xsl:choose>
                            <xsl:when test="$lastChar = ','">
                                <xsl:value-of
                                    select="substring($creator, 1, string-length($creator) - 1)"/>
                            </xsl:when>
                            <xsl:otherwise>
                                <xsl:value-of select="$creator"/>
                            </xsl:otherwise>
                        </xsl:choose>
                    </field>
                    <!-- origination_1st -->
                    <field name="origination_1st">
                        <xsl:value-of select="substring($creator, 1, 1)"/>
                    </field>
                    <!-- unitdate -->
                    <field name="unitdate">
                        <xsl:value-of
                            select="translate(descendant::mrc:datafield[@tag = '245']/mrc:subfield[@code = 'f'], '.', '')"
                        />
                    </field>
                    <!-- beginDate -->
                    <field name="beginDate">
                        <xsl:value-of
                            select="substring(descendant::mrc:controlfield[@tag = '008'], 8, 4)"/>
                    </field>
                    <!-- endDate -->
                    <field name="endDate">
                        <xsl:choose>
                            <xsl:when
                                test="substring(descendant::mrc:controlfield[@tag = '008'], 7, 1) = 'i'">
                                <xsl:value-of
                                    select=" substring(descendant::mrc:controlfield[@tag = '008'], 12, 4)"
                                />
                            </xsl:when>
                            <xsl:otherwise>
                                <xsl:value-of
                                    select=" substring(descendant::mrc:controlfield[@tag = '008'], 8, 4)"
                                />
                            </xsl:otherwise>
                        </xsl:choose>
                    </field>
                    <!-- subject -->
                    <xsl:for-each
                        select="descendant::mrc:datafield[starts-with(@tag,'6')] | descendant::mrc:datafield[@tag = '700'] | descendant::mrc:datafield[@tag = '710'] | descendant::mrc:datafield[@tag = '730']">
                        <field name="subject">
                            <xsl:call-template name="processSubjects"/>
                        </field>

                    </xsl:for-each>
                    <!-- For the purposes of the web app, fold geogname EAD field into "subject" 
          <xsl:for-each select="descendant::mrc:datafield[@tag = '651']">
            <field name="subject">
              <xsl:value-of select="normalize-space(.)"/>
            </field>
          </xsl:for-each>
-->
          <!-- corpname -->
                    <xsl:for-each
                        select="descendant::mrc:datafield[@tag = '610'] | descendant::mrc:datafield[@tag = '710']">
                        <field name="corpname">
                            <xsl:call-template name="processSubjects"/>
                        </field>
                    </xsl:for-each>
                    <!-- persname -->
                    <xsl:for-each
                        select=" descendant::mrc:datafield[@tag = '600'] | descendant::mrc:datafield[@tag = '700']">
                        <field name="persname">
                            <xsl:call-template name="processSubjects"/>
                        </field>
                    </xsl:for-each>
                    <!-- genreform -->
                    <xsl:for-each select="descendant::mrc:datafield[@tag = '655']">
                        <field name="genreform">
                            <xsl:call-template name="processSubjects"/>
                        </field>
                    </xsl:for-each>
                    <!-- title -->
                    <xsl:for-each select="descendant::mrc:datafield[@tag = '630']">
                        <field name="title">
                            <xsl:call-template name="processSubjects"/>
                        </field>
                    </xsl:for-each>
                    <!-- bioghist -->
                    <field name="bioghist">
                        <xsl:for-each select="descendant::mrc:datafield[@tag = '545']">
                            <xsl:value-of select="normalize-space(.)"/>
                            <xsl:text>
</xsl:text>
                        </xsl:for-each>
                    </field>
                    <!-- physdesc -->
                    <field name="physdesc">
                        <xsl:for-each select="descendant::mrc:datafield[@tag = '300']">
                            <xsl:call-template name="processSubfields"/>
                            <xsl:if test="position() != last()">
                                <xsl:text> </xsl:text>
                            </xsl:if>
                        </xsl:for-each>
                    </field>
                    <!-- scopecontent -->
                    <field name="scopecontent">
                        <xsl:for-each select="descendant::mrc:datafield[@tag = '520']">
                            <xsl:value-of select="normalize-space(.)"/>
                            <xsl:text>
</xsl:text>
                        </xsl:for-each>
                    </field>
                    <!-- accessConditions -->
                    <field name="accessConditions">
                        <xsl:for-each
                            select="descendant::mrc:datafield[@tag = '540'] | descendant::datafield[@tag = '506']">
                            <xsl:value-of select="normalize-space(.)"/>
                            <xsl:if test="position() != last()">
                                <xsl:text> </xsl:text>
                            </xsl:if>
                            <xsl:text>
</xsl:text>
                        </xsl:for-each>
                    </field>
                    <!-- project title -->
                    <field name="projectTitle">
                      <xsl:value-of select="$projectTitle"/>
                    </field>
                    <!-- * project_id -->
                    <field name="project_id">
                      <xsl:choose>
                        <xsl:when test="$level != 'c'">
                          <xsl:value-of select="descendant::mrc:datafield[@tag = '773']/mrc:subfield[@code = 'w']"/>
                        </xsl:when>
                        <xsl:otherwise>
                          <xsl:value-of select="$collection_id"/>
                        </xsl:otherwise>
                      </xsl:choose>
                    </field>
                    <!-- component_text -->
                    <field name="component_text">
                        <xsl:for-each
                            select="descendant::mrc:datafield[not(starts-with(@tag, '0'))]/mrc:subfield">
                            <xsl:value-of select="normalize-space(.)"/>
                            <xsl:text> </xsl:text>
                        </xsl:for-each>
                    </field>
                </doc>
            </xsl:for-each>
        </add>
    </xsl:template>
    <xsl:template name="processSubjects">
        <xsl:for-each select="child::mrc:subfield[(@code != '0') and (@code != '2')]">
            <xsl:value-of select="normalize-space(.)"/>
            <xsl:if test="position() != last()">
                <xsl:choose>
                    <xsl:when test="following-sibling::mrc:subfield[@code = 'd']">
                        <xsl:text> </xsl:text>
                    </xsl:when>
                    <xsl:when test="following-sibling::mrc:subfield[@code = 'b']">
                        <xsl:text> </xsl:text>
                    </xsl:when>
                    <xsl:when test="following-sibling::mrc:subfield[@code = 'e']">
                        <xsl:text> </xsl:text>
                    </xsl:when>
                    <xsl:when test="following-sibling::mrc:subfield[@code = '2']"> </xsl:when>
                    <xsl:otherwise>
                        <xsl:text>--</xsl:text>
                    </xsl:otherwise>
                </xsl:choose>
            </xsl:if>
        </xsl:for-each>
    </xsl:template>
    <xsl:template name="processSubfields">
        <xsl:for-each select="child::mrc:subfield">
            <xsl:value-of select="normalize-space(.)"/>
            <xsl:if test="position() != last()">
                <xsl:text> </xsl:text>
            </xsl:if>
        </xsl:for-each>
    </xsl:template>
</xsl:stylesheet>
