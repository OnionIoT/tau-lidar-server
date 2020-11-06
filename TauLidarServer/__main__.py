# __main__.py

from configparser import ConfigParser
from importlib import resources  # Python 3.7+
import sys

from TauLidarServer import server

def main():
    """Run the Tau LiDAR Camera Server"""

    # process arguments
    #   Not allowing cusotmized Websocket ports since it breaks the webviewer - see https://github.com/OnionIoT/tau-lidar-server/issues/13
    # if len(sys.argv) > 2:
    #     HTTP_PORT = int(sys.argv[1])
    #     WS_PORT = int(sys.argv[2])
    #
    #     server.serverLoop(HTTP_PORT, WS_PORT)

    if len(sys.argv) > 1:
        HTTP_PORT = int(sys.argv[1])

        server.serverLoop(HTTP_PORT)

    else:
        # run with defaults
        server.serverLoop()

if __name__ == "__main__":
    main()
