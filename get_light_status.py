import cv2
import numpy as np


class TrafficLightDetector:
	def __init__(self):
			
		# 2. Define Color Ranges (Hue, Saturation, Value)
		# Red has two ranges because it wraps around the 0/180 degree mark
		self.lower_red1 = np.array([0, 100, 100])
		self.upper_red1 = np.array([10, 255, 255])
		self.lower_red2 = np.array([160, 100, 100])
		self.upper_red2 = np.array([180, 255, 255])
		
		self.lower_yellow = np.array([15, 100, 100])
		self.upper_yellow = np.array([35, 255, 255])
		
		self.lower_green = np.array([40, 100, 100])
		self.upper_green = np.array([90, 255, 255])
		
		# Configuration
		self.CLASS_NAMES = ['Green', 'Red', 'Yellow'] # Ensure this matches your training order
		self.COLOR_MAP = {'Green': (0, 255, 0), 'Red': (0, 0, 255), 'Yellow': (0, 255, 255)}

	def get_light_state(self,crop):
		if crop is None or crop.size == 0:
		    return "UNKNOWN"
		
			
	    # 1. Convert to HSV
		hsv = cv2.cvtColor(crop, cv2.COLOR_BGR2HSV)
		h, w, _ = hsv.shape
	    
	
	    # 3. Create Masks
		mask_red = cv2.add(cv2.inRange(hsv, self.lower_red1, self.upper_red1),cv2.inRange(hsv, self.lower_red2, self.upper_red2))
		mask_yellow = cv2.inRange(hsv, self.lower_yellow, self.upper_yellow)
		mask_green = cv2.inRange(hsv, self.lower_green, self.upper_green)
	
	    # 2. Count non-zero pixels for each color
		counts = {
	        "Red": cv2.countNonZero(mask_red),
	        "Yellow": cv2.countNonZero(mask_yellow),
	        "Green": cv2.countNonZero(mask_green)
	    }

	    # 3. Find the dominant color
		state = max(counts, key=counts.get)
		
		# 4. Validation: Only return if the dominant color has enough "presence"
	    # A threshold of 10 pixels is very low—consider 5% of total area for robustness
		if counts[state] < (h * w * 0.05):
			return "UNKNOWN"
	
	    # # 5. Spatial Verification (Optional but recommended)
	    # # Check if the Red is actually in the upper half, etc.
	    # if state == "Red":
	    #     # Does at least 60% of red pixels appear in the top 60% of the box?
	    #     top_half_red = cv2.countNonZero(mask_red[0:int(h*0.6), :])
	    #     if top_half_red < (counts["Red"] * 0.6):
	    #         return "UNKNOWN" # Likely a reflection or tail light, not the signal head
		
		return state
	
	    # # 4. Divide crop into 3 horizontal zones (Top, Middle, Bottom)
	    # height, _ = mask_red.shape
	    # top = mask_red[0:height//3, :]
	    # mid = mask_yellow[height//3:2*height//3, :]
	    # bot = mask_green[2*height//3:height, :]
	
	    # # 5. Determine state based on pixel density in specific zones
	    # if cv2.countNonZero(top) > 10: # Threshold of 10 pixels
	    #     return "Red"
	    # elif cv2.countNonZero(mid) > 10:
	    #     return "Yellow"
	    # elif cv2.countNonZero(bot) > 10:
	    #     return "Green"
	    
	    # return "UNKNOWN"