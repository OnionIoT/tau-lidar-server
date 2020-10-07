import sys
import os
import asyncio
import json
from time import sleep, time
from threading import Thread, Lock

import websockets
from http.server import SimpleHTTPRequestHandler, HTTPServer
from http.client import HTTPSConnection
import socketserver

from TauLidarCamera.camera import Camera
from TauLidarCamera.constants import VALUE_10MHZ, VALUE_20MHZ
from TauLidarCommon.color import ColorMode

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

        ## you may simply use camera.setDefaultParameters()
        camera.setModulationFrequency(VALUE_20MHZ) ## frequency: 20MHZ
        camera.setModulationChannel(0)             ## autoChannelEnabled: 0, channel: 0
        camera.setMode(0)                          ## Mode 0, wide fov
        camera.setHdr(0)                           ## HDR off
        camera.setIntegrationTime3d(0, 800)        ## set integration time 0: 1000
        camera.setMinimalAmplitude(0, 60)          ## set minimal amplitude 0: 80
        camera.setOffset(0)                        ## set distance offset: 0
        camera.setRoi(0, 0, 159, 59)               ## set ROI to max width and height
        
        ## static
        Camera.setColorMode(ColorMode.DISTANCE)    ## use distance for point color
        Camera.setRange(0, 7500)                   ## points in the distance range to be colored
        
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
    sleep(0.1)

HTTP_PORT = 8080
WS_PORT = 5678
if len(sys.argv) == 3:
    HTTP_PORT = int(sys.argv[1])
    WS_PORT = int(sys.argv[2])

ip_address = '127.0.0.1'
# try:
#     s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#     s.connect(("8.8.8.8", 80))
#     ip_address = s.getsockname()[0]
#     s.close()
# except:
#     #print("No network ...")
#     pass

print("    IP address: %s" % ip_address)
print("    URL:  %s" % 'http://' + ip_address + ':' + str(HTTP_PORT))

print("\nPress Ctrl + C keys to shutdown ...")

_count = 0
start_time = time()
running = True

async def send3DPoints(websocket, path):
    global _count
    global running
    start_time = time()
    _count = 0

    async for message in websocket:
        data = json.loads(message)

        if data['cmd'] == 'read':
            frame = camera.readFrame()
            if frame == None:
                print('skip frame')
                continue
            points = json.dumps(frame.points_3d)
            try:
                await websocket.send(points)
            except:
                break
        elif data['cmd'] == 'set':
            if data['param'] == 'range':
                Camera.setRange(0, data['value'])
            elif data['param'] == 'intTime3D':
                camera.setIntegrationTime3d(0, data['value'])

ws_server = websockets.serve(send3DPoints, "127.0.0.1", WS_PORT)
asyncio.get_event_loop().run_until_complete(ws_server)

ws_t = Thread(target=asyncio.get_event_loop().run_forever)
ws_t.deamon = True
ws_t.start()

Handler = SimpleHTTPRequestHandler
Handler.extensions_map.update({
    ".js": "application/javascript",
});
#httpd = HTTPServer((ip_address, HTTP_PORT), SimpleHTTPRequestHandler)
httpd = socketserver.TCPServer(("", HTTP_PORT), Handler)

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
