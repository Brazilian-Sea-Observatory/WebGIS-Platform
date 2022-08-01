<?xml version="1.0" encoding="ISO-8859-1"?>
<StyledLayerDescriptor version="1.0.0"
                       xsi:schemaLocation="http://www.opengis.net/sld StyledLayerDescriptor.xsd"
                       xmlns="http://www.opengis.net/sld"
                       xmlns:ogc="http://www.opengis.net/ogc"
                       xmlns:xlink="http://www.w3.org/1999/xlink"
                       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <NamedLayer>
    <Name>currents</Name>
    <UserStyle>
      <Title>currents</Title>
      <FeatureTypeStyle>
        <Transformation>
          <ogc:Function name="ras:RasterAsPointCollection">
            <ogc:Function name="parameter">
              <ogc:Literal>data</ogc:Literal>
            </ogc:Function>
            <ogc:Function name="parameter">
              <ogc:Literal>interpolation</ogc:Literal>
              <ogc:Literal>InterpolationBilinear</ogc:Literal>
            </ogc:Function>
            <ogc:Function name="parameter">
              <ogc:Literal>scale</ogc:Literal>
              <ogc:Function name="Categorize">
                <ogc:Function name="env">
                  <ogc:Literal>wms_scale_denominator</ogc:Literal>
                </ogc:Function>

                <ogc:Literal>1</ogc:Literal>
                <ogc:Literal>50000</ogc:Literal>
                <ogc:Literal>0.4</ogc:Literal>
                <ogc:Literal>100000</ogc:Literal>
                <ogc:Literal>0.2</ogc:Literal>
                <ogc:Literal>500000</ogc:Literal>
                <ogc:Literal>0.1</ogc:Literal>
                <ogc:Literal>1000000</ogc:Literal>
                <ogc:Literal>0.05</ogc:Literal>
                <ogc:Literal>5000000</ogc:Literal>
                <ogc:Literal>0.024</ogc:Literal>
                <ogc:Literal>10000000</ogc:Literal>
                <ogc:Literal>0.012</ogc:Literal>
                <ogc:Literal>20000000</ogc:Literal>
                <ogc:Literal>0.006</ogc:Literal>
              </ogc:Function>
            </ogc:Function>
          </ogc:Function>
        </Transformation>
        <Rule>
          <Title>Heading</Title>
                    <ogc:Filter>
            <ogc:And>
              <ogc:PropertyIsNotEqualTo>
                <ogc:PropertyName>u</ogc:PropertyName>
                <ogc:Literal>0.0</ogc:Literal>
              </ogc:PropertyIsNotEqualTo>
              <ogc:PropertyIsNotEqualTo>
                <ogc:PropertyName>v</ogc:PropertyName>
                <ogc:Literal>0.0</ogc:Literal>
              </ogc:PropertyIsNotEqualTo>
            </ogc:And>
          </ogc:Filter>
          <PointSymbolizer>
            <Graphic>
              <Mark>
                <WellKnownName>extshape://narrow</WellKnownName>
                <Fill>
                  <CssParameter name="fill">
                    
                    <ogc:Function name="Categorize">
                      <ogc:Function name="sqrt">
                        <ogc:Add>
                          <ogc:Mul>
                            <ogc:PropertyName>u</ogc:PropertyName>
                            <ogc:PropertyName>u</ogc:PropertyName>
                          </ogc:Mul>
                          <ogc:Mul>
                            <ogc:PropertyName>v</ogc:PropertyName>
                            <ogc:PropertyName>v</ogc:PropertyName>
                          </ogc:Mul>
                        </ogc:Add>
                      </ogc:Function>
                      <ogc:Literal>#000000</ogc:Literal>
                      <ogc:Literal>0.3</ogc:Literal>
                      <ogc:Literal>#000000</ogc:Literal>
                      <ogc:Literal>0.2</ogc:Literal>
                      <ogc:Literal>#000000</ogc:Literal>
                      <ogc:Literal>0.1</ogc:Literal>
                      <ogc:Literal>#000000</ogc:Literal>
                      <ogc:Literal>0.05</ogc:Literal>
                      <ogc:Literal>#000000</ogc:Literal>
                      <ogc:Literal>0.02</ogc:Literal>
                      <ogc:Literal>#000000</ogc:Literal>
                    </ogc:Function>
                  </CssParameter>
                </Fill>
              </Mark>

              <Rotation>
                <ogc:Function name="toDegrees">
                  <ogc:Function name="atan2">
                    <ogc:PropertyName>u</ogc:PropertyName>
                    <ogc:PropertyName>v</ogc:PropertyName>
                  </ogc:Function>
                </ogc:Function>
              </Rotation>
            </Graphic>
          </PointSymbolizer>
        </Rule>
      </FeatureTypeStyle>
    </UserStyle>
  </NamedLayer>
</StyledLayerDescriptor>