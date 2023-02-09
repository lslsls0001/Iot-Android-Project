# this part of code is used to collect the EEG signals frequency data
# it is created and modifiid by Yibo Li

from timeit import default_timer as timer
import time

from pythonosc import dispatcher
from datetime import datetime
from pythonosc import osc_server

# *********************  we define the parameters here for all function to use  *********************
alpha_freq = [-1,-1,-1,-1]
beta_freq = [-1,-1,-1,-1]
delta_freq = [-1,-1,-1,-1]
theta_freq = [-1,-1,-1,-1]
gamma_freq = [-1,-1,-1,-1]

all_freq = [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1]

ip_address = "172.20.10.2"
port_num = 5000

file_dir = 'Events_4/bg.csv'
file_dir_2 = 'Events_4/'

file = open (file_dir,'a+')
title = 'time,A9,A7,A8,A10,B9,B7,B8,B10,D9,D7,D8,D10,T9,T7,T8,T10,G9,G7,G8,G10\n'

cur_file = ''
cur_event = 0
cur_row = 0
count = 0

sec = 6
record = False
flag = True
rec_dict = {"1"  : 6,"bg"  : 6,}
start_t = timer()

# handle alpha frequency channel
def alpha_handler(address: str,*args):
    global alpha_freq, beta_freq, delta_freq, theta_freq, gamma_freq

    if (len(args)==5):
        all_freq[0] = args[1]
        all_freq[1] = args[2]
        all_freq[2] = args[3]
        all_freq[3] = args[4]

# handle beta frequency channel
def beta_handler(address: str,*args):
    global alpha_freq, beta_freq, delta_freq, theta_freq, gamma_freq

    if (len(args)==5):
        all_freq[4] = args[1]
        all_freq[5] = args[2]
        all_freq[6] = args[3]
        all_freq[7] = args[4]

# handle delta frequency channel
def delta_handler(address: str,*args):
    global alpha_freq, beta_freq, delta_freq, theta_freq, gamma_freq

    if (len(args)==5):
        all_freq[8] = args[1]
        all_freq[9] = args[2]
        all_freq[10] = args[3]
        all_freq[11] = args[4]

# handle theta frequency channel
def theta_handler(address: str,*args):
    global alpha_freq, beta_freq, delta_freq, theta_freq, gamma_freq

    if (len(args)==5):
        all_freq[12] = args[1]
        all_freq[13] = args[2]
        all_freq[14] = args[3]
        all_freq[15] = args[4]

# handle gamma frequency channel
def gamma_handler(address: str,*args):
    global alpha_freq, beta_freq, delta_freq, theta_freq, gamma_freq, flag

    if (len(args)==5):
        all_freq[16] = args[1]
        all_freq[17] = args[2]
        all_freq[18] = args[3]
        all_freq[19] = args[4]

    if flag == False:
        for idx in range(0,19):
            file.write(str(all_freq[idx]) + ",")
        file.write(str(all_freq[19]))
        file.write("\n")
    else:
        collect_activity()

# ********* collect each event per one time *********
def collect_activity():
    global cur_event, cur_file
    global start_t, end_t, sec, cur_row, count

    end_t = timer()
    if (end_t - start_t) >= sec:
        start_t = timer()
        event = list(rec_dict.items())[cur_event][0]
        sec = list(rec_dict.items())[cur_event][1]
        cur_row = 0
        
        cur_date_time = datetime.now()
        cur_time = cur_date_time.strftime("%Y-%m-%d %H_%M_%S.%f")

        event = list(rec_dict.items())[cur_event][0]
        cur_file = file_dir_2 + event + '.' + cur_time + '.csv'
        event_file = open(cur_file,'a+')
        event_file.write(title)

        print(f"Think:\t {event}   \t\t{sec}  seconds")
        print(count)
        count = count + 1

        dict_len = len(rec_dict)
        if cur_event < dict_len-1:
            cur_event = cur_event + 1
        else:
            cur_event = 0
    else:
        if cur_file != '':
            event_file = open(cur_file,'a+')
            event_file.write(str(cur_row) + ',')
            cur_row = cur_row + 1
            for idx in range(0,19):
                event_file.write(str(all_freq[idx]) + ",")
            event_file.write(str(all_freq[19]))
            event_file.write("\n")
            time.sleep(4)

def marker_handler(address: str,i):
    global record, flag, start_t, end_t

    cur_date_time = datetime.now()
    cur_time = cur_date_time.strftime("%Y-%m-%d %H:%M:%S.%f")
    num = address[-1]
    file.write(cur_time+",,,,/Marker/"+num+"\n")
    start_t = timer()
    if (num=="1"):
        record = True
    if (num=="2"):
        file.close()
        server.shutdown()
    if (num=="3"):
        start_t = timer()

        for idx in range(len(rec_dict)):
            event = list(rec_dict.items())[idx][0]
            event_file = open (file_dir_2 + event + '.csv','a+')
            event_file.write(title)

        if flag == False:
            flag = True
            collect_activity()
        else:
            flag = False

if __name__ == "__main__":
    dispatcher = dispatcher.Dispatcher()

    dispatcher.map("/Marker/*", marker_handler)
    dispatcher.map("/muse/elements/delta_absolute", delta_handler,0)
    dispatcher.map("/muse/elements/theta_absolute", theta_handler,1)
    dispatcher.map("/muse/elements/alpha_absolute", alpha_handler,2)
    dispatcher.map("/muse/elements/beta_absolute",  beta_handler,3)
    dispatcher.map("/muse/elements/gamma_absolute", gamma_handler,4)

    server = osc_server.ThreadingOSCUDPServer((ip_address, port_num), dispatcher)
    server.serve_forever()