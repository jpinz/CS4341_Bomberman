# This is necessary to find the main code
import sys

sys.path.insert(0, '../bomberman')
# Import necessary stuff
from entity import CharacterEntity
from colorama import Fore, Back


class TestCharacter(CharacterEntity):

    # Gives where the character can physically move
    def find_available_moves(self, wrld, start_x, start_y):
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
    def find_safe_moves(self, wrld, surroundings, charloc):
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
                if charloc.y + deltaY + i in range(0, wrld.height()) and wrld.bomb_at(charloc.x,
                                                                                      charloc.y + deltaY + i):
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
            new_value = self.cal_q(new_world, curr_x, curr_y)

            if new_value > best_value
                best_value = new_value
                best_move = move

        self.last_best_value = best_value
        return best_move


    # ------------------------------------------------------------------------------------------------------------------------/


    def cal_q(self, world, x, y):
        f_monster = self.monster_dist(world, x, y)
        f_exit = self.exit_dist(world, x, y)
        f_cornered = self.cornered_dist()

        self.last_monster_dist = f_monster
        self.last_exit_dist = f_exit
        self.last_cornered_dist = f_cornered

        return (self.w_monster * f_monster) + (self.w_exit * f_exit) + (self.w_cornered * f_cornered)


    # ------------------------------------------------------------------------------------------------------------------------/


    def monster_dist(self, world, x, y):
        current = (-1, -1)
        monster_positions = self.get_monster_positions(world)

        if len(monsters) == 0:
            return 0

        start = (x,y)
        distances = []
        for monster in monster_positions:
            current = monster

            if x < 0 or y < 0:
                return 0
            if start == current:
                return 1
            else:
                path = self.a_star(world, start, current)
                distances.append(len(path))
        return 1 / (1 + min(distances))

    def exit_distance(self, world, x, y):
        exit = self.find_exit(world)
        start = (x,y)

        if start == exit:
            return 1
        path = self.a_star(world, start, exit)
        return 1 / (1 + len(path))

    def cornered_dist(self, world, x, y):
        immediate_moves = self.get_immediate_moves(world, x, y)
        safe_moves = determine_safe_moves(world, x, y)
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

    # TODO 
    def a_star();
        pass


    # ------------------------------------------------------------------------------------------------------------------------/


    # TODO
    def do(self, wrld):
        # Your code here
        pass