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
              
              
              <ColorMapEntry color="#040F8D" quantity="0.0002" label="0.0002" opacity="1" />
              <ColorMapEntry color="#0818BC" quantity="0.0006" label="0.0006" opacity="1" />
              <ColorMapEntry color="#0F24FB" quantity="0.0010" label="0.0010" opacity="1"/>
              <ColorMapEntry color="#1139FB" quantity="0.0014" label="0.0014" opacity="1"/>
                <ColorMapEntry color="#1461FB" quantity="0.0018" label="0.0018" opacity="1"/>
                <ColorMapEntry color="#24CCFD" quantity="0.0022" label="0.0022" opacity="1"/>
                <ColorMapEntry color="#2CFAFE" quantity="0.0026" label="0.0026" opacity="1"/>
                <ColorMapEntry color="#6EFD9B" quantity="0.0030"  label="0.0030" opacity="1"/>
                <ColorMapEntry color="#C8FD4C" quantity="0.0034"  label="0.0034" opacity="1"/>
                <ColorMapEntry color="#FEF536" quantity="0.0038" label="0.0038" opacity="1"/>
                
                <ColorMapEntry color="#FD9726" quantity="0.0042" label="0.0042" opacity="1" />
                <ColorMapEntry color="#FC581F" quantity="0.0046" label="0.0046" opacity="1" />
                <ColorMapEntry color="#F30F1A" quantity="0.0050" label="0.0050" opacity="1"/>
                <ColorMapEntry color="#AD080F" quantity="0.0054" label="0.0054" opacity="1"/>
  
                <ColorMapEntry color="#8A050A" quantity="0.0058" label="0.0058" opacity="1" />
          
            </ColorMap>
          </RasterSymbolizer>
        </Rule>
      </FeatureTypeStyle>
    </UserStyle>
  </NamedLayer>
</StyledLayerDescriptor>