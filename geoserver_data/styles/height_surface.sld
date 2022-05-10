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
              <ColorMapEntry color="#8A050A" quantity="-2.2" />
              <ColorMapEntry color="#AD080F" quantity="-1.8" />
              <ColorMapEntry color="#F30F1A" quantity="-1.4" />
              <ColorMapEntry color="#FC581F" quantity="-1.0" />
                <ColorMapEntry color="#FD9726" quantity="-0.6" />
                <ColorMapEntry color="#FEF536" quantity="-0.2" />
                <ColorMapEntry color="#C8FD4C" quantity="0.2" />
                <ColorMapEntry color="#6EFD9B" quantity="0.6" />
                <ColorMapEntry color="#2CFAFE" quantity="1.0" />
                <ColorMapEntry color="#24CCFD" quantity="1.4" />
                
                <ColorMapEntry color="#1461FB" quantity="1.8" />
                <ColorMapEntry color="#1139FB" quantity="2.2" />
                <ColorMapEntry color="#0F24FB" quantity="2.6" />
                <ColorMapEntry color="#0818BC" quantity="3.0" />
   
                <ColorMapEntry color="#040F8D" quantity="3.4" />
           
            </ColorMap>
          </RasterSymbolizer>
        </Rule>
      </FeatureTypeStyle>
    </UserStyle>
  </NamedLayer>
</StyledLayerDescriptor>