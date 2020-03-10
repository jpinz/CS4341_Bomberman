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
import math
import random


class TestCharacter(CharacterEntity):

    # predicted_move_1 = (0,0)
    # predicted_move_2 = (0,0)
    b_timer = 0

    # am_safe = False

    # discount = 0.9
    # learn_rate = 0.2
    # start_best_dist = 0

    # last_best_value = 0
    # last_monster_feature = 0
    # last_exit_feature = 0
    # last_cornered_feature = 0

    # last_x = 0
    # last_y = 0
    # steps_left = 100

    # f = open("weights.txt")
    # weights = f.read().splitlines()
    # w_monster=float(weights[0])
    # w_exit=float(weights[1])
    # w_cornered=float(weights[2])
    # f.close()

    # # Gives where the character can physically move
    # def get_available_moves(self, wrld, start_x, start_y):
    #     finds = dict([(i, []) for i in range(7)])

    #     for deltaX in [-1, 0, 1]:
    #         x = start_x + deltaX

    #         # Make sure we don't go out of bounds
    #         if 0 <= x < wrld.width():
    #             # Loop through the detla of y
    #             for deltaY in [-1, 0, 1]:
    #                 y = start_y + deltaY
    #                 # Skip the current cell the character is on
    #                 if deltaX != 0 or deltaY != 0:
    #                     # Make sure we don't go out of bounds
    #                     if 0 <= y < wrld.height():
    #                         # Check all the cases for what could be in a cell
    #                         if wrld.empty_at(x, y):  # Empty Cell
    #                             nf = finds[0]
    #                             nf.append((deltaX, deltaY))
    #                             finds[0] = nf
    #                         elif wrld.wall_at(x, y):  # Wall Cell
    #                             nf = finds[1]
    #                             nf.append((deltaX, deltaY))
    #                             finds[1] = nf
    #                         elif wrld.monsters_at(x, y):  # Monster Cell
    #                             nf = finds[2]
    #                             nf.append((deltaX, deltaY))
    #                             finds[2] = nf
    #                         elif wrld.characters_at(x, y):  # Character Cell
    #                             nf = finds[3]
    #                             nf.append((deltaX, deltaY))
    #                             finds[3] = nf
    #                         elif wrld.bomb_at(x, y):  # Bomb Cell
    #                             nf = finds[4]
    #                             nf.append((deltaX, deltaY))
    #                             finds[4] = nf
    #                         elif wrld.explosion_at(x, y):  # Explosion Cell
    #                             nf = finds[5]
    #                             nf.append((deltaX, deltaY))
    #                             finds[5] = nf
    #                         elif wrld.exit_at(x, y):  # Exit Cell
    #                             nf = finds[6]
    #                             nf.append((deltaX, deltaY))
    #                             finds[6] = nf

    #     # Return all the found cells
    #     return finds

    # # Takes find_available_moves and filters out all of the moves that are deemed 'unsafe'
    # def get_safe_moves(self, wrld, surroundings, x, y):
    #     safe_moves = set()
    #     unsafe_moves = set()
    #     for deltaX in [-1, 0, 1]:
    #         for deltaY in [-1, 0, 1]:
    #             if x + deltaX in range(0, wrld.width()) and y + deltaY in range(0, wrld.height()):
    #                 safe_moves.add((deltaX, deltaY))

    #     # print (safe_moves)
    #     # print (surroundings)
    #     # Check for locations with walls, bombs, explosions, character and monsters
    #     if wrld.bomb_at(x, y):
    #         safe_moves.remove((0, 0))
    #     # Surroundings order: empty, wall, monster, character, bomb, explosion, exit
    #     for cell in surroundings[1]:  # Wall
    #         safe_moves.remove(cell)
    #     for cell in surroundings[2]:  # Monster
    #         safe_moves.remove(cell)
    #     # for cell in surroundings[3]:  # Character
    #     #     safe_moves.remove(cell)
    #     for cell in surroundings[4]:  # Bomb
    #         safe_moves.remove(cell)
    #     for cell in surroundings[5]:  # Explosion
    #         safe_moves.remove(cell)

    #     # Find out how far the bomb explosion distance is
    #     explosion_range = wrld.expl_range + 1
    #     for (deltaX, deltaY) in safe_moves:
    #         # Make sure character is not in the x or y range of the explosion
    #         for i in range(-explosion_range, explosion_range + 1):
    #             # Check for explosions in the X axis
    #             if x + deltaX + i in range(0, wrld.width()) and wrld.bomb_at(x + deltaX + i, y):
    #                 unsafe_moves.add((deltaX, deltaY))
    #             # Check for explosions in the Y axis
    #             if y + deltaY + i in range(0, wrld.height()) and wrld.bomb_at(x, y + deltaY + i):
    #                 unsafe_moves.add((deltaX, deltaY))

    #     # Check the surrounding of monsters, to avoid being locked onto by aggressive monsters
    #     # monster_range = 3
    #     # for (deltaX, deltaY) in safe_moves:
    #     #     for i in range(-monster_range, monster_range + 1):
    #     #         for j in range(-monster_range, monster_range + 1):
    #     #             check_x = x + deltaX + i
    #     #             check_y = y + deltaY + j
    #     #             if 0 < check_x < wrld.width() and check_x != x and 0 < check_y < wrld.height() and check_y != y:
    #     #                 if wrld.monsters_at(check_x, check_y):
    #     #                     unsafe_moves.add((deltaX, deltaY))

    #     for (x,y) in safe_moves:
    #         for (dx,dy) in [(i,j) for i in [-4,-3,-2,-1,0,1,2,3,4] for j in [-4,-3,-2,-1,0,1,2,3,4]]:
    #             check_x = x + dx
    #             check_y = y + dy
    #             if 0 <= check_x < wrld.width() and 0 <= check_y < wrld.height():
    #                 if wrld.monsters_at(check_x, check_y):
    #                         unsafe_moves.add((deltaX, deltaY))


    #     # [(i,j) for i in range[-2,-1,0,1,2] for j in range[-2,-1,0,1,2]]

    #     for cell in unsafe_moves:
    #         safe_moves.remove(cell)

    #     # if len(safe_moves) > 1 and (0,0) in safe_moves:
    #     #     safe_moves.remove((0,0))

    #     # print (safe_moves)
    #     return safe_moves

    # def q_learn(self, world, safe_moves, x, y):
    #     best_value = -1000000
    #     best_move = (0,0)

    #     for move in safe_moves:
    #         curr_x = x + move[0] 
    #         curr_y = y + move[1]
    #         new_world = world.from_world(world)
    #         new_world.me(self).move(move[0], move[1])
    #         new_world, events = new_world.next()
    #         new_value = self.get_q(new_world, curr_x, curr_y)

    #         if new_value > best_value:
    #             best_value = new_value
    #             best_move = move

    #     self.last_best_value = best_value
    #     return best_move


    # # ------------------------------------------------------------------------------------------------------------------------/


    # def get_q(self, world, x, y):
    #     f_monster = self.get_monster_feature(world, x, y)
    #     f_exit = self.get_exit_feature(world, x, y)
    #     #f_cornered = self.get_cornered_feature(world, x, y)

    #     self.last_monster_feature = f_monster
    #     self.last_exit_feature = f_exit
    #     #self.last_cornered_feature = f_cornered

    #     return (self.w_monster * f_monster) - (self.w_exit * f_exit) # + (self.w_cornered * f_cornered)


    # # ------------------------------------------------------------------------------------------------------------------------/


    # def get_monster_feature(self, world, x, y):
    #     monster_positions = self.get_monster_positions(world)

    #     if len(monster_positions) == 0:
    #         return 0

    #     start = (x,y)
    #     distances = []

    #     for monster in monster_positions:
    #         if start == monster:
    #             return 1
    #         else:
    #             steps, path = self.a_star(world.grid, 0, x, y, monster)
    #             distances.append(steps)

    #     return 1 / (1 + min(distances))

    # def get_exit_feature(self, world, x, y):
    #     exit = self.get_exit(world)
    #     start = (x,y)

    #     if start == exit:
    #         return 1

    #     steps, path = self.a_star(world.grid, 0, x, y, exit)
    #     return 1 / (1 + steps)

    # def get_cornered_feature(self, world, x, y):
    #     available_moves = self.get_available_moves(world, x, y)
    #     # print('c')
    #     safe_moves = self.get_safe_moves(world, available_moves, x, y)

    #     if len(safe_moves) < 2:
    #         return 1
    #     else:
    #         return 0


    # # ------------------------------------------------------------------------------------------------------------------------/


    # def get_monster_positions(self, world):
    #     monster_postions = []

    #     for i in range(world.width()):
    #         for j in range(world.height()):
    #             if world.monsters_at(i, j):
    #                 monster_postions.append( (i,j) )

    #     return monster_postions

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
        lowest_y = 0
        m, n = len(grid), len(grid[0])

        if m + n - 2 <= k:
            return m + n - 2

        came_from = {}

        manhattan_distance = lambda y, x: m + n - y - x - 2
        neighborhood = lambda y, x: [
            (y, x) for y, x in [(y - 1, x), (y, x + 1), (y + 1, x), (y, x - 1), (y - 1, x - 1), (y + 1, x + 1), (y - 1, x + 1), (y + 1, x - 1)]
            if 0 <= y < m and 0 <= x < n
        ]
        
        # neighborhood = lambda y, x: [
        #     (y, x) for y, x in [(y - 1, x), (y, x + 1), (y + 1, x), (y, x - 1)]
        #     if 0 <= y < m and 0 <= x < n
        # ]

        fringe_heap = [(manhattan_distance(start_y, start_x), 0, 0, start_y, start_x)]
        min_eliminations = defaultdict(lambda: k + 1, {(0,0) : 0})

        while fringe_heap:
            estimation, steps, eliminations, curr_y, curr_x = heappop(fringe_heap)

            if (curr_y, curr_x) == goal:
                return (steps, self.construct_path(came_from, (curr_y, curr_x), start_x, start_y))

            if estimation - steps <= k - eliminations:
                return (steps, self.construct_path(came_from, (curr_y, curr_x), start_x, start_y))

            for y, x in neighborhood(curr_y, curr_x):
                # self.set_cell_color(y, x, Fore.GREEN + Back.RED)
                if lowest_y < x:
                    lowest_y = x

                next_eliminations = eliminations + grid[y][x]

                if next_eliminations < min_eliminations[(y, x)]:
                    came_from[(y,x)] = (curr_y, curr_x)
                    heappush(fringe_heap, (steps + 1 + manhattan_distance(y, x), steps + 1, next_eliminations, y, x))
                    min_eliminations[(y, x)] = next_eliminations
        
        return False, []

    def bfs(self, grid, k, xi, yi, goal):
        M, N, P, Q, D, L = len(grid)-1, len(grid[0])-1, [(xi,yi,0)], [], {}, 0
        neighborhood = lambda y, x: [
            (y, x) for y, x in [(y - 1, x), (y, x + 1), (y + 1, x), (y, x - 1), (y - 1, x - 1), (y + 1, x + 1), (y - 1, x + 1), (y + 1, x - 1)]
            if 0 <= y < M and 0 <= x < N
        ]
        if k >= M+N: return M+N
        while P:
            for (x,y,s) in P:
                if (x,y) == goal: return L
                for i,j in neighborhood(x,y):
                    if 0<=i<=M and 0<=j<=N:
                        t = s + grid[i][j]
                        if t <= k and D.get((i,j),math.inf) > t: D[(i,j)], _ = t, Q.append((i,j,t))
            P, Q, L = Q, [], L + 1
        return False


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


    # def get_monster_reward(self, world, x, y):
    #     reward = 0
    #     monsters_found = False
    #     for i in [-4,-3,-2,-1,0,1,2,3,4]:
    #         for j in [-4,-3,-2,-1,0,1,2,3,4]:
    #             new_x = x + i
    #             new_y = y + j
    #             if 0 <= new_x < world.width() and 0 <= new_y < world.height():
    #                 # print (world.monsters_at(new_x, new_y))
    #                 monsters = world.monsters_at(new_x, new_y)
    #                 if monsters:
    #                     monsters_found = True
    #                     for m in monsters:
    #                         # print (type(m))
    #                         # pprint (vars(m))
                            

    #                         safe_distance = 0
    #                         if m.name == 'aggressive':
    #                             safe_distance = 3
    #                         else:
    #                             safe_distance = 2
    #                         m_dx = m.dx
    #                         m_dy = m.dy

    #                         if not self.will_monster_change_direction(world, new_x, new_y, m_dx, m_dy) and m.name != 'stupid':
    #                             m_next_move = (new_x + m_dx, new_y + m_dy)
    #                             steps, path = self.a_star(world.grid, 0, x, y, m_next_move)
    #                             if steps == safe_distance:
    #                                 reward -= 500
    #                             elif steps < safe_distance:
    #                                 reward -= (1000 * (safe_distance - steps)) 
    #                             else:
    #                                 reward += (250 * (steps - safe_distance))
    #                         elif m.name != 'stupid':
    #                             m_poss_moves = []
    #                             for m in [-1,0,1]:
    #                                 for n in [-1,0,1]:
    #                                     nx = new_x + m
    #                                     ny = new_y + n
    #                                     if 0 <= nx < world.width() and 0 <= ny + y < world.height():
    #                                         if(world.exit_at(nx,ny) or world.empty_at(nx,ny)):
    #                                             m_poss_moves.append((nx,ny))

    #                             for move in m_poss_moves:
    #                                 steps, path = self.a_star(world.grid, 0, x, y, move)
    #                                 if steps == safe_distance:
    #                                     reward -= 250
    #                                 elif steps < safe_distance:
    #                                     reward -= (1000 * (safe_distance - steps)) 
    #                                 else:
    #                                     reward += (75 * (steps - safe_distance))
    #                         else:
    #                             m_poss_moves = []
    #                             for m in [-1,0,1]:
    #                                 for n in [-1,0,1]:
    #                                     nx = new_x + m
    #                                     ny = new_y + n
    #                                     if 0 <= nx < world.width() and 0 <= ny + y < world.height():
    #                                         if not world.wall_at(nx,ny):
    #                                             m_poss_moves.append((nx,ny))

    #                             for move in m_poss_moves:
    #                                 steps, path = self.a_star(world.grid, 0, x, y, move)
    #                                 if steps == safe_distance:
    #                                     reward -= 250
    #                                 elif steps < safe_distance:
    #                                     reward -= (1000 * (safe_distance - steps)) 
    #                                 else:
    #                                     reward += (75 * (steps - safe_distance))

    #     if not monsters_found:
    #         reward += 500
    #     return reward



    def will_monster_change_direction(self, world, x, y, dx, dy):
        nx = x + dx
        ny = y + dy

        if ((nx < 0) or (nx >= world.width()) or (ny < 0) or (ny >= world.height())):
            return True

        return (world.explosion_at(nx,ny) or world.wall_at(nx, ny) or world.monsters_at(nx, ny) or world.exit_at(nx, ny))

    # ------------------------------------------------------------------------------------------------------------------------/


    # def get_exit_reward(self, world, x, y):
    #     reward = 0
    #     exit = self.get_exit(world)
    #     steps, path = self.a_star(world.grid, 0, x, y, exit)
    #     progress = self.start_best_dist - steps
    #     reward += (progress * 35)

    #     return reward

    # def get_time_reward(self):
    #     reward = 0
    #     reward += (self.steps_left * 2)
    #     return reward


    # # ------------------------------------------------------------------------------------------------------------------------/


    # def get_reward(self, world, x, y):
    #     reward = 0
    #     reward += self.get_time_reward()
    #     reward += self.get_monster_reward(world, x, y)
    #     reward += self.get_exit_reward(world, x, y)
    #     return reward
    #     # if world.monsters_at(x,y):
    #     #     return -50
    #     # elif world.exit_at(x,y):
    #     #     return 100
    #     # elif world.explosion_at(x,y):
    #     #     return -25
    #     # elif world.bomb_at(x,y):
    #     #     return -25
    #     # else:
    #     #     return 1

    # def get_next_best(self, world, safe_moves, x, y):
    #     best_value = 0

    #     for vector in safe_moves:
    #         new_value = self.get_q(world, x+vector[0], y+vector[1])
    #         if new_value > best_value:
    #             best_value = new_value

    #     return best_value

    # def set_weights(self, difference, f_monster, f_exit, f_cornered):
    #     self.w_monster = self.w_monster + self.learn_rate * difference * f_monster
    #     self.w_exit = self.w_exit + self.learn_rate * difference * f_exit
    #     self.w_cornered = self.w_cornered + self.learn_rate * difference * f_cornered
    #     # print (self.w_monster, self.w_exit, self.w_cornered)


    # # ------------------------------------------------------------------------------------------------------------------------/


    # def is_passive(self, world, x, y, c_dx, c_dy, blast_zone):
    #     # Local function for possible next monster move
    #     m_next_moves = lambda x, y: [(x, y) for x, y in [(x,y), (x-1,y-1), (x+1,y+1), (x+1,y), (x+1,y-1), (x-1,y), (x-1,y+1), (x,y+1), (x,y-1)] if 0 <= x < world.width() and 0 <= y < world.height()]

    #     # Return bool for is move passive
    #     passive = True
        
    #     # for an area around our char
    #     for i in range(-6,7):
    #         for j in range(-6,7):
    #             new_x = x + i
    #             new_y = y + j

    #             # Bounds
    #             if 0 <= new_x < world.width() and 0 <= new_y < world.height():
                    
    #                 monsters = world.monsters_at(new_x, new_y)

    #                 # If monsters at spot
    #                 if monsters:

    #                     # For each monster at spot
    #                     for m in monsters:

    #                         # Set the safe distance from monster
    #                         safe_distance = 0
    #                         if m.name == 'aggressive':
    #                             safe_distance = 4
    #                         else:
    #                             safe_distance = 3

    #                         # Get monsters direction
    #                         m_dx = m.dx
    #                         m_dy = m.dy

    #                         change = self.will_monster_change_direction(world, new_x, new_y, m_dx, m_dy)

    #                         # If the monster have a garenteed behavior
    #                         if change == False and m.name != 'stupid':
    #                             print("FORCED MOVE TRY AND TAKE ADVANTAGE")
                                
    #                             # If char is garenteed safe on the next shorest step then set passive to true
    #                             m_next_move = (new_x + m_dx, new_y + m_dy)
    #                             # print(m_next_move)
    #                             nc_x = x + c_dx
    #                             nc_y = y + c_dy
    #                             # to_mon, _ = self.a_star(world.grid, 0, nc_x, nc_y, m_next_move)
    #                             # to_char, _ = self.a_star(world.grid, 0, m_next_move[0], m_next_move[1], (nc_x, nc_y))

    #                             # if to_char <= to_mon:
    #                             #     dist = to_char
    #                             # else:
    #                             #     dist = to_mon

    #                             dist = self.bfs(world.grid, 0, nc_x, nc_y, m_next_move)

    #                             # print (to_mon, to_char)
    #                             # print (dist)
    #                             if dist > safe_distance-1 and self.m_wont_win(nc_x, nc_y, m_next_move[0], m_next_move[1], safe_distance-2):
    #                                     # for cell in path_to_mon:
    #                                     #     self.set_cell_color(cell[0], cell[1], Fore.BLACK + Back.BLUE)
    #                                     # print ('Round_about')
    #                                     if (nc_x, nc_y) not in blast_zone:
    #                                         continue
    #                             else:
    #                                 print('CONTROL FORCED')
    #                                 passive = False
    #                                 goal = self.get_exit(world)
    #                                 s_mons = self.predict(world, x, y, c_dx, c_dy)
    #                                 unsafe_moves = self.preserve(world, s_mons)
    #                                 for cell in blast_zone:
    #                                     if cell not in unsafe_moves:
    #                                         unsafe_moves.append(cell)
    #                                 move = self.choose_move(world, x, y, unsafe_moves, s_mons, goal)
    #                                 return passive, move, s_mons
    #                         else:
    #                             print ('RANDOM MOVE STAY SAFE')
    #                             # If char is garenteed safe on the next shorest step then set passive to true
    #                             m_next_move = (new_x + m_dx, new_y + m_dy)
    #                             nc_x = x + c_dx
    #                             nc_y = y + c_dy
    #                             # to_mon, _ = self.a_star(world.grid, 0, nc_x, nc_y, m_next_move)
    #                             # to_char, _ = self.a_star(world.grid, 0, m_next_move[0], m_next_move[1], (nc_x, nc_y))

    #                             # if to_char <= to_mon:
    #                             #     dist = to_char
    #                             # else:
    #                             #     dist = to_mon

    #                             dist = self.bfs(world.grid, 0, nc_x, nc_y, m_next_move)
    #                             # print(dist)
    #                             # print (to_mon, to_char)
    #                             if dist > safe_distance and self.m_wont_win(nc_x, nc_y, m_next_move[0], m_next_move[1], safe_distance-1):
    #                                     # for cell in path_to_mon:
    #                                     #     self.set_cell_color(cell[0], cell[1], Fore.BLACK + Back.BLUE)
    #                                     # print ('Round_about')
    #                                     if (nc_x, nc_y) not in blast_zone:
    #                                         continue
    #                             else:
    #                                 print('CONTROL FORCED')
    #                                 passive = False
    #                                 goal = self.get_exit(world)
    #                                 s_mons = self.predict(world, x, y, c_dx, c_dy)
    #                                 unsafe_moves = self.preserve(world, s_mons)
    #                                 for cell in blast_zone:
    #                                     if cell not in unsafe_moves:
    #                                         unsafe_moves.append(cell)
    #                                 move = self.choose_move(world, x, y, unsafe_moves, s_mons, goal)
    #                                 return passive, move, s_mons
    #     return True, (), []






                                # elif (to_char <= safe_distance-1 or to_mon <= safe_distance-1):

                                #     e_dist = lambda x1, y1, x2, y2: math.sqrt((x1-x2)**2 + (y1-y2)**2)
                                    
                                #     print ('TOO CLOSE')
                                #     print (m_next_move)
                                #     bm = (x,y)
                                #     ms = 0
                                #     s_world = world.from_world(world)
                                #     for i in [-1,0,1]: 
                                #         for j in [-1,0,1]:
                                #             if 0 <= x + i < world.width() and 0 <= y + j < world.height():
                                #                 if not (world.monsters_at(x+i, y+j) or
                                #                     world.explosion_at(x+i, y+j) or
                                #                     world.wall_at(x+i, y+j)):

                                #                     nx, ny = (x+i, y+j)
                                #                     mx, my = m_next_move
                                #                     dist = e_dist(nx,ny,mx,my)
                                #                     print (dist)
                                #                     if dist > ms: 
                                #                         bm = (nx,ny)
                                #                         ms = dist
                                    
                                #     return False, bm
                                            


                                    # for 
                                    # if 0 <= x-m_dx < world.width() and 0 <= y-m_dy < world.height():
                                    #     return (passive, (x-m_dx, y-m_dy))
                                    # elif 0 <= x < world.width() and 0 <= y-m_dy < world.height():
                                    #     return (passive, (x, y-m_dy))
                                    # elif 0 <= x-m_dx < world.width() and 0 <= y < world.height():
                                    #     return (passive, (x-m_dx, y))

                                # else:
                                #     print ('here')
                                #     bm = (0,0)
                                #     ms = 1000
                                #     goal = self.get_exit(world)
                                #     for i in [-1,0,1]:
                                #         for j in [-1,0,1]:
                                #             if 0 <= x + i < world.width() and 0 <= y + j < world.height():
                                #                 if self.m_wont_win(x+i, y+j, m_next_move[0], m_next_move[1], safe_distance - 1):
                                #                     print ('Sprinting')
                                #                     s, p = self.a_star(world.grid, 0, x+i, y+j, goal)
                                #                     if s < ms:
                                #                         if p:
                                #                             bm = p.pop()
                                #     return (passive, bm)


                                # if steps >= safe_distance - 1:

                                #     # Move is safe Keep going
                                #     continue

                                # Else route is not passive but monster did not change direction
                                # else:
                            #     passive = False

                            #     # Again determine if monster will change dx dy
                            #     change = self.will_monster_change_direction(world, m_next_move[0], m_next_move[1], m_dx, m_dy)

                            #     # If monster will not change directions
                            #     if not change:
                            #         m_next_x = m_next_move[0] + m_dx
                            #         m_next_y = m_next_move[1] + m_dy

                            #         # Make all possible monster moves to avoid for new route calc 
                            #         for cell in self.get_unsafe_zone(world, safe_distance-1, m_next_x, m_next_y):

                            #             # Legal moves for deterministic monsters
                            #             if not world.wall_at(cell[0],cell[1]):

                            #                 # Dont add the same cell to avoid twice
                            #                 if cell not in avoid:
                            #                     avoid.append(cell)

                            #     # Else monster will change direction
                            #     else:
                            #         for move in m_next_moves(m_next_move[0], m_next_move[1]):
                            #             m_next_x = move[0]
                            #             m_next_y = move[1]

                            #             # Legal moves for deterministic monsters
                            #             if not (world.explosion_at(m_next_x, m_next_y) or world.wall_at(m_next_x, m_next_y)):

                            #                 for cell in self.get_unsafe_zone(world, safe_distance-1, m_next_x, m_next_y):

                            #                     # Legal moves for deterministic monsters
                            #                     if not world.wall_at(cell[0],cell[1]):

                            #                         if cell not in avoid:
                            #                             avoid.append(cell)

                            # # Else if monster is not comletely random and but will change direction intially
                            # elif change and m.name != 'stupid':
                            #     passive = False

                            #     # Make all possible monster moves to avoid for new route calc 
                            #     for move in m_next_moves(new_x, new_y):
                            #         m_next_x = move[0]
                            #         m_next_y = move[1]

                            #         # Legal moves for deterministic monsters
                            #         if not (world.explosion_at(m_next_x, m_next_y) or world.wall_at(m_next_x, m_next_y)):

                            #             change = self.will_monster_change_direction(world, m_next_x, m_next_y, move[0], move[1])

                            #             # If monster will not change directions
                            #             if not change:
                            #                 m_next_x = m_next_x + move[0]
                            #                 m_next_y = m_next_y + move[1]

                            #                 # Make all possible monster moves to avoid for new route calc 
                            #                 for cell in self.get_unsafe_zone(world, safe_distance-1, m_next_x, m_next_y):

                            #                     # Legal moves for deterministic monsters
                            #                     if not world.wall_at(cell[0],cell[1]):

                            #                         # Dont add the same cell to avoid twice
                            #                         if cell not in avoid:
                            #                             avoid.append(cell)

                            #             # Monster will change direction
                            #             else:
                            #                 for move in m_next_moves(m_next_x, m_next_y):
                            #                     m_next_x = move[0]
                            #                     m_next_y = move[1]

                            #                     # Legal moves for deterministic monsters
                            #                     if not (world.explosion_at(m_next_x, m_next_y) or world.wall_at(m_next_x, m_next_y)):

                            #                         for cell in self.get_unsafe_zone(world, safe_distance-1, m_next_x, m_next_y):

                            #                             # Legal moves for deterministic monsters
                            #                             if not world.wall_at(cell[0],cell[1]):

                            #                                 if cell not in avoid:
                            #                                     avoid.append(cell)

                            # # Else monster is completely random
                            # else:
                            #     # print (avoid)
                            #     print ('RANDOM AGENT DETECTED %s %s' % (new_x, new_y))
                            #     # print (m_next_moves(new_x, new_y))
                            #     # print (safe_distance)

                            #     passive = False

                            #     # Walls can cause longer paths.
                            #     # We can search for these as needs by reworking cells that are separated from the monster by a wall
                            #     walls = []

                            #     # Block off all immediate moves
                            #     for move in m_next_moves(new_x, new_y):
                            #         # self.set_cell_color(move[0], move[1], Fore.RED + Back.GREEN)
                            #         m_next_x = move[0]
                            #         m_next_y = move[1]

                            #         if 0 <= m_next_x < world.width() and 0 <= m_next_y < world.height():

                            #             # Legal moves for deterministic monsters
                            #             if not world.wall_at(m_next_x, m_next_y):

                            #                 for cell in self.get_unsafe_zone(world, safe_distance-1, m_next_x, m_next_y):

                            #                     # Legal moves for deterministic monsters
                            #                     if not world.wall_at(cell[0],cell[1]):

                            #                         if cell not in avoid:
                            #                             avoid.append(cell)

                            #                 # Block off the following move
                            #                 for smove in m_next_moves(m_next_x, m_next_y):
                            #                     # self.set_cell_color(smove[0], smove[1], Fore.RED + Back.GREEN)
                            #                     sm_next_x = smove[0]
                            #                     sm_next_y = smove[1]

                            #                     if 0 <= sm_next_x < world.width() and 0 <= sm_next_y < world.height():

                            #                         # Legal moves for deterministic monsters
                            #                         if not world.wall_at(sm_next_x, sm_next_y):

                            #                             for cell in self.get_unsafe_zone(world, safe_distance-1, sm_next_x, sm_next_y):

                            #                                 # Legal moves for deterministic monsters
                            #                                 if not world.wall_at(cell[0],cell[1]):

                            #                                     if cell not in avoid:
                            #                                         avoid.append(cell)
                            #                         else:
                            #                             if (sm_next_x, sm_next_y) not in walls:
                            #                                 walls.append((sm_next_x, sm_next_y))
                                        # else:
                                        #     if (m_next_x, m_next_y) not in walls:
                                        #         walls.append((m_next_x, m_next_y))


                                        # # Block off the following move
                                        # for smove in m_next_moves(m_next_x, m_next_y):
                                        #     # self.set_cell_color(smove[0], smove[1], Fore.RED + Back.GREEN)
                                        #     sm_next_x = smove[0]
                                        #     sm_next_y = smove[1]

                                        #     if 0 <= sm_next_x < world.width() and 0 <= sm_next_y < world.height():

                                        #         # Legal moves for deterministic monsters
                                        #         if not world.wall_at(sm_next_x, sm_next_y):

                                        #             for cell in self.get_unsafe_zone(world, safe_distance-1, sm_next_x, sm_next_y):

                                        #                 # Legal moves for deterministic monsters
                                        #                 if not world.wall_at(cell[0],cell[1]):

                                        #                     if cell not in avoid:
                                        #                         avoid.append(cell)
                                        #         else:
                                        #             if (sm_next_x, sm_next_y) not in walls:
                                        #                 walls.append((sm_next_x, sm_next_y))
                                # print(walls)
                                # # For each wall found
                                # for wall in walls:

                                #     # For each possible move adjacent to a wall
                                #     for move in m_next_moves(wall[0], wall[1]):

                                #         # If the move off 
                                #         if move[0] move[1]


        # If the move is garenteed safe we return true
        # print (passive, avoid)

        # for wall in walls:
        #     for move in m_next_moves(wall[0], wall[1]):
        #         if (move[0], m)


        # if avoid:
        #     for cell in avoid:
        #         self.set_cell_color(cell[0], cell[1], Fore.RED + Back.YELLOW)

        # return (passive, ())

        # def will_change(self, avoid):
        #     for move in m_next_moves(m_next_x, m_next_y):
        #         m_next_x = m_next_x + move[0]
        #         m_next_y = m_next_y + move[1]

        #         # Legal moves for deterministic monsters
        #         if not (world.explosion_at(m_next_x, m_next_y) or world.wall_at(m_next_x, m_next_y)):

        #             for cell in self.get_unsafe_zone(world, safe_distance-1, m_next_x, m_next_y):

        #                 # Legal moves for deterministic monsters
        #                 if not world.wall_at(cell[0],cell[1]):

        #                     if cell not in avoid:
        #                         avoid.append(cell)
        #     return

        # def wont_change(self):


    # def get_unsafe_zone(self, world, monster_range, x, y):
    #     unsafe_zone = []

    #     for dx in range(-monster_range, monster_range+1):
    #         for dy in range(-monster_range, monster_range+1):
    #             new_x = x + dx
    #             new_y = y + dy
    #             if 0 <= new_x < world.width() and 0 <= new_y < world.height():

    #                 # TODO BLEEDS THROUGH WALLS HERE

    #                 unsafe_zone.append((new_x, new_y))

    #     return unsafe_zone

    def m_wont_win(self, x, y, forced_mx, forced_my, monster_range):
        for i in range(-monster_range, monster_range+1):
            for j in range(-monster_range, monster_range+1):
                if x + i == forced_mx and y + j == forced_my:
                    return False
        return True



    # ------------------------------------------------------------------------------------------------------------------------/


    def do(self, wrld):

        # if self.predicted_move_1 != (0,0):

        #     for i in range(wrld.width()):
        #         for j in range(wrld.height()):
        #             if wrld.monsters_at(i,j):
        #                 if self.predicted_move_1 == ((i,j)):
        #                     print ('[+] PREDICTED MOVE %s %s' % (self.predicted_move_1[0], self.predicted_move_1[1]))
        #                 else:
        #                     print ('[-] PREDICTION WAS WRONG %s %s %s %s' % (self.predicted_move_1[0], self.predicted_move_1[1], i, j))

        # if self.predicted_move_2 != (0,0):

        #     if self.b_timer != 0:
        #         self.b_timer -= 1
        #     else:
        #         for i in range(wrld.width()):
        #             for j in range(wrld.height()):
        #                 if wrld.monsters_at(i,j):
        #                     if self.predicted_move_2 == ((i,j)):
        #                         print ('[+] PREDICTED MOVE')
        #                     else:
        #                         print ('[-] PREDICTION WAS WRONG')
        #         self.b_timer = 1
        #         self.predicted_move_2 = (0,0)

        if self.b_timer != 0:
            self.b_timer -= 1

        # Reset colors
        for i in range(wrld.width()):
            for j in range(wrld.height()):
                self.set_cell_color(i, j, Fore.BLACK + Back.BLACK)

        blast_zone = []
        blast = lambda x, y: [(x,y) for x,y in [(x,y),(x+1,y),(x+2,y),(x+3,y),(x+4,y),(x,y+1),(x,y+2),(x,y+3),(x,y+4),(x-1,y),(x-2,y),(x-3,y),(x-4,y),(x,y-1),(x,y-2),(x,y-3),(x,y-4)]]
        neighborhood = lambda y, x, wrld: [
            (y, x) for y, x in [(y - 1, x), (y, x + 1), (y + 1, x), (y, x - 1), (y - 1, x - 1), (y + 1, x + 1), (y - 1, x + 1), (y + 1, x - 1)]
            if 0 <= y < wrld.width() and 0 <= x < wrld.height()
        ]

        s_world = wrld.from_world(wrld)
        # print(vars(s_world))
        for i in range(wrld.width()):
            for j in range(wrld.height()):
                if wrld.bomb_at(i,j):
                    pbz = blast(i,j)
                    for m_id in s_world.monsters:
                        for monster in s_world.monsters[m_id]:
                            if (monster.x, monster.y) in pbz:
                                for move in neighborhood(monster.x, monster.y, wrld):
                                    if move not in pbz and wrld.wall_at(move[0],move[1]):
                                        monster.move(move[0], move[1])
                    for c_id in s_world.characters:
                        for character in s_world.characters[c_id]:
                            if (character.x, character.y) in pbz:
                                for move in neighborhood(character.x, character.y, wrld):
                                    if move not in pbz and wrld.wall_at(move[0],move[1]):
                                        character.move(move[0], move[1])

        nw, ev = s_world.next()
        
        for i in range(wrld.width()):
            for j in range(wrld.height()):
                if nw.explosion_at(i,j) or s_world.explosion_at(i,j):
                    blast_zone.append((i,j))
                    # print (i, j, nw.explosion_at(i,j))

        next_vectors = []
        for i in [-1,0,1]: 
            for j in [-1,0,1]:
                next_vectors.append((i,j))

            # Get me and exit
        me = wrld.me(self)
        goal = self.get_exit(wrld)
        
        # Find best passive path and then pop() first move
        steps, path = self.a_star(wrld.grid, 0, me.x, me.y, goal)
        if path:
            move = path.pop()
            dx = move[0] - me.x
            dy = move[1] - me.y
        else:
            move = me.x, me.y
            dx = move[0] - me.x
            dy = move[1] - me.y


        e_dist = lambda x1, y1, x2, y2: math.sqrt((x1-x2)**2 + (y1-y2)**2)
        # Optional: See best passive route found
        # for cell in path:
        #     self.set_cell_color(cell[0], cell[1], Fore.RED + Back.GREEN)

        # Determine the state of the character: passive or not passive
        # avoid will return as [] for passive and the character will move along the shortest passive path
        # avoid will rerutn a list of potenial dangerous squares given the 
        # passive, move, s_mons = self.is_passive(wrld, me.x, me.y, dx, dy, blast_zone)
        # if not move:
        #     move = next_shortest_move
        # if not s_mons:
        #     s_mons = self.predict(wrld, me.x, me.y, dx, dy)
        # if False:
        #     print('PASSIVE')

        #     if self.b_timer == 0 and (dx,dy) != (0,0):
        #         m_dist = {}
        #         for m in s_mons:
        #             dist = e_dist(me.x,me.y,m.x,m.y)
        #             m_dist[m] = dist
        #         for m in sorted(m_dist.items(), key=lambda x: x[1]):
        #             if m[0].name == 'aggressive':
        #                 s_dist = 5
        #             else:
        #                 s_dist = 4
                    
        #             if m[1] < s_dist:
        #                 mx = m[0].x + m[0].dx
        #                 my = m[0].y + m[0].dy

        #                 b_moves = {}
        #                 for ndx, ndy in next_vectors:
        #                     nx = me.x + ndx
        #                     ny = me.y + ndy

        #                     if 0 <= nx < wrld.width() and 0 <= ny < wrld.height():
        #                         dist = e_dist(nx,ny,mx,my)
        #                         b_moves[(nx,ny)] = dist

        #                 unsafe_cells = self.preserve(wrld, s_mons)
        #                 for cell in blast_zone:
        #                     if cell not in unsafe_cells:
        #                         unsafe_cells.append(cell)

        #                 for move in sorted(b_moves.items(), key=lambda x: x[1], reverse=True):
        #                     if move:
        #                         if move[0] not in unsafe_cells:
        #                             dx = move[0][0] - me.x
        #                             dy = move[0][0] - me.y
        #                             self.place_bomb()
        #                             self.b_timer = 3
        #                             print (dx,dy)
        #                             self.move(dx, dy)
        #                             return

        #     # if self.b_timer == 0 and (dx,dy) != (0,0):
        #     #     self.place_bomb()
        #     #     self.b_timer = 3



        #     print (dx,dy)
        #     self.move(dx, dy)
        #     return
        # else:


        print('START')
        # self.set_cell_color(move[0], move[1], Fore.GREEN + Back.YELLOW)
        dx = move[0] - me.x
        dy = move[1] - me.y

        s_mons = self.predict(wrld, me.x, me.y, dx, dy)

        unsafe_moves = self.preserve(wrld, s_mons)
        for cell in blast_zone:
            if cell not in unsafe_moves:
                unsafe_moves.append(cell)
        move = self.choose_move(wrld, me.x, me.y, unsafe_moves, s_mons, goal)

        if self.b_timer == 0:
            print ('HERE')
            print(path)
            if not path:
                self.place_bomb()
                self.b_timer = 5

        new_move = ()
        s_wrld = wrld.from_world(wrld)
        s_wrld.me(self).move(dx, dy)
        ns_wrld, ev = s_wrld.next()
        for event in ev:
            if event.other:
                if (event.other.name == me.name and event.tpe == 2) or (event.character.name == me.name and event.tpe == 3):

                    possible_moves = []
                    for dx, dy in next_vectors:
                        nx = me.x + dx
                        ny = me.y + dy
                        if 0 <= nx < wrld.width() and 0 <= ny < wrld.height():
                            possible_moves.append((nx,ny))
                    found = []
                    found = self.control_loop(wrld, me.x, me.y, dx, dy, [move], possible_moves, found)
                    if found:
                        e_dist = lambda x1, y1, x2, y2: math.sqrt((x1-x2)**2 + (y1-y2)**2)
                        q_table = {}
                        for (nx,ny) in found:
                            q = 0
                            for m in s_mons:
                                mx, my = m.x+m.dx, m.y+m.dy
                                dist = e_dist(nx,ny,mx,my)
                                if m.name == 'aggressive':
                                    wa = 0.5 * 1/1+dist
                                    q += wa
                                else:
                                    wb = 0.3 * 1/1+dist
                                    q += wb
                            we = 0.2 * 1/1+e_dist(nx,ny,goal[0],goal[1])
                            q += we
                            q_table[(nx,ny)] = q
                        for move in sorted(q_table.items(), key=lambda x: x[1], reverse=True):
                            if move:
                                n_move = move[0]
                                print('FOUND ALTERNATIVE')
                                dx = n_move[0] - me.x
                                dy = n_move[1] - me.y
                                print (dx,dy)
                                self.move(dx, dy)
                                return

        print('MAKE CHOICE')
        move = self.choose_move(wrld, me.x, me.y, unsafe_moves, s_mons, goal)
        dx = move[0] - me.x
        dy = move[1] - me.y
        # print (dx,dy)

        neighborhood = lambda y, x: [
            (y, x) for y, x in [(y - 1, x), (y, x + 1), (y + 1, x), (y, x - 1), (y - 1, x - 1), (y + 1, x + 1), (y - 1, x + 1), (y + 1, x - 1)]
            if 0 <= y < wrld.width() and 0 <= x < wrld.height()
        ]
        e_dist = lambda x1, y1, x2, y2: math.sqrt((x1-x2)**2 + (y1-y2)**2)

        s_wrld = wrld.from_world(wrld)
        print('----OLD----')
        # s_wrld.printit()
        s_wrld.me(self).move(dx, dy)
        ns_wrld, ev = s_wrld.next()
        print('----NEW-----')
        # ns_wrld.printit()
        for event in ev:
            if event.other:
                if (event.other.name == wrld.me(self).name and event.tpe == 2) or (event.character.name == wrld.me(self).name and event.tpe == 3):
                    print ('BOMB CASE')

                    q_table = {}
                    for (i,j) in neighborhood(me.x,me.y):
                        if (i,j) not in blast_zone:
                            q = 0
                            for m in s_mons:
                                mx, my = m.x+m.dx, m.y+m.dy
                                dist = e_dist(i,j,mx,my)
                                if m.name == 'aggressive':
                                    wa = 0.5 * 1/1+dist
                                    q += wa
                                else:
                                    wb = 0.3 * 1/1+dist
                                    q += wb
                            we = 0.2 * 1/1+e_dist(nx,ny,goal[0],goal[1])
                            q += we
                            q_table[(nx,ny)] = q
                    for move in sorted(q_table.items(), key=lambda x: x[1], reverse=True):
                        if move[0]:
                            print('HERE1')
                            if move[0] not in blast_zone:
                                print(move[0])
                                dx = move[0][0] - me.x
                                dy = move[0][1] - me.y

                                blast_zone = []
                                s_world = wrld.from_world(wrld)
                                # print(vars(s_world))
                                for i in range(wrld.width()):
                                    for j in range(wrld.height()):
                                        if wrld.bomb_at(i,j):
                                            pbz = blast(i,j)
                                            for m_id in s_world.monsters:
                                                for monster in s_world.monsters[m_id]:
                                                    if (monster.x, monster.y) in pbz:
                                                        for move in neighborhood(monster.x, monster.y):
                                                            if move not in pbz and wrld.wall_at(move[0],move[1]):
                                                                monster.move(move[0], move[1])
                                            for c_id in s_world.characters:
                                                for character in s_world.characters[c_id]:
                                                    if (character.x, character.y) in pbz:
                                                        for move in neighborhood(character.x, character.y):
                                                            if move not in pbz and wrld.wall_at(move[0],move[1]):
                                                                character.move(move[0], move[1])

                                nw, ev = s_world.next()
                                for i in range(wrld.width()):
                                    for j in range(wrld.height()):
                                        if nw.explosion_at(i,j) or wrld.explosion_at(i,j):
                                            blast_zone.append((i,j))

                                if move not in blast_zone:
                                    print('HERE2')
                                    self.move(dx,dy)
                                    return
                                else:
                                    q_table = {}
                                    for (i,j) in neighborhood(me.x,me.y):
                                        if not wrld.wall_at(i,j):
                                            if (i,j) not in blast_zone:
                                                q = 0
                                                for m in s_mons:
                                                    mx, my = m.x+m.dx, m.y+m.dy
                                                    dist = e_dist(i,j,mx,my)
                                                    if m.name == 'aggressive':
                                                        wa = 0.5 * 1/1+dist
                                                        q += wa
                                                    else:
                                                        wb = 0.3 * 1/1+dist
                                                        q += wb
                                                we = 0.2 * 1/1+e_dist(i,j,goal[0],goal[1])
                                                q += we
                                                q_table[(i,j)] = q
                                    for move in sorted(q_table.items(), key=lambda x: x[1], reverse=True):
                                        if move:
                                            if move[0] not in blast_zone:
                                                print('HERE3')
                                                dx = move[0][0] - me.x
                                                dy = move[0][1] - me.y
                                                print (blast_zone, move[0], me.x, me.y)
                                                print(dx,dy)
                                                self.move(dx,dy)
                                                return
        print('HERE4')
        print(dx,dy)
        self.move(dx, dy)
        return

            # m_dist = {}
            # for m in s_mons:
            #     dist = e_dist(me.x,me.y,m.x,m.y)
            #     m_dist[m] = dist
            # for m in sorted(m_dist.items(), key=lambda x: x[1]):
            #     mx = m[0].x + m[0].dx
            #     my = m[0].y + m[0].dy

            #     b_moves = {}
            #     for ndx, ndy in next_vectors:
            #         nx = me.x + ndx
            #         ny = me.y + ndy

            #         if 0 <= nx < wrld.width() and 0 <= ny < wrld.height():
            #             dist = e_dist(nx,ny,mx,my)
            #             b_moves[(nx,ny)] = dist

            #     for move in sorted(b_moves.items(), key=lambda x: x[1], reverse=True):
            #         if move[0]:
            #             dx = move[0][0] - me.x
            #             dy = move[0][0] - me.y
            #             self.place_bomb()
            #             self.b_timer = 3
            #             print (dx,dy)
            #             self.move(dx, dy)
            #             return







    def control_loop(self, wrld, x, y, dx, dy, bad_moves, possible_moves, found):
        print('CONTROL LOOP')
        goal = self.get_exit(wrld)
        s_mons = self.predict(wrld, x, y, dx, dy)
        unsafe_moves = self.preserve(wrld, s_mons)

        for move in bad_moves:
            unsafe_moves.append(move)

        if possible_moves:
            # print (bad_moves)

            move = possible_moves.pop()

            s_wrld = wrld.from_world(wrld)
            s_wrld.me(self).move(dx, dy)
            ns_wrld, ev = s_wrld.next()
            for event in ev:
                if event.other:
                    if (event.other.name == wrld.me(self).name and event.tpe == 2) or (event.character.name == wrld.me(self).name and event.tpe == 3):
                        bad_moves.append(move)
                        return self.control_loop(wrld, x, y, dx, dy, bad_moves, possible_moves, found)
                    else:
                        found.append(move)
        return found










                        

            # if self.b_timer == 0 and (dx,dy) != (0,0):
            #     m_dist = {}
            #     for m in s_mons:
            #         dist = e_dist(me.x,me.y,m.x,m.y)
            #         m_dist[m] = dist
            #     for m in sorted(m_dist.items(), key=lambda x: x[1]):
            #         if m[0].name == 'aggressive':
            #             s_dist = 5
            #         else:
            #             s_dist = 4
                    
            #         if m[1] < s_dist:
            #             mx = m[0].x + m[0].dx
            #             my = m[0].y + m[0].dy

            #             b_moves = {}
            #             for ndx, ndy in next_vectors:
            #                 nx = me.x + ndx
            #                 ny = me.y + ndy

            #                 if 0 <= nx < wrld.width() and 0 <= ny < wrld.height():
            #                     dist = e_dist(nx,ny,mx,my)
            #                     b_moves[(nx,ny)] = dist

            #             unsafe_cells = self.preserve(wrld, s_mons)
            #             for cell in blast_zone:
            #                 if cell not in unsafe_cells:
            #                     unsafe_cells.append(cell)

            #             for move in sorted(b_moves.items(), key=lambda x: x[1], reverse=True):
            #                 if move[0]:
            #                     if move[0] not in unsafe_cells:
            #                         dx = move[0][0] - me.x
            #                         dy = move[0][0] - me.y
            #                         self.place_bomb()
            #                         self.b_timer = 3
            #                         print (dx,dy)
            #                         self.move(dx, dy)
            #                         return
            # # if self.b_timer == 0 and (dx,dy) != (0,0):
            # #     self.place_bomb()
            # #     self.b_timer = 3
            # self.set_cell_color(move[0], move[1], Fore.GREEN + Back.YELLOW)
            # print (dx,dy)
            # self.move(dx, dy)
            # return

            # if next_shortest_move not in blast_zone:
        #         print('CONTROL 4')
        #         for cell in blast_zone:
        #             self.set_cell_color(cell[0], cell[1], Fore.GREEN + Back.YELLOW)
        #         print (next_shortest_move)
        #         print(dx,dy)
        #         self.move(dx, dy)

        # if passive:
        #     print('PASSIVE')
        #     if move:
        #         dx = move[0] - me.x
        #         dy = move[1] - me.y
        #         if move in unsafe_cells:
        #             print('CONTROL 1')
        #             s_mons = self.predict(wrld, me.x, me.y, dx, dy)
        #             unsafe_moves = self.preserve(wrld, s_mons)
        #             move = self.choose_move(wrld, me.x, me.y, unsafe_moves, s_mons, goal)
        #             dx = move[0] - me.x
        #             dy = move[1] - me.y
        #         else:
        #             print(dx,dy)
        #             self.move(dx,dy)

        #     if next_shortest_move not in blast_zone:
        #         print('CONTROL 4')
        #         for cell in blast_zone:
        #             self.set_cell_color(cell[0], cell[1], Fore.GREEN + Back.YELLOW)
        #         print (next_shortest_move)
        #         print(dx,dy)
        #         self.move(dx, dy)

        #     else:
        #         print('CONTROL 2')
        #         s_mons = self.predict(wrld, me.x, me.y, dx, dy)
        #         unsafe_moves = self.preserve(wrld, s_mons)
        #         for cell in unsafe_moves:
        #             self.set_cell_color(cell[0], cell[1], Fore.GREEN + Back.YELLOW)
        #         move = self.choose_move(wrld, me.x, me.y, unsafe_moves, s_mons, goal)
        #         dx = move[0] - me.x
        #         dy = move[1] - me.y

        #     # self.preserve(wrld, avoid, me.x, me.y, dx, dy)
        # else:
        #     print('CONTROL MAIN')
        #     s_mons = self.predict(wrld, me.x, me.y, dx, dy)
        #     unsafe_moves = self.preserve(wrld, s_mons)
        #     for (i,j) in blast_zone:
        #         if (i,j) not in unsafe_moves:
        #             unsafe_moves.append((i,j))

        #     move = self.choose_move(wrld, me.x, me.y, unsafe_moves, s_mons, goal)
        #     dx = move[0] - me.x
        #     dy = move[1] - me.y

        #     if self.b_timer == 0:
        #         self.place_bomb()
        #         self.b_timer = 3

        #     print (dx,dy)
        #     self.move(dx, dy)


            
    # ------------------------------------------------------------------------------------------------------------------------/



    def predict(self, world, x, y, dx, dy):

        # Copy the world
        copy_world = world.from_world(world)

        # Play the moves
        copy_world.me(self).move(dx,dy)
        sw, ev = copy_world.next()
    

        # Find next location of all monsters
        monsters = []
        for i in range(sw.width()):
            for j in range(sw.height()):
                if sw.monsters_at(i,j):
                    for monster in sw.monsters_at(i,j):
                        monsters.append(monster)
        return monsters

    def preserve(self, world, s_mons):
        unsafe_cells = []

        # Find unsafe cells for next movement
        for m in s_mons:
            if m.name == 'aggressive':
                safe_distance = 2
            else:
                safe_distance = 1

            for dx in range(-safe_distance, safe_distance+1):
                for dy in range(-safe_distance, safe_distance+1):
                    x = m.x + dx
                    y = m.y + dy
                    if 0 <= x < world.width() and 0 <= y < world.height():
                        unsafe_cells.append((x, y))
                        self.set_cell_color(x, y, Fore.BLACK + Back.RED)
            for i in range(world.width()):
                for j in range(world.height()):
                    if (world.monsters_at(i, j) or world.explosion_at(i, j) or world.wall_at(i, j) or world.bomb_at(i, j)):
                        if (i, j) not in unsafe_cells:
                            unsafe_cells.append((i, j))

        return unsafe_cells

    def choose_move(self, world, x, y, unsafe_cells, s_mons, goal):
        e_dist = lambda x1, y1, x2, y2: math.sqrt((x1-x2)**2 + (y1-y2)**2)
        blast = lambda x, y: [(x,y) for x,y in [(x,y),(x+1,y),(x+2,y),(x+3,y),(x+4,y),(x,y+1),(x,y+2),(x,y+3),(x,y+4),(x-1,y),(x-2,y),(x-3,y),(x-4,y),(x,y-1),(x,y-2),(x,y-3),(x,y-4)]]
        neighborhood = lambda y, x: [
            (y, x) for y, x in [(y - 1, x), (y, x + 1), (y + 1, x), (y, x - 1), (y - 1, x - 1), (y + 1, x + 1), (y - 1, x + 1), (y + 1, x - 1)]
            if 0 <= y < world.width() and 0 <= x < world.height()
        ]

        sw = world.from_world(world)
        copy_grid = sw.grid.copy()
        # print(unsafe_cells)
        for (i, j) in unsafe_cells:
            if 0 <= i < world.width() and 0 <= j < world.height():
                copy_grid[i][j] = True

        steps, path = self.a_star(copy_grid, 0, x, y, goal)
        if path:
            print ('SAFE MOVE AROUND')
            # for cell in path:
            #     self.set_cell_color(cell[0], cell[1], Fore.Black + Back.YELLOW)
            move = path.pop()
            return move
        else:
            print('DURDLE')
            move = self.durdle(world, x, y, unsafe_cells, s_mons, goal)

            blast_zone = []
            s_world = world.from_world(world)
            # print(vars(s_world))
            for i in range(world.width()):
                for j in range(world.height()):
                    if world.bomb_at(i,j):
                        pbz = blast(i,j)
                        for m_id in s_world.monsters:
                            for monster in s_world.monsters[m_id]:
                                if (monster.x, monster.y) in pbz:
                                    for move in neighborhood(monster.x, monster.y):
                                        if move not in pbz and world.wall_at(move[0],move[1]):
                                            monster.move(move[0], move[1])
                        for c_id in s_world.characters:
                            for character in s_world.characters[c_id]:
                                if (character.x, character.y) in pbz:
                                    for move in neighborhood(character.x, character.y):
                                        if move not in pbz and world.wall_at(move[0],move[1]):
                                            character.move(move[0], move[1])

            nw, ev = s_world.next()
            for i in range(world.width()):
                for j in range(world.height()):
                    if nw.explosion_at(i,j) or world.explosion_at(i,j):
                        blast_zone.append((i,j))

            if move not in blast_zone:
                print (move)
                return move
            else:
                q_table = {}
                for (i,j) in neighborhood(x,y):
                    if not world.wall_at(i,j):
                        if (i,j) not in blast_zone:
                            q = 0
                            for m in s_mons:
                                mx, my = m.x+m.dx, m.y+m.dy
                                dist = e_dist(i,j,mx,my)
                                if m.name == 'aggressive':
                                    wa = 0.5 * 1/1+dist
                                    q += wa
                                else:
                                    wb = 0.3 * 1/1+dist
                                    q += wb
                            we = 0.2 * 1/1+e_dist(i,j,goal[0],goal[1])
                            q += we
                            q_table[(i,j)] = q
                for move in sorted(q_table.items(), key=lambda x: x[1], reverse=True):
                    if move:
                        if move[0] not in blast_zone:
                            return move[0]

 
    # def work_path(self, grid, x, y, unsafe_cells, goal, old_cell):

       
    def durdle(self, world, x, y, unsafe_cells, s_mons, goal):
        blast_zone = []
        blast = lambda x, y: [(x,y) for x,y in [(x,y),(x+1,y),(x+2,y),(x+3,y),(x+4,y),(x,y+1),(x,y+2),(x,y+3),(x,y+4),(x-1,y),(x-2,y),(x-3,y),(x-4,y),(x,y-1),(x,y-2),(x,y-3),(x,y-4)]]
        neighborhood = lambda y, x: [
            (y, x) for y, x in [(y - 1, x), (y, x + 1), (y + 1, x), (y, x - 1), (y - 1, x - 1), (y + 1, x + 1), (y - 1, x + 1), (y + 1, x - 1)]
            if 0 <= y < world.width() and 0 <= x < world.height()
        ]
        e_dist = lambda x1, y1, x2, y2: math.sqrt((x1-x2)**2 + (y1-y2)**2)

        s_world = world.from_world(world)
        # print(vars(s_world))
        for i in range(world.width()):
            for j in range(world.height()):
                if world.bomb_at(i,j):
                    pbz = blast(i,j)
                    for m_id in s_world.monsters:
                        for monster in s_world.monsters[m_id]:
                            if (monster.x, monster.y) in pbz:
                                for move in neighborhood(monster.x, monster.y):
                                    if move not in pbz and world.wall_at(move[0],move[1]):
                                        monster.move(move[0], move[1])
                    for c_id in s_world.characters:
                        for character in s_world.characters[c_id]:
                            if (character.x, character.y) in pbz:
                                for move in neighborhood(character.x, character.y):
                                    if move not in pbz and world.wall_at(move[0],move[1]):
                                        character.move(move[0], move[1])

        nw, ev = s_world.next()
        
        for i in range(world.width()):
            for j in range(world.height()):
                if nw.explosion_at(i,j) or s_world.explosion_at(i,j):
                    blast_zone.append((i,j))

        next_vectors = []
        for i in [-1,0,1]: 
            for j in [-1,0,1]:
                next_vectors.append((i,j))

        possible_moves = {}
        for dx, dy in next_vectors:
            nx = x + dx
            ny = y + dy
            if 0 <= nx < world.width() and 0 <= ny < world.height():
                # print (unsafe_cells)
                if (nx,ny) not in unsafe_cells:
                    for ddx, ddy in next_vectors:
                        nnx = nx + ddx
                        nny = ny + ddy
                        if 0 <= nnx < world.width() and 0 <= nny < world.height():
                            if (nnx, nny) not in unsafe_cells:
                                if (nx,ny) in possible_moves:
                                    possible_moves[(nx,ny)] += 1
                                else:
                                    possible_moves[(nx,ny)] = 1

        for move in sorted(possible_moves.items(), key=lambda x: x[1], reverse=True):
            if move:
                if move[0] not in unsafe_cells:
                    dx = move[0][0] - x
                    dy = move[0][1] - y

                    s_wrld = world.from_world(world)
                    print('----OLD----')
                    # s_wrld.printit()
                    s_wrld.me(self).move(dx, dy)
                    ns_wrld, ev = s_wrld.next()
                    print('----NEW-----')
                    # ns_wrld.printit()
                    for event in ev:
                        if event.other:
                            if (event.other.name == world.me(self).name and event.tpe == 2) or (event.character.name == world.me(self).name and event.tpe == 3):
                                print ('BOMB-----CASE')

                                q_table = {}
                                for (i,j) in neighborhood(x,y):
                                    if not world.wall_at(i,j):
                                        if (i,j) not in blast_zone:
                                            q = 0
                                            for m in s_mons:
                                                mx, my = m.x+m.dx, m.y+m.dy
                                                dist = e_dist(i,j,mx,my)
                                                if m.name == 'aggressive':
                                                    wa = 0.5 * 1/1+dist
                                                    q += wa
                                                else:
                                                    wb = 0.3 * 1/1+dist
                                                    q += wb
                                            we = 0.2 * 1/1+e_dist(i,j,goal[0],goal[1])
                                            q += we
                                            q_table[(i,j)] = q
                                for move in sorted(q_table.items(), key=lambda x: x[1], reverse=True):
                                    if move:
                                        if move[0] not in blast_zone:
                                            return move[0]

        e_dist = lambda x1, y1, x2, y2: math.sqrt((x1-x2)**2 + (y1-y2)**2)
        q_table = {}
        for dx, dy in next_vectors:
            nx = x + dx
            ny = y + dy
            if 0 <= nx < world.width() and 0 <= ny < world.height():
                if not (world.monsters_at(nx, ny) or
                    world.explosion_at(nx, ny) or
                    world.wall_at(nx, ny) or
                    world.bomb_at(nx, ny)):               
                    if (nx,ny) not in unsafe_cells:
                        q = 0
                        for m in s_mons:
                            mx, my = m.x, m.y
                            dist = e_dist(nx,ny,mx,my)
                            if m.name == 'aggressive':
                                wa = 0.5 * 1/1+dist
                                q += wa
                            else:
                                wb = 0.3 * 1/1+dist
                                q += wb
                        we = 0.2 * 1/1+e_dist(nx,ny,goal[0],goal[1])
                        q += we
                        q_table[(nx,ny)] = q

        for move in sorted(q_table.items(), key=lambda x: x[1], reverse=True):
            if move:
                if move[0] not in unsafe_cells:
                    dx = move[0][0] - x
                    dy = move[0][1] - y

                    s_wrld = world.from_world(world)
                    print('----OLD----')
                    # s_wrld.printit()
                    s_wrld.me(self).move(dx, dy)
                    ns_wrld, ev = s_wrld.next()
                    print('----NEW-----')
                    # ns_wrld.printit()
                    for event in ev:
                        if event.other:
                            if (event.other.name == world.me(self).name and event.tpe == 2) or (event.character.name == world.me(self).name and event.tpe == 3):
                                print ('BOMB------CASE')

                                q_table = {}
                                for (i,j) in neighborhood(x,y):
                                    if not world.wall_at(i,j):
                                        if (i,j) not in blast_zone:
                                            q = 0
                                            for m in s_mons:
                                                mx, my = m.x+m.dx, m.y+m.dy
                                                dist = e_dist(i,j,mx,my)
                                                if m.name == 'aggressive':
                                                    wa = 0.5 * 1/1+dist
                                                    q += wa
                                                else:
                                                    wb = 0.3 * 1/1+dist
                                                    q += wb
                                            we = 0.2 * 1/1+e_dist(i,j,goal[0],goal[1])
                                            q += we
                                            q_table[(i,j)] = q
                                for move in sorted(q_table.items(), key=lambda x: x[1], reverse=True):
                                    if move[0]:
                                        return move[0]

        random_moves = []
        for (dx, dy) in next_vectors:
            nx = x + dx
            ny = y + dy
            if 0 <= nx < world.width() and 0 <= ny < world.height():
                if (nx,ny) not in unsafe_cells:
                    random_moves.append((nx, ny))

        if random_moves:
            print('RANDOM SAFE')
            return random.choice(random_moves)
        else:
            print ('RANDOM')
            random_moves = []
            for (dx, dy) in next_vectors:
                nx = x + dx
                ny = y + dy
                if 0 <= nx < world.width() and 0 <= ny < world.height():
                    if not world.wall_at(nx,ny):
                        random_moves.append((nx, ny))
            if random_moves:
                return random.choice(random_moves)
            else:
                return (0,0)
            





            

            # print ('LOOK FOR LOWEST SAFE SPACE')
            # # print (steps - 1)
            # best_safe_space = (x,y)
            # dist_to_exit = 1000
            # rows = world.height() - 1
            # if y <= opp_cots[1]:
            #     while rows >= 0:
            #         for dx in range(world.width()):
            #             if not copy_grid[dx][steps - 1]:
            #                 to_low, path_to_low = self.a_star(world.grid, 0, x, y, (dx, steps-1))
            #                 to_exit, path_to_exit = self.a_star(world.grid, 0, dx, steps-1, goal)
            #                 if path_to_low:
            #                     # print(path_to_low)
            #                     # print(to_exit)
            #                     for cell in path_to_low:
            #                         self.set_cell_color(cell[0], cell[1], Fore.RED + Back.BLUE)
            #                     if to_exit < dist_to_exit:
            #                         best_safe_space = path_to_low.pop()
            #                         if self.m_wont_win(best_safe_space[0], best_safe_space[1], opp_cots[0], opp_cots[1], 2):
            #                             return best_safe_space
            #         rows -= 1
                
            # print("FINAL LOOP")
            # sw2 = world.from_world(world)
            # copy2 = sw2.grid.copy()
            # for k in [-1,0,1]:
            #     for l in [-1,0,1]:
            #         if 0 <= opp_cots[0]+k < world.width() and 0 <= opp_cots[1]+l < world.height():
            #             copy2[opp_cots[0]+k][opp_cots[1]+l] = True
            # # print(opp_cots)
            # # print(x, y) 
            # bm = (0,0) 
            # ms = 1000 
            # for i in [-1,0,1]: 
            #     for j in [-1,0,1]:
            #         if 0 <= x + i < world.width() and 0 <= y + j < world.height(): 
            #             if self.m_wont_win(x+i, y+j, opp_cots[0], opp_cots[1], 3): 
            #                 print ('WINNING')
                            
            #                 s, p = self.a_star(world.grid, 0, x+i, y+j, goal) 
            #                 if s < ms: 
            #                     if p:
            #                         for cell in p:
            #                             self.set_cell_color(cell[0], cell[1], Fore.YELLOW + Back.BLUE)
            #                         bm = p.pop() 
            #                         return bm

            # for i in [-1,0,1]: 
            #     for j in [-1,0,1]:
            #         if 0 <= x + i < world.width() and 0 <= y + j < world.height():
            #             if world.monsters_at(x+i, y+j):
            #                 dx = opp_cots[0] - x+i
            #                 dy = opp_cots[1] - x+j
            #                 if 0 <= x-dx < world.width() and 0 <= y-dy < world.height():
            #                     return ((x-dx, y-dy))
            #                 elif 0 <= x < world.width() and 0 <= y-dy < world.height():
            #                     return ((x, y-dy))
            #                 elif 0 <= x-dx < world.width() and 0 <= y < world.height():
            #                     return ((x-dx, y))
            # print ('here')
            # return (100, 100)




            # print ('here')
            #                         bm = (0,0)
            #                         ms = 1000
            #                         goal = self.get_exit(world)
            #                         for i in [-1,0,1]:
            #                             for j in [-1,0,1]:
            #                                 if 0 <= x + i < world.width() and 0 <= y + j < world.height():
            #                                     if self.m_wont_win(x+i, y+j, m_next_move[0], m_next_move[1], safe_distance - 1):
            #                                         print ('Sprinting')
            #                                         s, p = self.a_star(world.grid, 0, x+i, y+j, goal)
            #                                         if s < ms:
            #                                             if p:
            #                                                 bm = p.pop()

            




        
        # else:
        #     print("FINAL LOOP")
        #     bm = (0,0)
        #     ms = 1000
        #     for i in [-1,0,1]:
        #         for j in [-1,0,1]:
        #             if 0 <= x + i < world.width() and 0 <= y + j < world.height():
        #                 print ()
        #                 if self.m_wont_win(x+i, y+j, opp_cots[0], opp_cots[1], 2):
        #                     print ('WINNING')
        #                     s, p = self.a_star(world.grid, 0, x+i, y+j, goal)
        #                     if s < ms:
        #                         if p:
        #                             bm = p.pop()

        #     print ("BM")
        #     print (bm)
        #     return bm
        # # elif y >= opp_cots[1]:
        #     print ('SAFELY MOVE TOWARDS THE EXIT SPACE')
        #     to_exit, path_to_exit = self.a_star(world.grid, 0, x, y, goal)
        #     print (to_exit, path_to_exit)
        #     if path_to_exit:
        #         for cell in path_to_exit:
        #             self.set_cell_color(cell[0], cell[1], Fore.RED + Back.GREEN)
        #         print('GUN IT')
        #         return path_to_exit.pop()
        #     else:

        #         # change = self.will_monster_change_direction(world, new_x, new_y, m_dx, m_dy)
        #         return (0,0)
        # else:
        #     return (0,0)










            # # Find lowest unblocked square
            # blocked_row = {}
            # for i in range(world.width()):
            #     for j in range(world.height()):
            #         if copy_grid[i][j]:

            #             if i not in blocked_row:
            #                 blocked_row[i] = {}

            #             if j in blocked_row[i]:
            #                 blocked_row[i][j] += 1
            #             else:
            #                 blocked_row[i][j] = 1

            #             if j-1 in blocked_row[i]:
            #                 blocked_row[i][j-1] += 1
            #             elif j-1 >= 0:
            #                 blocked_row[i][j-1] = 1

            #             if j+1 in blocked_row[i]:
            #                 blocked_row[i][j+1] += 1
            #             elif j+1 <= world.height():
            #                 blocked_row[i][j+1] = 1
            # print (blocked_row)

            # for i in range(world.height()):
            #     if [(x) for x in range(world.width())] in blocked_row[i]:
            #         print (i)
                    #return highest_blocked_row
                



    # def do(self, wrld):
    #     for i in range(wrld.width()):
    #         for j in range(wrld.height()):
    #             self.set_cell_color(i, j, Fore.BLACK + Back.BLACK)

    #     me = wrld.me(self)
    #     exit = self.get_exit(wrld)
    #     # print('\n\nSTART')
    #     # print ('current %s %s' % (me.x, me.y))
    #     steps, path = self.a_star(wrld.grid, 0, me.x, me.y, exit)
    #     # print (path)
    #     next_shortest_move = path.pop()
    #     dx = next_shortest_move[0] - me.x
    #     dy = next_shortest_move[1] - me.y
    #     # print (next_shortest_move)
    #     # print (dx,dy)
    #     # print (safe_moves)

    #     # for cell in path:
    #     #     self.set_cell_color(cell[0], cell[1], Fore.RED + Back.GREEN)

    #     passive, avoid = self.is_passive(wrld, me.x, me.y, dx, dy)
    #     if passive:
    #         # print ('passive')
    #         # self.last_x = next_shortest_move[0]
    #         # self.last_y = next_shortest_move[1]
    #         self.move(dx, dy)
    #     else:

    #     print (wrld.monsters_at(3, 9))
    #     # if self.ran_move == 10:
    #     #     self.random
    #     me = wrld.me(self)
    #     # available_moves = self.get_available_moves(wrld, me.x, me.y) 
    #     # safe_moves = self.get_safe_moves(wrld, available_moves, me.x, me.y)
    #     # im_moves = lambda y, x: [(x, y) for x, y in [(x - 1, y), (x, y + 1), (x + 1, y), (x, y - 1), (x - 1, y - 1), (x + 1, y + 1), (x - 1, y + 1), (x + 1, y - 1)]
    #     #     if 0 <= y < wrld.width() and 0 <= x < wrld.height()]
    #     # safe_moves = im_moves(me.x, me.y)
    #     # if not safe_moves:
    #     #     safe_moves = [(x, y) for x, y in [(x - 1, y), (x, y + 1), (x + 1, y), (x, y - 1), (x - 1, y - 1), (x + 1, y + 1), (x - 1, y + 1), (x + 1, y - 1)]
    #     #     if 0 <= y < wrld.width() and 0 <= x < wrld.height()]
    #     #     print ('\nHERE\n')
    #     #     print (safe_moves)
    #     if self.start_best_dist == 0:
    #         exit = self.get_exit(wrld)
    #         steps, path = self.a_star(wrld.grid, 0, me.x, me.y, exit)
    #         self.start_best_dist = steps

    #     safe_moves = []
    #     for x in [-1,0,1]:
    #         for y in [-1,0,1]:
    #             new_x = me.x + x
    #             new_y = me.y + y
    #             if 0 <= new_x < wrld.width() and 0 <= new_y + y < wrld.height():
    #                 if wrld.wall_at(new_x, new_y) or (new_x, new_y) == (me.x, me.y):
    #                     # print ('WALL %s %s' % (new_x, new_y))
    #                     continue
    #                 else:
    #                     safe_moves.append((x,y))

    #     # safe_moves = []
    #     # for (x,y) in available_moves:
            
    #     #     if wrld.wall_at(x, y):
    #     #         continue
    #     #     elif wlrd.exit_at(x, y):
    #     #         safe_moves.append((x,y))

    #     #     b = wrld.bomb_at(x, y)

    #     #     if wrld.wrld.monsters_at(x, y):
    #     #         continue
    #     #     elif wrld.wall_at(x, y):
    #     #         continue
    #     #     elif wrld.explosion_at(x, y):
    #     #         continue

    #     #     m = wrld.wrld.monsters_at(x, y)
    #     #     e = wrld.explosion_at(x, y)
    #     #     b = wrld.bomb_at(x, y)


    #     if self.last_best_value != 0:
    #         reward = self.get_reward(wrld, me.x, me.y)
    #         actual_value = reward + self.discount * self.get_next_best(wrld, safe_moves, me.x, me.y)
    #         difference = actual_value - self.last_best_value
    #         self.set_weights(difference, self.last_monster_feature, self.last_exit_feature, self.last_cornered_feature)
        
    #     # current_value = 0
    #     # new_value = 0
    #     # best_value = 0
    #     # best_Move = (0,0)

    #     #TODO change get_safe_moves to block exit if a bomb is still waiting to explode

    #     # if len(available_moves[6]) > 0:
    #     #     if available_moves[6][0] in safe_moves:
    #     #         self.move(available_moves[6][0][0], available_moves[6][0][1])
    #         # else:
    #             #TODO Durdle for a while until bomb explodes

    #     exit = self.get_exit(wrld)
    #     # print('\n\nSTART')
    #     # print ('current %s %s' % (me.x, me.y))
    #     steps, path = self.a_star(wrld.grid, 0, me.x, me.y, exit)
    #     # print (path)
    #     next_shortest_move = path.pop()
    #     dx = next_shortest_move[0] - me.x
    #     dy = next_shortest_move[1] - me.y
    #     # print (next_shortest_move)
    #     # print (dx,dy)
    #     # print (safe_moves)

    #     # for cell in path:
    #     #     self.set_cell_color(cell[0], cell[1], Fore.RED + Back.GREEN)

    #     passive, avoid = self.is_passive(wrld, me.x, me.y, dx, dy)
    #     if passive:
    #         # print ('passive')
    #         # self.last_x = next_shortest_move[0]
    #         # self.last_y = next_shortest_move[1]
    #         self.move(dx, dy)
    #     else:
    #         # print (avoid)
    #     #     print('trouble')
    #         move = self.q_learn(wrld, safe_moves, me.x, me.y)
    #         # print (safe_moves)
    #         # print (move)
    #         self.last_x = me.x + move[0]
    #         self.last_y = me.y + move[1]
            
    #         for dx in [-1,0,1]:
    #             for dy in [-1,0,1]:
    #                 new_x = me.x + dx
    #                 new_y = me.y + dy
    #                 if 0 <= new_x < wrld.width() and 0 <= new_y < wrld.height():

    #                     if wrld.exit_at(new_x, new_y):
    #                         reward = 25000
    #                         actual_value = reward + self.discount * self.get_next_best(wrld, safe_moves, me.x, me.y)
    #                         difference = actual_value - self.last_best_value
    #                         self.set_weights(difference, self.last_monster_feature, self.last_exit_feature, self.last_cornered_feature)
    #                         f = open("weights.txt", "w")
    #                         for i in range(3):
    #                             if i == 0:
    #                                 w_str1 = "%f\n" % self.w_monster
    #                                 f.write(w_str1)
    #                             if i == 1:
    #                                 w_str2 = "%f\n" % self.w_exit
    #                                 f.write(w_str2)
    #                             if i == 2:
    #                                 w_str3 = "%f\n" % self.w_cornered
    #                                 f.write(w_str3)
    #                             i += 1
    #                         f.close()
    #                         self.steps_left -= 1
    #                         self.move(dx, dy)
    #                         return
                       
    #         s_wrld = wrld.from_world(wrld)
    #         s_wrld.me(self).move(move[0], move[1])
    #         ns_wrld, ev = s_wrld.next()
    #         if ev:
    #             # pprint(vars(ev[0]))
    #             # print(ev[0].tpe)
    #             if ev[0].tpe == 3:
    #                 reward = -10000
    #                 actual_value = reward + self.discount * self.get_next_best(wrld, safe_moves, me.x, me.y)
    #                 difference = actual_value - self.last_best_value
    #                 self.set_weights(difference, self.last_monster_feature, self.last_exit_feature, self.last_cornered_feature)
    #                 f = open("weights.txt", "w")
    #                 for i in range(3):
    #                     if i == 0:
    #                         w_str1 = "%f\n" % self.w_monster
    #                         f.write(w_str1)
    #                     if i == 1:
    #                         w_str2 = "%f\n" % self.w_exit
    #                         f.write(w_str2)
    #                     if i == 2:
    #                         w_str3 = "%f\n" % self.w_cornered
    #                         f.write(w_str3)
    #                     i += 1
    #                 f.close()
    #                 self.steps_left -= 1
    #                 self.move(move[0], move[1])
    #                 return
            
    #         self.steps_left -= 1
    #         self.move(move[0], move[1])
    #         f = open("weights.txt", "w")
    #         for i in range(3):
    #             if i == 0:
    #                 w_str1 = "%f\n" % self.w_monster
    #                 f.write(w_str1)
    #             if i == 1:
    #                 w_str2 = "%f\n" % self.w_exit
    #                 f.write(w_str2)
    #             if i == 2:
    #                 w_str3 = "%f\n" % self.w_cornered
    #                 f.write(w_str3)
    #             i += 1
    #         f.close()
    #         return

    #     # for cell in path:
    #     self.set_cell_color(cell[0], cell[1], Fore.BLACK + Back.BLACK)