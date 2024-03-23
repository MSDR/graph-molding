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