import random, math, time
# from numba import jit
import matplotlib.pyplot as plt
import pygame


class CA(object):

    def __init__(self, board=None, kelp_prob=None, urchin_prob=None, otter_prob=None):  # initializing 2d ca
        if board == None:
            self.nb_otter = 0
            self.nb_urchin = 0
            self.nb_kelp = 0
            self.urchin_pos = []  # array of position of all urchins for otter hunt
            self.empty = []
            # creates the 2d array
            self.grid = []
            for i in range(100):
                self.grid.append([])

            for i in range(100):  # sets initial density : 0.1% otter, 59.9% empty, 30% kelp, 10% urchin
                for j in range(100):
                    temp = random.randint(1, 1000)
                    if temp == 1:
                        self.grid[i].append(Otter([i, j]))
                        self.nb_otter += 1

                    elif 2 <= temp <= 101:
                        self.grid[i].append(Urchin([i, j]))
                        self.urchin_pos.append([i, j])
                        self.nb_urchin += 1

                    elif 102 <= temp <= 401:
                        self.grid[i].append(Kelp([i, j]))
                        self.nb_kelp += 1

                    else:
                        self.grid[i].append([0])
                        self.empty.append([i, j])
        else:
            self.grid = board

    # kill otters if too old
    # kill urchins if too old
    # kill kelp if too old
    # make otters move
    # make urchins move
    # reproduce otters
    # reproduce urchins
    # reproduce kelp
    # make them age +1
    def updating(self):

        # KILLING THE OLD ANIMALS
        for i in range(100):
            for j in range(100):
                if self.grid[i][j] != [0]:
                    self.grid[i][j].death(self)

        # MOVING THE OTTERS
        for i in range(100):
            for j in range(100):
                if type(self.grid[i][j]) is Otter:  # checks if animal is an otter
                    self.grid[i][j].move(self)

        # MOVING THE URCHINS
        for i in range(100):
            for j in range(100):
                if type(self.grid[i][j]) is Urchin:  # checks if animal is an Urchin
                    self.grid[i][j].move(self)

        # REPRODUCTION FOR OTTERS
        for i in range(100):
            for j in range(100):
                if type(self.grid[i][j]) is Otter:  # checks if animal is an otter:
                    self.grid[i][j].reproduce(self)

        # REPRODUCTION FOR URCHINS
        for i in range(100):
            for j in range(100):
                if type(self.grid[i][j]) is Urchin:  # checks if animal is an urchin:
                    self.grid[i][j].reproduce(self)

        # REPRODUCTION FOR KELP
        for i in range(100):
            for j in range(100):
                if type(self.grid[i][j]) is Kelp:  # checks if animal is an kelp:
                    self.grid[i][j].reproduce(self)

        # MAKING THEM AGE +1
        for i in range(100):
            for j in range(100):
                if self.grid[i][j] != [0]:
                    self.grid[i][j].update_age()

    # initializes display screen
    def create_display(self):
        white = (255, 255, 255)
        screen = pygame.display.set_mode((1000, 1000))
        screen.fill(white)  # set background white
        return screen

    # updates display screen after every iteration
    def display(self, screen):
        URCHIN_COLOR = (255, 0, 0)  # Urchin is red
        KELP_COLOR = (0, 255, 0)  # Kelp is green
        OTTER_COLOR = blue = (0, 0, 255)  # Otter is Blue

        white = (255, 255, 255)
        black = (0, 0, 0)
        colour = []
        pygame.display.update()
        for i in range(100):
            for j in range(100):
                if type(self.grid[i][j]) is Kelp:  # set kelp colour to green
                    colour.append(KELP_COLOR)
                elif type(self.grid[i][j]) is Urchin:  # set urchin colour to red
                    colour.append(URCHIN_COLOR)
                elif type(self.grid[i][j]) is Otter:  # set otter colour to blue
                    colour.append(OTTER_COLOR)
                else:
                    colour.append(white)  # set empty colour to white

        i = 0
        for y in range(100):
            for x in range(100):
                rect = pygame.Rect(x * 10, y * 10, 10, 10)
                pygame.draw.rect(screen, colour[i], rect)
                i += 1

        blockSize = 10  # Set the size of the grid block
        for x in range(0, 1000, blockSize):
            for y in range(0, 1000, blockSize):
                rect = pygame.Rect(x, y, blockSize, blockSize)
                pygame.draw.rect(screen, black, rect, 1)

class Animal:
    def __init__(self, grid_position, reprod_chance, reprod=None, old=None, has_Moved=False):
        self.age = 0  # sets age to 0 when born
        self.reproduction_age = reprod  # sets age of reproduction
        self.old = old  # sets age of death
        self.has_moved = has_Moved  # Sets the movement to False when initialized
        self.position_X = grid_position[0]
        self.position_Y = grid_position[1]
        self.reprod_chance = reprod_chance

    def is_dead(self) -> bool:  # checks if it reached old age or hasn't eaten in a long time
        if type(self) is Urchin and self.has_eaten>=5:
            return True
        return self.age >= self.old

    def death(self, CA):
        boo = False
        if self.is_dead():
            # add the new empty location to the array
            # update the location of the animal from the board to be empty board[x][y] = 0
            # update the number of animals nb_animal
            # for urchin: remove location from urchin array
            boo = True
            if type(self) is Urchin:
                CA.urchin_pos.remove([self.position_X, self.position_Y])
            CA.grid[self.position_X][self.position_Y] = [0]
            CA.empty.append([self.position_X, self.position_Y])
        else:
            pass
        return boo

    def can_reproduce(self) -> bool:  # checks if creature reached reproduction age
        return self.age >= self.reproduction_age

    def reproduce(self, CA):  # reproduction function
        pass

    def update_age(self):
        self.age += 1
        return self.age

class Kelp(Animal):
    def __init__(self, grid_position):
        super().__init__(grid_position, 100, 1, 3)  # sets reprod_prob=100,reprod_age=1, death_age=3

    def reproduce(self, CA):
        if not self.can_reproduce():
            return CA

        if self.reprod_chance >= random.randint(0, 100):
            if (len(CA.empty)) == 0:
                return CA
            else:
                temp = random.randint(0, len(CA.empty) - 1)
                new_X = CA.empty[temp][0]
                new_Y = CA.empty[temp][1]
                # add a new kelp on the random empty location
                CA.grid[new_X][new_Y] = Kelp([new_X, new_Y])
                # updating the number of kelps
                CA.nb_kelp += 1
                # deleting from the empty the location of the new kelp
                CA.empty.pop(temp)
                return CA

    def death(self, CA):
        if super().death(CA):
            CA.nb_kelp -= 1  # removing kelp from number of kelps
        # delete(self)
        return CA

class Urchin(Animal):
    def __init__(self, grid_position):
        super().__init__(grid_position, 6, 2, 19)  # sets reprod_prob=6%,reprod_age=2, death_age=19
        self.has_eaten =0 # tracks how long it has been since urchin ate

    # RETURNS THE GRID
    def move(self, CA):
        if self.has_moved:
            self.has_moved = False
            return CA

        availablePositionsToMove = self.can_move(CA)

        if len(availablePositionsToMove) == 0:
            self.has_moved = False
            return CA

        else:
            temp = random.randint(0, len(availablePositionsToMove) - 1)
            new_position_X = availablePositionsToMove[temp][0]
            new_position_Y = availablePositionsToMove[temp][1]
            # Removing the Urchin from it's previous location
            CA.grid[self.position_X][self.position_Y] = [0]
            # updating the empty array from the grid
            CA.empty.append([self.position_X, self.position_Y])
            CA.urchin_pos.remove([self.position_X, self.position_Y])
            if type(CA.grid[new_position_X][new_position_Y]) is Kelp:
                CA.nb_kelp -= 1
                self.has_eaten =0 # urchin ate kelp
            else:
                self.has_eaten +=1  # urchin didn't eat kelp
                CA.empty.remove([new_position_X, new_position_Y])

            CA.grid[new_position_X][new_position_Y] = self
            self.position_X = new_position_X
            self.position_Y = new_position_Y
            # adding to urchin array
            CA.urchin_pos.append([new_position_X, new_position_Y])
            self.has_moved = True
            return CA

    # RETURNS THE ARRAY OF AVAILABLE POSITIONS
    def can_move(self, CA):
        # checking bounds
        moveDistance = 2
        limit_x1 = 2
        limit_x2 = 2
        limit_y1 = 2
        limit_y2 = 2
        availablePositionsToMove = []

        # out of bounds upwards
        if self.position_X - moveDistance < 0:
            if self.position_X - 1 < 0:
                limit_x1 = 0
            else:
                limit_x1 = 1
        # out of bounds downwards
        if self.position_X + moveDistance > 99:
            if self.position_X + 1 > 99:
                limit_x2 = 0
            else:
                limit_x2 = 1
                # out of bounds to the left
        if self.position_Y - moveDistance < 0:
            if self.position_Y - 1 < 0:
                limit_y1 = 0
            else:
                limit_y1 = 1
        # out of bounds to the right
        if self.position_Y + moveDistance > 99:
            if self.position_Y + 1 > 99:
                limit_y2 = 0
            else:
                limit_y2 = 1

        # now checking if he can actually move - Aka is everything filled ?
        for i in range(self.position_X - limit_x1, self.position_X + limit_x2 + 1):
            for j in range(self.position_Y - limit_y1, self.position_Y + limit_y2 + 1):
                if CA.grid[i][j] == [0] or type(CA.grid[i][j]) is Kelp:
                    availablePositionsToMove.append([i, j])

        return availablePositionsToMove

    def reproduce(self, CA):
        if not self.can_reproduce():
            return CA
        if self.reprod_chance >= random.randint(0, 100):
            positions = self.can_move(CA)  # adds urchin to empty or kelp square
            if (len(positions)) == 0:
                return CA

            else:
                temp = random.randint(0, len(positions) - 1)
                new_X = positions[temp][0]
                new_Y = positions[temp][1]
                if type(CA.grid[new_X][new_Y]) is Kelp:
                    CA.nb_kelp-=1
                else:
                    CA.empty.remove([new_X, new_Y])  # deleting from the empty the location of the new urchin
                # add a new urchin on the random location
                CA.grid[new_X][new_Y] = Urchin([new_X, new_Y])
                # adding to urchin array
                CA.urchin_pos.append([new_X, new_Y])
                CA.nb_urchin += 1
                return CA

    def death(self, CA):
        if super().death(CA):
            CA.nb_urchin -= 1

        return CA

class Otter(Animal):
    def __init__(self, grid_position):
        super().__init__(grid_position, 20, 4, 20)  # sets reprod_prob=20,reprod_age=4, death_age=20
        self.carrying_capacity=10 # sets carrying capacity to 10
    def has_space(self, CA):  # used for reproduction
        # checking bounds

        moveDistance = 1
        limit_x1 = 1
        limit_x2 = 1
        limit_y1 = 1
        limit_y2 = 1

        availablePositionsToMove = []

        # out of bounds upwards
        if self.position_X - moveDistance < 0:
            limit_x1 = 0
        # out of bounds downwards
        if self.position_X + moveDistance > 99:
            limit_x2 = 0
        # out of bounds to the left
        if self.position_Y - moveDistance < 0:
            limit_y1 = 0
        # out of bounds to the right
        if self.position_Y + moveDistance > 99:
            limit_y2 = 0
        # now checking if he can actually move - Aka is everything filled ?
        for i in range(self.position_X - limit_x1, self.position_X + limit_x2 + 1):
            for j in range(self.position_Y - limit_y1, self.position_Y + limit_y2 + 1):
                if CA.grid[i][j] == [0] or type(CA.grid[i][j]) is Kelp or type(CA.grid[i][j]) is Urchin:
                    availablePositionsToMove.append([i, j])
        return availablePositionsToMove

    def move(self, CA):
        if self.has_moved:
            self.has_moved = False
            return CA

        if len(CA.urchin_pos) > 0:  # moves to random urchin location
            temp = random.randint(0, len(CA.urchin_pos) - 1)
            CA.grid[self.position_X][self.position_Y] = [0]  # sets grid to empty
            CA.empty.append([self.position_X, self.position_Y])  # updating empty array
            move_location = CA.urchin_pos[temp]  # chooses random location tuple in urchin pos
            CA.grid[move_location[0]][move_location[1]] = self  # sets new location to otter
            CA.urchin_pos.pop(temp)  # deletes value from urchin pos
            CA.nb_urchin -= 1
            self.position_X, self.position_Y = move_location[0], move_location[1]  # changes coord of otter
        else:  # else doesn't move
            pass

        self.has_moved = True
        return CA

    def reproduce(self, CA):
        if not self.can_reproduce():
            return CA
        if CA.nb_otter < 2 or CA.nb_otter >= self.carrying_capacity:
            return CA

        if self.reprod_chance >= random.randint(1, 100):
            if (len(CA.empty)) == 0:
                return CA

        else:
            positions = self.has_space(CA)  # reproduces within a square
            if len(positions) <= 0:
                return CA
            else:
                temp = random.randint(0, len(positions) - 1)
                new_location = positions[temp]
                if type(CA.grid[new_location[0]][new_location[1]]) is Kelp:
                    CA.nb_kelp -= 1
                elif type(CA.grid[new_location[0]][new_location[1]]) is Urchin:
                    CA.urchin_pos.remove([new_location[0], new_location[1]])   # removes urchin from urchin array
                    CA.nb_urchin-=1
                else:
                    CA.empty.remove([new_location[0], new_location[1]])  # delete from empty
                CA.grid[new_location[0]][new_location[1]] = Otter([new_location[0], new_location[1]])  #spawns new otter
                CA.nb_otter += 1
        return CA

    def death(self, CA):
        if super().death(CA):
            CA.nb_otter -= 1
        return CA

def main():
    myBoard = CA()
    i =0
    screen = myBoard.create_display()
    kel=[] # kelp array for plot
    urch=[] # urchin array for plot
    ott=[] # otter array for plot
    x=[]
    while i < 100: # set number of cycles
        myBoard.updating()
        myBoard.display(screen)
        kel.append(myBoard.nb_kelp)
        urch.append(myBoard.nb_urchin)
        ott.append(myBoard.nb_otter)
        x.append(i)

        time.sleep(0.01)
        i += 1

    # plots kelp vs urchin vs otter
    plt.plot(x,kel,label='Kelp')
    plt.plot(x,urch,label='Urchin')
    plt.plot(x,ott,label='Otter')
    plt.xlabel('time')
    plt.grid(True)
    plt.legend()
    plt.show()

main()

