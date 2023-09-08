import json

class Node:
    def __init__(self, city: str, color: str = '') -> None:
        self.city: str = city
        self.color: str = color
        self.child: list = []

class CityGraph:
    def __init__(self) -> None:
        self.map = {}
        self.cities = {}

    def load_dataset(self, dataset_directory: str):
        self.map: dict = json.load(
            open(f'./dataset/{dataset_directory}/map.json'))
        self.city: dict = json.load(
            open(f'./dataset/{dataset_directory}/city.json'))
        
        self.cities = {city: Node(city) for city in self.city}

        self.create_adj_list()

    def create_adj_list(self):
        if len(self.map) < 1:
            return

        for data in self.map:
            self.cities[data['city1']].child.append(self.cities[data['city2']])
            self.cities[data['city2']].child.append(self.cities[data['city1']])

    def solve_map_coloring(self, colors: list = ['red', 'green', 'blue']):
        cities = list(self.cities.values())

        # define a function to check if a city has a conflicting color with its neighbors
        def has_conflict(city: Node):
            child_node: Node
            for child_node in city.child:
                if child_node.color == city.color:
                    return True
            return False

        # define a recursive function to try coloring the cities
        def color_cities(index: int):
            if index == len(cities):
                return True  # all cities have been colored

            city = cities[index]
            for color in colors:
                city.color = color
                if not has_conflict(city):
                    if color_cities(index + 1):
                        return True  # solution found
            city.color = ''  # backtrack
            return False  # no valid color found

        if color_cities(0):
            print("Solution found:")
            for city in sorted(cities, key=lambda x: x.city):
                print(f"{city.city}: {city.color}")
        else:
            print("No solution found.")


if __name__ == '__main__':
    graph = CityGraph()
    graph.load_dataset("australia")
    graph.solve_map_coloring()
    
