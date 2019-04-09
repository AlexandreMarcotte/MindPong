import os

from PyQt5.QtGui import (QFont, QPixmap)
from PyQt5.QtWidgets import (
    QTabWidget, QGridLayout, QLabel, 
    QPushButton, QDialog, QMessageBox
)
from PyQt5.QtCore import Qt
import emoji
from serial import SerialException


from mindpong.utils import get_project_root
from mindpong.view.utils import BACKGROUND_COLORS, IMAGES_PATH, MINDPONG_TITLE
from mindpong.model.game import GameState

ARROW_FILE_NAME = 'arrow.png'
PINGPONG_FILE_NAME = 'ball.png'

class PlayTab(QTabWidget):

    START_GAME_STRING = "▶️ Start"
    STOP_GAME_STRING = "⏹️ Stop"

    ARROW_SCALE = (1, 1)
    BALL_SCALE = (1/3, 1/3)

    def __init__(self):
        super().__init__()
        self.arrowPath = os.path.sep.join([get_project_root(), IMAGES_PATH, ARROW_FILE_NAME])
        self.ballPath = os.path.sep.join([get_project_root(), IMAGES_PATH, PINGPONG_FILE_NAME])

        self.centralGridLayout: QGridLayout
        self.playButton = QPushButton(emoji.emojize(PlayTab.START_GAME_STRING))
        self.countDownModal = QDialog(self)
        self.gameState = 0
        self.init_ui()

    def init_ui(self):
        self.set_labels_layout()
        self.init_buttons()
        self.init_error_message_box()

    def set_labels_layout(self):
        self.centralGridLayout = QGridLayout()
        self.setLayout(self.centralGridLayout)
        self.set_players_labels()
        self.arrow_label = self.set_picture_label(self.arrowPath, ((0, 3, 1, 1)), self.ARROW_SCALE)
        self.ball_label = self.set_picture_label(self.ballPath, (0, 2, 1, 1), self.BALL_SCALE)
        self.centralGridLayout.addWidget(QLabel("Math Question: "), 1, 0, 1, 2)
        self.centralGridLayout.addWidget(self.playButton, 2, 1, 1, 3)

    def set_players_labels(self):
        players = [QLabel("Player one"), QLabel("Player two")]
        for player in players:
            player.setFont(QFont("Times", 16, QFont.Bold))
            player.setMargin(30)
            player.setAlignment(Qt.AlignCenter)
        self.centralGridLayout.addWidget(players[0], 0, 0)
        self.centralGridLayout.addWidget(players[1], 0, 6)

    def set_picture_label(self, path, positions, scale):
        label = QLabel()
        label.setAlignment(Qt.AlignCenter)
        pixmap = QPixmap(path)
        
        label.setPixmap(pixmap.scaled(pixmap.width() * scale[0], pixmap.height() * scale[1], Qt.KeepAspectRatio))
        label.setFixedWidth(pixmap.width() * scale[0])
        self.centralGridLayout.addWidget(label, positions[0], positions[1], positions[2], positions[3])
        return label

    def init_buttons(self):
        self.playButton.setStyleSheet(BACKGROUND_COLORS['GREEN'])
        self.playButton.clicked.connect(self.click_start_button_callback)

    def init_error_message_box(self):
        self.errorBox: QMessageBox = QMessageBox()
        self.errorBox.setIcon(QMessageBox.Warning)
        self.errorBox.setWindowTitle(MINDPONG_TITLE)

    def set_delegate(self, delegate):
        self.delegate = delegate

    def click_start_button_callback(self):
        if self.delegate and self.delegate.game.state == GameState.INITIAL:
            self.start_game()

        elif self.delegate and self.delegate.game.state == GameState.IN_PLAY:
            self.delegate.end_game()
            self.playButton.setText(PlayTab.START_GAME_STRING)
            self.playButton.setStyleSheet(BACKGROUND_COLORS['GREEN'])

        else:
            print("error in game state \n")

    def resizeEvent(self, event):
        # TODO: adjust labels to fit the screen correctly
        # https://www.riverbankcomputing.com/static/Docs/PyQt4/qresizeevent.html
        return super(PlayTab, self).resizeEvent(event)

    def start_game(self):
        try:
            self.delegate.start_game()
        except SerialException as e:
            self.errorBox.setText("Error: can't connect to serial %s port" % (self.delegate.serial_communication.port))
            self.errorBox.show()
            return

        self.playButton.setText(PlayTab.STOP_GAME_STRING)
        self.playButton.setStyleSheet(BACKGROUND_COLORS["RED"])
