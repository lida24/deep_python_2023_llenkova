class Color:
    def __init__(self, name):
        print("Color.init")
        self.name = name

    def __get__(self, obj, objtype):
        print("Color.get", obj, objtype)
        return getattr(obj, self.name)

    def __set__(self, obj, val):
        if val not in ['white', 'black']:
            raise ValueError('Incorrect color, can only be white or black')
        setattr(obj, self.name, val)


class Piece:
    def __init__(self, name):
        print("Piece.init")
        self.name = name

    def __get__(self, obj, objtype):
        print("Piece.get", obj, objtype)
        return getattr(obj, self.name)

    def __set__(self, obj, val):
        if val not in ['Pawn', 'Knight', 'Bishop', 'Rook', 'Queen', 'King']:
            raise ValueError('There is no such piece in chess')
        setattr(obj, self.name, val)


class Coordinates:
    def __init__(self, name):
        print("Coordinates.init")
        self.name = name

    def __get__(self, obj, objtype):
        print("Coordinates.get", obj, objtype)
        return getattr(obj, self.name)

    def __set__(self, obj, val):
        letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
        digits = ['1', '2', '3', '4', '5', '6', '7', '8']
        if not (len(val) == 2 and val[0] in letters and val[1] in digits):
            raise ValueError('Chess board coordinates must consist of a letter (a-h) followed by a number (1-8)')
        setattr(obj, self.name, val)
