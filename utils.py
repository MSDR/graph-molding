def coords_to_str(x, y):
    return '('+str(x)+','+str(y)+')'

def coords_to_str(tup):
    x,y = tup
    return '('+str(x)+','+str(y)+')'

def coords_to_tuple(str):
    comma_index = str.index(',')
    x = int(str[1:comma_index])
    y = int(str[comma_index+1:-1])
    return (x, y)

def manhattan_distance(coords1, coords2):
    return abs(coords1[0] - coords2[0]) + abs(coords1[1] - coords2[1])

# world_size = (width, height)
def coords_within_world(coords, world_size):
    width, height = world_size
    if type(coords) == str:
        coords = coords_to_tuple(coords)
    
    x, y = coords
    if x < 0 or x > width or y < 0 or y > height:
        return False
    return True

# given center_coords and an adjacent point_coords,
# move distance on square surrounding center_coords from point_coords
def move_on_3x3_square_perimeter(center_coords, point_coords, distance):
    if type(center_coords) == str:
        center_coords = coords_to_tuple(center_coords)
        
    # coordinates of square perimeter
    cx, cy = center_coords
    perimeter_coords = [(cx-1,cy+1), (cx,cy+1), (cx+1,cy+1), (cx+1, cy), 
                        (cx+1, cy-1), (cx, cy-1), (cx-1, cy-1), (cx-1, cy)]

    # calculate new coordinates from distance
    point_index = perimeter_coords.index(point_coords)
    new_index = point_index + distance
    if new_index < 0:
        new_index = 8 + new_index
    elif new_index >= 8:
        new_index = new_index - 8

    return perimeter_coords[new_index]