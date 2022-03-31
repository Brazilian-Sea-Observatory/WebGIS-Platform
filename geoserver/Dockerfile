FROM kartoza/geoserver:2.15.2

WORKDIR /

COPY geoserver_data /opt/geoserver/data_dir
COPY geoserver_configs /usr/local/tomcat/webapps/geoserver/WEB-INF/lib/

CMD cp -R /opt/geoserver/data_dir/* /opt/geoserver/data/ && /usr/local/tomcat/bin/catalina.sh run
