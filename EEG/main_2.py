from datetime import datetime
from pythonosc import dispatcher
from pythonosc import osc_server

ip = "192.168.12.103"
port = 5000

alpha = [-1,-1,-1,-1]

def blink_handler(address, *args):
    print("blink")

def jaw_clench_handler(address, *args):
    print("jaw")

'''
def alpha_handler(address: str, *args):
    global alpha
    if len(args) == 5:
        for i in range(1,5):
            print(args[i])
'''

'''
def eeg_handler(address: str, *args):
    dateTimeObj = datetime.now()
    printStr = dateTimeObj.strftime("%Y-%m-%d %H:%M:%S.%f")
    for arg in args:
        printStr += "," + str(arg)
    print(printStr)
'''


if __name__ == "__main__":
    dispatcher = dispatcher.Dispatcher()
    #dispatcher.map("/muse/eeg", eeg_handler)
    dispatcher.map("/muse/elements/blink", blink_handler)
    dispatcher.map("/muse/elements/jaw_clench", jaw_clench_handler)
    #dispatcher.map("/muse/elements/alpha_absolute", alpha_handler, 2)

    server = osc_server.ThreadingOSCUDPServer((ip, port), dispatcher)
    print("Listening on UDP port " + str(port))
    server.serve_forever()