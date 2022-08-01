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
   				<ColorMapEntry color="#24CCFD" quantity="0.03" label="0.03" />
              <ColorMapEntry color="#2CFAFE" quantity="0.06" label="0.06"/>
              <ColorMapEntry color="#6EFD9B" quantity="0.09" label="0.09"/>
              <ColorMapEntry color="#C8FD4C" quantity="0.12" label="0.12"/>
                <ColorMapEntry color="#FEF536" quantity="0.15" label="0.15"/>
                <ColorMapEntry color="#FD9726" quantity="0.18" label="0.18"/>
                <ColorMapEntry color="#FC581F" quantity="0.21" label="0.21"/>
                <ColorMapEntry color="#F30F1A" quantity="0.24" label="0.24"/>
                <ColorMapEntry color="#AD080F" quantity="0.27" label="0.27"/>
                <ColorMapEntry color="#8A050A" quantity="0.30" label="0.30"/>
           
            </ColorMap>
          </RasterSymbolizer>
        </Rule>
      </FeatureTypeStyle>
    </UserStyle>
  </NamedLayer>
</StyledLayerDescriptor>