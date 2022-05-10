<?xml version="1.0" encoding="ISO-8859-1"?>
<StyledLayerDescriptor version="1.0.0" 
    xsi:schemaLocation="http://www.opengis.net/sld StyledLayerDescriptor.xsd" 
    xmlns="http://www.opengis.net/sld" 
    xmlns:ogc="http://www.opengis.net/ogc" 
    xmlns:xlink="http://www.w3.org/1999/xlink" 
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <NamedLayer>
    <Name>height_surface_normalize</Name>
    <UserStyle>
      <Title>height_surface_normalize</Title>
      <FeatureTypeStyle>
        <Rule>
          <RasterSymbolizer>
            <ColorMap>
			<!--ColorMapEntry color="#040F8D" quantity="-32767" opacity="0" /-->
              
              
                          <ColorMapEntry color="#0300BB" quantity="0.00" label="0.00" opacity="0" />
              <ColorMapEntry color="#0C33FF" quantity="0.03" label="0.03" opacity="1" />
              <ColorMapEntry color="#388AFE" quantity="0.06" label="0.06" opacity="1"/>
              <ColorMapEntry color="#60B6FF" quantity="0.09" label="0.09" opacity="1"/>
                <ColorMapEntry color="#7ED4FF" quantity="0.12" label="0.12" opacity="1"/>
                <ColorMapEntry color="#99EDFF" quantity="0.15" label="0.15" opacity="1"/>
                <ColorMapEntry color="#B7F8FF" quantity="0.18" label="0.18" opacity="1"/>
                <ColorMapEntry color="#D9FFFF" quantity="0.21"  label="0.21" opacity="1"/>
                <ColorMapEntry color="#FFFFFF" quantity="0.24"  label="0.24" opacity="1"/>
                <ColorMapEntry color="#FEFF53" quantity="0.27" label="0.27" opacity="1"/>
                <ColorMapEntry color="#FFEF02" quantity="0.30" label="0.30" opacity="1"/>
     
                <ColorMapEntry color="#FECD02" quantity="0.33" label="0.33" opacity="1" />
                <ColorMapEntry color="#FF9500" quantity="0.36" label="0.36" opacity="1" />
            </ColorMap>
          </RasterSymbolizer>
        </Rule>
      </FeatureTypeStyle>
    </UserStyle>
  </NamedLayer>
</StyledLayerDescriptor>