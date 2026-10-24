from movement import go_to
from utilities import harv, check_water, check_soil

def main_drone():
	v = BLOCKS["Grass"]
	x = v[0] 
	y = v[1] + 5
	w = 9 # width
	h = 4 # height
	for j in range(y , y + h):
		for i in range(x, x + w):
			go_to(i, j)
			harv()
			check_water()
			
def grass_drone():
	while True:	
		v = BLOCKS["Grass"]
		x = v[0] 
		y = v[1]
		w = 9 # width
		h = 5 # height 
		for j in range(y , y + h):
			for i in range(x, x + w):
				go_to(i, j)
				harv()
				check_water()
			
def carrot_drone():
	v = BLOCKS["Carrots"]
	x = v[0]
	y = v[1]
	w = 9 # width
	h = 9 # height 
	while True:	
		for j in range(y, y + h):
			for i in range(x, x + w):
				go_to(i, j)
				check_soil()
				harv()
				plant(Entities.Carrot)
				check_water()
			
def tree_strip(x, y, w, h):
	for j in range(y, y + h):
		for i in range(x, x + w):
			go_to(i, j)
			harv()
			if (i + j) % 2 == 1:
				plant(Entities.Tree)
				check_water()
			else:
				plant(Entities.Bush)

def tree1_drone():
	v = BLOCKS["Trees1"]
	while True:
		tree_strip(v[0], v[1], 18, 4)

def tree2_drone():
	v = BLOCKS["Trees2"]
	while True:
		tree_strip(v[0], v[1], 4, 22)
	
def pumpkin_drone():
	v = BLOCKS["Pumpkins"]
	x = v[0]
	y = v[1]
	w = 9 # width
	h = 9 # height
	def plant_entire_field(x, y, w, h):
		for j in range(y, y + h):
			for i in range(x, x + w):
				go_to(i, j)
				check_soil()
				plant(Entities.Pumpkin)
				check_water()
	
	def dead_pumps(x, y, w, h):
		# drone checks the field and appends their coordinates (x,y) as a tuple in the list: dead
		dead = []
		for	j in range(y, y + h):
			for i in range(x, x + w):
				go_to(i, j)
				pump = get_entity_type()
				if pump == Entities.Dead_Pumpkin or not can_harvest() or pump != Entities.Pumpkin:
					dead.append([i, j])
		return dead		
		
	def replant(dead):
		# drone checks the list and replants dead pumpkins recording the list: dead. After first replant 
		# checks the pumpkins that are still dead appends them to new list: still_dead and update the original list 
		while len(dead) > 0:
			still_dead = []
			for pos in dead:
				go_to(pos[0], pos[1])
				check_soil()
				if get_entity_type() != Entities.Pumpkin:
					plant(Entities.Pumpkin)
					check_water()
				pump = get_entity_type()
				if pump == Entities.Dead_Pumpkin or not can_harvest() or pump != Entities.Pumpkin:
					still_dead.append([pos[0], pos[1]])
			dead = still_dead 
			
	while True:
		plant_entire_field(x, y, w, h)
		dead = dead_pumps(x, y, w, h)
		replant(dead)
		go_to(x, y)
		harv()

def cactus_drone():
	v = BLOCKS["Cactus"]
	x = v[0]
	y = v[1]
	w = 9 # width
	h = 9 # height
	def plant_entire_field(x, y, w, h):
		for j in range(y, y + h):
			for i in range(x, x + w):
				go_to(i, j)
				check_soil()
				plant(Entities.Cactus)
				
	def wait_to_grow(x, y, w, h):
		ready = False 
		while not ready:
			ready = True
			for j in range(y, y + h):
				for i in range(x, x + w):
					go_to(i,j)
					if get_entity_type() != Entities.Cactus or not can_harvest():
						ready = False
		
	def sort_field(x, y, w, h):
		# uses buble sort to sort cactus, keeps track of if a swap happens in the loop and returns the result. 
		# stops after a loop has no swaps meanning the field is ready for harvest  
		swapped = False
		for j in range(y, y + h):
			for i in range(x, x + w):
				go_to(i, j)
				here = measure()
				if i < x + w - 1:
					if measure(East) != None and here > measure(East):
						swap(East) 
						swapped = True
						here = measure()
				if j < y + h - 1:
					if measure(North) != None and here > measure(North):
						swap(North) 
						swapped = True
						here = measure() 
		return swapped
							
	while True:
		plant_entire_field(x, y, w, h)
		wait_to_grow(x, y, w, h)
		while sort_field(x, y, w, h):
			pass
		go_to(x, y)
		harv()
	
def asign_drone(field):
	if field == "Carrots":
		spawn_drone(carrot_drone)
	elif field == "Cactus":
		spawn_drone(cactus_drone)
	elif field == "Pumpkins":
		spawn_drone(pumpkin_drone)
	elif field == "Grass":
		spawn_drone(grass_drone)
	elif field == "Trees1":
		spawn_drone(tree1_drone)
	else:
		spawn_drone(tree2_drone)

	
BLOCKS = {"Carrots" : (0,0), "Cactus" : (9,0), "Pumpkins" : (9,9), "Grass" : (0, 9), "Trees1" : (0, 18), "Trees2" : (18, 0)}
go_to(0,0)
drone_count = 0
for key in BLOCKS:
	if drone_count >= max_drones():
		break
	value = BLOCKS[key]
	go_to(value[0], value[1])
	asign_drone(key)
	
go_to(0, 14)
while True:
	main_drone()



	
	

	
		