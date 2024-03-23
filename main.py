import matplotlib.pyplot as plt
import networkx as nx
import world

display=True

if display:
    # set up plt
    plt.ion()
    plt.show(block=False)

# demoing the display
W = world.World()
W.simulate(display=display)

if display:
    plt.ioff()
