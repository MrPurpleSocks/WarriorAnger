
# importing OpenCV, time and Pandas library
import cv2
import pandas
import time as tm
from datetime import datetime
import numpy

def waitForStart():
	# Assigning our static_back to None
	static_back = None

	# List when any moving object appear
	motion_list = [ None, None ]

	# Time of movement
	time = []

	# Initializing DataFrame, one column is start
	# time and other column is end time
	df = pandas.DataFrame(columns = ["Start", "End"])

	# Capturing video
	video = cv2.VideoCapture(3)

	# Infinite while loop to treat stack of image as video
	while True:
		# Reading frame(image) from video

		check, plain_frame = video.read()

		h, w = plain_frame.shape[:2]
		mask = numpy.zeros_like(plain_frame)
		mask[:, :] = [255, 255, 255]
		mask = cv2.rectangle(mask, (0, h-250), (w, h), (0, 0, 0), -1)  # Bottom
		mask = cv2.rectangle(mask, (0,0), (w, 140), (0,0,0), -1)  # Top
		mask = cv2.rectangle(mask, (0, 50), (75, h-200), (0,0,0), -1)  # Left
		mask = cv2.rectangle(mask, (w-0, 80), (w-100, 260), (0, 0, 0), -1)  # Right
		mask = cv2.rectangle(mask, ((w//2)-150, 0), ((w//2)+120, h), (0, 0, 0), -1)  # Middle
		frame = cv2.bitwise_and(plain_frame, mask)


		# Initializing motion = 0(no motion)
		motion = 0

		# Converting color image to gray_scale image
		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

		# Converting gray scale image to GaussianBlur
		# so that change can be find easily
		gray = cv2.GaussianBlur(gray, (1, 1), 0)

		# In first iteration we assign the value
		# of static_back to our first frame
		if static_back is None:
			static_back = gray
			continue

		# Difference between static background
		# and current frame(which is GaussianBlur)
		diff_frame = cv2.absdiff(static_back, gray)

		# If change in between static background and
		# current frame is greater than 30 it will show white color(255)
		thresh_frame = cv2.threshold(diff_frame, 7, 255, cv2.THRESH_BINARY)[1]
		thresh_frame = cv2.dilate(thresh_frame, None, iterations = 2)

		# Finding contour of moving object
		cnts,_ = cv2.findContours(thresh_frame.copy(),
						cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

		for contour in cnts:
			if cv2.contourArea(contour) < 2000:
				continue
			motion = 1

			(x, y, w, h) = cv2.boundingRect(contour)
			# making green rectangle around the moving object
			cv2.rectangle(plain_frame, (x, y), (x + w, y + h), (0, 255, 0), 3)

		cv2.imshow("Start: Setup", frame)
		cv2.imshow("Start: Visualize", plain_frame)

		# Appending status of motion
		motion_list.append(motion)

		motion_list = motion_list[-2:]

		# Appending Start time of motion
		if motion_list[-1] == 1 and motion_list[-2] == 0:
			time.append(datetime.now())

		# Appending End time of motion
		if motion_list[-1] == 0 and motion_list[-2] == 1:
			time.append(datetime.now())

		if motion == 1:
			return True

		key = cv2.waitKey(1)
		# if q entered whole process will stop
		if key == ord('q'):
			# if something is movingthen it append the end time of movement
			if motion == 1:
				time.append(datetime.now())
			break

def waitForClear():
	timerTriggered = False
	# Assigning our static_back to None
	static_back = None

	# List when any moving object appear
	motion_list = [ None, None ]

	# Time of movement
	time = []

	# Initializing DataFrame, one column is start
	# time and other column is end time
	df = pandas.DataFrame(columns = ["Start", "End"])

	# Capturing video
	video = cv2.VideoCapture(3)

	# Infinite while loop to treat stack of image as video
	count = 0
	while True:
		# Reading frame(image) from video
		check, plain_frame = video.read()

		h, w = plain_frame.shape[:2]
		mask = numpy.zeros_like(plain_frame)
		mask[:, :] = [255, 255, 255]
		mask = cv2.rectangle(mask, (0, h-250), (w, h), (0, 0, 0), -1)  # Bottom
		mask = cv2.rectangle(mask, (0,0), (w, 150), (0,0,0), -1)  # Top
		mask = cv2.rectangle(mask, (0, 0), (55, h), (0,0,0), -1)  # Left
		mask = cv2.rectangle(mask, (w-0, 0), (w-135, 280), (0, 0, 0), -1)  # Right
		#mask = cv2.rectangle(mask, ((w//2)-100, 0), ((w//2)+90, h), (0, 0, 0), -1)
		frame = cv2.bitwise_and(plain_frame, mask)


		# Initializing motion = 0(no motion)
		motion = 0

		# Converting color image to gray_scale image
		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

		# Converting gray scale image to GaussianBlur
		# so that change can be find easily
		gray = cv2.GaussianBlur(gray, (1, 1), 0)

		# In first iteration we assign the value
		# of static_back to our first frame
		if static_back is None:
			static_back = gray
			continue
		if count == 50:
			static_back = gray
			count = 0
			continue

		# Difference between static background
		# and current frame(which is GaussianBlur)
		diff_frame = cv2.absdiff(static_back, gray)

		# If change in between static background and
		# current frame is greater than 30 it will show white color(255)
		thresh_frame = cv2.threshold(diff_frame, 9, 255, cv2.THRESH_BINARY)[1]
		thresh_frame = cv2.dilate(thresh_frame, None, iterations = 2)

		# Finding contour of moving object
		cnts,_ = cv2.findContours(thresh_frame.copy(),
						cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

		for contour in cnts:
			if cv2.contourArea(contour) < 2000:
				continue
			motion = 1

			(x, y, w, h) = cv2.boundingRect(contour)
			# making green rectangle around the moving object
			cv2.rectangle(plain_frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
			cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
		if not cnts:
			motion = 0

		if motion == 0 and not timerTriggered:
			start = tm.perf_counter()
			timerTriggered = True

		curTime = tm.perf_counter()

		if timerTriggered and round(curTime - start) == 30:
			if motion == 0:
				return True
			else:
				timerTriggered = False

		cv2.imshow("Clear: Setup", frame)
		cv2.imshow("Clear: Visualize", plain_frame)

		# Appending status of motion
		motion_list.append(motion)

		motion_list = motion_list[-2:]

		# Appending Start time of motion
		if motion_list[-1] == 1 and motion_list[-2] == 0:
			time.append(datetime.now())

		# Appending End time of motion
		if motion_list[-1] == 0 and motion_list[-2] == 1:
			time.append(datetime.now())

		key = cv2.waitKey(1)
		# if q entered whole process will stop
		if key == ord('q'):
			# if something is movingthen it append the end time of movement
			if motion == 1:
				time.append(datetime.now())
			break
		count += 1

waitForStart()
