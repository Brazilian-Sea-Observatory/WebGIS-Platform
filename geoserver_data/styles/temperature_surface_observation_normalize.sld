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

            <ColorMapEntry color="#0300BB" quantity="-400" label="-4" opacity="1" />
        <ColorMapEntry color="#0300BB" quantity="-200" label="-2" opacity="1" />
              <ColorMapEntry color="#0C33FF" quantity="0" label="0" opacity="1" />
              <ColorMapEntry color="#388AFE" quantity="200" label="2" opacity="1"/>
              <ColorMapEntry color="#60B6FF" quantity="400" label="4" opacity="1"/>
                <ColorMapEntry color="#7ED4FF" quantity="600" label="6" opacity="1"/>
                <ColorMapEntry color="#99EDFF" quantity="800" label="8" opacity="1"/>
                <ColorMapEntry color="#B7F8FF" quantity="1000" label="10" opacity="1"/>
                <ColorMapEntry color="#D9FFFF" quantity="1200"  label="12" opacity="1"/>
                <ColorMapEntry color="#FFFFFF" quantity="1400"  label="14" opacity="1"/>
                <ColorMapEntry color="#FEFF53" quantity="1600" label="16" opacity="1"/>
                <ColorMapEntry color="#FFEF02" quantity="1800" label="18" opacity="1"/>
     
                <ColorMapEntry color="#FECD02" quantity="2000" label="20" opacity="1" />
                <ColorMapEntry color="#FF9500" quantity="2200" label="22" opacity="1" />
                <ColorMapEntry color="#FF4D00" quantity="2400" label="24" opacity="1"/>
                <ColorMapEntry color="#FC0501" quantity="2600" label="26" opacity="1"/>
              
           <ColorMapEntry color="#CB0200" quantity="2800" label="28" opacity="1"/>
  
                <ColorMapEntry color="#C00201" quantity="3000" label="30" opacity="1" />
                 <ColorMapEntry color="#800100" quantity="3200" label="32" opacity="1" />
                 <ColorMapEntry color="#560000" quantity="3400" label="34" opacity="1" />
                 <ColorMapEntry color="#300000" quantity="3600" label="36" opacity="1" />


            </ColorMap>
          </RasterSymbolizer>
        </Rule>
      </FeatureTypeStyle>
    </UserStyle>
  </NamedLayer>
</StyledLayerDescriptor>