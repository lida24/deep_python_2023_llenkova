import unittest
#from descriptors import ChessMove
from descriptors import Color, Piece, Coordinates


class ChessMove:
    color = Color('color')
    piece = Piece('piece')
    coord = Coordinates('coord')

    def __init__(self, color='white', piece='Pawn', coord='c3'):
        self.color = color
        self.piece = piece
        self.coord = coord


class TestDescriptors(unittest.TestCase):
    def setUp(self) -> None:
        pass
        #self.move = ChessMove()
        #self.move_1 = ChessMove('white', 'Knight', 'c3')
        #self.move_2 = ChessMove('black', 'Pawn', 'f5')

    def tearDown(self) -> None:
        pass

    def test_init(self) -> None:
        move = ChessMove()
        self.assertEqual(move.color, 'white')
        self.assertEqual(move.piece, 'Knight')
        self.assertEqual(move.coord, 'c3')

        # self.assertEqual(self.move_2.color, 'black')
        # self.assertEqual(self.move_2.piece, 'Pawn')
        # self.assertEqual(self.move_2.coord, 'f5')

    # def test_validate_data(self) -> None:
    #     with self.assertRaises(ValueError) as err:
    #         ChessMove('pink', 'Queen', 'e5')
    #     self.assertEqual('Incorrect color, can only be white or black', str(err.exception))
    #     self.assertEqual(ValueError, type(err.exception))

