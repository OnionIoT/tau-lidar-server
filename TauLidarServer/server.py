import sys
import os
import asyncio
import json
from time import sleep, time
from threading import Thread, Lock
from pathlib import Path

import websockets
from http.server import SimpleHTTPRequestHandler, HTTPServer
from http.client import HTTPSConnection
import socketserver

from TauLidarCommon.frame import FrameType, Frame
from TauLidarCamera.camera import Camera
from TauLidarCamera.constants import VALUE_10MHZ, VALUE_20MHZ
from TauLidarCommon.color import ColorMode

def serverLoop(HTTP_PORT = 8080, WS_PORT = 5678):
    attempts = 0
    while True:
        try:
            '''
            By default, Camera will connect to the first available ToF device.
            Alternatively can specify serial port by using Camera.open('/dev/ttyACM0') to open specific port
            '''
            camera = Camera.open()

            cameraInfo = camera.info()
            print("\nToF camera opened successfully:")

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
                print("Exiting due to failure to start Tau Camera!")
                print("Error: %s" % str(e))
                try:
                    sys.exit(0)
                except SystemExit:
                    os._exit(0)
            sleep(5)
        sleep(0.1)


    ip_address = '127.0.0.1'

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
                '''
                Camera supports frame type FrameType.DISTANCE, FrameType.DISTANCE_GRAYSCALE and FrameType.DISTANCE_AMPLITUDE,
                default FrameType is FrameType.DISTANCE_GRAYSCALE

                frame = camera.readFrame(FrameType.DISTANCE_AMPLITUDE)

                To get a 3D Frame object directly from calling camera.readFrame() is an expensive call,
                alternatively you may call camera.readFrameRawData to get raw data
                and possibly to compose Frame from a separate thread
                to boost frame rate:

                ...
                from TauLidarCommon.d3 import FrameBuilder
                ...
                frameBuilder = FrameBuilder()
                ...
                dataArray = camera.readFrameRawData(frameType=FrameType.DISTANCE_GRAYSCALE)

                Possibly you may compose Frame from a separate thread
                frame = frameBuilder.composeFrame(dataArray, frameType=FrameType.DISTANCE_GRAYSCALE)

                Default FrameType is FrameType.DISTANCE_GRAYSCALE

                Following examples are how to construct depth map, grayscale and amplitude image accordingly:

                mat_depth_rgb = np.frombuffer(frame.data_depth_rgb, dtype=np.uint16, count=-1, offset=0).reshape(frame.height, frame.width, 3)
                mat_depth_rgb = mat_depth_rgb.astype(np.uint8)

                mat_grayscale = np.frombuffer(frame.data_grayscale, dtype=np.uint16, count=-1, offset=0).reshape(frame.height, frame.width)
                mat_grayscale = mat_grayscale.astype(np.uint8)

                mat_amplitude = np.frombuffer(frame.data_amplitude, dtype=np.float32, count=-1, offset=0).reshape(frame.height, frame.width)
                mat_amplitude = mat_amplitude.astype(np.uint8)
                '''
                frame = camera.readFrame(frameType=FrameType.DISTANCE_GRAYSCALE)
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

    # change dir to module directory
    web_dir = Path(__file__).absolute().parent
    os.chdir(web_dir)

    # start http server
    Handler = SimpleHTTPRequestHandler
    Handler.extensions_map.update({
        ".js": "application/javascript",
    })

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

if __name__ == "__main__":
    serverLoop()
