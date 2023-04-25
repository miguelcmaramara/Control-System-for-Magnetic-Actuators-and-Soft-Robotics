from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QPoint
from .gui.Window import Window
import multiprocessing as mp
# from multiprocessing import Process, Pipe, get_context
from .machinehandler.machinehandler import MachineHandler
import configparser
import os

"""
equivalent to: 
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    app.exec()
"""

def run(sysargs):
    # import configs
    config = configparser.ConfigParser()
    config_file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'config.ini'))
    config.read(config_file_path)
    config.sections()

    try:
        # FE/BE communiations
        mp.set_start_method('fork')
        parent_conn, child_conn = mp.Pipe()

        # create BackEnd
        mhandler = MachineHandler(config, child_conn)#, child_conn)
        be = mp.Process(target=mhandler.run)

        be.start()

        # create FrontEnd
        app = QApplication(sysargs)
        window = Window(parent_conn)
        screen_geometry = app.desktop().screenGeometry()

        # Initialize FrontEnd
        x = (screen_geometry.width()-window.width()) / 2
        y = (screen_geometry.height()-window.height()) / 2
        placement = QPoint(int(x),int(y))
        window.move(placement)
        window.show()
        # print(screen_geometry)

        app.exec()
    except KeyboardInterrupt:
        be.close()
        app.exit(0)
    be.close()
    app.exit(0)

