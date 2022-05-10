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
  <ColorMapEntry color="#040F8D" quantity="-2200" label="-1.0" opacity="1" />
              <ColorMapEntry color="#0818BC" quantity="-0.9" label="-0.9" opacity="1" />
              <ColorMapEntry color="#0F24FB" quantity="-0.6" label="-0.6" opacity="1"/>
              <ColorMapEntry color="#1139FB" quantity="-0.3" label="-0.3" opacity="1"/>
                <ColorMapEntry color="#1461FB" quantity="0" label="0.0" opacity="1"/>
                <ColorMapEntry color="#24CCFD" quantity="0.3" label="0.3" opacity="1"/>
                <ColorMapEntry color="#2CFAFE" quantity="0.6" label="0.6" opacity="1"/>
                <ColorMapEntry color="#6EFD9B" quantity="0.9"  label="0.9" opacity="1"/>
                <ColorMapEntry color="#C8FD4C" quantity="1.2"  label="1.2" opacity="1"/>
                <ColorMapEntry color="#FEF536" quantity="1.5" label="1.5" opacity="1"/>
                
                <ColorMapEntry color="#FD9726" quantity="1.8" label="1.8" opacity="1" />
                <ColorMapEntry color="#FC581F" quantity="2.1" label="2.1" opacity="1" />
                <ColorMapEntry color="#F30F1A" quantity="2.4" label="2.4" opacity="1"/>
                <ColorMapEntry color="#AD080F" quantity="2.7" label="2.7" opacity="1"/>
  
                <ColorMapEntry color="#8A050A" quantity="3.0" label="3.0" opacity="1" />
           
            </ColorMap>
          </RasterSymbolizer>
        </Rule>
      </FeatureTypeStyle>
    </UserStyle>
  </NamedLayer>
</StyledLayerDescriptor>