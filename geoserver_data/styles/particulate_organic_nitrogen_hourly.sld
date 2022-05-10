<?xml version="1.0" encoding="ISO-8859-1"?>
<StyledLayerDescriptor version="1.0.0" 
    xsi:schemaLocation="http://www.opengis.net/sld StyledLayerDescriptor.xsd" 
    xmlns="http://www.opengis.net/sld" 
    xmlns:ogc="http://www.opengis.net/ogc" 
    xmlns:xlink="http://www.w3.org/1999/xlink" 
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <NamedLayer>
    <Name>Two color gradient</Name>
    <UserStyle>
      <Title>SLD Cook Book: Two color gradient</Title>
      <FeatureTypeStyle>
        <Rule>
          <RasterSymbolizer>
            <ColorMap>
   				<ColorMapEntry color="#24CCFD" quantity="0.02" label="0.02" />
              <ColorMapEntry color="#2CFAFE" quantity="0.04" label="0.04"/>
              <ColorMapEntry color="#6EFD9B" quantity="0.06" label="0.06"/>
              <ColorMapEntry color="#C8FD4C" quantity="0.08" label="0.08"/>
                <ColorMapEntry color="#FEF536" quantity="0.10" label="0.10"/>
                <ColorMapEntry color="#FD9726" quantity="0.12" label="0.12"/>
                <ColorMapEntry color="#FC581F" quantity="0.14" label="0.14"/>
                <ColorMapEntry color="#F30F1A" quantity="0.16" label="0.16"/>
                <ColorMapEntry color="#AD080F" quantity="0.18" label="0.18"/>
                <ColorMapEntry color="#8A050A" quantity="0.20" label="0.20"/>
           
            </ColorMap>
          </RasterSymbolizer>
        </Rule>
      </FeatureTypeStyle>
    </UserStyle>
  </NamedLayer>
</StyledLayerDescriptor>