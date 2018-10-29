# HASS-circuitpython-air-quality-sensor-node
This project demonstrates a circuitpython board with various air quality sensors, powered over serial (USB) and piping data into Home-Assistant using json strings. Note that Home-Assitant is merely a consumer of the sensor data, and alternatively the data could be plotted in a Jupyter notebook, as [here](https://github.com/robmarkcole/Useful-python/blob/master/Pyserial/pyserial.ipynb).

I am running Home-Assistant on a raspberry pi, and whilst the sensors could be connected directly to this pi, having them on a separate board allows me to quickly plug the board into my laptop, iterate the hardware/code, and keep complex data parsing logic in python on the board. In Home-Assistant I simply need to add or remove variables being parsed from a json string, and don't need to worry about parsing data using YAML. I previously used this approach with a BBC microbit [here](https://github.com/robmarkcole/HASS-BBC-envirobit).

### Metro M0 Express
This project uses the Adafruit [Metro M0 Express](https://learn.adafruit.com/adafruit-metro-m0-express-designed-for-circuitpython/overview). This board has sufficient memory that the entire [Circuitpython Bundle library](https://github.com/adafruit/Adafruit_CircuitPython_Bundle) can be loaded. It has both 3.3 and 5V output, and all the connections are clearly labelled. The board shows up as an external USB drive, making it straightforward to update the code on the board. Don't forget to [update the firmware](https://learn.adafruit.com/welcome-to-circuitpython/installing-circuitpython) to Circuitpython 3, a process which simply involves dragging a `.uf2` file onto the board.

<p align="center">
<img src="https://github.com/robmarkcole/HASS-circuitpython-air-quality-sensor-node/blob/master/images/board.jpg" width="900">
</p>


### BME680
I have the Pimoroni BME680 sensor from [here](https://shop.pimoroni.com/products/bme680-breakout), which is compatible with the Circuitpython code from [here](https://learn.adafruit.com/adafruit-bme680-humidity-temperature-barometic-pressure-voc-gas/python-circuitpython). Note the BME680 library is included in the Circuitpython bundle.
Basic usage of the BME680 is quite straightforward:
```python
from busio import I2C
import adafruit_bme680
import time
import board

# Create library object using our Bus I2C port
i2c = I2C(board.SCL, board.SDA)
bme680 = adafruit_bme680.Adafruit_BME680_I2C(i2c)

# change this to match the location's pressure (hPa) at sea level
bme680.sea_level_pressure = 1013.25

while True:
    print((bme680.temperature, bme680.humidity))
    time.sleep(2)
```

### PMS5003 laser air sensor
This sensor and accompanying Circuitpython code is on the Adafruit website [here](https://learn.adafruit.com/pm25-air-quality-sensor). For more links see [here](https://github.com/OxygenLithium/Pollutant-Mapping). Basic usage is a bit more involved than the BME, as there are several checks on the data:

```python
import board
import busio
from digitalio import DigitalInOut, Direction

try:
    import struct
except ImportError:
    import ustruct as struct

led = DigitalInOut(board.D13)
led.direction = Direction.OUTPUT

# Connect the Sensor's TX pin to the board's RX pin
uart = busio.UART(board.TX, board.RX, baudrate=9600)

buffer = []

while True:
    data = uart.read(32)  # read up to 32 bytes
    data = list(data)
    # print("read: ", data)          # this is a bytearray type

    buffer += data

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

    print("Concentration Units (standard)")
    print("---------------------------------------")
    print("PM 1.0: %d\tPM2.5: %d\tPM10: %d" %
          (pm10_standard, pm25_standard, pm100_standard))
    print("Concentration Units (environmental)")
    print("---------------------------------------")
    print("PM 1.0: %d\tPM2.5: %d\tPM10: %d" % (pm10_env, pm25_env, pm100_env))
    print("---------------------------------------")
    print("Particles > 0.3um / 0.1L air:", particles_03um)
    print("Particles > 0.5um / 0.1L air:", particles_05um)
    print("Particles > 1.0um / 0.1L air:", particles_10um)
    print("Particles > 2.5um / 0.1L air:", particles_25um)
    print("Particles > 5.0um / 0.1L air:", particles_50um)
    print("Particles > 10 um / 0.1L air:", particles_100um)
    print("---------------------------------------")

    buffer = buffer[32:]
    # print("Buffer ", buffer)
```

## VS-code
Developing Circuitpython in [MS VS-code](https://code.visualstudio.com/) is quite a nice experience. I have the [pycom VS code extension installed](https://docs.pycom.io/pymakr/installation/vscode) which adds a terminal. I use the terminal to connect to the board using `screen`. First check which port the board is on with `ls /dev/tty.*` then connect to the board with e.g. `screen /dev/tty.usbmodem141401`. As the board shows up as a USB device you can drag the `code.py` file into VS-code and edit. On hitting `save` the board restarts and the edits are immediately implemented.

<p align="center">
<img src="https://github.com/robmarkcole/HASS-circuitpython-air-quality-sensor-node/blob/master/images/vs_code.png" width="1000">
</p>

## MU
If VS code is overkill for your application, [MU](https://codewith.mu/) is a user friendly QT5 GUI which allows programming with the circuitpython/micropython. It also allows [live plotting of data](https://codewith.mu/en/tutorials/1.0/plotter) just by printing a tuple of data. Github source [here](https://github.com/mu-editor/mu), and for further inspiration see https://madewith.mu/

<p align="center">
<img src="https://github.com/robmarkcole/HASS-circuitpython-air-quality-sensor-node/blob/master/images/mu_bme680.png" width="1000">
</p>

## Display
I wish to add a display, perhaps https://thepihut.com/collections/lcds-displays/products/adafruit-1-54-tri-color-eink-epaper-display-with-sram-ada3625

## Streaming data in Jupyter
For streaming see http://pyviz.org/tutorial/11_Streaming_Data.html

## Imports
We will require https://circuitpython.readthedocs.io/en/3.x/docs/library/ujson.html?highlight=ujson
