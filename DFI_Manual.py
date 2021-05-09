# Mohammad Yaghoobi, Alireza Abbaspourrad
# Cornell University, Ithaca, NY, USA
# Manual evaluation of DNA Fragmentation Index
# USAGE: Draw the white rectangle around the head of the sperm from
# bright field images and continue doing that for all sperm and the
# code will generate the necessay data and DFI and the figure of
# signal scattering

# M.Y., A.A. 05/09/2021
# Under MIT License

# import the necessary packages
import numpy as np
import cv2
import matplotlib.pyplot as plt

f = open("DFI.txt", "w")
Gpnts=[] #for RG diagram 
Rpnts=[] #for RG diagram

# initialize the list of reference points and boolean indicating
# whether cropping is being performed or not
refPt = []
imBit = 16;
cropping = False
def click_and_crop(event, x, y, flags, param):
    # grab references to the global variables
    global refPt, cropping
    # if the left mouse button was clicked, record the starting
    # (x, y) coordinates and indicate that cropping is being
    # performed
    if event == cv2.EVENT_LBUTTONDOWN:
        refPt = [(x, y)]
        cropping = True
    # check to see if the left mouse button was released
    elif event == cv2.EVENT_LBUTTONUP:
        # record the ending (x, y) coordinates and indicate that
        # the cropping operation is finished
        refPt.append((x, y))
        cropping = False
        # draw a rectangle around the region of interest
        cv2.rectangle(bfi, refPt[0], refPt[1], (2**(imBit)-1, 0, 0), 2)
        
        rI=red[refPt[0][1]:refPt[1][1], refPt[0][0]:refPt[1][0]]
        redMean=1.2*np.mean(rI)
        ret, rIC=cv2.threshold(rI,1.2*np.mean(rI),1,cv2.THRESH_BINARY)
        rm=rI*rIC
        rmean=rI*(1-rIC)
                
        gI=grn[refPt[0][1]:refPt[1][1], refPt[0][0]:refPt[1][0]]
        greenMean=1.2*np.mean(gI)
        ret, gIC=cv2.threshold(gI,1.2*np.mean(gI),1,cv2.THRESH_BINARY)
        gm=gI*gIC
        gmean=gI*(1-gIC)

        redsignal=np.max(rm)-np.max(rmean)
        Rpnts.append(redsignal)
        greensignal=np.max(gm)-np.max(gmean)
        Gpnts.append(greensignal)
        DFI=redsignal/(redsignal+greensignal)

        print(np.max(rm),np.max(rmean),np.max(gm),np.max(gmean)\
              ,redsignal,greensignal,DFI)
        cv2.imshow("image", bfi)
        cv2.imshow('g',gIC*(2**(imBit)-1))
        cv2.imshow('r',rIC*(2**(imBit)-1))
        cv2.moveWindow('r', 50,50)
        refPt=[]

file='raw 1-2' # file name containing field images
nfield=1 #Number of fields that images are token from
for N in range(nfield):

    grn0=cv2.imread(file+'\\img_000000{:0>3d}'.format(3*N+1)+'_Default_000.tif',cv2.IMREAD_UNCHANGED)
    red0=cv2.imread(file+'\\img_000000{:0>3d}'.format(3*N+2)+'_Default_000.tif',cv2.IMREAD_UNCHANGED)
    bfi0=cv2.imread(file+'\\img_000000{:0>3d}'.format(3*N)+'_Default_000.tif',cv2.IMREAD_UNCHANGED)

    newdim=(1024,1024)
    N1=[0,1,0,1]
    N2=[0,0,1,1]


    for X in range(0, 4):
            pnx=N1[X]
            pny=N2[X]
            grn=grn0[pnx*newdim[0]:(pnx+1)*newdim[0],pny*newdim[0]:(pny+1)*newdim[0]]
            red=red0[pnx*newdim[0]:(pnx+1)*newdim[0],pny*newdim[0]:(pny+1)*newdim[0]]
            bfi=bfi0[pnx*newdim[0]:(pnx+1)*newdim[0],pny*newdim[0]:(pny+1)*newdim[0]]

            grn=cv2.resize(grn,(700,700))
            red=cv2.resize(red,(700,700))
            bfi=cv2.resize(bfi,(700,700))

            clone = bfi.copy()
            #display the image and wait for a keypress
            cv2.imshow("image", bfi)
            cv2.setMouseCallback("image", click_and_crop)
            key = cv2.waitKey(0) & 0xFF
            #if the 'r' key is pressed, reset the cropping region
            if key == ord("r"):
                image = clone.copy()
                refPt = []
            # if there are two reference points, then crop the region of interest
            # from teh image and display it
            if len(refPt) == 2:
                    roi = clone[refPt[0][1]:refPt[1][1], refPt[0][0]:refPt[1][0]]
                    cv2.imshow("ROI", roi)
                    cv2.waitKey(0)
            # close all open windows
            cv2.destroyAllWindows()
plt.scatter(Rpnts,Gpnts,s=2)
plt.gca().set_aspect('equal', adjustable='box')
plt.xlim([0,500])
plt.ylim([0,1000])
plt.show()
