<?xml version="1.0" encoding="ISO-8859-1"?>
<StyledLayerDescriptor version="1.0.0" 
    xsi:schemaLocation="http://www.opengis.net/sld StyledLayerDescriptor.xsd" 
    xmlns="http://www.opengis.net/sld" 
    xmlns:ogc="http://www.opengis.net/ogc" 
    xmlns:xlink="http://www.w3.org/1999/xlink" 
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <NamedLayer>
    <Name>salinity_surface_normalize</Name>
    <UserStyle>
      <Title>salinity_surface_normalize</Title>
      <FeatureTypeStyle>
        <Rule>
          <RasterSymbolizer>
            <ColorMap>
			<!--ColorMapEntry color="#040F8D" quantity="-32767" opacity="0" /-->
              
             
  
                <ColorMapEntry color="#0301C4" quantity="21700"  label="33.0" opacity="1"/>
                <ColorMapEntry color="#2A67FF" quantity="22000"  label="33.4" opacity="1"/>
                <ColorMapEntry color="#68BDFF" quantity="22300" label="33.9" opacity="1"/>
                <ColorMapEntry color="#93E7FE" quantity="22600" label="34.3" opacity="1"/>
     
                <ColorMapEntry color="#C3FDFF" quantity="22900" label="34.8" opacity="1" />
                <ColorMapEntry color="#FFFFFF" quantity="23200" label="35.2" opacity="1" />
                <ColorMapEntry color="#FEFC01" quantity="23500" label="35.7" opacity="1"/>
                <ColorMapEntry color="#FEC101" quantity="23800" label="36.1" opacity="1"/>
              
           <ColorMapEntry color="#FE6300" quantity="24100" label="36.6" opacity="1"/>
  
                <ColorMapEntry color="#E90401" quantity="24400" label="37.0" opacity="1" />
                 <ColorMapEntry color="#800100" quantity="24700" label="37.5" opacity="1" />
          
            </ColorMap>
          </RasterSymbolizer>
        </Rule>
      </FeatureTypeStyle>
    </UserStyle>
  </NamedLayer>
</StyledLayerDescriptor>