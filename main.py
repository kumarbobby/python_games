import pygame
from sys import exit
from random import randint,choice

class Player(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		player_walk_1 = pygame.image.load('graphics/Player/player_walk_1.png').convert_alpha()
		player_walk_2 = pygame.image.load('graphics/Player/player_walk_2.png').convert_alpha()
		self.player_walk = [player_walk_1,player_walk_2]
		self.player_jump = pygame.image.load('graphics/Player/jump.png').convert_alpha()
		self.player_index = 0
		self.image = self.player_walk[self.player_index]
		self.rect = self.image.get_rect(midbottom = (80,300))
		self.gravity = 0
		
		self.jump_sound = pygame.mixer.Sound('audio/jump.mp3')
		self.jump_sound.set_volume(0.2)


	def player_input(self):
		key = pygame.key.get_pressed()
		if key[pygame.K_SPACE] and self.rect.bottom >= 300:
			self.gravity = -20
			self.jump_sound.play()

	def apply_gravity(self):
		self.gravity += 1
		self.rect.bottom += self.gravity
		if self.rect.bottom >= 300: self.rect.bottom = 300

	def animation_state(self):
		if self.rect.bottom < 300:
			self.image = self.player_jump
		else:
			self.player_index += 0.1
			if self.player_index > len(self.player_walk):
				self.player_index = 0
			self.image = self.player_walk[int(self.player_index)]

	def update(self):
		self.player_input()
		self.apply_gravity()
		self.animation_state()

class Obstacles(pygame.sprite.Sprite):
	def __init__(self,type):
		super().__init__()
		
		if type == 'fly':
			fly_frame_1 = pygame.image.load('graphics/Fly/Fly1.png').convert_alpha()
			fly_frame_2 = pygame.image.load('graphics/Fly/Fly2.png').convert_alpha()
			self.frames = [fly_frame_1,fly_frame_2]
			self.y_pos = 210
		else:
			snail_frame_1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
			snail_frame_2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
			self.frames = [snail_frame_1,snail_frame_2]
			self.y_pos = 300
 		
		self.animation_index = 0
		self.image = self.frames[self.animation_index]
		self.rect = self.image.get_rect(midbottom = (randint(900,1100),self.y_pos))

	def animation_state(self):
		self.animation_index += 0.1
		if self.animation_index >= len(self.frames):
			self.animation_index = 0
		self.image = self.frames[int(self.animation_index)]

	def destroy(self):
		if self.rect.x < -100:
			self.kill

	def update(self):
		self.animation_state()
		self.rect.left -= 6
		self.destroy()

def disp_score():
	current_time = int(pygame.time.get_ticks()/1000) - start_time
	score_surface = testFont.render(f'{current_time}',False,(64,64,64))
	score_rect = score_surface.get_rect(center = (400,50))
	screen.blit(score_surface,score_rect)
	return current_time

def collisions():
	if pygame.sprite.spritecollide(player.sprite,obstacle_group,False):
		obstacle_group.empty()
		return True
	else: return False

pygame.init()

# Set_screen
screen = pygame.display.set_mode((800,400))
pygame.display.set_caption("FissamPatti (Made by Sudhanshu)")
clock = pygame.time.Clock()

game_over = True
start_time = 0
score = 0
score_list=[]
high_score = 0

# Groups
player = pygame.sprite.GroupSingle()
player.add(Player())

obstacle_group = pygame.sprite.Group()


testFont = pygame.font.Font('font/Pixeltype.ttf',50)
bg_music = pygame.mixer.Sound('audio/music.wav')
bg_music.set_volume(0.1)
bg_music.play(loops = -1)

# Scene
skySurface = pygame.image.load('graphics/sky.png').convert()
gndSurface = pygame.image.load('graphics/ground.png').convert()

# Introscreen
player_stand = pygame.image.load('graphics/Player/player_stand.png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand,0,2)
player_stand_rect = player_stand.get_rect(center = (400,200))

game_name = testFont.render("FISSAMPATTI",False,(111,196,169))
game_name_rect = game_name.get_rect(center = (400,60))

start_game = testFont.render("Press Space To Start",False,(111,196,169))
start_game_rect = start_game.get_rect(center = (400,340))

# Timers
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer,1500)

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			exit()
		# if not game_over:
			if player_rect.bottom == 300:	
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_SPACE:
						player_gravity = -20
				if event.type == pygame.MOUSEBUTTONDOWN:
					if player_rect.collidepoint(event.pos):
						player_gravity = -20
		
		if game_over == True:
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE:
					game_over = False
					start_time = int(pygame.time.get_ticks()/1000) 

		if not game_over:	
			if event.type == obstacle_timer:

				obstacle_group.add(Obstacles(choice(['fly','snail','snail','snail'])))

	
	if not game_over:
		screen.blit(skySurface,(0,0))
		screen.blit(gndSurface,(0,300))
		
		#Score_calculation
		score = disp_score()
		score_list.append(score)
		high_score = max(score_list)
		
		# Display on screen
		player.draw(screen)
		player.update()
		
		obstacle_group.draw(screen)
		obstacle_group.update()


		# game_over
		game_over = collisions()

	else:    #game_over
		screen.fill((94,129,162))
		screen.blit(game_name,game_name_rect)
		screen.blit(player_stand,player_stand_rect)
		score_message = testFont.render(f"Your Score : {score}",False,(111,196,169))
		score_message_rect = score_message.get_rect(center = (400,340))
		high_score_text = testFont.render(f"HI: {high_score}",False,(111,196,169))
		high_score_text_rect = high_score_text.get_rect(midleft = (650,60))

		if score == 0:	screen.blit(start_game,start_game_rect)
		else:
			screen.blit(score_message,score_message_rect)
			screen.blit(high_score_text,high_score_text_rect)

		

	pygame.display.update()
	clock.tick(60)