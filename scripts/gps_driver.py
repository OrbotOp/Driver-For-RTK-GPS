#!/usr/bin/env python3


import serial
import rospy
from rtk_gps.msg import gps_msg
import utm
c = int(1)

def parseGPS(data):
    
    gngga_line = data[2]
    sdata = gngga_line.decode("utf-8").split(",")
    
    header = sdata[0]
    time_stamp = sdata[1]
    hour = int(time_stamp[0:2])*3600
    mins = int(time_stamp[2:4])*60
    sec = int(time_stamp[4:6])
    time_pub = (hour+mins+sec)
    #nsecs = (time_pub)*(10**9)
    nsecs = int(time_stamp[-2:])*(10**9)
    lat = float(sdata [2])
    a_lat = lat/100
    lat_d = sdata [3]
    lon = float(sdata [4])
    a_lon = lon/100
    lon_d = sdata [5]
    alt = float(sdata [9])
    utm_data = utm.from_latlon(a_lat, a_lon)
    u_east = float(utm_data[0])
    u_north = float(utm_data[1])
    Zone = int(utm_data[2])
    Letter = str(utm_data[3])
    fix = int(sdata[6])
    
    
    gps_rosmsg(header,lat,lat_d,lon,lon_d,alt,u_east,u_north,Zone,Letter,fix,time_pub,nsecs)

 
def gps_rosmsg(header,lat,lat_d,lon,lon_d,alt,u_east,u_north,Zone,Letter,fix,time_pub,nsecs):
    pub = rospy.Publisher('/gps', gps_msg, queue_size=10)
    rospy.init_node('gps_data', anonymous = "TRUE")
    rate = rospy.Rate(10)
    
        
    pub_data = gps_msg()
    global c
    pub_data.Header.seq = c
    c = c+1
    pub_data.Header.stamp.secs = time_pub
    pub_data.Header.stamp.nsecs = nsecs
    pub_data.Header.frame_id = "GPS1_Frame"
    pub_data.Latitude = lat
    pub_data.Longitude = lon
    pub_data.Altitude = alt
    pub_data.UTM_easting = u_east
    pub_data.UTM_northing = u_north
    pub_data.Zone = Zone
    pub_data.Letter = Letter
    pub_data.Fix = fix 
    
    rospy.loginfo(pub_data)
    pub.publish(pub_data)
    rate.sleep()
 
 
port = rospy.get_param("port")
print ("Receiving GPS data")
ser = serial.Serial(port, baudrate = 4800, timeout = 0.5)
data = []
while not rospy.is_shutdown():
    try:
        data = [line for line in ser.readlines() if line.decode().strip()]
        parseGPS(data)
    except Exception as e:
        print(e)
        
    
