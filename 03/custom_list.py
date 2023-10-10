class CustomList(list):
    def __add__(self, other):
        print("Выполняется метод __add__.")
        print("other: ", other)
        if isinstance(other, (CustomList, list)):
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
        else:
            return CustomList([element + other for element in self])

    def __radd__(self, other):
        print("Выполняется метод __radd__.")
        return self.__add__(other)

    def __iadd__(self, other):
        print("Выполняется метод __iadd__.")
        if isinstance(other, (CustomList, list)):
            length = max(len(self), len(other))
            self[:] = [
                self[i] + other[i]
                if i < len(self) and i < len(other)
                else self[i]
                if i < len(self)
                else other[i]
                for i in range(length)
            ]
        else:
            self[:] = [element + other for element in self]
        return self


if __name__ == "__main__":
    print(CustomList([5, 1, 3, 7]) + CustomList([1, 2, 7]))  # CustomList([6, 3, 10, 7])
    print(CustomList([1]) + [2, 5])  # CustomList([3, 5])
    print([2, 5] + CustomList([1]))  # CustomList([3, 5])
    print(CustomList([5, 1, 3, 7]) + 1)
