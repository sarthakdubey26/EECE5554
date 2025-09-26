#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from gps_driver.msg import Customgps
import random
import utm

class GPSDriver(Node):
    def __init__(self):
        super().__init__('gps_driver')
        self.publisher_ = self.create_publisher(Customgps, '/gps', 10)
        self.timer = self.create_timer(1.0, self.publish_fake_data)  # 1 Hz

    def publish_fake_data(self):
        msg = Customgps()
        msg.header.frame_id = "GPS1_Frame"
        msg.header.stamp.sec = 0
        msg.header.stamp.nanosec = 0

        # Fake data for testing
        lat = 42.361145 + random.uniform(-0.0001, 0.0001)
        lon = -71.057083 + random.uniform(-0.0001, 0.0001)
        msg.latitude = lat
        msg.longitude = lon
        msg.altitude = 10.0
        utm_data = utm.from_latlon(lat, lon)
        msg.utm_easting = utm_data[0]
        msg.utm_northing = utm_data[1]
        msg.zone = int(utm_data[2])
        msg.letter = utm_data[3]
        msg.hdop = 0.8
        msg.gpgga_read = f"FAKE,{lat},{lon}"
        self.publisher_.publish(msg)
        self.get_logger().info(f"Published fake GPS data: {lat}, {lon}")

def main(args=None):
    rclpy.init(args=args)
    node = GPSDriver()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
