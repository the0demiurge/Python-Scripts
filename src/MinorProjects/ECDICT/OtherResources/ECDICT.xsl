<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" 
	xmlns:d="http://www.apple.com/DTDs/DictionaryService-1.0.rng" version="1.0">
	<xsl:output method="xml" encoding="UTF-8" indent="no" doctype-public="-//W3C//DTD XHTML 1.1//EN" doctype-system="http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd" />


	<xsl:template match="div[@class='definition']">
		<xsl:if test="$display-definition = '1'">
			<xsl:copy>
				<xsl:apply-templates select="@*|node()" />
			</xsl:copy>
		</xsl:if>
	</xsl:template>

	<xsl:template match="div[@class='tags']">
		<xsl:if test="$display-tags = '1'">
			<xsl:copy>
				<xsl:apply-templates select="@*|node()" />
			</xsl:copy>
		</xsl:if>
	</xsl:template>


	<!--
	Default rule for all other tags
-->
	<xsl:template match="@*|node()">
		<xsl:copy>
			<xsl:apply-templates select="@*|node()" />
		</xsl:copy>
	</xsl:template>

</xsl:stylesheet>
