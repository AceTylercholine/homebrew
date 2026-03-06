import time
import RPi.GPIO as GPIO

# Pin definitions (Broadcom numbering)
TX_PIN = 17
RX_PIN = 18

# Setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(TX_PIN, GPIO.OUT)
# Configure receiver pin as input
GPIO.setup(RX_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# Activate the transmitter
GPIO.output(TX_PIN, GPIO.HIGH)
print("IR beam active. Waiting for break...")

try:
    last_state = GPIO.input(RX_PIN)
    while True:
        current_state = GPIO.input(RX_PIN)
        
        if current_state != last_state:
            # 0 indicates the beam is blocked (no IR detected)
            # 1 indicates the beam is hitting the receiver (IR detected)
            if current_state == 0:
                print("Beam broken! (Object detected)")
            else:
                print("Beam restored.")
            last_state = current_state
            
        time.sleep(0.05)

except KeyboardInterrupt:
    print("\nTest terminated.")

finally:
    # Safely turn off the LED and release the GPIO pins
    GPIO.output(TX_PIN, GPIO.LOW)
    GPIO.cleanup()