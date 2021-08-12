import time

###############################################################################
import subprocess
import shlex
import cv2
import os
####################################################i###########################

# def FFPlayer(PlayCmd):
#
#     # if PlayerProc:
#     #     # PlayerProc.terminate()
#     #     PlayerProc.kill()
#     #     subprocess.run(["/usr/bin/killall", "ffplay"])
#     # else:
#     # PlayerProc = subprocess.Popen(WrapPlayCmd)
#     PlayerProc = subprocess.Popen(shlex.split(PlayCmd),
#         stdout=subprocess.DEVNULL,
#         stderr=subprocess.DEVNULL,
#         stdin=subprocess.DEVNULL
#     )

def openCvPlay(fifo = './fifo_file',save=False):
    cap = cv2.VideoCapture()
    ret = cap.open(fifo)
    _, img = cap.read()
    count=0
    while True:
        try:
            flag, img = cap.read()
            # img = cv2.imread(fifo)
            #tag =pass(img)
            # img = tag +img
            if img.shape:
                print(img.shape)
            #if flag and save and count%10==0:
            if flag and count % 10 == 0:

                w, h, c = img.shape
                img=cv2.resize(img,(int(h/2),int(w/2)))
                cv2.imshow('img', img)
                #cv2.imwrite(os.path.join('./output',str(int(count/10)).zfill(6)+'.jpg'),img)
            count+=1
            if cv2.waitKey(1) & 0xff == ord('q'):
                break
        except KeyboardInterrupt:
            return


if __name__ == '__main__':
    openCvPlay(save=True)
