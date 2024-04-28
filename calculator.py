import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QGridLayout, QPushButton, QLineEdit, QLabel, QShortcut
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QKeySequence

class Calculator(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()
        self.memory_register = 0
        self.grand_total = 0

    def initUI(self):
        self.setWindowTitle('Calculator')
        self.setWindowIcon(QIcon('icon.png'))  # Set window icon
        self.setGeometry(100, 100, 300, 500)  # Increased height to accommodate the bottom line

        # Disable maximize button
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowMaximizeButtonHint)

        self.layout = QVBoxLayout()

        self.result_display = QLineEdit()
        self.result_display.setFixedHeight(50)
        self.result_display.setAlignment(Qt.AlignRight)
        self.layout.addWidget(self.result_display)

        buttons_layout = QGridLayout()

        buttons = [
            ('-3%', 0, 0, 1, 1), ('-5%', 0, 1, 1, 1), ('-12%', 0, 2, 1, 1), ('-18%', 0, 3, 1, 1), ('-28%', 0, 4, 1, 1),
            ('3%', 1, 0, 1, 1), ('5%', 1, 1, 1, 1), ('12%', 1, 2, 1, 1), ('18%', 1, 3, 1, 1), ('28%', 1, 4, 1, 1),
            ('GT', 2, 0, 1, 1), ('%', 2, 1, 1, 1), ('CE', 2, 2, 1, 1), ('C', 2, 3, 1, 1), ('DEL', 2, 4, 1, 1),
            ('M+', 3, 0, 1, 1), ('M-', 3, 1, 1, 1), ('MR', 3, 2, 1, 1), ('MC', 3, 3, 1, 1), ('+/-', 3, 4, 1, 1),
            ('7', 4, 0, 1, 1), ('8', 4, 1, 1, 1), ('9', 4, 2, 1, 1), ('/', 4, 3, 1, 1), ('√', 4, 4, 1, 1),
            ('4', 5, 0, 1, 1), ('5', 5, 1, 1, 1), ('6', 5, 2, 1, 1), ('*', 5, 3, 1, 1), ('x²', 5, 4, 1, 1),
            ('1', 6, 0, 1, 1), ('2', 6, 1, 1, 1), ('3', 6, 2, 1, 1), ('-', 6, 3, 1, 1), ('%', 6, 4, 1, 1),
            ('0', 7, 0, 1, 1), ('00', 7, 1, 1, 1), ('.', 7, 2, 1, 1), ('+', 7, 3, 1, 1), ('=', 7, 4, 1, 1),
        ]

        for (text, row, col, rowspan, colspan) in buttons:
            button = QPushButton(text)
            button.setFixedSize(60, 60)
            button.clicked.connect(lambda _, text=text: self.on_button_click(text))
            buttons_layout.addWidget(button, row, col, rowspan, colspan)

        bottom_line = QLabel("Powered by Rahul Tumma")
        bottom_line.setAlignment(Qt.AlignCenter)
        self.layout.addLayout(buttons_layout)
        self.layout.addWidget(bottom_line)  # Add bottom line
        self.setLayout(self.layout)

        # Create keyboard shortcuts
        self.create_shortcuts()

    def create_shortcuts(self):
        shortcuts = {
            'C': Qt.Key_C,
            'CE': Qt.Key_Delete,
            'DEL': Qt.Key_Backspace,
            'M+': Qt.Key_Plus,
            'M-': Qt.Key_Minus,
            'MR': Qt.Key_R,
            'MC': Qt.Key_M,
            '+': Qt.Key_Plus,
            '-': Qt.Key_Minus,
            '*': Qt.Key_Asterisk,
            '/': Qt.Key_Slash,
            '=': Qt.Key_Enter,
        }

        for text, key in shortcuts.items():
            shortcut = QShortcut(key, self)
            

    def on_button_click(self, text):
        if text == '=':
            self.calculate()
        elif text in {'C', 'CE'}:
            self.clear()
        elif text == 'DEL':
            self.delete()
        elif text == '+/-':
            self.sign_change()
        elif text == 'x²':
            self.square()
        elif text == '√':
            self.square_root()
        elif text == 'GT':
            self.recall_grand_total()
        elif text in {'M+', 'M-', 'MR', 'MC'}:
            self.memory_operation(text)
        else:
            self.append_to_display(text)

    def append_to_display(self, text):
        current_text = self.result_display.text()
        if '%' in text:  
            try:
                value = float(current_text)
                if text.startswith('-'):  
                    percentage = -float(text.replace('%', '').replace('-', '')) / 100
                else:
                    percentage = float(text.replace('%', '')) / 100
                result = value * percentage+value
                self.result_display.setText(str(result))
            except ValueError:
                self.result_display.setText("Error")
        else:
            new_text = current_text + text
            self.result_display.setText(new_text)

    def clear(self):
        self.result_display.clear()

    def delete(self):
        current_text = self.result_display.text()
        new_text = current_text[:-1]  # Remove the last character
        self.result_display.setText(new_text)

    def sign_change(self):
        current_text = self.result_display.text()
        if current_text:
            if current_text[0] == '-':
                new_text = current_text[1:]
            else:
                new_text = '-' + current_text
            self.result_display.setText(new_text)

    def square(self):
        current_text = self.result_display.text()
        try:
            value = float(current_text)
            result = value ** 2
            self.result_display.setText(str(result))
        except ValueError:
            self.result_display.setText("Error")

    def square_root(self):
        current_text = self.result_display.text()
        try:
            value = float(current_text)
            result = value ** 0.5
            self.result_display.setText(str(result))
        except ValueError:
            self.result_display.setText("Error")

    def recall_grand_total(self):
        self.result_display.setText(str(self.grand_total))

    def memory_operation(self, op):
        try:
            value = float(self.result_display.text())
        except ValueError:
            value = 0.0

        if op == 'M+':
            self.memory_register += value
        elif op == 'M-':
            self.memory_register -= value
        elif op == 'MR':
            self.result_display.setText(str(self.memory_register))
        elif op == 'MC':
            self.memory_register = 0

    def calculate(self):
        expression = self.result_display.text()
        try:
            result = eval(expression)
            self.grand_total += result
            self.result_display.setText(str(result))
        except OverflowError:
            self.result_display.setText("Result is too large")
        except Exception as e:
            self.result_display.setText("Error")

    def keyPressEvent(self, event):
        key = event.key()
        if key == Qt.Key_Enter or key == Qt.Key_Return:
            self.on_button_click('=')
        elif Qt.Key_0 <= key <= Qt.Key_9:
            self.append_to_display(str(key - Qt.Key_0))
        elif key == Qt.Key_Period:
            self.append_to_display('.')
        elif key == Qt.Key_Plus:
            self.on_button_click('+')
        elif key == Qt.Key_Minus:
            self.on_button_click('-')
        elif key == Qt.Key_Asterisk:
            self.on_button_click('*')
        elif key == Qt.Key_Slash:
            self.on_button_click('/')
        elif key == Qt.Key_Backspace:
            self.delete()
        elif key == Qt.Key_Delete:
            self.clear()
        elif key == Qt.Key_M:
            self.on_button_click('MC')
        elif key == Qt.Key_R:
            self.on_button_click('MR')
        elif key == Qt.Key_C:
            self.on_button_click('C')
        elif key == Qt.Key_Equal:
            self.on_button_click('=')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Calculator()
    window.show()
    sys.exit(app.exec_())
