import pathlib
import random
import json

from typing import List, Optional, Tuple


Cell = Tuple[int, int]
Cells = List[int]
Grid = List[Cells]


class GameOfLife:
    
    def __init__(
        self,
        size: Tuple[int, int],
        randomize: bool=True,
        max_generations: Optional[float]=float('inf')
    ) -> None:
        # Размер клеточного поля
        self.rows, self.cols = size
        # Предыдущее поколение клеток
        self.prev_generation = self.create_grid()
        # Текущее поколение клеток
        self.curr_generation = self.create_grid(randomize=randomize)
        # Максимальное число поколений
        self.max_generations = max_generations
        # Текущее число поколений
        self.generations = 1

    def create_grid(self, randomize: bool=False) -> Grid:
        grid = []

        for i in range(self.rows):
            row = []
            
            for j in range(self.cols):
                if randomize:
                    cell = random.randint(0,1)
                else:
                    cell = 0

                row.append(cell)
            grid.append(row)
    
        return grid

    def get_neighbours(self, cell: Cell) -> Cells:
        arr = []

        for i in range(cell[0]-1, cell[0]+2):
            for j in range(cell[1]-1, cell[1]+2):
                if not 0 <= i < self.rows:
                    continue
                if not 0 <= j < self.cols:
                    continue
                if i == cell[0] and j == cell[1]:
                    continue
                arr.append(self.curr_generation[i][j])
        return arr

    def get_next_generation(self) -> Grid:
        new_grid = self.create_grid()

        for i in range(len(new_grid)):
            for j in range(len(new_grid[i])):
                neighbours_count = sum(self.get_neighbours((i, j)))

                if self.curr_generation[i][j] == 0:
                    new_grid[i][j] = neighbours_count == 3
                else:
                    if neighbours_count < 2 or neighbours_count > 3:
                        new_grid[i][j] = 0
                    else:
                        new_grid[i][j] = 1

        return new_grid

    def step(self) -> None:
        """
        Выполнить один шаг игры.
        """
        self.prev_generation = self.curr_generation
        self.curr_generation = self.get_next_generation()
        self.generations += 1

    @property
    def is_max_generations_exceeded(self) -> bool:
        """
        Не превысило ли текущее число поколений максимально допустимое.
        """
        return self.generations >= self.max_generations

    @property
    def is_changing(self) -> bool:
        """
        Изменилось ли состояние клеток с предыдущего шага.
        """
        return self.prev_generation != self.curr_generation

    @staticmethod
    def from_file(filename: pathlib.Path) -> 'GameOfLife':
        """
        Прочитать состояние клеток из указанного файла.
        """
        with open(filename, 'r') as file:
            obj = json.load(file)
        
        game = GameOfLife(
            size=(obj["rows"], obj["cols"]),
            randomize=False,
            max_generations=obj["max_generations"]
        )

        game.prev_generation = obj["prev_generation"]
        game.curr_generation = obj["curr_generation"]
        game.generations = obj["generations"]

        return game

    def save(self, filename: pathlib.Path) -> None:
        """
        Сохранить текущее состояние клеток в указанный файл.
        """
        obj = {
            'rows': self.rows,
            'cols': self.cols,
            'prev_generation': self.prev_generation,
            'curr_generation': self.curr_generation,
            'max_generations': self.max_generations,
            'generations': self.generations
        }

        with open(filename, 'w') as file:
            json.dump(obj, file)