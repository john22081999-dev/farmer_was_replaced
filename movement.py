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