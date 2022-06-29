import RPi.GPIO as GPIO

GPIO.setMode(GPIO.BOARD)
pinLed = 10
pinBtn = 12

statusLed = False

def button_callback():
    global statusLed
    statusLed = not statusLed
    if statusLed:
        GPIO.output(pinLed, GPIO.HIGH)
    else:
        GPIO.output(pinLed, GPIO.LOW)
    
GPIO.setup(pinLed, GPIO.OUT)

GPIO.setup(pinBtn, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.add_event_detect(pinBtn, GPIO.RISING, callback=button_callback,bouncetim=300)

message = input("Press enter to quit/n")
GPIO.cleanup()