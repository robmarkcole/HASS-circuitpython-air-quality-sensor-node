# HASS-circuitpython-air-quality-sensor-node
This project demonstrates a circuitpython board with various air quality sensors, powered over serial (USB) and piping data into Home-Assistant using json strings. Note that Home-Assitant is merely a consumer of the sensor data, and alternatively the data could be plotted in a Jupyter notebook, as [here](https://github.com/robmarkcole/Useful-python/blob/master/Pyserial/pyserial.ipynb).


I am running Home-Assistant on a raspberry pi, and whilst the sensors could be connected directly to this pi, having them on a separate board allows me to quickly plug the board into my laptop, iterate the hardware/code, and keep complex data parsing logic in python on the board. In Home-Assistant I simply need to add or remove variables being parsed from a json string, and don't need to worry about parsing data using YAML. I previously used this approach with a BBC microbit [here](https://github.com/robmarkcole/HASS-BBC-envirobit).

### The Circuitpython Board - Metro M0 Express
This project uses the Adafruit [Metro M0 Express](https://learn.adafruit.com/adafruit-metro-m0-express-designed-for-circuitpython/overview). This board has sufficient memory that the entire [Circuitpython Bundle library](https://github.com/adafruit/Adafruit_CircuitPython_Bundle) can be loaded. It has both 3.3 and 5V output, and all the connections are clearly labelled. The board shows up as an external USB drive, making it straightforward to update the code on the board. Don't forget to [update the firmware](https://learn.adafruit.com/welcome-to-circuitpython/installing-circuitpython) to Circuitpython 3, a process which simply involves dragging a `.uf2` file onto the board.

<p align="center">
<img src="https://github.com/robmarkcole/HASS-circuitpython-air-quality-sensor-node/blob/master/images/board.jpg" width="900">
</p>

### PMS5003 laser air sensor
This sensor and accompanying Circuitpython code is on the Adafruit website [here](https://learn.adafruit.com/pm25-air-quality-sensor). For more links see [here](https://github.com/OxygenLithium/Pollutant-Mapping). For advanced use see [here](https://kapusta.cc/2017/12/02/home-made-air-quality-monitoring-using-wipy/).

### BME680
I have the Pimoroni BME680 sensor from [here](https://shop.pimoroni.com/products/bme680-breakout), which is compatible with the Circuitpython code from [here](https://learn.adafruit.com/adafruit-bme680-humidity-temperature-barometic-pressure-voc-gas/python-circuitpython). Note the BME680 library is included in the Circuitpython bundle.

## MU
[MU](https://codewith.mu/) is a QT5 GUI which allows programming with the micropython board, but also [live plotting of data](https://codewith.mu/en/tutorials/1.0/plotter), just by printing a tuple of data. Github source [here](https://github.com/mu-editor/mu), and for further inspiration see https://madewith.mu/

<p align="center">
<img src="https://github.com/robmarkcole/HASS-circuitpython-air-quality-sensor-node/blob/master/images/mu_bme680.png" width="1000">
</p>

## VS-code
Developing Circuitpython in VS-code is quite a decent experience. I use the terminal to connect to the board using `screen`. First check which port the board is on with `ls /dev/tty.*` then connect to the board with e.g. `screen /dev/tty.SLAB_USBtoUART`. As the board shows up as a USB device you can drag the `code.py` file into VS-code and edit. Om hitting `save` edits are applied immediately.

<p align="center">
<img src="https://github.com/robmarkcole/HASS-circuitpython-air-quality-sensor-node/blob/master/images/vs_code.png" width="1000">
</p>

## Display
I wish to add a display, perhaps https://thepihut.com/collections/lcds-displays/products/adafruit-1-54-tri-color-eink-epaper-display-with-sram-ada3625
