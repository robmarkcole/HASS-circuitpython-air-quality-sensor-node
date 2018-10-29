import board
import busio
from busio import I2C
from digitalio import DigitalInOut, Direction
import adafruit_bme680

try:
    import struct
except ImportError:
    import ustruct as struct

led = DigitalInOut(board.D13)
led.direction = Direction.OUTPUT

# Setup BME
# Create library object using our Bus I2C port
i2c = I2C(board.SCL, board.SDA)
bme680 = adafruit_bme680.Adafruit_BME680_I2C(i2c)
# change this to match the location's pressure (hPa) at sea level
bme680.sea_level_pressure = 1013.25

# Main  loop reads from PMS sensor
# Connect the Sensor's TX pin to the board's RX pin
uart = busio.UART(board.TX, board.RX, baudrate=9600)
buffer = []

while True:
    try:
        data = uart.read(32)  # read up to 32 bytes
        data = list(data)
        buffer += data
    except:
        continue

    while buffer and buffer[0] != 0x42:
        buffer.pop(0)

    if len(buffer) > 200:
        buffer = []  # avoid an overrun if all bad data
    if len(buffer) < 32:
        continue

    if buffer[1] != 0x4d:
        buffer.pop(0)
        continue

    frame_len = struct.unpack(">H", bytes(buffer[2:4]))[0]
    if frame_len != 28:
        buffer = []
        continue

    frame = struct.unpack(">HHHHHHHHHHHHHH", bytes(buffer[4:]))

    pm10_standard, pm25_standard, pm100_standard, pm10_env, \
        pm25_env, pm100_env, particles_03um, particles_05um, particles_10um, \
        particles_25um, particles_50um, particles_100um, skip, checksum = frame

    check = sum(buffer[0:30])

    if check != checksum:
        buffer = []
        continue

    data_dict = {}
    data_dict['temperature'] = bme680.temperature
    data_dict['humidity'] = bme680.humidity
    data_dict['pressure'] = bme680.pressure
    data_dict['gas'] = bme680.gas
    data_dict['particles_03um'] = particles_03um
    data_dict['particles_05um'] = particles_05um
    data_dict['particles_10um'] = particles_10um
    data_dict['particles_25um'] = particles_25um
    data_dict['particles_50um'] = particles_50um
    data_dict['particles_100um'] = particles_100um
    print(data_dict)
    print("---------------------------------------")

    buffer = buffer[32:]
    # print("Buffer ", buffer)
