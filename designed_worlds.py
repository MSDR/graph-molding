import world

# tokyo rail network?
# https://i.makeagif.com/media/9-28-2018/9gYd4-.gif
def gif_mold():
    W = world.World(mold_pos=(47,48))
    W.place_food(food_coords=[((75,94), 1000),((53,90), 1000),((28,84), 1000),((35,84), 1000),((26,81), 1000),((40,81), 1000),((50,79), 1000),((71,82), 1000),((37,72), 1000),((62,68), 1000),
                              ((43,62), 1000),((44,57), 1000),((55,57), 1000),((72,59), 1000),((66,52), 1000),((34,47), 1000),((55,48), 1000),((63,49), 1000),((77,49), 1000),((83,48), 1000),
                              ((69,43), 1000),((35,42), 1000),((44,35), 1000),((58,36), 1000),((59,43), 1000),((54,31), 1000),((67,31), 1000),((33,29), 1000),((37,30), 1000),((41,27), 1000),
                              ((28,26), 1000),((45,24), 1000),((66,19), 1000),((18,15), 1000),((25, 7), 1000),((52, 9), 1000)])
    return W


