# HASS-circuitpython-air-quality-sensor-node
This project demonstrates a circuitpython board with various air quality sensors, powered over serial (USB) and piping data into Home-Assistant using json strings. Note that Home-Assitant is merely a consumer of the sensor data, and alternatively the data could be plotted in a Jupyter notebook, as [here](https://github.com/robmarkcole/Useful-python/blob/master/Pyserial/pyserial.ipynb).


I am running Home-Assistant on a raspberry pi, and whilst the sensors could be connected directly to this pi, having them on a separate board allows me to quickly plug the board into my laptop, iterate the hardware/code, and keep complex data parsing logic in python on the board. In Home-Assistant I simply need to add or remove variables being parsed from a json string, and don't need to worry about parsing data using YAML.

### The Circuitpython Board - Metro M0 Express
This project uses the Adafruit [Metro M0 Express](https://learn.adafruit.com/adafruit-metro-m0-express-designed-for-circuitpython/overview). This board has sufficient memory that the entire [Circuitpython helpers library](https://github.com/adafruit/Adafruit_CircuitPython_Bundle) can be loaded. It has both 3.3 and 5V output, and all the connections are clearly labelled. The board shows up as an external USB drive, making it straightforward to update the code on the board. Don't forget to [update the firmware](https://learn.adafruit.com/welcome-to-circuitpython/installing-circuitpython) to Circuitpython 3, a process which simply involves dragging a `.uf2` fole onto the board.

<p align="center">
<img src="https://github.com/robmarkcole/HASS-circuitpython-air-quality-sensor-node/blob/master/images/board.jpg" width="500">
</p>

### PMS5003 laser air sensor
This sensor and accompanying Circuitpython code is on the Adafruit website [here](https://learn.adafruit.com/pm25-air-quality-sensor). For more links see [here](https://github.com/OxygenLithium/Pollutant-Mapping). For advanced use see [here](https://kapusta.cc/2017/12/02/home-made-air-quality-monitoring-using-wipy/). 

### BME680
I have the Pimoroni BME680 sensor from [here](https://shop.pimoroni.com/products/bme680-breakout). I should be able to use the Circuitpython code from [here](https://learn.adafruit.com/adafruit-bme680-humidity-temperature-barometic-pressure-voc-gas/python-circuitpython).

## MU
[MU](https://codewith.mu/) is a QT5 GUI which allows programming with the micropython board, but also [live plotting of data](https://codewith.mu/en/tutorials/1.0/plotter), just by printing a tuple of data. Github source [here](https://github.com/mu-editor/mu), and for further inspiration see https://madewith.mu/
