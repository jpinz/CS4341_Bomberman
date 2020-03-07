# This is necessary to find the main code
import sys

sys.path.insert(0, '../bomberman')
# Import necessary stuff
from entity import CharacterEntity
from colorama import Fore, Back

# Import our stuff
from heapq import heappush, heappop
from collections import defaultdict
from pprint import pprint


class TestCharacter(CharacterEntity):

    discount = 0.9
    learn_rate= 0.2

    last_best_value = 0
    last_monster_feature = 0
    last_exit_feature = 0
    last_cornered_feature = 0

    last_x = 0
    last_y = 0

    f = open("weights.txt")
    weights = f.read().splitlines()
    w_monster=float(weights[0])
    w_exit=float(weights[1])
    w_cornered=float(weights[2])
    f.close()

    # Gives where the character can physically move
    def get_available_moves(self, wrld, start_x, start_y):
        finds = dict([(i, []) for i in range(7)])

        for deltaX in [-1, 0, 1]:
            x = start_x + deltaX

            # Make sure we don't go out of bounds
            if 0 <= x < wrld.width():
                # Loop through the detla of y
                for deltaY in [-1, 0, 1]:
                    y = start_y + deltaY
                    # Skip the current cell the character is on
                    if deltaX != 0 or deltaY != 0:
                        # Make sure we don't go out of bounds
                        if 0 <= y < wrld.height():
                            # Check all the cases for what could be in a cell
                            if wrld.empty_at(x, y):  # Empty Cell
                                nf = finds[0]
                                nf.append((deltaX, deltaY))
                                finds[0] = nf
                            elif wrld.wall_at(x, y):  # Wall Cell
                                nf = finds[1]
                                nf.append((deltaX, deltaY))
                                finds[1] = nf
                            elif wrld.monsters_at(x, y):  # Monster Cell
                                nf = finds[2]
                                nf.append((deltaX, deltaY))
                                finds[2] = nf
                            elif wrld.characters_at(x, y):  # Character Cell
                                nf = finds[3]
                                nf.append((deltaX, deltaY))
                                finds[3] = nf
                            elif wrld.bomb_at(x, y):  # Bomb Cell
                                nf = finds[4]
                                nf.append((deltaX, deltaY))
                                finds[4] = nf
                            elif wrld.explosion_at(x, y):  # Explosion Cell
                                nf = finds[5]
                                nf.append((deltaX, deltaY))
                                finds[5] = nf
                            elif wrld.exit_at(x, y):  # Exit Cell
                                nf = finds[6]
                                nf.append((deltaX, deltaY))
                                finds[6] = nf

        # Return all the found cells
        return finds

    # Takes find_available_moves and filters out all of the moves that are deemed 'unsafe'
    def get_safe_moves(self, wrld, surroundings, x, y):
        safe_moves = set()
        unsafe_moves = set()
        for deltaX in [-1, 0, 1]:
            for deltaY in [-1, 0, 1]:
                if x + deltaX in range(0, wrld.width()) and y + deltaY in range(0, wrld.height()):
                    safe_moves.add((deltaX, deltaY))

        # print (safe_moves)
        # print (surroundings)
        # Check for locations with walls, bombs, explosions, character and monsters
        if wrld.bomb_at(x, y):
            safe_moves.remove((0, 0))
        # Surroundings order: empty, wall, monster, character, bomb, explosion, exit
        for cell in surroundings[1]:  # Wall
            safe_moves.remove(cell)
        for cell in surroundings[2]:  # Monster
            safe_moves.remove(cell)
        # for cell in surroundings[3]:  # Character
        #     safe_moves.remove(cell)
        for cell in surroundings[4]:  # Bomb
            safe_moves.remove(cell)
        for cell in surroundings[5]:  # Explosion
            safe_moves.remove(cell)

        # Find out how far the bomb explosion distance is
        explosion_range = wrld.expl_range + 1
        for (deltaX, deltaY) in safe_moves:
            # Make sure character is not in the x or y range of the explosion
            for i in range(-explosion_range, explosion_range + 1):
                # Check for explosions in the X axis
                if x + deltaX + i in range(0, wrld.width()) and wrld.bomb_at(x + deltaX + i, y):
                    unsafe_moves.add((deltaX, deltaY))
                # Check for explosions in the Y axis
                if y + deltaY + i in range(0, wrld.height()) and wrld.bomb_at(x, y + deltaY + i):
                    unsafe_moves.add((deltaX, deltaY))

        # Check the surrounding of monsters, to avoid being locked onto by aggressive monsters
        monster_range = 2
        for (deltaX, deltaY) in safe_moves:
            for i in range(-monster_range, monster_range + 1):
                for j in range(-monster_range, monster_range + 1):
                    check_x = x + deltaX + i
                    check_y = y + deltaY + j
                    if 0 < check_x < wrld.width() and check_x != x and 0 < check_y < wrld.height() and check_y != y:
                        if wrld.monsters_at(check_x, check_y):
                            unsafe_moves.add((deltaX, deltaY))

        for cell in unsafe_moves:
            safe_moves.remove(cell)

        if len(safe_moves) > 1 and (0,0) in safe_moves:
            safe_moves.remove((0,0))

        # print (safe_moves)
        return safe_moves

    def q_learn(self, world, safe_moves, x, y):
        best_value = -100
        best_move = (0,0)

        for move in safe_moves:
            curr_x = x + move[0] 
            curr_y = y + move[1]
            new_world = world.from_world(world)
            new_world.me(self).move(move[0], move[1])
            new_world, events = new_world.next()
            new_value = self.get_q(new_world, curr_x, curr_y)

            if new_value > best_value:
                best_value = new_value
                best_move = move

        self.last_best_value = best_value
        return best_move


    # ------------------------------------------------------------------------------------------------------------------------/


    def get_q(self, world, x, y):
        f_monster = self.get_monster_feature(world, x, y)
        f_exit = self.get_exit_feature(world, x, y)
        f_cornered = self.get_cornered_feature(world, x, y)

        self.last_monster_feature = f_monster
        self.last_exit_feature = f_exit
        self.last_cornered_feature = f_cornered

        return (self.w_monster * f_monster) + (self.w_exit * f_exit) + (self.w_cornered * f_cornered)


    # ------------------------------------------------------------------------------------------------------------------------/


    def get_monster_feature(self, world, x, y):
        monster_positions = self.get_monster_positions(world)

        if len(monster_positions) == 0:
            return 0

        start = (x,y)
        distances = []

        for monster in monster_positions:
            if start == monster:
                return 1
            else:
                steps, path = self.a_star(world.grid, 0, x, y, monster)
                distances.append(steps)

        return 1 / (1 + min(distances))

    def get_exit_feature(self, world, x, y):
        exit = self.get_exit(world)
        start = (x,y)

        if start == exit:
            return 1

        steps, path = self.a_star(world.grid, 0, x, y, exit)
        return 1 / (1 + steps)

    def get_cornered_feature(self, world, x, y):
        available_moves = self.get_available_moves(world, x, y)
        print('c')
        safe_moves = self.get_safe_moves(world, available_moves, x, y)

        if len(safe_moves) < 3:
            return 1
        else:
            return 0


    # ------------------------------------------------------------------------------------------------------------------------/


    def get_monster_positions(self, world):
        monster_postions = []

        for i in range(world.width()):
            for j in range(world.height()):
                if world.monsters_at(i, j):
                    monster_postions.append( (i,j) )

        return monster_postions

    def get_exit(self, world):
        w = world.width() - 1
        h = world.height() - 1

        while h >= 0:
            while w >= 0:
                if world.exit_at(w, h):
                    return (w, h)
                w -= 1
            h -= 1
            w = world.width() - 1

        return (0, 0)

    def a_star(self, grid, k, start_y, start_x, goal):
        m, n = len(grid), len(grid[0])

        if m + n - 2 <= k:
            return 0

        came_from = {}

        manhattan_distance = lambda y, x: m + n - y - x - 2
        neighborhood = lambda y, x: [
            (y, x) for y, x in [(y - 1, x), (y, x + 1), (y + 1, x), (y, x - 1)]
            if 0 <= y < m and 0 <= x < n
        ]

        fringe_heap = [(manhattan_distance(start_y, start_x), 0, 0, start_y, start_x)]
        min_eliminations = defaultdict(lambda: k + 1, {(0, 0): 0})

        while fringe_heap:
            estimation, steps, eliminations, curr_y, curr_x = heappop(fringe_heap)

            if (curr_y, curr_x) == goal:
                return (steps, self.construct_path(came_from, (curr_y, curr_x), start_x, start_y))

            if estimation - steps <= k - eliminations:
                return (steps, self.construct_path(came_from, (curr_y, curr_x), start_x, start_y))
            
            for y, x in neighborhood(curr_y, curr_x):
                next_eliminations = eliminations + grid[y][x]

                if next_eliminations < min_eliminations[(y, x)]:
                    came_from[(y,x)] = (curr_y, curr_x)
                    heappush(fringe_heap, (steps + 1 + manhattan_distance(y, x), steps + 1, next_eliminations, y, x))
                    min_eliminations[(y, x)] = next_eliminations
        
        return 0


    # ------------------------------------------------------------------------------------------------------------------------/


    def construct_path(self, came_from, curr_corr, start_x, start_y):
        total_path = [curr_corr]

        while curr_corr in came_from:
            curr_corr = came_from[curr_corr]
            if curr_corr == (start_y, start_x):
                break
            else:
                total_path.append(curr_corr)

        return total_path


    # ------------------------------------------------------------------------------------------------------------------------/


    def get_reward(self, world, x, y):

        if world.monsters_at(x,y):
            return -30
        elif world.exit_at(x,y):
            return 75
        elif world.explosion_at(x,y):
            return -25
        elif world.bomb_at(x,y):
            return -25
        else:
            return 1

    def get_next_best(self, world, safe_moves, x, y):
        best_value = 0

        for vector in safe_moves:
            new_value = self.get_q(world, x+vector[0], y+vector[1])
            if new_value > best_value:
                best_value = new_value

        return best_value

    def set_weights(self, difference, f_monster, f_exit, f_cornered):
        self.w_monster = self.w_monster + self.learn_rate * difference * f_monster
        self.w_exit = self.w_exit + self.learn_rate * difference * f_exit
        self.w_cornered = self.w_cornered + self.learn_rate * difference * f_cornered


    # ------------------------------------------------------------------------------------------------------------------------/


    def do(self, wrld):
        me = wrld.me(self)
        available_moves = self.get_available_moves(wrld, me.x, me.y)
        safe_moves = self.get_safe_moves(wrld, available_moves, me.x, me.y)

        if not safe_moves:
            safe_moves = [(x,y) for x in [-1,0,1] for y in [-1,0,1]]
            print ('\nHERE\n')
            print (safe_moves)

        if self.last_best_value != 0:
            reward = self.get_reward(wrld, me.x, me.y)
            actual_value = reward + self.discount * self.get_next_best(wrld, safe_moves, me.x, me.y)
            difference = actual_value - self.last_best_value
            self.set_weights(difference, self.last_monster_feature, self.last_exit_feature, self.last_cornered_feature)
        
        # current_value = 0
        # new_value = 0
        # best_value = 0
        # best_Move = (0,0)

        #TODO change get_safe_moves to block exit if a bomb is still waiting to explode

        if len(available_moves[6]) > 0:
            if available_moves[6][0] in safe_moves:
                self.move(available_moves[6][0][0], available_moves[6][0][1])
            # else:
                #TODO Durdle for a while until bomb explodes

        exit = self.get_exit(wrld)
        steps, path = self.a_star(wrld.grid, 0, me.x, me.y, exit)
        # print (path)
        next_shortest_move = path.pop()
        dx = next_shortest_move[0] - me.x
        dy = next_shortest_move[1] - me.y
        print(next_shortest_move)
        print (me.x , me.y)
        print (dx,dy)
        print (safe_moves)

        for cell in path:
            self.set_cell_color(cell[0], cell[1], Fore.RED + Back.GREEN)

        # if (dx, dy) not in safe_moves:
        #     print ('passive')
        #     self.last_x = next_shortest_move[0]
        #     self.last_y = next_shortest_move[1]
        #     self.move(dx, dy)
        # else:
        print('trouble')
        move = self.q_learn(wrld, safe_moves, me.x, me.y)
        self.last_x = me.x + move[0]
        self.last_y = me.y + move[1]
        self.move(move[0], move[1])

        f = open("weights.txt", "w")
        for i in range(3):
            if i == 0:
                w_str1 = "%f\n" % self.w_monster
                f.write(w_str1)
            if i == 1:
                w_str2 = "%f\n" % self.w_exit
                f.write(w_str2)
            if i == 2:
                w_str3 = "%f\n" % self.w_cornered
                f.write(w_str3)
            i += 1
        f.close()

        # for cell in path:
        #     self.set_cell_color(cell[0], cell[1], Fore.BLACK + Back.BLACK)
