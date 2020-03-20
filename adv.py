from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []
traversal_stack = []
visited = set()

current_room = world.rooms[0]

while len(visited) < len(world.rooms):
    choices = []
    visited.add(current_room.id)
    if current_room.n_to is not None and current_room.n_to.id not in visited:
        choices.append('n')
    if current_room.s_to is not None and current_room.s_to.id not in visited:
        choices.append('s')
    if current_room.e_to is not None and current_room.e_to.id not in visited:
        choices.append('e')
    if current_room.w_to is not None and current_room.w_to.id not in visited:
        choices.append('w')
    elif len(choices) == 0:
        last_move = traversal_stack.pop()
        if last_move == 'n':
            current_room = current_room.s_to
            traversal_path.append('s')
        if last_move == 's':
            current_room = current_room.n_to
            traversal_path.append('n')
        if last_move == 'e':
            current_room = current_room.w_to
            traversal_path.append('w')
        if last_move == 'w':
            current_room = current_room.e_to
            traversal_path.append('e')

    if len(choices) > 0:
        choice = random.choice(choices)
        traversal_path.append(choice)
        traversal_stack.append(choice)
        if choice == 'n':
            current_room = current_room.n_to
        if choice == 's':
            current_room = current_room.s_to
        if choice == 'e':
            current_room = current_room.e_to
        if choice == 'w':
            current_room = current_room.w_to


# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
player.current_room.print_room_description(player)
while True:
    cmds = input("-> ").lower().split(" ")
    if cmds[0] in ["n", "s", "e", "w"]:
        player.travel(cmds[0], True)
    elif cmds[0] == "q":
        break
    else:
        print("I did not understand that command.")
