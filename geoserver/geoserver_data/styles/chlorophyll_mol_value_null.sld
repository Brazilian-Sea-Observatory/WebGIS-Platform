<?xml version="1.0" encoding="ISO-8859-1"?>
<StyledLayerDescriptor version="1.0.0" 
                       xsi:schemaLocation="http://www.opengis.net/sld StyledLayerDescriptor.xsd" 
                       xmlns="http://www.opengis.net/sld" 
                       xmlns:ogc="http://www.opengis.net/ogc" 
                       xmlns:xlink="http://www.w3.org/1999/xlink" 
                       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <NamedLayer>
    <Name>chlorophyll_mol</Name>
    <UserStyle>
      <Title>chlorophyll_mol</Title>
      <FeatureTypeStyle>
        <Rule>
          <RasterSymbolizer>
            <ColorMap type="ramp">
              <ColorMapEntry color="#9831FB" quantity="0.00" label="0.00" opacity="0" />              				  <ColorMapEntry color="#9831FB" quantity="0.03" label="0.03" opacity="1" />
              <ColorMapEntry color="#0B34F1" quantity="0.10" label="0.10" opacity="1"/>
              <ColorMapEntry color="#B5FEDC" quantity="0.30" label="0.30" opacity="1"/>
              <ColorMapEntry color="#5BE52A" quantity="1.00" label="1.00" opacity="1"/>
              <ColorMapEntry color="#F9FD6E" quantity="3.00" label="3.00" opacity="1"/>
              <ColorMapEntry color="#FC4D29" quantity="10.0" label="10.0" opacity="1"/>
              <ColorMapEntry color="#750307" quantity="30.0" label="30.0" opacity="1"/>
            </ColorMap>
          </RasterSymbolizer>
        </Rule>
      </FeatureTypeStyle>
    </UserStyle>
  </NamedLayer>
</StyledLayerDescriptor>