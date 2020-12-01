# Getting Started with the Onion Tau LiDAR Camera

This guide will help you set up your Tau LiDAR Camera for the first time. We’ll cover:

* Unboxing your Tau Camera
* Installing the required software
* Connecting the Tau Camera to your computer
* Using the Tau Studio web application

## First Time Setup

Steps you'll only need to do once!

### Unbox and Prep the Tau Camera

📦 Unpack the Tau Camera

📷 Make sure to remove the protective sticker from the lens

### Installing Software

To use the Tau Studio Web App, you'll need to have Python and TauLidarServer installed.

#### 🐍 Install python
Download and install Python at https://www.python.org/downloads/. **Make sure you install version 3.6.1 or higher**.

If you have questions about using Python, check out the [official Python.org  instructions](https://docs.python.org/3/using/index.html).

#### 📩 Install the `TauLidarServer` Python module

Open a command-line window, and run the following command:
`python -m pip install TauLidarServer`

#### 🥳 You're ready to use your Tau Camera!

## Using the Tau Camera

### 📸 Connecting the Tau Camera to your Computer

Use a USB cable to connect the Tau Camera to your computer. It has a USB Type-C port, so you'll need a compatible cable.

### ⚙️ Starting the Tau Studio Software

To start the Tau Studio Web App, run this in a command line window:

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

### 🖥 Using the Tau Studio web app

Use a **web browser** to navigate to the **URL** listed in the command line output from the last step! And you've arrived to the Tau Studio Web App

![Onion Tau Studio Web App](img/onion-tau-studio-00.png)

Hit the question mark button in the sidebar for more info on how to work with the Tau Studio

🍻 Have fun!

## Troubleshooting

A few troubleshooting tips in case you encounter any issues!

### Bad frame ignored error -> Need a better cable

**The Problem:**

If you launch the Tau Studio and get an error in the command line that looks something like this:

```
Data error, actual size: 33788, expected size: 38480
Bad frame ignored, bytes length: 33708
skip frame
Bad frame ignored, bytes length: 0
skip frame
Bad frame ignored, bytes length: 0
skip frame
...
```

**The Solution:**

Try switching to a high-quality cable! If possible, try using a not-super-long USB-C to USB-C cable from a reputable brand.

Then try running the program again.
