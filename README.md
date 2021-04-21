# TauLidarServer
Python package for Tau Studio web application

![Onion Tau Lidar Camera](https://github.com/OnionIoT/tau-lidar-server/raw/master/img/onion-tau-lidar-camera-00.png)

## Main Features

Starts the Tau LiDAR Camera server - initialize the camera and start the Tau Studio Web Application. Use Tau Studio with your browser to visualize data from the Camera and adjust the settings.

![Onion Tau Studio Web App](https://github.com/OnionIoT/tau-lidar-server/raw/master/img/onion-tau-studio-00.png)

## [Getting Started Guide](https://github.com/OnionIoT/tau-lidar-server/blob/master/GET-STARTED.md)

Check out the [Getting Started Guide](https://github.com/OnionIoT/tau-lidar-server/blob/master/GET-STARTED.md) for step-by-step instructions on how to get up and running with the Tau Camera.

(And for troubleshooting tips to resolve common issues)

## Installation & Supported Versions

Install using pip on the command line:

```
python -m pip install TauLidarServer
```

Supports Python 3.7+

## Running the Application

Run on the command line:

```
python -m TauLidarServer
```

If a Tau Camera is connected, you will see output like this:

```
ToF camera opened successfully:
    model:      4.0
    firmware:   3.3
    uid:        69.549
    resolution: 160x60
    port:       /dev/cu.usbmodem00000000001A1
    IP address: 127.0.0.1
    URL:  http://127.0.0.1:8080

Press Ctrl + C keys to shutdown ...
```

Use a **web browser** to navigate to the URL listed in the command line output!

## Contributing to Development

See the [development document](https://github.com/OnionIoT/tau-lidar-server/blob/master/DEVELOPMENT.md) for instructions on local development.

More info on contributing coming soon!
