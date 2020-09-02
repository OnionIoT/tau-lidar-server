import sys
import os
import asyncio
import json
from time import sleep, time
from threading import Thread, Lock

import websockets
from http.server import SimpleHTTPRequestHandler, HTTPServer
from http.client import HTTPSConnection

from tof.camera import Camera
from tof.color import ColorMode

attempts = 0
while True:
    try:
        camera = Camera.open() #alternatively can use camera.open('/dev/ttyACM0') to open specific port

        cameraInfo = camera.info()
        print("ToF camera opened successfully:")

        print("    model:      %s" % cameraInfo.model)
        print("    firmware:   %s" % cameraInfo.firmware)
        print("    uid:        %s" % cameraInfo.uid)
        print("    resolution: %s" % cameraInfo.resolution)
        print("    port:       %s" % cameraInfo.port)

        camera.setDefaultParameters()
        camera.setIntegrationTime3d(0, 600)
        camera.setIntegrationTimeGrayscale(6000)
        Camera.setRange(50, 7500)
        break

    except Exception as e:
        attempts += 1

        if attempts > 10:            
            print("Exiting due to failure of opening ToF camera!")
            print("Error: %s" % str(e))
            try:
                sys.exit(0)
            except SystemExit:
                os._exit(0)
        sleep(5)

HTTP_PORT = 8080
WS_PORT = 5678
if len(sys.argv) == 3:
    HTTP_PORT = int(sys.argv[1])
    WS_PORT = int(sys.argv[2])

ip_address = '127.0.0.1'
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip_address = s.getsockname()[0]
    s.close()
except:
    #print("No network ...")
    pass

print("    IP address: %s" % ip_address)  
print("    URL:  %s" % 'http://' + ip_address + ':' + str(HTTP_PORT))  

print("\nPress Ctrl + C keys to shutdown ...")  

camera.setDefaultParameters()
camera.setIntegrationTime3d(0, 1000)
camera.setIntegrationTimeGrayscale(6000)
Camera.setRange(1000, 4000)

_count = 0
start_time = time()
running = True

async def send3DPoints(websocket, path):
    global _count
    global running
    start_time = time()
    _count = 0
    while running:
        frame = camera.readFrame()
        if frame == None: 
            sleep(0.1)
            continue
        
        _count += 1

        points = json.dumps(frame.points_3d)

        try:
            await websocket.send(points)
        except:
            break  
    end_time = time()
    seconds_elapsed = end_time - start_time
    fps = float(_count) / float(seconds_elapsed)
    print("Session closed, overall fps: %d" % fps)

ws_server = websockets.serve(send3DPoints, "127.0.0.1", WS_PORT)
asyncio.get_event_loop().run_until_complete(ws_server)

ws_t = Thread(target=asyncio.get_event_loop().run_forever)
ws_t.deamon = True
ws_t.start()

httpd = HTTPServer((ip_address, HTTP_PORT), SimpleHTTPRequestHandler)
try:
    httpd.serve_forever()
except KeyboardInterrupt:  
    running = False
    print('\nShutting down ...')
    sleep(0.1)
    camera.close()
    try:
        httpd.socket.close()
        httpd.server_close()
        
        sys.exit(0)
    except SystemExit:
        os._exit(0)
