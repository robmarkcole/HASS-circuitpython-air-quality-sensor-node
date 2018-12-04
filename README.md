# HASS-circuitpython-air-quality-sensor-node
This project demonstrates a circuitpython board with an PMS5003 air quality sensor, powered over serial (USB) and using Home Assistant to process the data using. Note that Home Assistant is merely a consumer of the sensor data, and alternatively the data could be plotted in a Jupyter notebook, as [here](https://github.com/robmarkcole/Useful-python/blob/master/Pyserial/pyserial.ipynb).

I am running Home Assistant on a raspberry pi, and whilst the sensors could be connected directly to this pi, having them on a separate board allows me to quickly plug the board into my laptop, iterate the hardware/code, and keep data parsing logic in python on the board. In Home Assistant I simply need to add or remove variables being parsed from a json string, and don't need to worry about parsing data using YAML. I previously used this approach with a BBC microbit [here](https://github.com/robmarkcole/HASS-BBC-envirobit).

## Metro M0 Express
This project uses the Adafruit [Metro M0 Express](https://learn.adafruit.com/adafruit-metro-m0-express-designed-for-circuitpython/overview). This board has sufficient memory that the entire [Circuitpython Bundle library](https://github.com/adafruit/Adafruit_CircuitPython_Bundle) can be loaded (this project assumes you have done this). The board has both 3.3 and 5V output, and all the connections are clearly labelled. The board shows up as an external USB drive, making it straightforward to update the code on the board. Don't forget to [update the board firmware](https://learn.adafruit.com/welcome-to-circuitpython/installing-circuitpython) to Circuitpython 3, a process which simply involves dragging a `.uf2` file onto the board. Copy `code.py` from this repository onto the board, and wire up the sensor as described in the next section.

<p align="center">
<img src="https://github.com/robmarkcole/HASS-circuitpython-air-quality-sensor-node/blob/master/images/board.jpg" width="800">
</p>

## PMS5003 laser air sensor
This sensor and accompanying Circuitpython code is on the Adafruit website [here](https://learn.adafruit.com/pm25-air-quality-sensor). For more links see [here](https://github.com/OxygenLithium/Pollutant-Mapping). The wiring between the PMS (by cable colour) and the Metro M0 board are given in the table below. Note that the RX (receive line) of the PMS is wired to the TX (transmit line) of the Metro, and vice versa, to enable comms.

| PMS (cable) |  Metro M0 |
|:-----------:|:---------:|
| 5V (purple) | 5V output |
| 0V (orange) |    GND    |
|  RX (blue)  |   1 (TX)  |
|  TX (green) |   0 (RX)  |

## Mu editor
For development I recommend [Mu editor](https://codewith.mu/), which is a user friendly python editor. Just `pip install mu-editor` and run with `mu-editor`. Mu makes it easy to [live plot data](https://codewith.mu/en/tutorials/1.0/plotter) just by printing a tuple. Github source [here](https://github.com/mu-editor/mu), and for further inspiration see https://madewith.mu/.

<p align="center">
<img src="https://github.com/robmarkcole/HASS-circuitpython-air-quality-sensor-node/blob/master/images/mu.png" width="1000">
</p>

## Home Assistant integration
We integrate the board via a [serial sensor](https://www.home-assistant.io/components/sensor.serial/) and breakout the individual readings using [template sensors](https://www.home-assistant.io/components/sensor.template/):

Add to your Home Assistant `configuration.yaml` file:
```yaml
sensor:
  - platform: serial
    serial_port: /dev/tty.usbmodem141301
  - platform: template
    sensors:
      particles_01um:
        friendly_name: particles_01um
        unit_of_measurement: 'particles'
        value_template: "{{ states.sensor.serial_sensor.attributes.a }}"
  - platform: template
    sensors:
      particles_025um:
        friendly_name: particles_025um
        unit_of_measurement: 'particles'
        value_template: "{{ states.sensor.serial_sensor.attributes.b }}"
  - platform: template
    sensors:
      particles_10um:
        friendly_name: particles_10um
        unit_of_measurement: 'particles'
        value_template: "{{ states.sensor.serial_sensor.attributes.c }}"

history_graph:
  pms5003:
    entities:
      - sensor.particles_01um
      - sensor.particles_025um
      - sensor.particles_10um
```

Note you will need to update the `serial_port` for your own computer, on mac you can list serial connections using `ls /dev/tty.*`

<p align="center">
<img src="https://github.com/robmarkcole/HASS-circuitpython-air-quality-sensor-node/blob/master/images/ha.png" width="550">
</p>


## Streaming data in Jupyter
For streaming see http://pyviz.org/tutorial/11_Streaming_Data.html

## VS-code
Developing Circuitpython in [MS VS-code](https://code.visualstudio.com/) is quite straightforward, although not as seamless as using Mu. For instance, I found the terminal often froze between restarts of the board, which wasn't an issue with Mu. I have the [pycom VS code extension installed](https://docs.pycom.io/pymakr/installation/vscode) which adds a terminal. I use the terminal to connect to the board using `screen`. First check which port the board is on with `ls /dev/tty.*` then connect to the board with e.g. `screen /dev/tty.usbmodem141401`. As the board shows up as a USB device you can drag the `code.py` file into VS-code and edit. On hitting `save` the board restarts and the edits are immediately implemented.

## Presentation
See a presentation on this project at https://github.com/robmarkcole/HASS-circuitpython-air-quality-sensor-node/blob/master/images/PyData%20flash%20talk%204-12-2018.pdf

## Links
* [Awesome Circuitpython](https://github.com/adafruit/awesome-circuitpython)
* https://www.adafruit.com/circuitpython
