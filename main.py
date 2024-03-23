import matplotlib.pyplot as plt
import networkx as nx
import world

# set up plt
plt.ion()
plt.show(block=False)

# demoing the display
W = world.World()
W.display()
q = 0
while (q < 10000000):
    q += 1
W.mold.add_node((75,50), 100) # after a few seconds, a second node is added
W.mold.add_edge((50,50), (75,50), 20)
W.display()
q = 0
while (q < 100000000):
    q += 1
plt.ioff()
