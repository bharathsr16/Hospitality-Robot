import sys
from PyQt5.QtWidgets import QApplication
from hospitality_robot.gui import RobotGui

def main():
    """
    Main function for the hospitality robot.
    """
    app = QApplication(sys.argv)
    gui = RobotGui()
    gui.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
