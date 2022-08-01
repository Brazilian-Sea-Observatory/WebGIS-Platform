<?xml version="1.0" encoding="ISO-8859-1"?>
<StyledLayerDescriptor version="1.0.0" 
                       xsi:schemaLocation="http://www.opengis.net/sld StyledLayerDescriptor.xsd" 
                       xmlns="http://www.opengis.net/sld" 
                       xmlns:ogc="http://www.opengis.net/ogc" 
                       xmlns:xlink="http://www.w3.org/1999/xlink" 
                       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <NamedLayer>
    <Name>nitrate_mol</Name>
    <UserStyle>
      <Title>nitrate_mol</Title>
      <FeatureTypeStyle>
        <Rule>
          <RasterSymbolizer>
            <ColorMap>
                   <!--ColorMapEntry color="#EDB8FD" quantity="160" label="0" opacity="0" /-->
               
              <ColorMapEntry color="#F1CDF1" quantity="180" label="180" opacity="1" />
              <ColorMapEntry color="#E7A7E7" quantity="200" label="200" opacity="1"/>
              <ColorMapEntry color="#B175D6" quantity="220" label="220" opacity="1"/>
              <ColorMapEntry color="#466BE5" quantity="240" label="240" opacity="1"/>
              <ColorMapEntry color="#7CCCE6" quantity="260" label="260" opacity="1"/>

              <ColorMapEntry color="#50C483" quantity="280" label="280" opacity="1"/>
              <ColorMapEntry color="#2CD937" quantity="300" label="300" opacity="1"/>
              <ColorMapEntry color="#9AD961" quantity="320" label="320" opacity="1"/>
              <ColorMapEntry color="#F4DD32" quantity="340" label="340" opacity="1"/>
              <ColorMapEntry color="#F39127" quantity="360" label="360" opacity="1"/>
              <ColorMapEntry color="#EF4127" quantity="380" label="380" opacity="1"/>
              <ColorMapEntry color="#FD8C7D" quantity="400" label="400" opacity="1"/>
              <ColorMapEntry color="#FED7A8" quantity="420" label="420" opacity="1"/>


            </ColorMap>
          </RasterSymbolizer>
        </Rule>
      </FeatureTypeStyle>
    </UserStyle>
  </NamedLayer>
</StyledLayerDescriptor>