from lib.usb_dev import USBDev
from lib.fifo_writer import FIFOWriter
import time
from utils.yaml_wrapper import YamlHandler

StatusInterval = 0.5

headset = USBDev()
headset.startDevCheckThread()

fifo = FIFOWriter()
fifo.Open()

# State globals:
BytesWritten = 0
LastStatus = 0
StatusData = dict()
StatusData['Msg'] = "Starting Up"

###############################################################################

def PrintStatus(update):
    """Update the program status"""
    global LastStatus
    now = time.time()
    if (now - LastStatus) < StatusInterval:
        return
    print(update['Msg'] + "               ", end='\r')
    LastStatus = now

def main(opts):
    flag = True
    time_sleep = opts['time_sleep']
    global BytesWritten
    while True:
        PrintStatus(StatusData)
        # print(StatusData)

        # just run at first epoch

        if headset.DevicePresent != False:
            data = headset.RecvData()
        else:
            # print("Waiting on headset...")
            StatusData['Msg'] = "Waiting on headset..."
            # If we are waiting on a headset and data has been written, everything needs to be reset:
            if BytesWritten:
                BytesWritten = 0
                fifo.Reset()

            # No sense being speedy on the loop when we are waiting on a human
            time.sleep(time_sleep)
            continue

        if data != None:
            out = fifo.Write(data)
            '''
            if flag:
                print('out2file ...')
                flag=False
            else:
                print('out2file .....')
                flag = True
            '''
        else:
            # print("RecvData() returned None: {}".format(headset.LastError.strerror))
            StatusData['Msg'] = "Device State: " + headset.DeviceStatus
            continue


        if out:
            BytesWritten += out
            StatusData['Total'] = BytesWritten
            #print('byte2out')
        else:
            # print("Pausing fifo, no readers...")
            StatusData['Msg'] = "Output buffer full, pausing fifo..."
            time.sleep(time_sleep)
            continue

        # print("In write loop, error: " + str(fifo.LastError) + ", total bytes written: " + str(BytesWritten))
        StatusData['Msg'] = "Device State: " + headset.DeviceStatus
        # time.sleep(.5)
        # exit()

if __name__ == '__main__':
    opts = YamlHandler('./options/settings.yaml').read_yaml()
    main(opts)