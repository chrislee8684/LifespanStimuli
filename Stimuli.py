import RPi.GPIO as GPIO #pin connection
import time
from tkinter import *
import numpy
import pygame
import adafruit_mcp4725 as Adafruit_MCP4725
import board
import busio

#initial pin setup
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
LED = 14
GPIO.setup(LED, GPIO.OUT)
i2c = busio.I2C(board.SCL, board.SDA)
dac = Adafruit_MCP4725.MCP4725(i2c, address=0x60)


#LED functions
def LED_ON():
    GPIO.output(LED, 1)
   
def LED_OFF():
    GPIO.output(LED, 0)

def SOUND_ON():
    dac.raw_value = 4095

def SOUND_OFF():
    dac.raw_value = 0

#initialize GUI
interface = Tk()
interface.geometry("370x250")
interface.title("Mindset Project User Interface")

#GUI functions
light_switch = StringVar()
sound_switch = StringVar()
wave_switch = StringVar()
freq_switch = StringVar()

def send_command():
    #get all input values
    light_status = light_switch.get()
    sound_status = sound_switch.get()
    wave_state = wave_switch.get()
    freq = int(freq_switch.get())
    duty = int(duty_entry.get())
    phase = int(phase_entry.get())
    time_value = int(time_entry.get())
   
    #display input values
    print("Light Status: " + light_status)
    print("Frequency: " + str(freq) + "Hz")
    print("Duty Cycle: " + str(duty) + "%")
    print("\n")
    print("Sound Status: " + sound_status)
    print("Sound Wave Pattern: " + wave_state)
    print("\n")
    print("Phase Difference: " + str(phase) + "Degrees")
    print("Time: " + str(time_value) + "Seconds")
   
    #equations
    delayON = (1*(duty/100))/freq
    delayOFF = (1*(1-duty/100))/freq
    period = delayON+delayOFF
    phase_diff_milli = (phase*(period))/360
   
    #variables
    led_time = phase_diff_milli
    sound_time = 0
    led_state = 1
    sound_state = 1
   
   
    #conditions and loops
    start_time = time.time()
   
    if light_status == "ON" and sound_status == "ON": #both light and sound on
        if wave_state == "Square":
            turnON = True
            while turnON:
                end_time = time.time()
               
                if led_state==1 and (end_time-start_time)-led_time >= delayON:
                    LED_OFF()
                    led_time += delayON
                    led_state=0
                   
                elif led_state==0 and (end_time-start_time)-led_time >= delayOFF:
                    LED_ON()
                    led_time += delayOFF
                    led_state=1
                   
                if sound_state==1 and (end_time-start_time)-sound_time >= delayON:
                    SOUND_OFF()
                    sound_time += delayON
                    sound_state=0
                   
                elif sound_state==0 and (end_time-start_time)-sound_time >= delayOFF:
                    SOUND_ON()
                    sound_time += delayOFF
                    sound_state=1
           
                if end_time - start_time >= time_value: #checks time passed
                    print("Time Over: Exiting Program")
                    turnON = False
        elif wave_state == "Sawtooth":
            duty_level = 0
       
            turnON = True
            while turnON:
                end_time = time.time()
               
                if led_state==1 and (end_time-start_time)-led_time >= delayON:
                    LED_OFF()
                    led_time += delayON
                    led_state=0
                   
                elif led_state==0 and (end_time-start_time)-led_time >= delayOFF:
                    LED_ON()
                    led_time += delayOFF
                    led_state=1
               
                if (end_time - start_time) - sound_time >= period/4095:
                    if duty_level<4095:
                        duty_level+=1
                        dac.raw_value = duty_level
                        sound_time += period/4095
                    else:
                        duty_level = 0
                        sound_time += period/4095

                if end_time - start_time >= time_value: #checks time passed
                    print("Time Over: Exiting Program")
                    turnON = False
           
    elif light_status == "ON" and sound_status == "OFF": #only light is on
        turnON = True
        while turnON:
            end_time = time.time()

            if led_state==1 and (end_time-start_time)-led_time >= delayON:
                LED_OFF()
                led_time += delayON
                led_state=0
               
            elif led_state==0 and (end_time-start_time)-led_time >= delayOFF:
                LED_ON()
                led_time += delayOFF
                led_state=1
               
            if end_time - start_time >= time_value: #checks time passed
                print("Time Over: Exiting Program")
                turnON = False
               
    elif light_status == "OFF" and sound_status == "ON": #only sound on
        if wave_state == "Square":
   
            turnON = True
            while turnON:
                end_time = time.time()
               
                if sound_state==1 and (end_time-start_time)-sound_time >= delayON:
                    SOUND_OFF()
                    sound_time += delayON
                    sound_state=0
                   
                elif sound_state==0 and (end_time-start_time)-sound_time >= delayOFF:
                    SOUND_ON()
                    sound_time += delayOFF
                    sound_state=1
           
                if end_time - start_time >= time_value: #checks time passed
                    print("Time Over: Exiting Program")
                    turnON = False
                   
        elif wave_state == "Sawtooth":
            duty_level = 0
       
            turnON = True
            while turnON:
                end_time = time.time()
                               
                if (end_time - start_time) - sound_time >= period/4095:
                    if duty_level<4095:
                         duty_level += 1
                         dac.raw_value = duty_level
                         sound_time += period/4095
                    else:
                         duty_level = 0
                         sound_time += period/4095

                if end_time - start_time >= time_value: #checks time passed
                    print("Time Over: Exiting Program")
                    turnON = False
       

#GUI labels & entries
               
    #light labels & entries
light_label = Label(interface, text = "Light Status")
light_label.grid(row=1, column=0)

light_freq_label = Label(interface, text = "Frequency (Hz)")
light_freq_label.grid(row=2,column=0)

duty_label = Label(interface, text = "Duty cycle (%)")
duty_label.place(relx=0.2, rely=0.4)


light_choices = ['ON', 'OFF']
light_entry = OptionMenu(
    interface,
    light_switch,
    *light_choices
)
light_entry.grid(row=1,column=1)

freq_choices = ['20', '40', '80']
wave_choice_entry = OptionMenu(
    interface,
    freq_switch,
    *freq_choices
)
wave_choice_entry.grid(row=2,column=1)

duty_entry = Entry(interface,width=10)
duty_entry.place(relx=0.5, rely=0.4)

    #sound labels & entries

sound_label = Label(interface, text="Sound Status")
sound_label.grid(row=1,column=2)

wave_pattern_label = Label(interface, text="Wave Pattern")
wave_pattern_label.grid(row=2,column=2)


sound_choices = ['ON', 'OFF']
sound_entry = OptionMenu(
    interface,
    sound_switch,
    *sound_choices
)
sound_entry.grid(row=1,column=3)

wave_choices = ['Sawtooth', 'Square']
wave_choice_entry = OptionMenu(
    interface,
    wave_switch,
    *wave_choices
)
wave_choice_entry.grid(row=2,column=3)

   
    #Other labels & entries
phase_label=Label(interface, text="Phase (Degrees)")
phase_label.place(relx=0.2, rely=0.5)

phase_entry=Entry(interface,width=10)
phase_entry.place(relx=0.5, rely=0.5)

time_label=Label(interface, text="Time (Seconds)")
time_label.place(relx=0.2, rely=0.6)

time_entry=Entry(interface, width=10)
time_entry.place(relx=0.5, rely=0.6)

send_command_button = Button(
    interface,
    text="Send Command",
    command = send_command
)
send_command_button.place(relx=0.4, rely=0.8)

#GUI loop
interface.mainloop()
