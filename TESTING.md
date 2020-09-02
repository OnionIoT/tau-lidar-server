## Testing server.py locally

```
cd TauLidarServer
```

setup virtual environment (only needs to be done once):
```
python3 -m venv .
```

activate virtual environment:
```
source bin/activate
```

install TauLidarCamera test package
```
python3 -m pip install --index-url https://test.pypi.org/simple/ --no-deps TauLidarCamera
```

install dependencies
```
python3 -m pip install pyserial websockets
```

run program
```
python3 server.py
```
