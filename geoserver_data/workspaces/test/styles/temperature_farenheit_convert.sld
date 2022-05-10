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
      <ColorMapEntry color="#0300BB" quantity="2840" label="-2" opacity="1" />

              <ColorMapEntry color="#0C33FF" quantity="3200" label="0" opacity="1" />
              <ColorMapEntry color="#388AFE" quantity="3560" label="2" opacity="1"/>
              <ColorMapEntry color="#60B6FF" quantity="3920" label="4" opacity="1"/>
                <ColorMapEntry color="#7ED4FF" quantity="4280" label="6" opacity="1"/>
                <ColorMapEntry color="#99EDFF" quantity="4640" label="8" opacity="1"/>
                <ColorMapEntry color="#B7F8FF" quantity="5000" label="10" opacity="1"/>
                <ColorMapEntry color="#D9FFFF" quantity="5360"  label="12" opacity="1"/>
                <ColorMapEntry color="#FFFFFF" quantity="5720"  label="14" opacity="1"/>
                <ColorMapEntry color="#FEFF53" quantity="6080" label="16" opacity="1"/>
                <ColorMapEntry color="#FFEF02" quantity="6440" label="18" opacity="1"/>
     
                <ColorMapEntry color="#FECD02" quantity="6880" label="20" opacity="1" />
                <ColorMapEntry color="#FF9500" quantity="7160" label="22" opacity="1" />
                <ColorMapEntry color="#FF4D00" quantity="7520" label="24" opacity="1"/>
                <ColorMapEntry color="#FC0501" quantity="7880" label="26" opacity="1"/>
              
           <ColorMapEntry color="#CB0200" quantity="8240" label="28" opacity="1"/>
  
                <ColorMapEntry color="#C00201" quantity="8600" label="30" opacity="1" />
                 <ColorMapEntry color="#800100" quantity="8960" label="32" opacity="1" />
                 <ColorMapEntry color="#560000" quantity="9320" label="34" opacity="1" />
                 <ColorMapEntry color="#300000" quantity="9680" label="36" opacity="1" />
            </ColorMap>
          </RasterSymbolizer>
        </Rule>
      </FeatureTypeStyle>
    </UserStyle>
  </NamedLayer>
</StyledLayerDescriptor>