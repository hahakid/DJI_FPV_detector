cat ./output/*.jpg | ffmpeg -f image2pipe -vcodec mjpeg -i - -c:v h264 -r 24 output.mp4
