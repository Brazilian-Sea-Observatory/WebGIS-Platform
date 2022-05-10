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
			<ColorMapEntry color="#040F8D" quantity="-99" opacity="0"/>
              
              

                <ColorMapEntry color="#1461FB" quantity="0" label="0" opacity="1"/>
                <ColorMapEntry color="#24CCFD" quantity="400" label="400" opacity="1"/>
                <ColorMapEntry color="#2CFAFE" quantity="800" label="800" opacity="1"/>
                <ColorMapEntry color="#6EFD9B" quantity="1200"  label="1200" opacity="1"/>
                <ColorMapEntry color="#C8FD4C" quantity="1600"  label="1600" opacity="1"/>
                <ColorMapEntry color="#FEF536" quantity="2000" label="2000" opacity="1"/>
                
                <ColorMapEntry color="#FD9726" quantity="2400" label="2400" opacity="1" />
                <ColorMapEntry color="#FC581F" quantity="2800" label="2800" opacity="1" />
                <ColorMapEntry color="#F30F1A" quantity="3200" label="3200" opacity="1"/>
                <ColorMapEntry color="#AD080F" quantity="3600" label="3600" opacity="1"/>
  
                <ColorMapEntry color="#8A050A" quantity="4000" label="4000" opacity="1" />
          
            </ColorMap>
          </RasterSymbolizer>
        </Rule>
      </FeatureTypeStyle>
    </UserStyle>
  </NamedLayer>
</StyledLayerDescriptor>