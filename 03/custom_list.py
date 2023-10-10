class CustomList(list):
    def __add__(self, other):
        length = max(len(self), len(other))
        return CustomList(
            [
                self[i] + other[i]
                if i < len(self) and i < len(other)
                else self[i]
                if i < len(self)
                else other[i]
                for i in range(length)
            ]
        )

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        length = max(len(self), len(other))
        return CustomList(
            [
                self[i] - other[i]
                if i < len(self) and i < len(other)
                else self[i]
                if i < len(self)
                else -other[i]
                for i in range(length)
            ]
        )

    def __rsub__(self, other):
        length = max(len(self), len(other))
        return CustomList(
            [
                other[i] - self[i]
                if i < len(self) and i < len(other)
                else -self[i]
                if i < len(self)
                else other[i]
                for i in range(length)
            ]
        )

    def __eq__(self, other):
        return sum(self) == sum(other)

    def __ne__(self, other):
        return sum(self) != sum(other)

    def __gt__(self, other):
        return sum(self) > sum(other)

    def __ge__(self, other):
        return sum(self) >= sum(other)

    def __lt__(self, other):
        return sum(self) < sum(other)

    def __le__(self, other):
        return sum(self) <= sum(other)

    def __str__(self):
        return f"Элементы списка: {list(self)}, их сумма: {sum(self)}"
