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
              
              
              <ColorMapEntry color="#040F8D" quantity="-2200" label="-2200" opacity="1" />
              <ColorMapEntry color="#0818BC" quantity="-1800" label="-1800" opacity="1" />
              <ColorMapEntry color="#0F24FB" quantity="-1400" label="-1400" opacity="1"/>
              <ColorMapEntry color="#1139FB" quantity="-1000" label="-1000" opacity="1"/>
                <ColorMapEntry color="#1461FB" quantity="-800" label="-800" opacity="1"/>
                <ColorMapEntry color="#24CCFD" quantity="-600" label="-600" opacity="1"/>
                <ColorMapEntry color="#2CFAFE" quantity="-200" label="-200" opacity="1"/>
                <ColorMapEntry color="#6EFD9B" quantity="200"  label="200" opacity="1"/>
                <ColorMapEntry color="#C8FD4C" quantity="600"  label="600" opacity="1"/>
                <ColorMapEntry color="#FEF536" quantity="1000" label="1000" opacity="1"/>
                
                <ColorMapEntry color="#FD9726" quantity="1400" label="1400" opacity="1" />
                <ColorMapEntry color="#FC581F" quantity="1800" label="1800" opacity="1" />
                <ColorMapEntry color="#F30F1A" quantity="2200" label="2200" opacity="1"/>
                <ColorMapEntry color="#AD080F" quantity="2600" label="2600" opacity="1"/>
  
                <ColorMapEntry color="#8A050A" quantity="3000" label="3000" opacity="1" />
          
            </ColorMap>
          </RasterSymbolizer>
        </Rule>
      </FeatureTypeStyle>
    </UserStyle>
  </NamedLayer>
</StyledLayerDescriptor>