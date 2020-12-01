<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:saxon="http://saxon.sf.net/"
    xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:xs="http://www.w3.org/2001/XMLSchema"
    version="2.0" xpath-default-namespace="http://www.loc.gov/MARC21/slim">

    <xsl:output indent="yes" encoding="UTF-8" method="xml" exclude-result-prefixes="#all"/>


    <!-- send repo code as param when processing -->
    <xsl:param name="repo">nnc-rb</xsl:param>

    <xsl:variable name="inline_delim">
        <xsl:text>&#160;</xsl:text>
    </xsl:variable>
    <xsl:variable name="lf">
        <xsl:text>&#xa;</xsl:text>
    </xsl:variable>


    <xsl:template match="/">
        <xsl:message>Record count: <xsl:value-of select="count(collection/record)"/></xsl:message>
        
        <add>
            <xsl:apply-templates select="collection/record"/>

        </add>


    </xsl:template>




    <xsl:template match="record">

        <!-- Collection-level variables -->

        <xsl:variable name="bibid">
            <xsl:value-of select="controlfield[@tag = '001']"/>
        </xsl:variable>

        <xsl:variable name="title">
            <xsl:for-each select="datafield[@tag='245']/subfield">
                <xsl:value-of select="."/>
                <xsl:text> </xsl:text>
            </xsl:for-each>
        </xsl:variable>

        <xsl:variable name="sort_title">
            <xsl:call-template name="get_sort_string">
                <xsl:with-param name="str"><xsl:value-of select="$title"/></xsl:with-param>
            </xsl:call-template>
        </xsl:variable>

        <xsl:variable name="creator">
            <xsl:for-each select="datafield[@tag = '100'] | datafield[@tag = '110']">
                <xsl:value-of select="subfield[@code = 'a']"/>
                <xsl:if test="subfield[@code = 'd']">
                    <xsl:text> </xsl:text>
                    <xsl:value-of select="subfield[@code = 'd']"/>
                </xsl:if>
            </xsl:for-each>
        </xsl:variable>

        <xsl:variable name="begin_date">
            <xsl:value-of select="substring(controlfield[@tag = '008'], 8, 4)"/>
        </xsl:variable>

        <xsl:variable name="end_date">
            <xsl:if test="not(contains(substring(controlfield[@tag = '008'], 12, 1), ' '))">
                <xsl:value-of select="substring(controlfield[@tag = '008'], 12, 4)"/>
            </xsl:if>
        </xsl:variable>



        <!-- Solr Fields -->

        <doc>

            <field name="id">
                <xsl:text>ldpd_</xsl:text>
                <xsl:value-of select="$bibid"/>
            </field>


            <field name="ead">
                <xsl:choose>
                    <!-- TODO: figure out why some records have more than one 856! -->
                    <xsl:when
                        test="contains(datafield[@tag='856'][1]/subfield[@code='u'],'findingaids.')">
                        <xsl:text>yes</xsl:text>
                    </xsl:when>
                    <xsl:otherwise>
                        <xsl:text>no</xsl:text>
                    </xsl:otherwise>
                </xsl:choose>
            </field>

            <field name="filename">
                <xsl:text>ldpd_</xsl:text>
                <xsl:value-of select="$bibid"/>
                <xsl:text>_ead.xml</xsl:text>

            </field>

            <field name="level">
                <xsl:text>collection</xsl:text>
            </field>

            <field name="repository_code">
                <xsl:value-of select="$repo"/>
            </field>

            <field name="pageName">
                <xsl:text>https://findingaids.library.columbia.edu/ead/</xsl:text>
                <xsl:value-of select="$repo"/>
                <xsl:text>/ldpd_</xsl:text>
                <xsl:value-of select="$bibid"/>
            </field>

            <field name="unittitle">
                <xsl:value-of select="normalize-space($title)"/>
            </field>


            <field name="sort_title">
                
                <xsl:value-of select="normalize-space($sort_title)"/>
                
            </field>

            <field name="sort_title_1st">
                <xsl:call-template name="get_sort_key">
                    <xsl:with-param name="str">
                        <xsl:value-of select="$sort_title"/>
                    </xsl:with-param>
                </xsl:call-template>
            </field>

            <field name="origination">
                <!-- code for origination -->
                <xsl:value-of select="$creator"/>
            </field>

            <field name="origination_1st">
                <xsl:call-template name="get_sort_key">
                    <xsl:with-param name="str">
                        <xsl:value-of select="$creator"/>
                    </xsl:with-param>
                </xsl:call-template>
            </field>

            <field name="unitid">
                <xsl:value-of select="datafield[@tag='852']/subfield[@code='j']"/>
            </field>

            <field name="unitdate">
                <xsl:value-of
                    select="translate(datafield[@tag = '245']/subfield[@code = 'f'], '.', '')"/>
            </field>
            <field name="beginDate">
                <xsl:value-of select="$begin_date"/>
            </field>

            <field name="endDate">
                <xsl:value-of select="$end_date"/>
            </field>


            <!-- subjects -->
            <xsl:for-each select="datafield[@tag = ('650','651','610','611','710','711')]">
                <xsl:comment><xsl:value-of select="@tag"/></xsl:comment>
                <field name="subject">
                    <xsl:for-each select="subfield[(@code != '0') and (@code != '2')]">
                        <xsl:call-template name="subelements-inline"/>
                    </xsl:for-each>
                </field>
            </xsl:for-each>


            <!-- corpnames -->
            <xsl:for-each select="datafield[@tag = '110']">
                <xsl:comment><xsl:value-of select="@tag"/></xsl:comment>
                <field name="corpname">
                    <xsl:for-each select="subfield[(@code != '0') and (@code != '2')]">
                        <xsl:call-template name="subelements-inline"/>
                    </xsl:for-each>
                </field>
            </xsl:for-each>

            <!-- persname -->
            <xsl:for-each select="datafield[@tag = '600']">
                <xsl:comment><xsl:value-of select="@tag"/></xsl:comment>
                <field name="persname">
                    <xsl:for-each select="subfield[(@code != '0') and (@code != '2')]">
                        <xsl:call-template name="subelements-inline"/>
                    </xsl:for-each>
                </field>
            </xsl:for-each>


            <!-- genreform -->
            <xsl:for-each select="datafield[@tag = '655']">
                <xsl:comment><xsl:value-of select="@tag"/></xsl:comment>
                <field name="genreform">
                    <xsl:for-each select="subfield[(@code != '0') and (@code != '2')]">
                        <xsl:call-template name="subelements-inline"/>
                    </xsl:for-each>
                </field>
            </xsl:for-each>

            <!-- title -->
            <xsl:for-each select="datafield[@tag = '630']">
                <xsl:comment><xsl:value-of select="@tag"/></xsl:comment>
                <field name="title">
                    <xsl:for-each select="subfield">
                        <xsl:call-template name="subelements-inline"/>
                    </xsl:for-each>
                </field>
            </xsl:for-each>

            <!-- physdesc -->
            <field name="physdesc">
                <xsl:for-each select="datafield[@tag = '300']/subfield">
                    <xsl:call-template name="subelements-inline"/>
                </xsl:for-each>
            </field>

            <!-- scopecontent -->
            <field name="scopecontent">
                <xsl:for-each select="datafield[@tag = '520']/subfield">
                    <xsl:call-template name="subelements-inline"/>
                </xsl:for-each>
            </field>

            <!-- component_text -->
            <field name="component_text">
                <xsl:for-each select="datafield[@tag = ('100','110','111','130','245','300','351','506','520','524','530','540','541','544','545','546','555','561','583','600','610','611','630','650','651','655','656','657','697','700','710','711','730','852','856')]">
                    <xsl:value-of select="normalize-space(.)"/>
                    <xsl:text> </xsl:text>
                </xsl:for-each>
            </field>

        </doc>
    </xsl:template>

    <xsl:template name="get_sort_string">
        <xsl:param name="str"/>
<!-- TODO: Code to remove articles, quote marks, brackets, etc. -->
        <xsl:analyze-string select="$str" regex="^\W">
        <xsl:matching-substring/>
            
            <xsl:non-matching-substring>
                <xsl:analyze-string select="." regex="^The\s+" flags="i">
                    <xsl:matching-substring/>
                    <xsl:non-matching-substring>
                <xsl:value-of select="."/>
                    </xsl:non-matching-substring>
    </xsl:analyze-string>
            </xsl:non-matching-substring>
            
        </xsl:analyze-string>
        
    </xsl:template>
    


    <xsl:template name="get_sort_key">
        <!-- get first alpha character -->
        <xsl:param name="str"/>
        <xsl:analyze-string select="$str" regex="^\W?([\w])">
            <xsl:matching-substring>
                <xsl:value-of select="regex-group(1)"/>
            </xsl:matching-substring>
            <xsl:non-matching-substring>
                <!-- in case match fails -->
            </xsl:non-matching-substring>
        </xsl:analyze-string>
    </xsl:template>



    <!-- TODO: This seems overly complicated. Refactor? -->
    <xsl:template name="subelements-inline">
        <xsl:value-of select="normalize-space(.)"/>
        <xsl:if test="position() != last()">
            <xsl:choose>
                <xsl:when test="ancestor::datafield/@tag = ('520', '545')">
                    <xsl:value-of select="$lf"/>
                </xsl:when>
                <xsl:when test="ancestor::datafield/@tag = '300'">
                    <xsl:value-of select="$inline_delim"/>
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
    </xsl:template>
</xsl:stylesheet>
