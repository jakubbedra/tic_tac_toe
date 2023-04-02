import sys

from PyQt5.QtWidgets import QApplication

from game_pyqt import TicTacToePyQT

if __name__ == '__main__':
    version = sys.argv[1]
    if version == 'pyqt':
        app = QApplication(sys.argv)
        ticTacToe = TicTacToePyQT()
        ticTacToe.show()
        sys.exit(app.exec_())
    elif version == 'gtk':
        app = Gtk.Application()
        ticTacToe = TicTacToeGTK()
        ticTacToe.show()
        app.run(sys.argv)
    else:
        print('Nieznana wersja podana jako parametr startowy: ' + version)
