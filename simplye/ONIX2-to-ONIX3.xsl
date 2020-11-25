<?xml version="1.0" encoding="UTF-8"?>
<!-- Stylesheet to convert ONIX 2.1 to ONIX 3, for ingest into SimplyE. Source and result use "reference" tags; to convert to short tags, use "switch-onix-3.0-tagnames-2.0.xsl. See Basecamp thread. -->

<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    xmlns="http://ns.editeur.org/onix/3.0/reference"
    exclude-result-prefixes="xs" 
    version="2.0">
    
    <xsl:output indent="yes"/>
    
    

    
    <xsl:template match="ONIXMessage">
        <ONIXMessage release="3.0">
        <xsl:apply-templates select="Header"/>
        <xsl:apply-templates select="Product"/>
      </ONIXMessage>
    </xsl:template>
    
    
    <xsl:template match="Header">
        <Header>
            <Sender>
                <SenderName><xsl:value-of select="FromCompany"/></SenderName>
                <ContactName><xsl:value-of select="FromPerson"/></ContactName>
                <EmailAddress><xsl:value-of select="FromEmail"/></EmailAddress>
            </Sender>

            <MessageNumber>231</MessageNumber>
            <SentDateTime>20200325T1115-0400</SentDateTime>
            <MessageNote>Sample message</MessageNote>
        </Header>
    </xsl:template>
    
    
    <xsl:template match="Product">
        <Product>
           
            <xsl:apply-templates select="RecordReference" mode="copy-no-namespaces"/>
            <xsl:apply-templates select="NotificationType" mode="copy-no-namespaces"/>
            <xsl:apply-templates select="ProductIdentifier" mode="copy-no-namespaces"/>

            
            <DescriptiveDetail>
                <ProductComposition>00</ProductComposition>
                <ProductForm>EA</ProductForm>
                
<!--             Type: EPUB or PDF?   -->
                <xsl:choose>
                    <xsl:when test="EpubType = '002'">
                        <!--			PDF --> <ProductFormDetail>E107</ProductFormDetail>
                    </xsl:when>
                    <xsl:when test="EpubType = '029'">
                        <!--			EPUB -->  <ProductFormDetail>E101</ProductFormDetail>
                    </xsl:when>
                </xsl:choose>
              
                
                
                <!--	leave out classification, collection		-->
                
                <TitleDetail>
                    <TitleType>01</TitleType>
                    <TitleElement>
                        <TitleElementLevel>01</TitleElementLevel>
 
                        <TitleText><xsl:value-of select="Title/TitleText"/></TitleText>
                        <xsl:apply-templates select="Title/Subtitle" mode="copy-no-namespaces"/>
                       
                    </TitleElement>
                </TitleDetail>
                
                
<!--                Contributors -->
               <xsl:for-each select="Contributor">
                   <xsl:apply-templates select="." mode="copy-no-namespaces"/>
               </xsl:for-each>
      		
                <xsl:apply-templates select="ContributorStatement" mode="copy-no-namespaces"/>
      		
                <xsl:apply-templates select="Language" mode="copy-no-namespaces"/>
    
    
                <!--			page count-->
                <Extent>
                    <ExtentType>07</ExtentType>
                    <ExtentValue><xsl:value-of select="NumberOfPages"/></ExtentValue>
                    <ExtentUnit>03</ExtentUnit>
                </Extent>
                
                
<!--            SUBJECTS    -->
  
                <xsl:for-each select="Subject">
                    <xsl:apply-templates select="." mode="copy-no-namespaces"/>
                </xsl:for-each>
  
                
                <!-- skip audience-->
            </DescriptiveDetail>
    
            <CollateralDetail>
<!--            Description text    -->
                <TextContent>
                    <TextType>03</TextType>
                    <ContentAudience>00</ContentAudience>
                    <Text><xsl:value-of select="OtherText/Text"/>
                    </Text>
                </TextContent>
                
            </CollateralDetail>
 
            
            <!-- there is no Block 3 -->
            <PublishingDetail>
                <Imprint>
                    <ImprintName>Johns Hopkins University Press</ImprintName>
                </Imprint>
                <Publisher>
                    <PublishingRole>01</PublishingRole>
                    
                    <PublisherName>Johns Hopkins University Press</PublisherName>
                    <Website>
                        <WebsiteRole>01</WebsiteRole>
                        <WebsiteLink>http://jhupbooks.press.jhu.edu</WebsiteLink>
                    </Website>
                </Publisher>
                
                
            </PublishingDetail>
            
            
            
        </Product>
    </xsl:template>
    
    <xsl:template match="*" mode="copy-no-namespaces">
        <xsl:element name="{local-name()}">
            <xsl:copy-of select="@*"/>
            <xsl:apply-templates select="node()" mode="copy-no-namespaces"/>
        </xsl:element>
    </xsl:template>
    
    
</xsl:stylesheet>