# main.py -- put your code here!

import ujson
import boot
import utime

from umqtt.simple import MQTTClient

import uasyncio
from uasyncio.websocket.server import WSReader, WSWriter

from machine import I2C, Pin
import mpu6050

from filter import SpeedFilter

speed_filter = None

def get_accel_raw():
    i2c = I2C(scl=Pin(32), sda=Pin(33))
    accelerometer = mpu6050.accel(i2c)
    return accelerometer.get_values()

def get_accel():
    accel = get_accel_raw()
    now_speed = speed_filter.update(accel['AcX'], accel['AcY'], accel['AcZ'])

    accel['SpX'] = now_speed[0]
    accel['SpY'] = now_speed[1]
    accel['SpZ'] = now_speed[2]
    accel['AcX'] = speed_filter.accel[0]
    accel['AcY'] = speed_filter.accel[1]
    accel['AcZ'] = speed_filter.accel[2]

    del accel['GyX']
    del accel['GyY']
    del accel['GyZ']
    del accel['Tmp']

    return accel

def advertise_ip():
    payload = ujson.dumps({'mac': boot.mac_address(), 'ip': boot.ip_address(), 'time': utime.time()})

    c = MQTTClient(boot.mac_address(), "m14.cloudmqtt.com", port=21432, user="cyofmydg", password="BHdp0t9D8DPF", ssl=True)
    c.connect()
    c.publish(b"/wireless-dj", payload)
    c.disconnect()

    print("advertised")
    print(payload)

async def accel_server(reader, writer):
    # Consume GET line
    # yield from reader.readline()
    #
    # # reader = yield from WSReader(reader, writer)
    # writer = WSWriter(reader, writer)
    #
    # # while 1:
    # #     l = yield from reader.read(256)
    # #     print(l)
    # #     if l == b"\r":
    # #         await writer.awrite(b"\r\n")
    # #     else:
    # #         await writer.awrite(l)
    # while 1:
    #     await writer.awrite(ujson.dumps(get_accel()))
    #     utime.sleep_ms(100)

    # accel = get_accel()
    # speed_filter = Speed(accel['AcX'], accel['AcY'], accel['AcZ'])

    yield from reader.readline()

    reader = yield from WSReader(reader, writer)
    writer = WSWriter(reader, writer)

    while True:
        accel = get_accel()
        # now_speed = speed_filter.update(accel['AcX'], accel['AcY'], accel['AcZ'])
        # accel['SpX'] = now_speed[0]
        # accel['SpY'] = now_speed[1]
        # accel['SpZ'] = now_speed[2]
        # print(ujson.dumps(accel))
        await writer.awrite(ujson.dumps(accel))
        await uasyncio.sleep_ms(50)

def main():
    pin = Pin(19, Pin.OUT)
    pin.value(0)

    # advertise_ip()

    pin.value(1)

    global speed_filter
    get_accel_raw()
    get_accel_raw()
    get_accel_raw()
    get_accel_raw()
    get_accel_raw()
    accel = get_accel_raw()
    speed_filter = SpeedFilter(accel['AcX'], accel['AcY'], accel['AcZ'])

    loop = uasyncio.get_event_loop()
    loop.create_task(uasyncio.start_server(accel_server, "0.0.0.0", 8081))
    loop.run_forever()
    loop.close()

    # while True:
    #     accel = get_accel()
    #     print(accel)
    #     utime.sleep_ms(100)

if __name__ == "__main__":
    main()
