class Car:
    def __init__(self, brand, model, year):
        self.brand = brand
        self.model = model
        self.year = year

    def __str__(self):
        return f"{self.brand} {self.model} ({self.year})"


class CarNode:
    def __init__(self, car):
        self.car = car
        self.left = None
        self.right = None


class CarPark:
    def __init__(self):
        self.root = None
        self.count = 0

    def add(self, car):
        if not self.root:
            self.root = CarNode(car)
        else:
            self._add(self.root, car)
        self.count += 1

    def _add(self, node, car):
        if car.model < node.car.model:
            if node.left is None:
                node.left = CarNode(car)
            else:
                self._add(node.left, car)
        elif car.model > node.car.model:
            if node.right is None:
                node.right = CarNode(car)
            else:
                self._add(node.right, car)
        else:
            node.car = car

    def search(self, model):
        return self._search(self.root, model)

    def _search(self, node, model):
        if node is None:
            return None
        if model == node.car.model:
            return node.car
        elif model < node.car.model:
            return self._search(node.left, model)
        else:
            return self._search(node.right, model)

    def remove(self, model):
        self.root, deleted = self._remove(self.root, model)
        if deleted:
            self.count -= 1
        return deleted

    def _remove(self, node, model):
        if node is None:
            return node, False
        deleted = False
        if model == node.car.model:
            deleted = True
            if node.left is None and node.right is None:
                return None, True
            elif node.left is None:
                return node.right, True
            elif node.right is None:
                return node.left, True
            else:
                min_larger_node = self._find_min(node.right)
                node.car = min_larger_node.car
                node.right, _ = self._remove(node.right, min_larger_node.car.model)
        elif model < node.car.model:
            node.left, deleted = self._remove(node.left, model)
        else:
            node.right, deleted = self._remove(node.right, model)
        return node, deleted

    def _find_min(self, node):
        while node.left:
            node = node.left
        return node

    def __len__(self):
        return self.count

    def sell_car(self, client, model):
        car = self.search(model)
        if car:
            self.remove(model)
            print(f"Клієнт {client} купив {car}")
            return car
        else:
            print(f"Авто {model} не знайдено для клієнта {client}")
            return None


if __name__ == "__main__":
    park = CarPark()
    park.add(Car("Toyota", "Camry", 2020))
    park.add(Car("BMW", "X5", 2018))
    park.add(Car("Audi", "A6", 2019))

    print("Всього авто в парку:", len(park))

    found = park.search("X5")
    print("Знайдено:", found)

    park.sell_car("Іван", "X5")
    print("Всього авто після продажу:", len(park))
