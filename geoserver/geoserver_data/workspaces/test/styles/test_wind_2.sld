<StyledLayerDescriptor version="1.0.0"
                       xmlns="http://www.opengis.net/sld" xmlns:gml="http://www.opengis.net/gml"
                       xmlns:ogc="http://www.opengis.net/ogc" xmlns:xlink="http://www.w3.org/1999/xlink"
                       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                       xsi:schemaLocation="http://www.opengis.net/sld ./StyledLayerDescriptor.xsd">
  <NamedLayer>
    <Name>contour_lines</Name>
    <UserStyle>
      <FeatureTypeStyle>
        <Transformation>
          <ogc:Function name="gs:RasterAsPointCollection">
            <ogc:Function name="parameter">
              <ogc:Literal>data</ogc:Literal>
            </ogc:Function>
          </ogc:Function>
        </Transformation>


         <Rule>
          <Name>NaN</Name>
          <Title>NaN</Title>
          <ogc:Filter>
            <ogc:And>
              <ogc:PropertyIsEqualThan>
                <ogc:Function name="sqrt">
                  <ogc:Add>
                    <ogc:Mul>
                      <ogc:PropertyName>U</ogc:PropertyName>
                      <ogc:PropertyName>U</ogc:PropertyName>
                    </ogc:Mul>
                    <ogc:Mul>
                      <ogc:PropertyName>V</ogc:PropertyName>
                      <ogc:PropertyName>V</ogc:PropertyName>
                    </ogc:Mul>
                  </ogc:Add>
                </ogc:Function>
                <ogc:Literal>NaN</ogc:Literal>
              </ogc:PropertyIsEqualThan>
        <ogc:PropertyIsEqualThan>
                <ogc:Function name="sqrt">
                  <ogc:Add>
                    <ogc:Mul>
                      <ogc:PropertyName>U</ogc:PropertyName>
                      <ogc:PropertyName>U</ogc:PropertyName>
                    </ogc:Mul>
                    <ogc:Mul>
                      <ogc:PropertyName>V</ogc:PropertyName>
                      <ogc:PropertyName>V</ogc:PropertyName>
                    </ogc:Mul>
                  </ogc:Add>
                </ogc:Function>
                <ogc:Literal>NaN</ogc:Literal>
              </ogc:PropertyIsEqualThan>
            </ogc:And>
          </ogc:Filter>
          <TextSymbolizer>
            <Label><![CDATA[ ]]></Label> <!-- fake label -->
            <Graphic>
              <Mark>
                <WellKnownName>extshape://narrow</WellKnownName>
                <Fill>
                  <CssParameter name="fill">#08A8E7</CssParameter>
                </Fill>
 <Stroke>
            <CssParameter name="stroke">#000000</CssParameter>
            <CssParameter name="stroke-width">1</CssParameter>
          </Stroke>
              </Mark>
              <Size>4</Size>
              <Rotation>
                <ogc:Add>
                  <ogc:Function name="toDegrees">
                    <ogc:Function name="atan2">
                      <ogc:PropertyName>U</ogc:PropertyName>
                      <ogc:PropertyName>V</ogc:PropertyName>
                    </ogc:Function>
                  </ogc:Function>
                  <ogc:Literal>0</ogc:Literal>
                </ogc:Add>
              </Rotation>
            </Graphic>
            <Priority>
              <ogc:Add>
                <ogc:Mul>
                  <ogc:PropertyName>U</ogc:PropertyName>
                  <ogc:PropertyName>U</ogc:PropertyName>
                </ogc:Mul>
                <ogc:Mul>
                  <ogc:PropertyName>V</ogc:PropertyName>
                  <ogc:PropertyName>V</ogc:PropertyName>
                </ogc:Mul>
              </ogc:Add>
            </Priority>
            <VendorOption name="conflictResolution">false</VendorOption>
          </TextSymbolizer> 
        </Rule>
  
        <Rule>
          <Name>0 to 2</Name>
          <Title>0 to 2</Title>
          <ogc:Filter>
            <ogc:And>
              <ogc:PropertyIsLessThan>
                <ogc:Function name="sqrt">
                  <ogc:Add>
                    <ogc:Mul>
                      <ogc:PropertyName>U</ogc:PropertyName>
                      <ogc:PropertyName>U</ogc:PropertyName>
                    </ogc:Mul>
                    <ogc:Mul>
                      <ogc:PropertyName>V</ogc:PropertyName>
                      <ogc:PropertyName>V</ogc:PropertyName>
                    </ogc:Mul>
                  </ogc:Add>
                </ogc:Function>
                <ogc:Literal>2</ogc:Literal>
              </ogc:PropertyIsLessThan>
            </ogc:And>
          </ogc:Filter>
          <TextSymbolizer>
            <Label><![CDATA[ ]]></Label> <!-- fake label -->
            <Graphic>
              <Mark>
                <WellKnownName>extshape://narrow</WellKnownName>
                <Fill>
                  <CssParameter name="fill">#004A6</CssParameter>
                </Fill>
 <Stroke>
            <CssParameter name="stroke">#000000</CssParameter>
            <CssParameter name="stroke-width">1</CssParameter>
          </Stroke>
              </Mark>
              <Size>4</Size>
              <Rotation>
                <ogc:Add>
                  <ogc:Function name="toDegrees">
                    <ogc:Function name="atan2">
                      <ogc:PropertyName>U</ogc:PropertyName>
                      <ogc:PropertyName>V</ogc:PropertyName>
                    </ogc:Function>
                  </ogc:Function>
                  <ogc:Literal>0</ogc:Literal>
                </ogc:Add>
              </Rotation>
            </Graphic>
            <Priority>
              <ogc:Add>
                <ogc:Mul>
                  <ogc:PropertyName>U</ogc:PropertyName>
                  <ogc:PropertyName>U</ogc:PropertyName>
                </ogc:Mul>
                <ogc:Mul>
                  <ogc:PropertyName>V</ogc:PropertyName>
                  <ogc:PropertyName>V</ogc:PropertyName>
                </ogc:Mul>
              </ogc:Add>
            </Priority>
            <VendorOption name="conflictResolution">false</VendorOption>
          </TextSymbolizer> 
        </Rule>


        <Rule>
          <Name>moderado</Name>
          <Title>2 to 4</Title>
          <ogc:Filter>
            <ogc:And>
              <ogc:PropertyIsLessThan>
                <ogc:Function name="sqrt">
                  <ogc:Add>
                    <ogc:Mul>
                      <ogc:PropertyName>U</ogc:PropertyName>
                      <ogc:PropertyName>U</ogc:PropertyName>
                    </ogc:Mul>
                    <ogc:Mul>
                      <ogc:PropertyName>V</ogc:PropertyName>
                      <ogc:PropertyName>V</ogc:PropertyName>
                    </ogc:Mul>
                  </ogc:Add>
                </ogc:Function>
                <ogc:Literal>4</ogc:Literal>
              </ogc:PropertyIsLessThan>
        <ogc:PropertyIsGreaterThanOrEqualTo>
                <ogc:Function name="sqrt">
                  <ogc:Add>
                    <ogc:Mul>
                      <ogc:PropertyName>U</ogc:PropertyName>
                      <ogc:PropertyName>U</ogc:PropertyName>
                    </ogc:Mul>
                    <ogc:Mul>
                      <ogc:PropertyName>V</ogc:PropertyName>
                      <ogc:PropertyName>V</ogc:PropertyName>
                    </ogc:Mul>
                  </ogc:Add>
                </ogc:Function>
                <ogc:Literal>2</ogc:Literal>
              </ogc:PropertyIsGreaterThanOrEqualTo>
            </ogc:And>
          </ogc:Filter>
          <TextSymbolizer>
            <Label><![CDATA[ ]]></Label> <!-- fake label -->
            <Graphic>
              <Mark>
                <WellKnownName>extshape://narrow</WellKnownName>
                <Fill>
                  <CssParameter name="fill">#0043BF</CssParameter>
                </Fill>
 <Stroke>
            <CssParameter name="stroke">#000000</CssParameter>
            <CssParameter name="stroke-width">1</CssParameter>
          </Stroke>
              </Mark>
              <Size>4</Size>
              <Rotation>
                <ogc:Add>
                  <ogc:Function name="toDegrees">
                    <ogc:Function name="atan2">
                      <ogc:PropertyName>U</ogc:PropertyName>
                      <ogc:PropertyName>V</ogc:PropertyName>
                    </ogc:Function>
                  </ogc:Function>
                  <ogc:Literal>0</ogc:Literal>
                </ogc:Add>
              </Rotation>
            </Graphic>
            <Priority>
              <ogc:Add>
                <ogc:Mul>
                  <ogc:PropertyName>U</ogc:PropertyName>
                  <ogc:PropertyName>U</ogc:PropertyName>
                </ogc:Mul>
                <ogc:Mul>
                  <ogc:PropertyName>V</ogc:PropertyName>
                  <ogc:PropertyName>V</ogc:PropertyName>
                </ogc:Mul>
              </ogc:Add>
            </Priority>
            <VendorOption name="conflictResolution">false</VendorOption>
          </TextSymbolizer> 
        </Rule>

        <Rule>
          <Name>moderado</Name>
          <Title>4 to 6</Title>
          <ogc:Filter>
            <ogc:And>
              <ogc:PropertyIsLessThan>
                <ogc:Function name="sqrt">
                  <ogc:Add>
                    <ogc:Mul>
                      <ogc:PropertyName>U</ogc:PropertyName>
                      <ogc:PropertyName>U</ogc:PropertyName>
                    </ogc:Mul>
                    <ogc:Mul>
                      <ogc:PropertyName>V</ogc:PropertyName>
                      <ogc:PropertyName>V</ogc:PropertyName>
                    </ogc:Mul>
                  </ogc:Add>
                </ogc:Function>
                <ogc:Literal>6</ogc:Literal>
              </ogc:PropertyIsLessThan>
        <ogc:PropertyIsGreaterThanOrEqualTo>
                <ogc:Function name="sqrt">
                  <ogc:Add>
                    <ogc:Mul>
                      <ogc:PropertyName>U</ogc:PropertyName>
                      <ogc:PropertyName>U</ogc:PropertyName>
                    </ogc:Mul>
                    <ogc:Mul>
                      <ogc:PropertyName>V</ogc:PropertyName>
                      <ogc:PropertyName>V</ogc:PropertyName>
                    </ogc:Mul>
                  </ogc:Add>
                </ogc:Function>
                <ogc:Literal>4</ogc:Literal>
              </ogc:PropertyIsGreaterThanOrEqualTo>
            </ogc:And>
          </ogc:Filter>
          <TextSymbolizer>
            <Label><![CDATA[ ]]></Label> <!-- fake label -->
            <Graphic>
              <Mark>
                <WellKnownName>extshape://narrow</WellKnownName>
                <Fill>
                  <CssParameter name="fill">#0073DB</CssParameter>
                </Fill>
 <Stroke>
            <CssParameter name="stroke">#000000</CssParameter>
            <CssParameter name="stroke-width">1</CssParameter>
          </Stroke>
              </Mark>
              <Size>4</Size>
              <Rotation>
                <ogc:Add>
                  <ogc:Function name="toDegrees">
                    <ogc:Function name="atan2">
                      <ogc:PropertyName>U</ogc:PropertyName>
                      <ogc:PropertyName>V</ogc:PropertyName>
                    </ogc:Function>
                  </ogc:Function>
                  <ogc:Literal>0</ogc:Literal>
                </ogc:Add>
              </Rotation>
            </Graphic>
            <Priority>
              <ogc:Add>
                <ogc:Mul>
                  <ogc:PropertyName>U</ogc:PropertyName>
                  <ogc:PropertyName>U</ogc:PropertyName>
                </ogc:Mul>
                <ogc:Mul>
                  <ogc:PropertyName>V</ogc:PropertyName>
                  <ogc:PropertyName>V</ogc:PropertyName>
                </ogc:Mul>
              </ogc:Add>
            </Priority>
            <VendorOption name="conflictResolution">false</VendorOption>
          </TextSymbolizer> 
        </Rule>


        <Rule>
          <Name>moderado</Name>
          <Title>6 to 8</Title>
          <ogc:Filter>
            <ogc:And>
              <ogc:PropertyIsLessThan>
                <ogc:Function name="sqrt">
                  <ogc:Add>
                    <ogc:Mul>
                      <ogc:PropertyName>U</ogc:PropertyName>
                      <ogc:PropertyName>U</ogc:PropertyName>
                    </ogc:Mul>
                    <ogc:Mul>
                      <ogc:PropertyName>V</ogc:PropertyName>
                      <ogc:PropertyName>V</ogc:PropertyName>
                    </ogc:Mul>
                  </ogc:Add>
                </ogc:Function>
                <ogc:Literal>8</ogc:Literal>
              </ogc:PropertyIsLessThan>
        <ogc:PropertyIsGreaterThanOrEqualTo>
                <ogc:Function name="sqrt">
                  <ogc:Add>
                    <ogc:Mul>
                      <ogc:PropertyName>U</ogc:PropertyName>
                      <ogc:PropertyName>U</ogc:PropertyName>
                    </ogc:Mul>
                    <ogc:Mul>
                      <ogc:PropertyName>V</ogc:PropertyName>
                      <ogc:PropertyName>V</ogc:PropertyName>
                    </ogc:Mul>
                  </ogc:Add>
                </ogc:Function>
                <ogc:Literal>6</ogc:Literal>
              </ogc:PropertyIsGreaterThanOrEqualTo>
            </ogc:And>
          </ogc:Filter>
          <TextSymbolizer>
            <Label><![CDATA[ ]]></Label> <!-- fake label -->
            <Graphic>
              <Mark>
                <WellKnownName>extshape://narrow</WellKnownName>
                <Fill>
                  <CssParameter name="fill">#08A8E7</CssParameter>
                </Fill>
 <Stroke>
            <CssParameter name="stroke">#000000</CssParameter>
            <CssParameter name="stroke-width">1</CssParameter>
          </Stroke>
              </Mark>
              <Size>4</Size>
              <Rotation>
                <ogc:Add>
                  <ogc:Function name="toDegrees">
                    <ogc:Function name="atan2">
                      <ogc:PropertyName>U</ogc:PropertyName>
                      <ogc:PropertyName>V</ogc:PropertyName>
                    </ogc:Function>
                  </ogc:Function>
                  <ogc:Literal>0</ogc:Literal>
                </ogc:Add>
              </Rotation>
            </Graphic>
            <Priority>
              <ogc:Add>
                <ogc:Mul>
                  <ogc:PropertyName>U</ogc:PropertyName>
                  <ogc:PropertyName>U</ogc:PropertyName>
                </ogc:Mul>
                <ogc:Mul>
                  <ogc:PropertyName>V</ogc:PropertyName>
                  <ogc:PropertyName>V</ogc:PropertyName>
                </ogc:Mul>
              </ogc:Add>
            </Priority>
            <VendorOption name="conflictResolution">false</VendorOption>
          </TextSymbolizer> 
        </Rule>


        <Rule>
          <Name>moderado</Name>
          <Title>8 to 10</Title>
          <ogc:Filter>
            <ogc:And>
              <ogc:PropertyIsLessThan>
                <ogc:Function name="sqrt">
                  <ogc:Add>
                    <ogc:Mul>
                      <ogc:PropertyName>U</ogc:PropertyName>
                      <ogc:PropertyName>U</ogc:PropertyName>
                    </ogc:Mul>
                    <ogc:Mul>
                      <ogc:PropertyName>V</ogc:PropertyName>
                      <ogc:PropertyName>V</ogc:PropertyName>
                    </ogc:Mul>
                  </ogc:Add>
                </ogc:Function>
                <ogc:Literal>10</ogc:Literal>
              </ogc:PropertyIsLessThan>
        <ogc:PropertyIsGreaterThanOrEqualTo>
                <ogc:Function name="sqrt">
                  <ogc:Add>
                    <ogc:Mul>
                      <ogc:PropertyName>U</ogc:PropertyName>
                      <ogc:PropertyName>U</ogc:PropertyName>
                    </ogc:Mul>
                    <ogc:Mul>
                      <ogc:PropertyName>V</ogc:PropertyName>
                      <ogc:PropertyName>V</ogc:PropertyName>
                    </ogc:Mul>
                  </ogc:Add>
                </ogc:Function>
                <ogc:Literal>8</ogc:Literal>
              </ogc:PropertyIsGreaterThanOrEqualTo>
            </ogc:And>
          </ogc:Filter>
          <TextSymbolizer>
            <Label><![CDATA[ ]]></Label> <!-- fake label -->
            <Graphic>
              <Mark>
                <WellKnownName>extshape://narrow</WellKnownName>
                <Fill>
                  <CssParameter name="fill">#61C87D</CssParameter>
                </Fill>
 <Stroke>
            <CssParameter name="stroke">#000000</CssParameter>
            <CssParameter name="stroke-width">1</CssParameter>
          </Stroke>
              </Mark>
              <Size>4</Size>
              <Rotation>
                <ogc:Add>
                  <ogc:Function name="toDegrees">
                    <ogc:Function name="atan2">
                      <ogc:PropertyName>U</ogc:PropertyName>
                      <ogc:PropertyName>V</ogc:PropertyName>
                    </ogc:Function>
                  </ogc:Function>
                  <ogc:Literal>0</ogc:Literal>
                </ogc:Add>
              </Rotation>
            </Graphic>
            <Priority>
              <ogc:Add>
                <ogc:Mul>
                  <ogc:PropertyName>U</ogc:PropertyName>
                  <ogc:PropertyName>U</ogc:PropertyName>
                </ogc:Mul>
                <ogc:Mul>
                  <ogc:PropertyName>V</ogc:PropertyName>
                  <ogc:PropertyName>V</ogc:PropertyName>
                </ogc:Mul>
              </ogc:Add>
            </Priority>
            <VendorOption name="conflictResolution">false</VendorOption>
          </TextSymbolizer> 
        </Rule>



        <Rule>
          <Name>moderado</Name>
          <Title>10 to 12</Title>
          <ogc:Filter>
            <ogc:And>
              <ogc:PropertyIsLessThan>
                <ogc:Function name="sqrt">
                  <ogc:Add>
                    <ogc:Mul>
                      <ogc:PropertyName>U</ogc:PropertyName>
                      <ogc:PropertyName>U</ogc:PropertyName>
                    </ogc:Mul>
                    <ogc:Mul>
                      <ogc:PropertyName>V</ogc:PropertyName>
                      <ogc:PropertyName>V</ogc:PropertyName>
                    </ogc:Mul>
                  </ogc:Add>
                </ogc:Function>
                <ogc:Literal>12</ogc:Literal>
              </ogc:PropertyIsLessThan>
        <ogc:PropertyIsGreaterThanOrEqualTo>
                <ogc:Function name="sqrt">
                  <ogc:Add>
                    <ogc:Mul>
                      <ogc:PropertyName>U</ogc:PropertyName>
                      <ogc:PropertyName>U</ogc:PropertyName>
                    </ogc:Mul>
                    <ogc:Mul>
                      <ogc:PropertyName>V</ogc:PropertyName>
                      <ogc:PropertyName>V</ogc:PropertyName>
                    </ogc:Mul>
                  </ogc:Add>
                </ogc:Function>
                <ogc:Literal>10</ogc:Literal>
              </ogc:PropertyIsGreaterThanOrEqualTo>
            </ogc:And>
          </ogc:Filter>
          <TextSymbolizer>
            <Label><![CDATA[ ]]></Label> <!-- fake label -->
            <Graphic>
              <Mark>
                <WellKnownName>extshape://narrow</WellKnownName>
                <Fill>
                  <CssParameter name="fill">#CBE207</CssParameter>
                </Fill>
 <Stroke>
            <CssParameter name="stroke">#000000</CssParameter>
            <CssParameter name="stroke-width">1</CssParameter>
          </Stroke>
              </Mark>
              <Size>4</Size>
              <Rotation>
                <ogc:Add>
                  <ogc:Function name="toDegrees">
                    <ogc:Function name="atan2">
                      <ogc:PropertyName>U</ogc:PropertyName>
                      <ogc:PropertyName>V</ogc:PropertyName>
                    </ogc:Function>
                  </ogc:Function>
                  <ogc:Literal>0</ogc:Literal>
                </ogc:Add>
              </Rotation>
            </Graphic>
            <Priority>
              <ogc:Add>
                <ogc:Mul>
                  <ogc:PropertyName>U</ogc:PropertyName>
                  <ogc:PropertyName>U</ogc:PropertyName>
                </ogc:Mul>
                <ogc:Mul>
                  <ogc:PropertyName>V</ogc:PropertyName>
                  <ogc:PropertyName>V</ogc:PropertyName>
                </ogc:Mul>
              </ogc:Add>
            </Priority>
            <VendorOption name="conflictResolution">false</VendorOption>
          </TextSymbolizer> 
        </Rule>


        <Rule>
          <Name>moderado</Name>
          <Title>12 to 14</Title>
          <ogc:Filter>
            <ogc:And>
              <ogc:PropertyIsLessThan>
                <ogc:Function name="sqrt">
                  <ogc:Add>
                    <ogc:Mul>
                      <ogc:PropertyName>U</ogc:PropertyName>
                      <ogc:PropertyName>U</ogc:PropertyName>
                    </ogc:Mul>
                    <ogc:Mul>
                      <ogc:PropertyName>V</ogc:PropertyName>
                      <ogc:PropertyName>V</ogc:PropertyName>
                    </ogc:Mul>
                  </ogc:Add>
                </ogc:Function>
                <ogc:Literal>14</ogc:Literal>
              </ogc:PropertyIsLessThan>
        <ogc:PropertyIsGreaterThanOrEqualTo>
                <ogc:Function name="sqrt">
                  <ogc:Add>
                    <ogc:Mul>
                      <ogc:PropertyName>U</ogc:PropertyName>
                      <ogc:PropertyName>U</ogc:PropertyName>
                    </ogc:Mul>
                    <ogc:Mul>
                      <ogc:PropertyName>V</ogc:PropertyName>
                      <ogc:PropertyName>V</ogc:PropertyName>
                    </ogc:Mul>
                  </ogc:Add>
                </ogc:Function>
                <ogc:Literal>12</ogc:Literal>
              </ogc:PropertyIsGreaterThanOrEqualTo>
            </ogc:And>
          </ogc:Filter>
          <TextSymbolizer>
            <Label><![CDATA[ ]]></Label> <!-- fake label -->
            <Graphic>
              <Mark>
                <WellKnownName>extshape://narrow</WellKnownName>
                <Fill>
                  <CssParameter name="fill">#E0B900</CssParameter>
                </Fill>
 <Stroke>
            <CssParameter name="stroke">#000000</CssParameter>
            <CssParameter name="stroke-width">1</CssParameter>
          </Stroke>
              </Mark>
              <Size>4</Size>
              <Rotation>
                <ogc:Add>
                  <ogc:Function name="toDegrees">
                    <ogc:Function name="atan2">
                      <ogc:PropertyName>U</ogc:PropertyName>
                      <ogc:PropertyName>V</ogc:PropertyName>
                    </ogc:Function>
                  </ogc:Function>
                  <ogc:Literal>0</ogc:Literal>
                </ogc:Add>
              </Rotation>
            </Graphic>
            <Priority>
              <ogc:Add>
                <ogc:Mul>
                  <ogc:PropertyName>U</ogc:PropertyName>
                  <ogc:PropertyName>U</ogc:PropertyName>
                </ogc:Mul>
                <ogc:Mul>
                  <ogc:PropertyName>V</ogc:PropertyName>
                  <ogc:PropertyName>V</ogc:PropertyName>
                </ogc:Mul>
              </ogc:Add>
            </Priority>
            <VendorOption name="conflictResolution">false</VendorOption>
          </TextSymbolizer> 
        </Rule>

        <Rule>
          <Name>moderado</Name>
          <Title>14 to 16</Title>
          <ogc:Filter>
            <ogc:And>
              <ogc:PropertyIsLessThan>
                <ogc:Function name="sqrt">
                  <ogc:Add>
                    <ogc:Mul>
                      <ogc:PropertyName>U</ogc:PropertyName>
                      <ogc:PropertyName>U</ogc:PropertyName>
                    </ogc:Mul>
                    <ogc:Mul>
                      <ogc:PropertyName>V</ogc:PropertyName>
                      <ogc:PropertyName>V</ogc:PropertyName>
                    </ogc:Mul>
                  </ogc:Add>
                </ogc:Function>
                <ogc:Literal>16</ogc:Literal>
              </ogc:PropertyIsLessThan>
        <ogc:PropertyIsGreaterThanOrEqualTo>
                <ogc:Function name="sqrt">
                  <ogc:Add>
                    <ogc:Mul>
                      <ogc:PropertyName>U</ogc:PropertyName>
                      <ogc:PropertyName>U</ogc:PropertyName>
                    </ogc:Mul>
                    <ogc:Mul>
                      <ogc:PropertyName>V</ogc:PropertyName>
                      <ogc:PropertyName>V</ogc:PropertyName>
                    </ogc:Mul>
                  </ogc:Add>
                </ogc:Function>
                <ogc:Literal>14</ogc:Literal>
              </ogc:PropertyIsGreaterThanOrEqualTo>
            </ogc:And>
          </ogc:Filter>
          <TextSymbolizer>
            <Label><![CDATA[ ]]></Label> <!-- fake label -->
            <Graphic>
              <Mark>
                <WellKnownName>extshape://narrow</WellKnownName>
                <Fill>
                  <CssParameter name="fill">#ED9500</CssParameter>
                </Fill>
 <Stroke>
            <CssParameter name="stroke">#000000</CssParameter>
            <CssParameter name="stroke-width">1</CssParameter>
          </Stroke>
              </Mark>
              <Size>4</Size>
              <Rotation>
                <ogc:Add>
                  <ogc:Function name="toDegrees">
                    <ogc:Function name="atan2">
                      <ogc:PropertyName>U</ogc:PropertyName>
                      <ogc:PropertyName>V</ogc:PropertyName>
                    </ogc:Function>
                  </ogc:Function>
                  <ogc:Literal>0</ogc:Literal>
                </ogc:Add>
              </Rotation>
            </Graphic>
            <Priority>
              <ogc:Add>
                <ogc:Mul>
                  <ogc:PropertyName>U</ogc:PropertyName>
                  <ogc:PropertyName>U</ogc:PropertyName>
                </ogc:Mul>
                <ogc:Mul>
                  <ogc:PropertyName>V</ogc:PropertyName>
                  <ogc:PropertyName>V</ogc:PropertyName>
                </ogc:Mul>
              </ogc:Add>
            </Priority>
            <VendorOption name="conflictResolution">false</VendorOption>
          </TextSymbolizer> 
        </Rule>


        <Rule>
          <Name>moderado</Name>
          <Title>16 to 4</Title>
          <ogc:Filter>
            <ogc:And>
              <ogc:PropertyIsLessThan>
                <ogc:Function name="sqrt">
                  <ogc:Add>
                    <ogc:Mul>
                      <ogc:PropertyName>U</ogc:PropertyName>
                      <ogc:PropertyName>U</ogc:PropertyName>
                    </ogc:Mul>
                    <ogc:Mul>
                      <ogc:PropertyName>V</ogc:PropertyName>
                      <ogc:PropertyName>V</ogc:PropertyName>
                    </ogc:Mul>
                  </ogc:Add>
                </ogc:Function>
                <ogc:Literal>4</ogc:Literal>
              </ogc:PropertyIsLessThan>
        <ogc:PropertyIsGreaterThanOrEqualTo>
                <ogc:Function name="sqrt">
                  <ogc:Add>
                    <ogc:Mul>
                      <ogc:PropertyName>U</ogc:PropertyName>
                      <ogc:PropertyName>U</ogc:PropertyName>
                    </ogc:Mul>
                    <ogc:Mul>
                      <ogc:PropertyName>V</ogc:PropertyName>
                      <ogc:PropertyName>V</ogc:PropertyName>
                    </ogc:Mul>
                  </ogc:Add>
                </ogc:Function>
                <ogc:Literal>16</ogc:Literal>
              </ogc:PropertyIsGreaterThanOrEqualTo>
            </ogc:And>
          </ogc:Filter>
          <TextSymbolizer>
            <Label><![CDATA[ ]]></Label> <!-- fake label -->
            <Graphic>
              <Mark>
                <WellKnownName>extshape://narrow</WellKnownName>
                <Fill>
                  <CssParameter name="fill">#FF2700</CssParameter>
                </Fill>
 <Stroke>
            <CssParameter name="stroke">#000000</CssParameter>
            <CssParameter name="stroke-width">1</CssParameter>
          </Stroke>
              </Mark>
              <Size>4</Size>
              <Rotation>
                <ogc:Add>
                  <ogc:Function name="toDegrees">
                    <ogc:Function name="atan2">
                      <ogc:PropertyName>U</ogc:PropertyName>
                      <ogc:PropertyName>V</ogc:PropertyName>
                    </ogc:Function>
                  </ogc:Function>
                  <ogc:Literal>0</ogc:Literal>
                </ogc:Add>
              </Rotation>
            </Graphic>
            <Priority>
              <ogc:Add>
                <ogc:Mul>
                  <ogc:PropertyName>U</ogc:PropertyName>
                  <ogc:PropertyName>U</ogc:PropertyName>
                </ogc:Mul>
                <ogc:Mul>
                  <ogc:PropertyName>V</ogc:PropertyName>
                  <ogc:PropertyName>V</ogc:PropertyName>
                </ogc:Mul>
              </ogc:Add>
            </Priority>
            <VendorOption name="conflictResolution">false</VendorOption>
          </TextSymbolizer> 
        </Rule>

        <Rule>
          <Name>moderado</Name>
          <Title>4 to 20</Title>
          <ogc:Filter>
            <ogc:And>
              <ogc:PropertyIsLessThan>
                <ogc:Function name="sqrt">
                  <ogc:Add>
                    <ogc:Mul>
                      <ogc:PropertyName>U</ogc:PropertyName>
                      <ogc:PropertyName>U</ogc:PropertyName>
                    </ogc:Mul>
                    <ogc:Mul>
                      <ogc:PropertyName>V</ogc:PropertyName>
                      <ogc:PropertyName>V</ogc:PropertyName>
                    </ogc:Mul>
                  </ogc:Add>
                </ogc:Function>
                <ogc:Literal>20</ogc:Literal>
              </ogc:PropertyIsLessThan>
        <ogc:PropertyIsGreaterThanOrEqualTo>
                <ogc:Function name="sqrt">
                  <ogc:Add>
                    <ogc:Mul>
                      <ogc:PropertyName>U</ogc:PropertyName>
                      <ogc:PropertyName>U</ogc:PropertyName>
                    </ogc:Mul>
                    <ogc:Mul>
                      <ogc:PropertyName>V</ogc:PropertyName>
                      <ogc:PropertyName>V</ogc:PropertyName>
                    </ogc:Mul>
                  </ogc:Add>
                </ogc:Function>
                <ogc:Literal>4</ogc:Literal>
              </ogc:PropertyIsGreaterThanOrEqualTo>
            </ogc:And>
          </ogc:Filter>
          <TextSymbolizer>
            <Label><![CDATA[ ]]></Label> <!-- fake label -->
            <Graphic>
              <Mark>
                <WellKnownName>extshape://narrow</WellKnownName>
                <Fill>
                  <CssParameter name="fill">#FF2700</CssParameter>
                </Fill>
 <Stroke>
            <CssParameter name="stroke">#000000</CssParameter>
            <CssParameter name="stroke-width">1</CssParameter>
          </Stroke>
              </Mark>
              <Size>4</Size>
              <Rotation>
                <ogc:Add>
                  <ogc:Function name="toDegrees">
                    <ogc:Function name="atan2">
                      <ogc:PropertyName>U</ogc:PropertyName>
                      <ogc:PropertyName>V</ogc:PropertyName>
                    </ogc:Function>
                  </ogc:Function>
                  <ogc:Literal>0</ogc:Literal>
                </ogc:Add>
              </Rotation>
            </Graphic>
            <Priority>
              <ogc:Add>
                <ogc:Mul>
                  <ogc:PropertyName>U</ogc:PropertyName>
                  <ogc:PropertyName>U</ogc:PropertyName>
                </ogc:Mul>
                <ogc:Mul>
                  <ogc:PropertyName>V</ogc:PropertyName>
                  <ogc:PropertyName>V</ogc:PropertyName>
                </ogc:Mul>
              </ogc:Add>
            </Priority>
            <VendorOption name="conflictResolution">false</VendorOption>
          </TextSymbolizer> 
        </Rule>



      </FeatureTypeStyle>
    </UserStyle>
  </NamedLayer>
</StyledLayerDescriptor>