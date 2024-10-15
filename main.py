import numpy as np
import cv2
import glob

# Define the chess board rows and columns
rows = 6
cols = 8


criteria = (cv2.TERM_CRITERIA_MAX_ITER + cv2.TERM_CRITERIA_EPS, 30, 0.001)
objectPoints = np.zeros((rows * cols, 3), np.float32)
objectPoints[:, :2] = np.mgrid[0:rows, 0:cols].T.reshape(-1, 2)


objectPointsArray = []
imgPointsArray = []


for path in glob.glob('dataset/cam1/*.png'):
    # Load the image
    img = cv2.imread(path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Find corners
    ret, corners = cv2.findChessboardCorners(gray, (rows, cols), None)
    if ret:
        corners = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
        objectPointsArray.append(objectPoints)
        imgPointsArray.append(corners)

        cv2.drawChessboardCorners(img, (rows, cols), corners, ret)
  
   # save the image
    cv2.imwrite('output/cam1/' + path.split('/')[-1], img)

# Calibrate the camera and save the results
ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objectPointsArray, imgPointsArray, gray.shape[::-1], None, None)
np.savez('output/cam1/calib.npz', mtx=mtx, dist=dist, rvecs=rvecs, tvecs=tvecs)

# Print the camera calibration error
error = 0

for i in range(len(objectPointsArray)):
    imgPoints, _ = cv2.projectPoints(objectPointsArray[i], rvecs[i], tvecs[i], mtx, dist)
    error += cv2.norm(imgPointsArray[i], imgPoints, cv2.NORM_L2) / len(imgPoints)


print("Total error: ", error / len(objectPointsArray))
print("Distortion coefficients: ", dist)
print("Intrinsic matrix: ", mtx)


# loop load image and undistort
for i,path in enumerate(glob.glob('dataset/cam1/*.png')):
    # Load one of the test images
    img = cv2.imread(path)
    h, w = img.shape[:2]

    # Obtain the new camera matrix and undistort the image
    newCameraMtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (w, h), 0.5, (w, h))
    undistortedImg = cv2.undistort(img, mtx, dist, None, newCameraMtx)

    # Crop the undistorted image
    x, y, w, h = roi
    undistortedImg = undistortedImg[y:y + h, x:x + w]
    # save image 
    name = path.split('/')[-1]
    cv2.imwrite(f'output/cam1/undistorted_{name}.png', undistortedImg)
