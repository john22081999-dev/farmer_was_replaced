# --- MOVEMMENTS ---
#=================================================
def go_to(x, y):
	while get_pos_x() != x:
		dx = (x - get_pos_x()) % get_world_size()
		if dx <= get_world_size() / 2:
				move(East)
		else:
				move(West)
	while get_pos_y() != y:
		dy = (y - get_pos_y()) % get_world_size()
		if dy <= get_world_size() / 2:
			move(North)
		else:
			move(South)
#=================================================
# --- UTILITIES --- 	
#=================================================	
def harv():
	if can_harvest():
		harvest()
		
def check_soil():
	if get_ground_type() != Grounds.Soil:
		till()
		
def check_water():
	if get_water() < 0.75:
			use_item(Items.Water)
	
def decision(x,y, field):
	if field == "Carrots":
		carrot_field(x, y, 6, 6)
	elif field == "Grass":
		grass_field(x, y, 6, 6)
	elif field == "Trees1":
		tree_field(x, y, 12, 4)
	else:
		tree_field(x, y, 4, 16)
				
#def check_field(i, j):
#	block_i = i // 6 # 6x6 Blocks and trees will wrap arround.
#	block_j = j // 6
#	if block_i < 2 and block_j < 2:
#		return BLOCKS[block_i][block_j]
#	else:
#		return "Trees"
			
#=================================================
# --- Fields ---
#=================================================
# 1. CARROTS  
def carrot_field(x, y, w, h):
	for j in range(y, y + h):
		for i in range(x, x + w):
			go_to(i, j)
			check_soil()
			harv()
			plant(Entities.Carrot)
			check_water()
#-------------------------------------------------
# 2. GRASS		
def grass_field(x, y, w, h):
	for j in range(y , y + h):
		for i in range(x, x + w):
			go_to(i, j)
			harv()
			check_water()
#-------------------------------------------------
# 3. PUMPKINS 		
def pumpkin_field(x, y, w, h, visits, dead):
	
	def plant_entire_field(x, y, w, h):
		for j in range(y, y + h):
			for i in range(x, x + w):
				go_to(i, j)
				check_soil()
				plant(Entities.Pumpkin)
				check_water()
	
	def dead_pumps(x, y, w, h):
		dead = []
		for j in range(y, y + h):
			for i in range(x, x + w):
				go_to(i, j)
				pump = get_entity_type()
				if pump == Entities.Dead_Pumpkin or not can_harvest() or pump != Entities.Pumpkin:
					dead.append([i, j])
		return dead		
		
	def replant(x, y, w, h, dead):
		if len(dead) > 0:
			still_dead = []
			for pos in dead:
				go_to(pos[0], pos[1])
				check_soil()
				plant(Entities.Pumpkin)
				check_water()
				pump = get_entity_type()
				if pump == Entities.Dead_Pumpkin or not can_harvest() or pump != Entities.Pumpkin:
					still_dead.append([pos[0], pos[1]])
			dead = still_dead 
			return dead 
					
	if visits == 0:
		plant_entire_field(x, y, w, h)
		dead = dead_pumps(x, y, w, h)
	else:
		dead = replant(x, y, w, h, dead)
		
	return dead
#-------------------------------------------------
# 4. CACTUS
def cactus_field(x, y, w, h, visits, flag):
	
	def plant_entire_field(x, y, w, h):
		for j in range(y, y + h):
			for i in range(x, x + w):
				go_to(i, j)
				check_soil()
				plant(Entities.Cactus)
				check_water()
	
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
		
	if visits == 0:
		plant_entire_field(x, y, w, h)
		wait_to_grow(x, y, w, h)
	else:
		flag = not sort_field(x, y, w, h)
		if not flag:
			flag = not sort_field(x, y, w, h)
	return flag
						
#-------------------------------------------------
# 5. TREES
def tree_field(x, y, w, h):
	for j in range(y, y + h):
		for i in range(x, x + w):
			go_to(i, j)
			harv()
			if (i % 2 == 1 and j % 2 == 0) or (i % 2 == 0 and j % 2 == 1):
				plant(Entities.Tree)
			else:
				plant(Entities.Bush)
#-------------------------------------------------
	

	
BLOCKS = {"Carrots" : (0,0), "Cactus" : (6,0), "Pumpkins" : (6,6), "Grass" : (0, 6), "Trees1" : (0, 12), "Trees2" : (12, 0)}
pumpkin_visits = 0
dead_pumpkins = []
cactus_visits = 0
cactus_sorted = False
while True:
	for key in BLOCKS:
		value = BLOCKS[key]
		if key == "Pumpkins":
			dead_pumpkins = pumpkin_field(value[0], value[1], 6, 6, pumpkin_visits, dead_pumpkins)
			if dead_pumpkins == []:
				go_to(value[0], value[1])
				harv()
				pumpkin_visits = 0
				dead_pumpkins = pumpkin_field(value[0], value[1], 6, 6, pumpkin_visits, dead_pumpkins)
				pumpkin_visits = 1
			else:
				pumpkin_visits += 1
		elif key == "Cactus":
			cactus_sorted = cactus_field(value[0], value[1], 6, 6, cactus_visits, cactus_sorted)
			if cactus_sorted:
				go_to(value[0], value[1])
				harv()
				cactus_visits = 0
				cactus_field(value[0], value[1], 6, 6, cactus_visits, cactus_sorted)
				cactus_sorted = False
				cactus_visits += 1
			else:
				cactus_visits += 1
		else:
			decision(value[0], value[1], key)
			
	 		
	 	