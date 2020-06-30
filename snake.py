#
#		A SNAKE GAME
#
# The "settings" or the Main Variables to change how look and feel are just below the import statements

import sys
import os
import random
import time
try:
	import pygame
except ModuleNotFoundError:
	print("Looks like you havent downloaded PyGame in your system. May I?(y/n): ")
	ch = input()
	if ch == 'y' or ch =='Y':
		try:
			s = os.system('pip3 install pygame')
		except:
			try:
				s = os.system('pip install pygame')
			except:
				pass
		else:
			if s == 0:
				print(" Pygame has been installed successfully!! Lets go")
				os.system('python3 snake.py')
				sys.exit()
			else:
				print(" Sorry, we are facing trouble right now, Please try again Later")
				sys.exit() 
	else:
		print(" Without it we cannot run this game, forced quit activated!")
		sys.exit()
except Exception as e:
	print(e)
	print("An error occured, Sorry")
	sys.exit()

pygame.init()
#pygame.mixer.init()   #this was for sounds not yet ready

# ----Global Variables----
#-- Also your Settings panel --

#-- The dimensions of the screen
Scr_width = 500
Scr_height = 500
wall_border = 20	#---width of the wall
	
#----Colours and fonts
wall_color = pygame.Color("navy")
snake_clr = pygame.Color("green")
bg_clr = pygame.Color("black")			#----The Background Colour
fruit_clr = pygame.Color("red")
font = pygame.font.Font("freesansbold.ttf",Scr_width//60)

#----radius of the fruit
fruit_rad = 10

#--- Snake initial parameters
speed = 12		
last_press = pygame.K_RIGHT  #--last pressed direction
length = 5
snake_block = 20
max_length = length
speed_inc = 2		#----Increments to the speed after eating fruit

#levels = [10, 20, 27, 33, 38]
#level = 0

#---playable region dimension---- not to be changed!!!
sw = (Scr_width-2*wall_border)  
sh = (Scr_height - 5*wall_border)


#----- classes -----


class food:
	global screen, fruit_clr
	def __init__(self, pos, rad):
		self.x = pos[0]
		self.y = pos[1]
		self.fruit_rad = rad

	def show(self, pnt = [0,0]):
		global bg_clr
		if pnt != [0,0]:
			pygame.draw.circle(screen, bg_clr, (self.x, self.y), self.fruit_rad)
			self.x, self.y = pnt[0], pnt[1]
		pygame.draw.circle(screen, fruit_clr, (self.x, self.y), self.fruit_rad)

	def update(self, snake, blk):
		global Scr_height, Scr_width, wall_border, length, speed, max_length, speed_inc
		fd = [self.x, self.y]
#		print("x: food = {}, snake = {}".format(self.x, snake[0]))
#		print("y: food = {}, snake = {}".format(self.y, snake[1]))
		temp = range(0,blk+ self.fruit_rad//2)
		if ((fd[0] - snake[0]) in temp) and ((fd[1] - snake[1]) in temp) : 
#			print("True")
			length +=1
			if length>max_length:
				max_length = length
			speed += speed_inc
#			print(speed)
			fd = None
			while fd is None:
				nf = list(find_pos())
				fd = nf if nf not in snake else None
			show_score(Scr_width//3, wall_border)
			self.show(fd)
			ate = 1
		else:
#			print("False")
			ate = 0
		return(ate)


class Snake:
	global length
	body=[]
	def __init__(self, x, y, blk):
		self.x = x
		self.y = y
		self.body_blk = blk
		self.body = [[x,y], [x-self.body_blk, y], [x-2*self.body_blk,y]]
		if length > len(self.body):
			for i in range(3,length+1):
				self.body.append([x - i*self.body_blk, y])

	def show(self, eat = 0):
		pass
		global screen, bg_clr, snake_clr
		if eat == 0:
			pygame.draw.rect(screen, bg_clr, pygame.Rect(self.body[-1][0], self.body[-1][1], self.body_blk, self.body_blk))
			self.body.pop()
		else:
			pygame.draw.rect(screen, snake_clr, pygame.Rect(self.body[-1][0], self.body[-1][1], self.body_blk, self.body_blk))
		
		pygame.draw.rect(screen, snake_clr, pygame.Rect(self.body[0][0], self.body[0][1], self.body_blk, self.body_blk))

	def check_press(self, key, head):
		global last_press
		if key == pygame.K_DOWN or key == pygame.K_s:
			last_press = pygame.K_DOWN
			head[1] += self.body_blk
		if key == pygame.K_UP or key == pygame.K_w:
			last_press = pygame.K_UP
			head[1] -= self.body_blk
		if key == pygame.K_LEFT or key == pygame.K_a:
			last_press = pygame.K_LEFT
			head[0] -= self.body_blk
		if key == pygame.K_RIGHT or key == pygame.K_d:
			last_press = pygame.K_RIGHT
			head[0] += self.body_blk
		return head

	def update(self, fruit_1):
		global sh, sw, bg_clr, screen, last_press, wall_border
		head = [self.body[0][0], self.body[0][1]]
		event = pygame.event.poll()
		flg = 1
		if head[0] < 2*wall_border or head[0] > (sw - self.body_blk + 5):
#			print("Horizontal limit exceeded\n")
			The_end(1)
		elif (head[1] < (5*wall_border - 10)) or (head[1] > (sh + 3*wall_border - self.body_blk)):
#			print("Vertical limit exceeded\n")
			The_end(1)
		elif event.type == pygame.KEYDOWN:
			key = event.key
#			print(str( head in self.body[1:]))
			if key == pygame.K_DOWN and last_press == pygame.K_UP:
				flg = 1
			elif key == pygame.K_UP and last_press == pygame.K_DOWN:
				flg = 1
			elif key == pygame.K_RIGHT and last_press == pygame.K_LEFT:
				flg = 1
			elif key == pygame.K_LEFT and last_press == pygame.K_RIGHT:
				flg = 1
			else:
				flg = 2
#				head = self.check_press(key, head)
		elif head in self.body[1:]:
			The_end(1)
		elif event.type == pygame.QUIT:
			The_end()
		if flg==1:
			head = self.check_press(last_press, head)
		else:
			head = self.check_press(key, head)
		self.body.insert(0, head)
		if fruit_1.update(self.body[0], self.body_blk) == 1:
			self.show(1)
		else:
			self.show(0)

#Function to get the position of the next Fruit
def find_pos():
	global wall_border, sw, sh
	x = wall_border + (random.randrange(wall_border,sw-2*wall_border)//10)*10 +5
	y = 5*wall_border + (random.randrange(sh-3*wall_border)//10)*10 +5	
	return((x,y))

#To decide whether the program should continue or not
def The_end(flg = 0):
	if flg == 1:
		time.sleep(0.5)
		main()
	else:
		print("\n Thank You!! :-)\n")
	sys.exit()
#	pygame.quit()

#Prints the Score and max Score to the screen
def show_score(x,y):
	global length, screen, bg_clr, max_length, wall_border
	pygame.draw.rect(screen, bg_clr, pygame.Rect(0, 0, Scr_width, 3*wall_border))
#	screen.blit(scr, (x, y))
	s = " SNAKE "
	n = random.randint(1,100000)
	if n == 12398:
		s = " SNAEK "
	scr = font.render(" Length: " + str(length) , True, (255,255,255))
	screen.blit(scr, (x - wall_border,y))
	scr2 = font.render(s , True, (255,255,255))
	screen.blit(scr2, ((3*x)//2 - wall_border,y))
	scr3 = font.render(" Highest Length: " + str(max_length), True, (255,255,255))
	screen.blit(scr3 ,(2*x,y))


# Creating the Screen object
if Scr_height <= 300 or Scr_width <= 400:
	print("\n The User Set Dimensions are not playable!!\n Reverting to default\n")
	Scr_width = 1250
	Scr_height = 600
	sw, sh = (Scr_width-2*wall_border), (Scr_height - 5*wall_border)

screen = pygame.display.set_mode((Scr_width, Scr_height))


def main():
	global wall_border, Scr_width, Scr_height, sh, sw, wall_color, bg_clr, last_press, length, snake_block, fruit_rad, speed
	last_press = pygame.K_RIGHT
#	ball_1.reset(random.randrange(2*wall_border,Scr_width - 100), random.randrange(2*wall_border,Scr_height - 100), ball_vel[0], ball_vel[1])
	length = 5
	speed = 12
	show_score(Scr_width//3, wall_border)
	fruit_1 = food(find_pos(), fruit_rad)
	snake = Snake((sw//40)*10, (sh//20)*10, snake_block)
	# The walls
	pygame.draw.rect(screen, wall_color, pygame.Rect(0, 3*wall_border, Scr_width, Scr_height))
	pygame.draw.rect(screen, bg_clr, pygame.Rect(wall_border, 4*wall_border, (Scr_width-2*wall_border), (Scr_height - 5*wall_border)))
	clk = pygame.time.Clock()
	while True:
		e = pygame.event.poll()
		if e.type == pygame.QUIT:
			break
		fruit_1.show()
		clk.tick(speed)
		snake.update(fruit_1)
		pygame.display.flip()
	print("\n Thank You!! :-)\n")
	pygame.quit()	

if __name__=='__main__':
	main()
'''
Snaek Game1.1
Made By HariSK20
'''