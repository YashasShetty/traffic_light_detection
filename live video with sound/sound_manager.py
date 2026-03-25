import time
import pygame

class TrafficSoundManager:
	def __init__(self, cooldown=0.25):
		pygame.mixer.init()
		
		path = "music/"
		self.Red_light_sound = pygame.mixer.Sound(path + "red.ogg")
		self.Yellow_light_sound = pygame.mixer.Sound(path +"yellow.ogg")
		self.Green_light_sound = pygame.mixer.Sound(path +"green.ogg")
		self.UNKNOWN_light_sound = pygame.mixer.Sound(path +"unknown.ogg")
		
		# State tracking
		self.previous_state = None
		self.last_play_time = 0
		self.cooldown = cooldown  # Seconds between repeat sounds
		
	def update(self, current_state):
		current_time = time.time()

		time_passed = current_time - self.last_play_time
        
		# 1. Trigger on State Change (e.g., Green -> Red)
		if current_state != self.previous_state and time_passed>=self.cooldown:
			if(current_state=="Red"):
				self.Red_light_sound.play()
			elif(current_state=="Yellow"):
				self.Yellow_light_sound.play()
			elif(current_state=="Green"):
				self.Green_light_sound.play()
			elif(current_state=="UNKNOWN"):
				self.UNKNOWN_light_sound.play()
				
			# Reset timer and update memory
			self.last_play_time = current_time
			self.previous_state = current_state
            
        # # 2. Optional: Repeat sound if state stays "Red" longer than cooldown
        # elif current_state == "Red" and (now - self.last_play_time) > self.cooldown:
        #     self.red_sound.play()
        #     self.last_play_time = now

	def cleanup(self):
		"""Manually stop all sounds and shut down the mixer."""
		# print("Cleaning up audio resources...")
		pygame.mixer.stop()  # Stop all active sound channels
		pygame.mixer.quit()  # Uninitialize the mixer
		
	def __del__(self):
		"""Magic method: runs automatically when the object is destroyed."""
		try:
			self.cleanup()
		except:
			pass # Prevent errors if mixer was already closed

# --- Initialization ---
sound_manager = TrafficSoundManager()