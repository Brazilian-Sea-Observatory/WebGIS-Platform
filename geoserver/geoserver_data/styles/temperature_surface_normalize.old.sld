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
              <ColorMapEntry color="#040F8D" quantity="-32767" opacity="0" />
 <!--ColorMapEntry color="#030082" quantity="-2000" label="-5" opacity="1" /-->


           <ColorMapEntry color="#0300BB" quantity="-960" label="-3.0" opacity="1" />
              <ColorMapEntry color="#282cc7" quantity="-480" label="-1.5" opacity="1" />
              <ColorMapEntry color="#4d58d2" quantity="0" label="0.0" opacity="1"/>
              <ColorMapEntry color="#7284de" quantity="480" label="1.5" opacity="1"/>
              <ColorMapEntry color="#7284de" quantity="960" label="3.0" opacity="1"/>
                <ColorMapEntry color="#97b0ea" quantity="1440" label="4.5" opacity="1"/>
                <ColorMapEntry color="#bbdcf6" quantity="1920" label="6.0" opacity="1"/>
                <ColorMapEntry color="#daffff" quantity="2400" label="7.5" opacity="1"/>
                <ColorMapEntry color="#e1ffff" quantity="2880"  label="9.0" opacity="1"/>
                <ColorMapEntry color="#e7ffff" quantity="3360"  label="10.5" opacity="1"/>
                <ColorMapEntry color="#eeffff" quantity="3840" label="12.0" opacity="1"/>
                <ColorMapEntry color="#f5ffff" quantity="4320" label="13.5" opacity="1"/>
     
                <ColorMapEntry color="#fbffff" quantity="4800" label="15.0" opacity="1" />
                <ColorMapEntry color="#fff8ed" quantity="5280" label="16.5" opacity="1" />
                <ColorMapEntry color="#ffe5c1" quantity="5760" label="18.0" opacity="1"/>
                <ColorMapEntry color="#ffd395" quantity="6240" label="19.5" opacity="1"/>
              
           <ColorMapEntry color="#ffc16a" quantity="6720" label="21.0" opacity="1"/>
  
                <ColorMapEntry color="#ffaf3e" quantity="7200" label="22.5" opacity="1" />
                 <ColorMapEntry color="#ff9c12" quantity="7680" label="24.0" opacity="1" />
                 <ColorMapEntry color="#ff8600" quantity="8160" label="25.5" opacity="1" />
                 <ColorMapEntry color="#fe6d00" quantity="8640" label="27.0" opacity="1" />


                <ColorMapEntry color="#fe5400" quantity="9120" label="28.5" opacity="1" />
                 <ColorMapEntry color="#fd3c01" quantity="9600" label="30.0" opacity="1" />
                 <ColorMapEntry color="#fd2301" quantity="10080" label="31.5" opacity="1" />
                 <ColorMapEntry color="#fc0a01" quantity="10560" label="33.0" opacity="1" />

             <ColorMapEntry color="#eb0401" quantity="11040" label="34.5" opacity="1"/>
  
                <ColorMapEntry color="#d60401" quantity="11520" label="36.0" opacity="1" />
                 <ColorMapEntry color="#c00301" quantity="12000" label="37.5" opacity="1" />
           <ColorMapEntry color="#950200" quantity="12480" label="39.0" opacity="1" />
  
            </ColorMap>
          </RasterSymbolizer>
        </Rule>
      </FeatureTypeStyle>
    </UserStyle>
  </NamedLayer>
</StyledLayerDescriptor>