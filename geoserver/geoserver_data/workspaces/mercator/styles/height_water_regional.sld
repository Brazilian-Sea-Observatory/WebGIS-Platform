<?xml version="1.0" encoding="ISO-8859-1"?>
<StyledLayerDescriptor version="1.0.0" 
    xsi:schemaLocation="http://www.opengis.net/sld StyledLayerDescriptor.xsd" 
    xmlns="http://www.opengis.net/sld" 
    xmlns:ogc="http://www.opengis.net/ogc" 
    xmlns:xlink="http://www.w3.org/1999/xlink" 
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <NamedLayer>
    <Name>height_water_regional</Name>
    <UserStyle>
      <Title>height_water_regional</Title>
      <FeatureTypeStyle>
        <Rule>
          <RasterSymbolizer>
            <ColorMap>
   				<ColorMapEntry color="#32aac5" quantity="-0.5" label="-0.5"/>
   				<ColorMapEntry color="#63a5b6" quantity="-0.4" label="-0.4"/>
   				<ColorMapEntry color="#80a0a6" quantity="-0.3" label="-0.3"/>
   				<ColorMapEntry color="#959b97" quantity="-0.2" label="-0.2"/>
                <ColorMapEntry color="#a79588" quantity="-0.1" label="-0.1"/>
              	<ColorMapEntry color="#b59079" quantity="0.0" label="0.0"/>
              	<ColorMapEntry color="#c38a6a" quantity="0.1" label="0.1"/>
              	<ColorMapEntry color="#ce835b" quantity="0.2" label="0.2"/>
              	<ColorMapEntry color="#d97c4b" quantity="0.3" label="0.3"/>
              	<ColorMapEntry color="#e3753b" quantity="0.4" label="0.4"/>
              	<ColorMapEntry color="#ec6d29" quantity="0.5" label="0.5"/>
            </ColorMap>
          </RasterSymbolizer>
        </Rule>
      </FeatureTypeStyle>
    </UserStyle>
  </NamedLayer>
</StyledLayerDescriptor>