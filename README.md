# HASS-circuitpython-air-quality-sensor-node
This project demonstrates a circuitpython board with various air quality sensors, powered over serial (USB) and piping data into Home-Assistant using json strings.
I am running Home-Assistant on a raspberry pi, and whilst the sensors could be connected directly to this pi, having them on a separate board allows me to quickly plug the board into my laptop, iterate the hardware/code, and keep complex data parsing logic in python on the board. In Home-Assistant I simply need to add or remove variables being parsed from a json string, and don't need to worry about parsing data using YAML.

### The Circuitpython Board - Metro M0 Express
This project uses the Adafruit [Metro M0 Express](https://learn.adafruit.com/adafruit-metro-m0-express-designed-for-circuitpython/overview). This board has sufficient memory that the entire [Circuitpython helpers library](https://github.com/adafruit/Adafruit_CircuitPython_Bundle) can be loaded. It has both 3.3 and 5V output, and all the connections are clearly labelled. Don't forget to [update the firmware](https://learn.adafruit.com/welcome-to-circuitpython/installing-circuitpython) to Circuitpython 3.

<p align="center">
<img src="https://github.com/robmarkcole/HASS-circuitpython-air-quality-sensor-node/blob/master/images/board.jpg" width="500">
</p>
