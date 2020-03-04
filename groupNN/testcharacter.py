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

    def do(self, wrld):
        # Your code here
        pass
