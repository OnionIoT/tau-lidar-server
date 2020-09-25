# Development Guide

## Testing server.py locally

> Development before code is restructured as a package

```
cd TauLidarServer
```

setup virtual environment **(only needs to be done once)**:
```
python3 -m venv .
```

activate virtual environment:
```
source bin/activate
```

Make sure you have a local version of the [tau-lidar-camera repo](https://github.com/OnionIoT/tau-lidar-camera)

Then install TauLidarCamera package
```
python -m pip install -e /path/to/tau-lidar-camera
```

install dependencies
```
python -m pip install websockets
```

run program
```
python server.py
```


## Local Development of the Package

> Will use [Virtual Environments](https://docs.python.org/3/tutorial/venv.html) and [PIP Editable Installs](https://pip.pypa.io/en/latest/reference/pip_install/#editable-installs) to locally install the package for development purposes

In your testing directory, setup the virtual environment **(only needs to be done once)**:
```
python3 -m venv .
```

Activate virtual environment:
```
source bin/activate
```

Local install of the tau-lidar-camera package:
```
python -m pip install -e /path/to/tau-lidar-server
```

Now test the package as you see fit.

**Any edits to the `tau-lidar-server` package source code in `/path/to/tau-lidar-server` will be reflected when the testing program is run again**
