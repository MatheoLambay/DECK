import pygame

#button class
class Button():
	def __init__(self,screen,x, y,text,text_color,font_size,center_pos = "topleft"):
		
		self.screen = screen

		self.text = text
		self.text_color = text_color
		self.font_size = font_size
		self.data_font = pygame.font.Font("freesansbold.ttf", self.font_size)
		self.data = self.data_font.render(self.text,True,self.text_color)
		self.rect = self.data.get_rect()
			
			
		if center_pos == "topleft":
			self.rect.topleft = (x,y)
		elif center_pos == "topright":
			self.rect.topright = (x,y)
		elif center_pos == "bottomright":
			self.rect.bottomright = (x,y)
		elif center_pos == "bottomleft":
			self.rect.bottomleft = (x,y)
		elif center_pos == "center":
			self.rect.center = (x,y)
		else:
			print('position error')

		self.clicked = False
		self.activated = None
	

	def draw(self):
	
		self.activated = True
		self.data_font = pygame.font.Font("freesansbold.ttf", self.font_size)
		self.data = self.data_font.render(self.text,True,self.text_color)
		self.screen.blit(self.data, (self.rect.x, self.rect.y))
		
	
	def detect(self):
		if self.activated:
			action = False
			#get mouse position
			pos = pygame.mouse.get_pos()

			#check mouseover and clicked conditions
			if self.rect.collidepoint(pos):
					
				if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
					self.clicked = True
					action = True

			if pygame.mouse.get_pressed()[0] == 0:
				self.clicked = False

			return action
		