# smart_filter_cube

## Working Principle

- A filter is simulated using ball valve.
- The pressure in front of the ball valve (the filter) is measured with a pressure sensor.
- The pressure sensor sends a current-coded 4-20mA signal to the microcontroller (MKR 1000).
- The microcontroller converts the current signals to pressure values and it sends the sensor values over the network to a gateway (Raspberry Pi)
- The microcontroller and gateway are connected to the router.
- The IoT platform Thingsboard and the MQTT messaging broker Mosquitto are installed on the Raspberry
- The current and historical pressure values can be shown on a dashboard locally in the cube, but also on a smart device, whereby the smart device must be connected to the router and be able to call the IP address of the dashboard in an internet browser.
- In the Cube, the sensor values can be visualized on a 5-inch display which is connected with HDMI cable to the RPi.
- All services were dockerized (Docker Containers) and run with docker-compose.

## Sources:
The IoT Platform:
https://thingsboard.io/

The open source messaging broker Mosquitto
https://mosquitto.org/

## Smart Filter Cube

![SFC190319_001](https://user-images.githubusercontent.com/47817165/167089367-cf96f437-eb5c-40a6-b049-f859af2001bf.jpg)

![SFC190319_003](https://user-images.githubusercontent.com/47817165/167089390-1bb64d92-1d91-40dd-886e-e1ac7a820d25.jpg)
