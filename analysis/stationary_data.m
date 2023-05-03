bag = rosbag('stationary_data.bag');
bSel = select(bag,'Topic','/gps');
msgStruct = readMessages(bSel,'DataFormat','struct');
msgStruct{1}



time = cellfun(@(m) double(m.Header.Stamp.Sec),msgStruct);
latitude = cellfun(@(m) double(m.Latitude),msgStruct);
longitude = cellfun(@(m) double(m.Longitude),msgStruct);
altitude = cellfun(@(m) double(m.Altitude),msgStruct);
utm_easting = cellfun(@(m) double(m.UTMEasting),msgStruct);
utm_northing = cellfun(@(m) double(m.UTMNorthing),msgStruct);
quality = cellfun(@(m) double(m.Quality), msgStruct);
figure(1);
plot (time,latitude)
xlabel("Time")
ylabel("latitude")
figure(2);
plot (time,longitude)
xlabel("Time")
ylabel("longitude")
figure(3);
geoplot(latitude,-longitude,'*')
figure(4);
plot (time,quality)
xlabel("Time")
ylabel("Quality")
figure(5);
scatter3(latitude,longitude,altitude)
xlabel("Latitude")
ylabel("Longitude")
zlabel("Altitude")