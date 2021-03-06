import sys

from PyQt5.QtWidgets import QApplication, QStyleFactory

from mindpong.view.MainMenu import MainMenu
from mindpong.model.game import Game
from mindpong.model.serial_communication import SerialCommunication
from mindpong.delegate.delegate import Delegate
from mindpong.utils import create_palette


def main():
    app = QApplication(sys.argv)
    QApplication.setPalette(create_palette())
    app.setStyle(QStyleFactory.create('Fusion'))

    # delegate
    delegate = Delegate()

    # view
    menu = MainMenu()

    # model
    serial_communication = SerialCommunication()
    game = Game([
        lambda data: print('I am updating my data', data),
        serial_communication.send_data,
        menu.playTab.update_signal_event.emit,
    ])

    # bind view to model with delegate
    delegate.set_model(game, serial_communication)
    menu.set_delegate(delegate)
    
    menu.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
