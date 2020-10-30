import pygame
import random

from pygame.locals import *
from typing import List, Tuple


Cell = Tuple[int, int]
Cells = List[int]
Grid = List[Cells]


class GameOfLife:

    def __init__(self, width: int=640, height: int=480, cell_size: int=10, speed: int=10, randomize_grid=False) -> None:
        self.width = width
        self.height = height
        self.cell_size = cell_size

        self.cell_width = self.width // self.cell_size
        self.cell_height = self.height // self.cell_size

        # Устанавливаем размер окна
        self.screen_size = width, height
        # Создание нового окна
        self.screen = pygame.display.set_mode(self.screen_size)

        # Вычисляем количество ячеек по вертикали и горизонтали

        # Скорость протекания игры
        self.speed = speed

    def draw_lines(self) -> None:
        """ Отрисовать сетку """
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                    (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                    (0, y), (self.width, y))

    def run(self) -> None:
        """ Запустить игру """
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption('Game of Life')
        self.screen.fill(pygame.Color('white'))

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
            
            self.screen.fill(pygame.Color('white'))
            self.draw_lines()
            self.draw_grid()
            self.grid = self.get_next_generation()

            pygame.display.flip()
            clock.tick(self.speed)

        pygame.quit()

    def create_grid(self, randomize: bool=False) -> Grid:
        """
        Создание списка клеток.

        Клетка считается живой, если ее значение равно 1, в противном случае клетка
        считается мертвой, то есть, ее значение равно 0.

        Parameters
        ----------
        randomize : bool
            Если значение истина, то создается матрица, где каждая клетка может
            быть равновероятно живой или мертвой, иначе все клетки создаются мертвыми.

        Returns
        ----------
        out : Grid
            Матрица клеток размером `cell_height` х `cell_width`.
        """
        grid = []

        for i in range(self.cell_height):
            row = []
            
            for j in range(self.cell_width):
                if randomize:
                    cell = random.randint(0,1)
                else:
                    cell = 0

                row.append(cell)
            grid.append(row)
    
        return grid
    
    def draw_grid(self) -> None:
        """
        Отрисовка списка клеток с закрашиванием их в соответствующе цвета.
        """
        for i in range(self.cell_height):
            for j in range(self.cell_width):
                if self.grid[i][j] == 0:
                    continue

                x = j * self.cell_size
                y = i * self.cell_size
                
                circle = (x - self.cell_size // 2, y - self.cell_size // 2)
                pygame.draw.circle(self.screen, pygame.Color('black'), circle, self.cell_size // 2)

    def get_neighbours(self, cell: Cell) -> Cells:
        """
        Вернуть список соседних клеток для клетки `cell`.

        Соседними считаются клетки по горизонтали, вертикали и диагоналям,
        то есть, во всех направлениях.

        Parameters
        ----------
        cell : Cell
            Клетка, для которой необходимо получить список соседей. Клетка
            представлена кортежем, содержащим ее координаты на игровом поле.

        Returns
        ----------
        out : Cells
            Список соседних клеток.
        """

        arr = []

        for i in range(cell[0]-1, cell[0]+2):
            for j in range(cell[1]-1, cell[1]+2):
                if not 0 <= i < self.cell_height:
                    continue
                if not 0 <= j < self.cell_width:
                    continue
                if i == cell[0] and j == cell[1]:
                    continue
                arr.append(self.grid[i][j])
        return arr

    def get_next_generation(self) -> Grid:
        """
        Получить следующее поколение клеток.

        Returns
        ----------
        out : Grid
            Новое поколение клеток.
        """

        new_grid = self.create_grid()

        for i in range(len(new_grid)):
            for j in range(len(new_grid[i])):
                neighbours_count = sum(self.get_neighbours((i, j)))

                if self.grid[i][j] == 0:
                    new_grid[i][j] = neighbours_count == 3
                else:
                    if neighbours_count < 2 or neighbours_count > 3:
                        new_grid[i][j] = 0
                    else:
                        new_grid[i][j] = 1

        return new_grid

if __name__ == "__main__":
    game = GameOfLife(randomize_grid=True)
    game.grid = game.create_grid(randomize=True)
    game.run()