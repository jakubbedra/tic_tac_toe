import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QPushButton, QVBoxLayout, QAction, QMenuBar, \
    QMessageBox, QLabel

from board import Board


class TicTacToe(QWidget):
    def __init__(self):
        super().__init__()
        self.board = Board()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Kółko i krzyżyk')
        self.setFixedSize(400, 600)

        # Create a grid layout
        grid_layout = QGridLayout()
        grid_layout.setSpacing(20)

        # Create the buttons for the board
        self.buttons = []
        for i in range(self.board.size):
            row = []
            for j in range(self.board.size):
                button = QPushButton(' ', self)
                button.setFixedSize(100, 100)
                button.clicked.connect(lambda _, i=i, j=j: self.make_move(i, j))
                font = QFont()
                font.setPointSize(32)
                button.setFont(font)
                row.append(button)
                grid_layout.addWidget(button, i, j)
            self.buttons.append(row)

        # Create the restart button
        restart_button = QPushButton('Resetuj', self)
        restart_button.clicked.connect(lambda _: self.reset_board())
        restart_button.setFixedSize(370, 40)

        # Create a label for the player turn
        self.player_label = QLabel('Ruch gracza: ' + self.board.current_player, self)
        self.player_label.setMargin(0)
        font = QFont()
        font.setPointSize(32)
        self.player_label.setFont(font)
        self.player_label.setAlignment(Qt.AlignCenter)

        # Create a vertical layout to contain the grid layout and the restart button
        layout = QVBoxLayout()
        layout.setMenuBar(self.create_menu_bar())
        layout.addWidget(self.player_label)
        layout.addLayout(grid_layout)
        layout.addWidget(restart_button)
        self.setLayout(layout)

    def create_menu_bar(self):
        menu_bar = QMenuBar(self)
        help_menu = menu_bar.addMenu('Pomoc')
        about_action = QAction('o grze', self)
        about_action.triggered.connect(self.show_about_window)
        help_menu.addAction(about_action)
        return menu_bar

    def show_about_window(self):
        about = QMessageBox()
        about.setWindowTitle("O grze")
        about.setText(
            "Kółko i krzyżyk to gra, w której dwóch graczy stara się ułożyć swoje symbole (krzyżyki lub kółka) w jednej linii - poziomej, pionowej lub skośnej - na planszy o wymiarach 3x3.")
        about.exec_()

    def make_move(self, y, x):
        player = self.board.current_player
        if self.board.make_move(x, y):
            self.buttons[y][x].setText(player)
            self.buttons[y][x].setEnabled(False)
        if self.board.state == 'DRAW':
            font = QFont()
            font.setPointSize(16)
            self.player_label.setFont(font)
            self.player_label.setText("Koniec gry: remis! ")
            self.block_all_grids()
        elif self.board.state == 'END':
            font = QFont()
            font.setPointSize(16)
            self.player_label.setFont(font)
            self.player_label.setText("Koniec gry: gracz "+self.board.current_player+" wygrał!")
            self.block_all_grids()
        else:
            self.player_label.setText("Ruch gracza: " + self.board.current_player)

    def block_all_grids(self):
        for row in self.buttons:
            for button in row:
                button.setEnabled(False)

    def reset_board(self):
        for row in self.buttons:
            for button in row:
                button.setText('')
                button.setEnabled(True)
        self.board = Board()
        font = QFont()
        font.setPointSize(32)
        self.player_label.setFont(font)
        self.player_label.setText("Ruch gracza: " + self.board.current_player)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ticTacToe = TicTacToe()
    ticTacToe.show()
    sys.exit(app.exec_())
