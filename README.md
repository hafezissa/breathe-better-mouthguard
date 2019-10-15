# Breathe Better Mouth-Guard
The *Breathe Better Mouthguard* is a new __method__ of **personal fitness tracking** that is dedicated to the betterment of achieving **instantaneous fitness measurements**. With an increasing amount of people turning to new methods of fitness tracking every year, more devices are created to be able to deliver those fitness measurements. Despite new improvements in these devices, a specific group of the general demographic, athlete’s, do not have many methods of tracking their fitness and endurance in the midst of their sports. The *Breathe Better Mouthguard* is able to provide accurate and instant data about their own physical performance in real time. The mouthguard creates a seamless amalgamation between an already present safety device, worn by countless athletes in a wide range of sports, and a method of fitness tracking.  It is intended to be used exactly like any other mouthguard and is equally as customizable as one as well, with a moldable putty used to get the oral imprint of any user. Using a **carbon dioxide (CO2) sensor** built into the mouthguard shell itself, the mouthguard is able to give **detailed measurements of any user’s breathing patterns**, specifically the **CO2 concentration that they exhale**. 
## Getting Started .. 
This 6-week project is composed of a *high-fidelity*  prototype (3D-printed mouth guard) and a *computational* prototype:
- Raspberry Pi
- MQ2 gas sensor
- PCF8591 analog-to-digital converter                 <img alt="Breadboard Configuration" src="https://github.com/hafezissa/breathe-better-mouthguard/blob/master/breadboard_config.png" align="right" width="500" height="500">
- GPIO extension
- button and wiring

### Method ..
The computing prototype makes use of a button and an MQ2 gas sensor which is suitable to measure liquid petroleum gas (LPG) , Hydrogen gas, methane, carbon monoxide, alcohol, smoke and propane. This sensor, although unable to detect CO2, works in a similar manner as a CO2 gas sensor. Gas sensors in general, sense changes in conductivity as concentrations increase. This is then converted as a voltage output by an analog-to-digital converter. The decision to use a gas sensor in place of CO2 specific gas sensor was to test for the computational prototype while simulating the real test. A sensor would register concentrations in an expelled breath and provide an output, in the form of a color coded graph, that displays whether these concentrations are in a normal range, slightly outside of the normal range, or well exceeding. The device only outputs its readings when a pressure sensor experiences the force of a user biting down. The test plan accounts for several scenarios, which both test the functionality of the program and those that are likely to occur with use. 

## Application ..
Test plan runs as follows, 4 scenarios --> each with a combination of triggering the pressure sensor and varying amounts of carbon dioxide expelled by breathing.

| Test Number |   Description  | Graphical Output |
| -- | -- | -- |
| Test One | &#9745; CO2 gas - normal respiration<br/>&#9744; Pressure Sensor | no plot created |
| Test Two | &#9745; CO2 gas - normal respiration<br/>&#9745; Pressure Sensor | green curve, indicating average level of CO2 |
| Test Three | &#9745; CO2 gas - under-average respiration</br>&#9745; Pressure Sensor | red curve, indicating dangerous levels of CO2 |
| Test Four | &#9745; CO2 gas - above-average respiration</br>&#9745; Pressure Sensor | red curve, indicating dangerous levels of CO2 |

### Running The Tests ..
The program itself functions in the way by cycling through inputs of gas in the same time intervals and provides a curve that is plotted in real time. The pressure sensor is represented by a button connected to the breadboard. The **gas sensor can be tested using LPG released from a pocket lighter**. However, a lighter will not provide varying levels in concentration as the test plan includes. Instead, the lighter must be **held at varying distances away from the sensor** so that less gas is being inputted.

| Test Number | Description | Graphical Output |
| -- | -- | -- |
| Test One | &#9745; LPG Release</br>&#9744; Button Pressed | no plot created |
| Test Two | &#9745; LPG Release - from 4 cm away to 3 cm away</br>&#9745; Button Pressed | green to yellow curve |
| Test Three | &#9745; LPG Release - from 3 cm away to 2 cm away</br>&#9745; Button Pressed | yellow to red curve |
| Test Four | &#9745; LPG Release - from <1cm away to 4 cm away</br>&#9745; Button Pressed | red to yellow to green curve |

#### Graphical Analysis ..
As a comparison to Test One, this would require holding the lighter to the sensor without the button being pressed and seeing if inputs are being read, but no graph is plotted. Test two requires that the lighter is held at a distance of 4 centimeters (cm) away from the sensor, first without the button pressed and then with the button pressed. Once the button is pressed, the lighter is moved closer to the sensor at an approximate distance of 3cm away, so that the graph colour changes from green to yellow. Test three requires the button to be pressed as the lighter is held at a farther distance away from the sensor than previously. The lighter is continuously moved closer, until the graph shifts from yellow to red zone. Test four requires the button to be pressed and the lighter to be held at an approximate distance of 1 cm away. The sensor reads and outputs very high levels of LPG which the graph plots in red. As the distance is increased, the graphs values will decrease and return to green.

#### Calculation .. 
Calculations were made to **convert the scale that is read by the analog to digital converter** and **outputted to a graph that reads units of parts per million**. The analog to digital converter outputs an integer on a scale of 0 to 255 which represents voltage reading due to a signal. In order calculate this conversion, several resistance values also had to be accounted for. The breadboard and ADC itself provide a constant load resistance which is set to ten kilohms. Due to the sensitivity of the gas sensor, the ADC reading in ambient conditions, assumed to be a typical environment with standard air quality, was reading a value of 105.<img alt="MQ20 Datasheet" src="https://github.com/hafezissa/breathe-better-mouthguard/blob/master/MQ2%20Datasheet.png" align="right" width="400" height="400"> This value was subtracted from the maximum value (ie. 255) over the same max value. Effectively, this was a measure taken to offset the inaccuracies that the sensor was initially reading. This calibrated factor was then multiplied with the load resistance to achieve the  air resistance value in ideal conditions. Ideal conditions would be  purified  air, however in a typical environment,  pure air quality is off by a factor of 9.83. This was factored into our calculation of air resistance. 

When the gas sensor inputs readings of LPG, the ADC acts to output this data. These values display as a logarithmic graph similar to the figure. From this  graph we interpolated values to make better sense of the scale. The log graph was calibrated to produce a more visual representation of the data in ppm values that display as a points along a curve. These values are somewhat arbitrary, with a specific purpose that all three colour zones displayed on the graph while testing with the LPG lighter. 
