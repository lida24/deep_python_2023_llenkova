import unittest
from descriptors import ChessMove


class TestDescriptors(unittest.TestCase):
    def setUp(self) -> None:
        self.move_1 = ChessMove("white", "Knight", "c3")
        self.move_2 = ChessMove("black", "Pawn", "f5")

    def tearDown(self) -> None:
        pass

    def test_valid_data(self) -> None:
        self.assertEqual(self.move_1.color, "white")
        self.assertEqual(self.move_1.piece, "Knight")
        self.assertEqual(self.move_1.coord, "c3")

        self.assertEqual(self.move_2.color, "black")
        self.assertEqual(self.move_2.piece, "Pawn")
        self.assertEqual(self.move_2.coord, "f5")

    def test_invalid_data(self) -> None:
        with self.assertRaises(ValueError) as err:
            ChessMove("pink", "Queen", "e5")
        self.assertEqual(
            "Incorrect color, can only be white or black", str(err.exception)
        )
        self.assertEqual(ValueError, type(err.exception))

        with self.assertRaises(ValueError) as err:
            ChessMove("black", "Han", "c4")
        self.assertEqual("There is no such piece in chess", str(err.exception))
        self.assertEqual(ValueError, type(err.exception))

        with self.assertRaises(ValueError) as err:
            ChessMove("black", "Bishop", "E12")
        self.assertEqual(
            "Chess board coordinates must consist of a letter (a-h) followed by a number (1-8)",
            str(err.exception),
        )
        self.assertEqual(ValueError, type(err.exception))

    def test_change_attribute_with_valid_data(self) -> None:
        self.move_1.color = "black"
        self.assertEqual(self.move_1.color, "black")

        self.move_2.piece = "Rook"
        self.assertEqual(self.move_2.piece, "Rook")

        self.move_1.coord = "h7"
        self.assertEqual(self.move_1.coord, "h7")

    def test_change_attribute_with_invalid_data(self) -> None:
        with self.assertRaises(ValueError) as err:
            self.move_2.color = "green"
        self.assertEqual(
            "Incorrect color, can only be white or black", str(err.exception)
        )
        self.assertEqual(ValueError, type(err.exception))

        with self.assertRaises(ValueError) as err:
            self.move_2.piece = "Chicken"
        self.assertEqual("There is no such piece in chess", str(err.exception))
        self.assertEqual(ValueError, type(err.exception))

        with self.assertRaises(ValueError) as err:
            self.move_1.coord = "i15"
        self.assertEqual(
            "Chess board coordinates must consist of a letter (a-h) followed by a number (1-8)",
            str(err.exception),
        )
        self.assertEqual(ValueError, type(err.exception))
