# This is necessary to find the main code
import sys

sys.path.insert(0, '../bomberman')
# Import necessary stuff
from entity import CharacterEntity
from colorama import Fore, Back

# Import our stuff
from heapq import heappush, heappop
from collections import defaultdict


class TestCharacter(CharacterEntity):

    discount = 0.9

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
    def get_safe_moves(self, wrld, surroundings, charloc):
        safe_moves = set()
        unsafe_moves = set()
        for deltaX in [-1, 0, 1]:
            for deltaY in [-1, 0, 1]:
                if charloc.x + deltaX in range(0, wrld.width()) and charloc.y in range(0, wrld.height()):
                    safe_moves.add((deltaX, deltaY))

        # Check for locations with walls, bombs, explosions, character and monsters
        if wrld.bomb_at(charloc.x, charloc.y):
            safe_moves.remove((0, 0))
        # Surroundings order: empty, wall, monster, character, bomb, explosion, exit
        for cell in surroundings[1]:  # Wall
            safe_moves.remove(cell)
        for cell in surroundings[2]:  # Monster
            safe_moves.remove(cell)
        for cell in surroundings[3]:  # Character
            safe_moves.remove(cell)
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
                if charloc.x + deltaX + i in range(0, wrld.width()) and wrld.bomb_at(charloc.x + deltaX + i, charloc.y):
                    unsafe_moves.add((deltaX, deltaY))
                # Check for explosions in the Y axis
                if charloc.y + deltaY + i in range(0, wrld.height()) and wrld.bomb_at(charloc.x, charloc.y + deltaY + i):
                    unsafe_moves.add((deltaX, deltaY))

        # Check the surrounding of monsters, to avoid being locked onto by aggressive monsters
        monster_range = 2
        for (deltaX, deltaY) in safe_moves:
            for i in range(-monster_range, monster_range + 1):
                for j in range(-monster_range, monster_range + 1):
                    check_x = charloc.x + deltaX + i
                    check_y = charloc.y + deltaY + j
                    if 0 < check_x < wrld.width() and check_x != charloc.x and 0 < check_y < wrld.height() and check_y != charloc.y:
                        if wrld.monsters_at(check_x, check_y):
                            unsafe_moves.add((deltaX, deltaY))

        for cell in unsafe_moves:
            safe_moves.remove(cell)

        return safe_moves

    def q_learn(self, world, safe_moves, x, y):
        best_value = -100
        best_move = (0,0)

        for move in safe_moves:
            curr_x = x + move[0] 
            curr_y + move[1]
            world.me(self).move(move[0], move[1])
            new_world, events = world.next()
            new_value = self.get_q(new_world, curr_x, curr_y)

            if new_value > best_value
                best_value = new_value
                best_move = move

        self.last_best_value = best_value
        return best_move


    # ------------------------------------------------------------------------------------------------------------------------/


    def get_q(self, world, x, y):
        f_monster = self.get_monster_feature(world, x, y)
        f_exit = self.get_exit_dist(world, x, y)
        f_cornered = self.get_cornered_dist()

        self.last_monster_feature = f_monster
        self.last_exit_feature = f_exit
        self.last_cornered_feature = f_cornered

        return (self.w_monster * f_monster) + (self.w_exit * f_exit) + (self.w_cornered * f_cornered)


    # ------------------------------------------------------------------------------------------------------------------------/


    def get_monster_feature(self, world, x, y):
        monster_positions = self.get_monster_positions(world)

        if len(monster_postions) == 0:
            return 0

        start = (x,y)
        distances = []

        for monster in monster_positions:
            if start == monster:
                return 1
            else:
                path = self.a_star(world.grid, 0, x, y, monster)
                distances.append(len(path))

        return 1 / (1 + min(distances))

    def get_exit_feature(self, world, x, y):
        exit = self.get_exit(world)
        start = (x,y)

        if start == exit:
            return 1

        path = self.a_star(world.grid, 0, x, y, exit)
        return 1 / (1 + len(path))

    def get_cornered_feature(self, world, x, y):
        immediate_moves = self.get_available_moves(world, x, y)
        safe_moves = get_safe_moves(world, x, y)

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
        w = wrld.width() - 1
        h = wrld.height() - 1

        while h >= 0:
            while w >= 0:
                if world.exit_at(w, h):
                    return (w, h)
                w -= 1
            h -= 1
            w = wrld.width() - 1

        return (0, 0)

    def a_star(self, grid, k, start_x, start_y, goal):
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
                return steps

            if estimation - steps <= k - eliminations:
                return steps
            
            for y, x in neighborhood(curr_y, curr_x):
                next_eliminations = eliminations + grid[y][x]

                if next_eliminations < min_eliminations[(y, x)]:
                    came_from[(y,x)] = (curr_y, curr_x)
                    heappush(fringe_heap, (steps + 1 + manhattan_distance(y, x), steps + 1, next_eliminations, y, x))
                    min_eliminations[(y, x)] = next_eliminations
        
        return 0


    # ------------------------------------------------------------------------------------------------------------------------/


    def get_reward(self, world, x, y):

        if world.monster_at(x,y):
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
        safe_moves = self.safe_moves(wrld, available_moves, me)

        if self.last_best_value != 0:
            reward = self.get_reward(wrld, me.x, me.y)
            actual_value = reward + self.discount * self.get_next_best(wrld, safe_moves, me.x, me.y)
            difference = actual_value - self.last_best_value
            self.set_weights(difference, self.last_monster_feature, self.last_exit_feature, self.last_cornered_feature)
        
        current_value = 0
        new_value = 0
        best_value = 0
        best_Move = (0,0)

    #TODO change get_safe_moves to block exit if a bomb is still waiting to explode

    if len(available_move[6]) > 0:
        if available_move[6][0] in safe_moves:
            self.move(available_moves[6][0][0], available_moves[6][0][1])
        else:
            #TODO Durdle for a while until bomb explodes

    move = self.q_learn(self, world, safe_moves, x, y)
    self.last_x = me.x + move[0]
    self.last_y = me.y + move[1]
    self.move(move[0], move[1])

    f = open("weights.txt", "w")
    for i in range(3):
        if i == 0:
            w_str1 = "%f\n" % self.w1
            f.write(w_str1)
        if i == 1:
            w_str2 = "%f\n" % self.w2
            f.write(w_str2)
        if i == 2:
            w_str3 = "%f\n" % self.w3
            f.write(w_str3)
        i += 1
    f.close()
