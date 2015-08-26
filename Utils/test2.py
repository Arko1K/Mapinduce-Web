__author__ = 'arko1k'


import numpy as np
import cv2
from PIL import Image
from matplotlib import pyplot as plt


# def rect_for_contour(con):
#     # Get coordinates of a rectangle around the contour
#     leftmost = tuple(con[con[:,:,0].argmin()][0])
#     topmost = tuple(con[con[:,:,1].argmin()][0])
#     bottommost = tuple(con[con[:,:,1].argmax()][0])
#     rightmost = tuple(con[con[:,:,0].argmax()][0])
#
#     return leftmost[0], topmost[1], rightmost[0], bottommost[1]
#
#
# def contour_to_image(con, original_image):
#     # Get the rect coordinates of the contour
#     lm, tm, rm, bm = rect_for_contour(con)
#
#     con_im = original_image.crop((lm, tm, rm, bm))
#
#     if con_im.size[0] == 0 or con_im.size[1] == 0:
#         return None
#
#     con_pixels = con_im.load()
#
#     for x in range(0, con_im .size[0]):
#         for y in range(0, con_im.size[1]):
#             # If the pixel is already white, don't bother checking it
#             if con_im.getpixel((x, y)) == (255, 255, 255):
#                 continue
#
#             # Check if the pixel is outside the contour. If so, clear it
#             if cv2.pointPolygonTest(con, (x + lm, y + tm), False) < 0:
#                 con_pixels[x, y] = (255, 255, 255)
#
#     return con_im
#
#
# image_orig = cv2.imread('img.png') # Load your image in here
#
# lower = np.array([20,0,155], dtype=np.uint8)
# upper = np.array([255,120,250], dtype=np.uint8)
# image = cv2.inRange(image_orig.copy(), lower, upper)
#
#
# contours, hierarchy = cv2.findContours(image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
#
# print(len(contours))
# big_cnt = None
# big_area = 0
# for cnt in contours:
#     x, y, w, h = cv2.boundingRect(cnt)
#     a = w * h
#     if a > big_area:
#         big_area = a
#         big_cnt = cnt
#
# # Your code to threshold
# # image = cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 45, 0)
# #
# # Perform morphology
# # se = np.ones((7,7), dtype=np.uint8)
# # image_close = cv2.morphologyEx(image, cv2.MORPH_CLOSE, se)
# #
# # # Your code now applied to the closed image
# # cnt = cv2.findContours(image_close, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)[0]
# # mask = np.zeros(image.shape[:2], np.uint8)
# # im = cv2.drawContours(mask, cnt, -1, 255, -1)
#
# con_im = contour_to_image(big_cnt, Image.open('img.png'))
# con_im.save('processed.png')
#
# x,y,w,h = cv2.boundingRect(big_cnt)
# # cv2.rectangle(image,(x,y),(x+w,y+h),(0,255,0),2)
# print(x,y,w,h)
# # cv2.imshow('Features', image)
# # cv2.imwrite('processed.png', image)
# # cv2.destroyAllWindows()


im = cv2.imread('img.png')

lower = np.array([20,0,155])
upper = np.array([255,120,250])
shapeMask = cv2.inRange(im, lower, upper)

se = np.ones((7,7), dtype=np.uint8)
image_close = cv2.morphologyEx(shapeMask, cv2.MORPH_CLOSE, se)

# # imgray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
# ret,thresh = cv2.threshold(im,127,255,0)
# imgray = cv2.cvtColor(thresh,cv2.COLOR_BGR2GRAY)
contours, hierarchy = cv2.findContours(shapeMask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
#
# big_cnt = None
# big_area = 0
# for cnt in contours:
#     a = cv2.contourArea(cnt)
#     if a < 3799.5 and a > big_area:
#         big_area = a
#         big_cnt = cnt
#

print(len(contours))

# print(cv2.contourArea(big_cnt))
# drawing = np.zeros(im.shape)
cv2.drawContours(im, contours, -1, (0,255,0), 3)
cv2.imwrite('processed.png', im)