# lidar vals based matrix (90x90 grid)
# path matrix (start and end points with lines from both that meet)
# keep checking from the centre of the body to the destination
# if conflict -> pivot line from dest point and body centre until both lines have no conflict in betwwen 
# from that intersection point confirm surrounding conflicts for dimensions of bot
# if conflict -> move intersection point by number of conflict blocks
# ↓
# add to check conflicts

'''
RPLIDAR A1-M8 SPECS
Range: 6m radius

CALC
0.15m squares => 12m -> 80
80X80 grid
gt                                                                                                           -
Bot is always the centre of the matrix
'''

# down facing ultrasonic for fall prevention
