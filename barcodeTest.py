from imutils.video import VideoStream
from pyzbar import pyzbar
import argparse
import datetime
import imutils
import time
import cv2
import csv

ap = argparse.ArgumentParser()
ap.add_argument("-o", "--output", type=str, default="barcodes.csv",
	help="path to output CSV file containing barcodes")
args = vars(ap.parse_args())


def print_bar_data(i):
    with open('rest.csv') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        sk = list(csvfile)
        # for row in reader:
        print(sk[i])
    csvfile.close()





# initialize the video stream and allow the camera sensor to warm up
print("[INFO] starting video stream...")
vs = VideoStream(src=0).start()
#vs = VideoStream(usePiCamera=True).start()
time.sleep(2.0)
csv1 = open(args["output"], "w")


found = set()
i=0

while True:
    # grab the frame from the threaded video stream and resize it to
    # have a maximum width of 400 pixels
    frame = vs.read()
    frame = imutils.resize(frame, width=400)

    # find the barcodes in the frame and decode each of the barcodes
    barcodes = pyzbar.decode(frame)
    # loop over the detected barcodes
    for barcode in barcodes:
        # extract the bounding box location of the barcode and draw
        # the bounding box surrounding the barcode on the image
        (x, y, w, h) = barcode.rect
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # the barcode data is a bytes object so if we want to draw it
        # on our output image we need to convert it to a string first
        barcodeData = barcode.data.decode("utf-8")
        barcodeType = barcode.type

        # draw the barcode data and barcode type on the image
        text = "{} ({})".format(barcodeData, datetime.datetime.today())
        cv2.putText(frame, text, (x, y - 10),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        # if the barcode text is currently not in our CSV file, write
        # the timestamp + barcode to disk and update the set
        if barcodeData not in found:
            #csv.write("{},{}\n".format(datetime.datetime.now(),barcodeData))
            csv1.write("{}\n".format(barcodeData))
            csv1.flush()
            found.add(barcodeData)
            print(barcodeData)
            if (barcodeData=='Onion1'):
                print_bar_data(0)
            if (barcodeData=='Onion2'):
                print_bar_data(1)
            if (barcodeData=='Onion3'):
                print_bar_data(2)
            if (barcodeData=='Bacon1'):
                print_bar_data(3)
            if (barcodeData=='Bacon2'):
                print_bar_data(4)
            if (barcodeData=='Bacon3'):
                print_bar_data(5)
            if (barcodeData=='Pasta1'):
                print_bar_data(6)
            if (barcodeData=='Pasta2'):
                print_bar_data(7)
            if (barcodeData=='Pasta3'):
                print_bar_data(8)

        #if barcodeData == data:
            #csv1.write("{}\n".format(data))
            # show the output frame
    cv2.imshow("Barcode Scanner", frame)
    key = cv2.waitKey(1) & 0xFF
        # if the `q` key was pressed, break from the loop
    if key == ord("q"):
        break

    # close the output CSV file do a bit of cleanup
print("[INFO] cleaning up...")
csv1.close()
cv2.destroyAllWindows()
vs.stop()