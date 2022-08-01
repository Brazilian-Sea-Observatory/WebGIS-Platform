<?xml version="1.0" encoding="ISO-8859-1"?>
<StyledLayerDescriptor version="1.0.0" 
                       xsi:schemaLocation="http://www.opengis.net/sld StyledLayerDescriptor.xsd" 
                       xmlns="http://www.opengis.net/sld" 
                       xmlns:ogc="http://www.opengis.net/ogc" 
                       xmlns:xlink="http://www.w3.org/1999/xlink" 
                       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <NamedLayer>
    <Name>silicate_mol</Name>
    <UserStyle>
      <Title>silicate_mol</Title>
      <FeatureTypeStyle>
        <Rule>
          <RasterSymbolizer>
            <ColorMap>
              <!--ColorMapEntry color="#342D85" quantity="-1"  opacity="0" /-->

              <ColorMapEntry color="#342D85" quantity="0" label="0" opacity="1" />
              <ColorMapEntry color="#126ADD" quantity="25" label="25" opacity="1"/>
              <ColorMapEntry color="#3087D2" quantity="50" label="50" opacity="1"/>
              <ColorMapEntry color="#1DA6C4" quantity="75" label="75" opacity="1"/>
              <ColorMapEntry color="#3FB89E" quantity="100" label="100" opacity="1"/>


              <ColorMapEntry color="#94BC74" quantity="125" label="125" opacity="1"/>
              <ColorMapEntry color="#E0B859" quantity="150" label="150" opacity="1"/>
              <ColorMapEntry color="#FEC645" quantity="175" label="175" opacity="1"/>
              <ColorMapEntry color="#F8FA3A" quantity="200" label="200" opacity="1"/>


            </ColorMap>
          </RasterSymbolizer>
        </Rule>
      </FeatureTypeStyle>
    </UserStyle>
  </NamedLayer>
</StyledLayerDescriptor>