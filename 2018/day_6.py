# --- Day 6: Chronal Coordinates ---
# The device on your wrist beeps several times, and once again you feel like you're falling.

# "Situation critical," the device announces. "Destination indeterminate. Chronal interference detected. Please specify new target coordinates."

# The device then produces a list of coordinates (your puzzle input). Are they places it thinks are safe or dangerous? It recommends you check manual page 729. The Elves did not give you a manual.

# If they're dangerous, maybe you can minimize the danger by finding the coordinate that gives the largest distance from the other points.

# Using only the Manhattan distance, determine the area around each coordinate by counting the number of integer X,Y locations that are closest to that coordinate (and aren't tied in distance to any other coordinate).

# Your goal is to find the size of the largest area that isn't infinite. For example, consider the following list of coordinates:

# 1, 1
# 1, 6
# 8, 3
# 3, 4
# 5, 5
# 8, 9
# If we name these coordinates A through F, we can draw them on a grid, putting 0,0 at the top left:

# ..........
# .A........
# ..........
# ........C.
# ...D......
# .....E....
# .B........
# ..........
# ..........
# ........F.
# This view is partial - the actual grid extends infinitely in all directions. Using the Manhattan distance, each location's closest coordinate can be determined, shown here in lowercase:

# aaaaa.cccc
# aAaaa.cccc
# aaaddecccc
# aadddeccCc
# ..dDdeeccc
# bb.deEeecc
# bBb.eeee..
# bbb.eeefff
# bbb.eeffff
# bbb.ffffFf
# Locations shown as . are equally far from two or more coordinates, and so they don't count as being closest to any.

# In this example, the areas of coordinates A, B, C, and F are infinite - while not shown here, their areas extend forever outside the visible grid. However, the areas of coordinates D and E are finite: D is closest to 9 locations, and E is closest to 17 (both including the coordinate's location itself). Therefore, in this example, the size of the largest area is 17.

# What is the size of the largest area that isn't infinite?

# Your puzzle answer was 4215.

# --- Part Two ---
# On the other hand, if the coordinates are safe, maybe the best you can do is try to find a region near as many coordinates as possible.

# For example, suppose you want the sum of the Manhattan distance to all of the coordinates to be less than 32. For each location, add up the distances to all of the given coordinates; if the total of those distances is less than 32, that location is within the desired region. Using the same coordinates as above, the resulting region looks like this:

# ..........
# .A........
# ..........
# ...###..C.
# ..#D###...
# ..###E#...
# .B.###....
# ..........
# ..........
# ........F.
# In particular, consider the highlighted location 4,3 located at the top middle of the region. Its calculation is as follows, where abs() is the absolute value function:

# Distance to coordinate A: abs(4-1) + abs(3-1) =  5
# Distance to coordinate B: abs(4-1) + abs(3-6) =  6
# Distance to coordinate C: abs(4-8) + abs(3-3) =  4
# Distance to coordinate D: abs(4-3) + abs(3-4) =  2
# Distance to coordinate E: abs(4-5) + abs(3-5) =  3
# Distance to coordinate F: abs(4-8) + abs(3-9) = 10
# Total distance: 5 + 6 + 4 + 2 + 3 + 10 = 30
# Because the total distance to all coordinates (30) is less than 32, the location is within the region.

# This region, which also includes coordinates D and E, has a total size of 16.

# Your actual region will need to be much larger than this example, though, instead including all locations with a total distance of less than 10000.

# What is the size of the region containing all locations which have a total distance to all given coordinates of less than 10000?

# Your puzzle answer was 40376.

import itertools

input = [
    (158, 163),
    (287, 68),
    (76, 102),
    (84, 244),
    (162, 55),
    (272, 335),
    (345, 358),
    (210, 211),
    (343, 206),
    (219, 323),
    (260, 238),
    (83, 94),
    (137, 340),
    (244, 172),
    (335, 307),
    (52, 135),
    (312, 109),
    (276, 93),
    (288, 274),
    (173, 211),
    (125, 236),
    (200, 217),
    (339, 56),
    (286, 134),
    (310, 192),
    (169, 192),
    (313, 106),
    (331, 186),
    (40, 236),
    (194, 122),
    (244, 76),
    (159, 282),
    (161, 176),
    (262, 279),
    (184, 93),
    (337, 284),
    (346, 342),
    (283, 90),
    (279, 162),
    (112, 244),
    (49, 254),
    (63, 176),
    (268, 145),
    (334, 336),
    (278, 176),
    (353, 135),
    (282, 312),
    (96, 85),
    (90, 105),
    (354, 312),
]


def distance(point1, point2):
    return abs(point1[0] - point2[0]) + abs(point1[1] - point2[1])


TIE = -1


def size(box):
    return len(box), len(box[0])


def create_box(input):
    row_num, col_num  = max(i[0] for i in input) + 1, max(i[1] for i in input) + 1
    box = [[TIE for col in range(col_num)] for row in range(row_num)]
    return box


def allcoords(box):
    row_num, col_num = size(box)
    return itertools.product(range(row_num), range(col_num))
    
    
def create_voronoi(input):
    voronoi = create_box(input)
    MAX = sum(size(voronoi)) + 1
    for current_point in allcoords(voronoi):
        minsofar = MAX
        for id, pivot in enumerate(input):
            d = distance(current_point, pivot)
            if d == minsofar:
                voronoi[current_point[0]][current_point[1]] = TIE
            if d < minsofar:
                voronoi[current_point[0]][current_point[1]] = id
                minsofar = d
    return voronoi


def get_stats(voronoi, input):
    stats = [0 for _ in input]
    for i, j in allcoords(voronoi):
        id = voronoi[i][j]
        if id == TIE:
            continue
        stats[id] += 1 
    return stats
    

def get_infinite(voronoi):
    infinite_pivots = set()
    row_num, col_num = len(voronoi), len(voronoi[0])
    for col in range(col_num):
        infinite_pivots.add(voronoi[0][col])
        infinite_pivots.add(voronoi[row_num - 1][col])
    for row in range(row_num):
        infinite_pivots.add(voronoi[row][0])
        infinite_pivots.add(voronoi[row][col_num - 1])
    return infinite_pivots


def get_max_finite(stats, infinite_pivots):
    maxsofar = -1
    for id in range(len(stats)):
        if id in infinite_pivots:
            continue
        maxsofar = max(maxsofar, stats[id])
    return maxsofar
        
    
def print_voronoi(voronoi):
    for row in voronoi:
        print(''.join('{:>4}'.format(e) for e in row))
            
            
def part1(input):
    voronoi = create_voronoi(input)
    stats = get_stats(voronoi, input)
    return get_max_finite(stats, get_infinite(voronoi))


SAFE = 0


def mark(box, input, maxdist):
    for i, j in allcoords(box):
        if sum(distance((i, j), p) for p in input) < maxdist:
            box[i][j] = SAFE


def get_area(start_point, box, visited):
    row_num, col_num = size(box)
    area = 0
    stack = [start_point]
    while stack:
        i, j = stack.pop()
        if (i < 0 or j < 0 or i >= row_num or j >= col_num
            or visited[i][j]
            or box[i][j] != SAFE):
                continue
        visited[i][j] = True
        area += 1
        stack.extend(((i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)))
    return area

                            
def part2(input, maxdist):
    box = create_box(input)
    mark(box, input, maxdist)
    row_num, col_num = size(box)
    visited = [[False for j in range(col_num)] for i in range(row_num)]
    return max(get_area(p, box, visited) for p in allcoords(box))


if __name__ == '__main__':
    print(part1(input) == 4215)
    print(part2(input, 10000) == 40376)
        
