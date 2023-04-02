import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from board import Board


class TicTacToeGtk(Gtk.Window):
    def __init__(self):
        super().__init__(title='Kółko i krzyżyk')
        self.set_default_size(400, 600)

        self.board = Board()

        # Create the grid layout
        grid_layout = Gtk.Grid(column_spacing=20, row_spacing=20)
        self.add(grid_layout)

        # Create the buttons for the board
        self.buttons = []
        for i in range(self.board.size):
            row = []
            for j in range(self.board.size):
                button = Gtk.Button(label=' ')
                button.set_size_request(110, 110)
                button.connect('clicked', self.make_move, i, j)
                font = button.get_style_context().get_font(Gtk.StateFlags.NORMAL)
                font.set_property('size', 32)
                button.get_style_context().set_font(font)
                row.append(button)
                grid_layout.attach(button, j, i, 1, 1)
            self.buttons.append(row)

        # Create the restart button
        restart_button = Gtk.Button(label='Resetuj')
        restart_button.connect('clicked', self.reset_board)
        restart_button.set_size_request(370, 40)

        # Create a label for the player turn
        self.player_label = Gtk.Label(label='Ruch gracza: ' + self.board.current_player)
        self.player_label.set_margin_top(10)
        self.player_label.set_margin_bottom(10)
        font = self.player_label.get_style_context().get_font(Gtk.StateFlags.NORMAL)
        font.set_property('size', 26)
        self.player_label.get_style_context().set_font(font)
        self.player_label.set_halign(Gtk.Align.CENTER)

        # Create a box to contain the restart button and the player label
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        box.pack_start(self.player_label, False, False, 0)
        box.pack_start(restart_button, False, False, 0)
        grid_layout.attach(box, 0, 3, self.board.size, 1, Gtk.AttachOptions.FILL, Gtk.AttachOptions.FILL, 0, 0)

        # Create the menu bar
        menu_bar = Gtk.MenuBar()
        help_menu = Gtk.Menu()
        about_action = Gtk.MenuItem(label='o grze')
        about_action.connect('activate', self.show_about_window)
        help_menu.append(about_action)
        help_menu_item = Gtk.MenuItem(label='Pomoc')
        help_menu_item.set_submenu(help_menu)
        menu_bar.append(help_menu_item)
        grid_layout.attach(menu_bar, 0, 0, self.board.size, 1)

    def show_about_window(self, widget):
        dialog = Gtk.MessageDialog(parent=self, flags=0, message_type=Gtk.MessageType.INFO, buttons=Gtk.ButtonsType.OK,
                                   text="O grze")
        dialog.format_secondary_text(
            "Kółko i krzyżyk to gra, w której dwóch graczy stara się ułożyć swoje symbole (krzyżyki lub kółka) w jednej linii - poziomej, pionowej lub skośnej - na planszy o wymiarach 3x3.")
        dialog.run()
        dialog.destroy()

    def make_move(self, y, x):
        player = self.board.current_player
        if self.board.make_move(x, y):
            button = self.buttons[y][x]
            button.set_label(player)
            button.set_sensitive(False)
        if self.board.state == 'DRAW':
            font = Pango.FontDescription('sans-serif 16')
            self.player_label.modify_font(font)
            self.player_label.set_text("Koniec gry: remis!")
            self.block_all_grids()
        elif self.board.state == 'END':
            self.color_grids()
            font = Pango.FontDescription('sans-serif 14')
            self.player_label.modify_font(font)
            self.player_label.set_text("Koniec gry: gracz " + self.board.current_player + " wygrał!")
            self.block_all_grids()
        else:
            self.player_label.set_text("Ruch gracza: " + self.board.current_player)

    def color_grids(self):
        for grid in self.board.winning_grids:
            button = self.buttons[grid[0]][grid[1]]
            button.override_background_color(Gtk.StateType.NORMAL, Gdk.RGBA(1, 1, 1, 1))

    def block_all_grids(self):
        for row in self.buttons:
            for button in row:
                button.set_sensitive(False)

    def reset_board(self):
        for row in self.buttons:
            for button in row:
                button.set_label('')
                button.override_background_color(Gtk.StateType.NORMAL, Gdk.RGBA(0, 0, 0, 0))
                font_desc = Pango.FontDescription.from_string("Sans 26")
                button.modify_font(font_desc)
                button.set_sensitive(True)
                button.show()
        self.board = Board()
        font_desc = Pango.FontDescription.from_string("Sans 26")
        self.player_label.modify_font(font_desc)
        self.player_label.set_text("Ruch gracza: " + self.board.current_player)
