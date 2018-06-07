#
# from machine import I2C, Pin
# import mpu6050
#
# i2c = I2C(scl=Pin(32), sda=Pin(33))
# accelerometer = mpu6050.accel(i2c)
#
# print(accelerometer.get_values())

# SSID_NAME = "kmd-wireless0"
# SSID_PASS = "komediadesign"

SSID_NAME = "Xperia XZ1_d2aa"
SSID_PASS = "ujyumakoto"

ESP01_MAC = "30:ae:a4:01:58:78"
ESP02_MAC = "30:ae:a4:05:59:28"

import utime
import network
import machine
import sys

# sys.path[1] = '/flash/lib'
sys.path[1] = '/lib'

def mac_address():
    import ubinascii
    return ubinascii.hexlify(network.WLAN(network.STA_IF).config('mac'),':').decode()

def ip_address():
    return network.WLAN().ifconfig()[0]

def time_sync():
    import untplib
    c = untplib.NTPClient()
    resp = c.request('ntp.nict.jp')

    rtc = machine.RTC()
    rtc.init(utime.localtime(utime.time() + resp.offset + 32400))

def disconnect_wifi():
    wifi= network.WLAN(network.STA_IF)
    wifi.disconnect()

def connect_wifi(ssid, passkey, timeout=10):
    wifi= network.WLAN(network.STA_IF)
    if wifi.isconnected() :
        print('already Connected.    connect skip')
        return wifi
    else :
        wifi.active(True)
        wifi.connect(ssid, passkey)
        while not wifi.isconnected() and timeout > 0:
            print('.')
            utime.sleep(1)
            timeout -= 1

    if wifi.isconnected():
        print('Connected')
        return wifi
    else:
        print('Connection failed!')
        return null

if __name__ == "__main__":
    wifi = connect_wifi(SSID_NAME, SSID_PASS)
    if not wifi.isconnected() :
        # sys.exit(0)
        print("Will restart...")
        utime.sleep(10)
        machine.reset()

    # time_sync()
