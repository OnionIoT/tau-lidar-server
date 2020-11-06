# Development Guide

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

Make sure you have local versions of the [tau-lidar-common](https://github.com/OnionIoT/tau-lidar-common) and [tau-lidar-camera](https://github.com/OnionIoT/tau-lidar-camera) repos.

Locally install the TauLidarCommon package
```
python -m pip install -e /path/to/tau-lidar-common
```

Locally install the TauLidarCamera package
```
python -m pip install -e /path/to/tau-lidar-camera
```

Local install of **this** tau-lidar-server package:
```
python -m pip install -e /path/to/tau-lidar-server
```

Now test the package as you see fit.

### To run the program:

After the above setup is complete

```
python -m TauLidarServer
```

### Note on Code Updates

**Any edits to the `tau-lidar-server` package source code in `/path/to/tau-lidar-server` will be reflected when the testing program is run again**


## Testing server.py locally

**This is no longer necessary! All development should be done with the above method!**
