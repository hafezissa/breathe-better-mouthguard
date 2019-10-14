import PCF8591 as ADC
import RPi.GPIO as GPIO
from time import sleep, time   
from datetime import datetime
from math import pow,log
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
from matplotlib.dates import DateFormatter
import numpy as np
import random
from gpiozero import Button

DEBUG = False
button = Button(10)    ## button assigned GPIO pin 10

def print_debug(*args):
        if DEBUG == True:
                print(*args)

def setup():
        ADC.setup(0x48)

def sensor_Resistance(RL=10):    ## loopVolatage set to 5V - loadResistance set to 10 Kilohms
        LPG = [2.3,0.72,-0.34]    ## from the datasheet, first point, last point, and slope of the line -- used to interpolate 
        RsAir = (RL*(255-105)/105)    ## ambient sensing resistance -- in clean air environment
        Ro = RsAir/9.83    ## clean air factor constant -- calculated using sensing resistance in ambeint conditions

        Rs = (RL*(255-ADC.read(0))/ADC.read(0))    ## sensing resistance during input of LPG -- ADC reading 
        
        ppmLPG = pow(10,(((log(Rs/Ro, 10)-LPG[1])/LPG[2]) + LPG[0])) - pow(10,(((log(RsAir/Ro, 10)-LPG[1])/LPG[2]) + LPG[0]))    ## interpolate data from the datasheet to obtain ppm value
        return ppmLPG
                   
def animate(i, xs, ys, ax):
        global line
        
        if button.is_pressed:    ## button acting as a pressure sensor, when held the code will run

                ## READ -- ppm from MQ2
                ppmcalc = sensor_Resistance()

                if ppmcalc > 1000000:
                        ppmcalc = 1000000

                ## PLOT -- add x and y to lists
                now = datetime.now()    ## date
                xs.append(now)     ## adds the date to xs

                ## CALIBRATION -- for a better visual representation of the graph, the ppm values are plotted accordingly
                if (ppmcalc < 200):    ## in ambient conditions, a LOW concentration of LPG is present in the air
                        ys.append(random.randint(0,2000))    ## adds the 'reading' from the sensor to ys
                        line.set_color('green')
                elif (ppmcalc<1000):    ## in 'low' conditions
                        ys.append(random.randint(0,20000))
                        line.set_color('green')
                elif (ppmcalc > 1000) and (ppmcalc < 10000):    ## in 'mid' conditions
                        ys.append(random.randint(20000,30000))
                        line.set_color('yellow')
                else:    ## in 'high' conditions
                        ys.append(random.randint(30000, 55000))
                        line.set_color('red')
                        
                ## FORMAT -- limit x and y lists to 20 items
                xs = xs[-20:]
                ys = ys[-20:]

                line.set_xdata(xs)    ## adds point to the x coordinate
                line.set_ydata(ys)    ## adds point to the y coordinate
                
                ax.set_xlim([min(xs), max(xs)])    ## changes lower and upper lim on x-axis, x-values would update
                
        return line,

def main():
        global line
        ## INITIALIZE -- establish scatter plot system
        fig = plt.figure()
        ax = fig.add_subplot(1,1,1)
        xs = [datetime.now()]*20
        ys = [0]*20

        ## Raspberry-Pi Format (Hardware/Software)
        setup()
        
        ax.xaxis_date()    ## sets up x-axis ticks and labels that treat the x data as dates
        myFmt = DateFormatter("%H:%M:%S")    ## only projects hours:minutes:seconds
        ax.xaxis.set_major_formatter(myFmt)     ## sets the formatter of the graph

        ax.set_ylim([0, 60000])    ## restricts y-scale to 60000 ppm (due to sensor and adc inaccuracy)
        line, = ax.plot(xs, ys)    ## assings the plot to line
        
        ## Plot Format
        fig.autofmt_xdate()    
        ax.set_title("PPM vs TIME")    ## title of graph
        ax.set_xlabel("TIME, (H:M:S)")    ## x-axis label
        ax.set_ylabel("Concentration of LPG, (PPM)")    ## y-axis label
        
        ani = animation.FuncAnimation(fig, animate, fargs=(xs,ys,ax,), interval=10)    ## animate graph (live feed)
        plt.show()
        
try:
        main()
except AttributeError:
        print("Goodbye ;)")
