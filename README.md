# smart_filter_cube

## Working Principle

A ball valve simulates a filter.
The pressure in front of the ball valve (the filter) is measured with a pressure sensor.
The pressure sensor sends a current-coded 4-20mA signal to the microcontroller (MKR 1000).
The microcontroller converts the current signals to pressure values and it sends the sensor values over the network to a gateway (Raspberry Pi).
The microcontroller and gateway are connected to the router.
The IoT platform Thingsboard is installed on the Raspberry Pi single-board computer.
The current and historical pressure values can be shown on a dashboard locally in the cube, but also on a smart device, whereby the smart device must be connected to the router and be able to call the IP address of the dashboard.
In the Cube, the sensor values can be visualized on a 5-inch display.

## Sourcers:
The IoT Platform:
https://thingsboard.io/
