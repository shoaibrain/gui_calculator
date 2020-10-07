import sys

# Import for Graphical User Interface
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QMainWindow

from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QVBoxLayout

# Imports for Controller
from functools import partial


# An error message
ERROR = "ERROR"

# Subclass of main window for calculator for Graphical User Interface


class PyCalcUi(QMainWindow):
    """
    Calculator View
    """

    def __init__(self):
        """
        Initialize the view
        """
        super().__init__()
        # Set some main window's properties
        self.setWindowTitle('Calculator')
        self.setFixedSize(400, 470)
        # Set the central widget
        self.generalLayout = QVBoxLayout()
        self._centralWidget = QWidget(self)
        self.setCentralWidget(self._centralWidget)
        self._centralWidget.setLayout(self.generalLayout)

        # Creates Display buttons
        self._createDisplay()
        self._createButtons()

    """
    Creates the display
    """

    def _createDisplay(self):
        # Creates display widget
        self.display = QLineEdit()
        # Sets display properties
        self.display.setFixedHeight(35)
        self.display.setAlignment(Qt.AlignRight)
        self.display.setReadOnly(True)
        # Adds display to general widget
        self.generalLayout.addWidget(self.display)

    def _createButtons(self):
        """
        Creates UI buttons
        """
        self.buttons = {}
        buttonsLayout = QGridLayout()
        # Dictionary keys --> buttons
        # Dictionary values --> position of buttons

        buttons = {'7': (0, 0),
                   '8': (0, 1),
                   '9': (0, 2),
                   '/': (0, 3),
                   'C': (0, 4),
                   '4': (1, 0),
                   '5': (1, 1),
                   '6': (1, 2),
                   '*': (1, 3),
                   '(': (1, 4),
                   '1': (2, 0),
                   '2': (2, 1),
                   '3': (2, 2),
                   '-': (2, 3),
                   ')': (2, 4),
                   '0': (3, 0),
                   '00': (3, 1),
                   '.': (3, 2),
                   '+': (3, 3),
                   '=': (3, 4),
                   }
        # Adds buttons to the grid layout of calculator
        for btnText, pos in buttons.items():
            self.buttons[btnText] = QPushButton(btnText)
            self.buttons[btnText].setFixedSize(60, 60)
            buttonsLayout.addWidget(self.buttons[btnText], pos[0], pos[1])

        # Adds buttonsLayout to the main layout of calculator
        self.generalLayout.addLayout(buttonsLayout)

    def setDisplayText(self, text):
        """
        Set display's text.
        """
        self.display.setText(text)
        self.display.setFocus()

    def displayText(self):
        """
        Get display's text.
        """
        return self.display.text()

    def clearDisplay(self):
        """
        Clear the display.
        """
        self.setDisplayText('')

# Create a Model to handle the calculator's operation


def evaluateExpression(expression):
    """
    Evaluate an expression.
    """
    try:
        result = str(eval(expression, {}, {}))
    except Exception:
        result = ERROR

    return result


# Class Controller to connect gui and model
class Controller:
    """
    A controller Class
    """

    def __init__(self, model, view):
        """
        Initializer
        """
        self._evaluate = model
        self._view = view
        self._connectSignals()

    def _calculateResult(self):
        """
        Evaluate expressions.
        """
        result = self._evaluate(expression=self._view.displayText())
        self._view.setDisplayText(result)

    def _buildExpression(self, sub_exp):
        """
        A method to build expression.
        """
        if self._view.displayText() == ERROR:
            self._view.clearDisplay()

        expression = self._view.displayText() + sub_exp
        self._view.setDisplayText(expression)

    def _connectSignals(self):
        """
        A method to connect signals and slots
        """
        for btnText, btn in self._view.buttons.items():
            if btnText not in {'=', 'C'}:
                btn.clicked.connect(partial(self._buildExpression, btnText))

        self._view.buttons['='].clicked.connect(self._calculateResult)
        self._view.display.returnPressed.connect(self._calculateResult)
        self._view.buttons['C'].clicked.connect(self._view.clearDisplay)


def main():
    """Main function."""
    # An instance of calculator application
    pycalc = QApplication(sys.argv)
    # Displays the User Interface
    view = PyCalcUi()
    view.show()

    model = evaluateExpression
    Controller(model=model, view=view)
    # Runs the calcultor's main loop
    sys.exit(pycalc.exec_())


if __name__ == '__main__':
    main()
