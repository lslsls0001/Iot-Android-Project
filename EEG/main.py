# use this tested code to transfer the brain signal (blink eye or jaw teeth) to Raspberry PI to control the motor arm.

from datetime import datetime
from pythonosc import dispatcher
from pythonosc import osc_server

ip = "192.168.12.103"
port = 5000

def blink_handler(address, *args):
    # directly transferring signals to Respberry Pi to control motor
    print("blink")

def jaw_clench_handler(address, *args):
    # directly transferring signals to Respberry Pi to control motor
    print("jaw")


if __name__ == "__main__":
    dispatcher = dispatcher.Dispatcher()
    dispatcher.map("/muse/elements/blink", blink_handler)
    dispatcher.map("/muse/elements/jaw_clench", jaw_clench_handler)

    server = osc_server.ThreadingOSCUDPServer((ip, port), dispatcher)
    print("Listening on UDP port " + str(port))
    server.serve_forever()