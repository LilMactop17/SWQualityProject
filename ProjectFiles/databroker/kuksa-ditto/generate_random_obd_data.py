import random
import time

def main():
    # Repeat Infinitely
    while True:
        # Generate random values for each feature with the defined ranges
        VehicleSpeed = random.randrange(0, 255, 1)
        EngineSpeed = random.randrange(0, 1000, 1)
        ThrottlePosition = random.randrange(0, 200, 1)
        CoolantTemperature = random.randrange(0, 500, 1)

        # Print the value for each feature
        print('Vehicle Speed =', VehicleSpeed)
        print('Engine Speed =', EngineSpeed)
        print('Throttle Position =', ThrottlePosition)
        print('Coolant Temperature =', CoolantTemperature)

        # Pause for 1 second
        time.sleep(1)

        print('-----------------------------')

# Run the main function
main()
