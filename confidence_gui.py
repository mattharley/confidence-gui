#!/usr/bin/env python

"""PySide port of the layouts/dynamiclayouts example from Qt v4.x"""

import logging
import socket
import sys
from time import sleep

import OSC
from PySide.QtCore import Qt, QSize
from PySide.QtGui import (QApplication, QDialog, QLayout, QGridLayout, QHBoxLayout,
                          QMessageBox, QPushButton, QGroupBox, QSpinBox, QSlider,
                          QProgressBar, QDial, QDialogButtonBox,
                          QComboBox, QLabel)

logger = logging.getLogger(__name__)

PREPARE = '/session/prepare'
START = '/session/playback/start'
PAUSE = '/session/playback/pause'
RESUME = '/session/playback/resume'
RESET = '/session/reset'
FINISH = '/session/finish'
BG = '/test/bg'

def setup_logging(loglevel = 1):
    logformat = "%(asctime)s: %(message)s"
    if loglevel:
        logging.basicConfig(level=logging.DEBUG,format=logformat)
    else:
        logging.basicConfig(level=logging.INFO,format=logformat)

REPETITIONS = 10

class OSCSender(object):
    def __init__(self):
        self.osc_client = OSC.OSCClient()
        self.osc_client.connect(('255.255.255.255', 8000))
        self.osc_client.socket.setsockopt(socket.SOL_SOCKET,socket.SO_BROADCAST,1)

    def send_lots(self, message):
        for i in range(REPETITIONS):
            self.osc_client.send(message)
            sleep(0.01)

    def prepare(self):
        self.send_lots(OSC.OSCMessage(address=PREPARE))

    def start(self):
        self.send_lots(OSC.OSCMessage(address=START))

    def pause(self):
        self.send_lots(OSC.OSCMessage(address=PAUSE))

    def resume(self):
        self.send_lots(OSC.OSCMessage(address=RESUME))

    def reset(self):
        self.send_lots(OSC.OSCMessage(address=RESET))

    def finish(self):
        self.send_lots(OSC.OSCMessage(address=FINISH))

    def bg(self):
        m = OSC.OSCMessage(address=BG)
        m.append("#C62818")
        self.osc_client.send(m)

class Dialog(QDialog):
    def __init__(self):
        super(Dialog, self).__init__()

        self.osc = OSCSender()

        self.createPreControlBox()
        self.createPlayControlBox()
        self.createButtonBox()

        mainLayout = QGridLayout()
        mainLayout.addWidget(self.preControlBox, 0, 0)
        mainLayout.addWidget(self.playControlBox, 1, 0)
        mainLayout.addWidget(self.buttonBox, 2, 0)
        mainLayout.setSizeConstraint(QLayout.SetMinimumSize)

        self.mainLayout = mainLayout
        self.setLayout(self.mainLayout)

        self.setWindowTitle("Confidence Man")

    def createButtonBox(self):
        self.buttonBox = QDialogButtonBox()

        closeButton = self.buttonBox.addButton(QDialogButtonBox.Close)
        helpButton = self.buttonBox.addButton(QDialogButtonBox.Help)
        closeButton.clicked.connect(self.close)
        helpButton.clicked.connect(self.show_help)

    def createPlayControlBox(self):
        self.playControlBox = QGroupBox("Player Controls")
        playControlLayout = QHBoxLayout()

        playButton = QPushButton("Play")
        playButton.clicked.connect(self.playClicked)
        playControlLayout.addWidget(playButton)

        pauseButton = QPushButton("Pause")
        pauseButton.clicked.connect(self.pauseClicked)
        playControlLayout.addWidget(pauseButton)

        resumeButton = QPushButton("Resume")
        resumeButton.clicked.connect(self.resumeClicked)
        playControlLayout.addWidget(resumeButton)

        self.playControlBox.setLayout(playControlLayout)

    def createPreControlBox(self):
        self.preControlBox = QGroupBox("Pre-Show Controls")
        preControlLayout = QHBoxLayout()

        resetButton = QPushButton("Reset")
        resetButton.clicked.connect(self.resetClicked)
        preControlLayout.addWidget(resetButton)

        # TODO - make togglePushButton.setCheckable(True)
        prepareButton = QPushButton("Prepare")
        prepareButton.clicked.connect(self.prepareClicked)
        preControlLayout.addWidget(prepareButton)

        bgButton = QPushButton("Background")
        bgButton.clicked.connect(self.bgClicked)
        preControlLayout.addWidget(bgButton)

        self.preControlBox.setLayout(preControlLayout)

    def playClicked(self):
        logger.debug("Play clicked")
        self.osc.start()

    def pauseClicked(self):
        logger.debug("Pause clicked")
        self.osc.pause()

    def resumeClicked(self):
        logger.debug("Resume clicked")
        self.osc.resume()

    def resetClicked(self):
        logger.debug("Reset clicked")
        self.osc.reset()

    def prepareClicked(self):
        logger.debug("Prepare clicked")
        self.osc.prepare()

    def bgClicked(self):
        logger.debug("Background clicked")
        self.osc.bg()

    def show_help(self):
        QMessageBox.information(self, "Confidence Man Help",
                            "Help yourself.")

if __name__ == '__main__':
    setup_logging()
    app = QApplication(sys.argv)
    dialog = Dialog()
    dialog.exec_()
