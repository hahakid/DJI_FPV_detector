import time
###############################################################################
import subprocess
import shlex
import cv2
import os
from lib import darknet
####################################################i###########################
#yolo configs

config_file='./cfg/yolov4-tiny.cfg' #model structures
data_file='./cfg/coco.data' #class defines based dataset and labels
weights='./cfg/yolov4-tiny.weights' # model weights for filters
##################################
def image_detection(image, network, class_names, class_colors, thresh):
    # Darknet doesn't accept numpy images.
    # Create one with image we reuse for each detect
    width = darknet.network_width(network)
    height = darknet.network_height(network)
    darknet_image = darknet.make_image(width, height, 3)
    is_bgr=True #confirm if needed
    #image = cv2.imread(image_path)
    if is_bgr:
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    else:
        image_rgb=image
    image_resized = cv2.resize(image_rgb, (width, height),
                               interpolation=cv2.INTER_LINEAR)

    darknet.copy_image_from_bytes(darknet_image, image_resized.tobytes())
    detections = darknet.detect_image(network, class_names, darknet_image, thresh=thresh)
    darknet.free_image(darknet_image)
    image = darknet.draw_boxes(detections, image_resized, class_colors)
    return cv2.cvtColor(image, cv2.COLOR_BGR2RGB), detections

############################################
def detector(fifo = './fifo_file',save=False):
    #'''
    network, class_names, class_colors = darknet.load_network(
        config_file,
        data_file,
        weights,
        batch_size=1 #default
    )
    dont_show=False
    #'''
    cap = cv2.VideoCapture()
    ret = cap.open(fifo)
    flag, img = cap.read()
    index=0
    while True:
        try:
            flag, img = cap.read()
            if flag:
            #'''
            #if flag and index%10==0:
                #img=cv2.resize(img,(int(h/2),int(w/2)))# based on device&model to speed up
                prev_time = time.time()
                #w, h, c = img.shape
                #img = cv2.resize(img, (int(h / 2), int(w / 2)))
                #cv2.imshow('img', img)
                img, detections = image_detection(img, network, class_names, class_colors, thresh=0.25)
                #darknet.print_detections(detections, True)#print bbox info
                #darknet.print_detections(detections, False)  # print bbox info
                cv2.imshow('img', img)
                fps = int(1 / (time.time() - prev_time))
                print(fps)
                cv2.imwrite(os.path.join('./output',str(index).zfill(6)+'.jpg'),img)
                index += 1
                if cv2.waitKey(1) & 0xff == ord('q'):
                    break
            #index += 1
        except KeyboardInterrupt:
            return

#if __name__ == '__main__':
#    detector(save=False)
