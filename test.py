# [Create a window]

import sys
from PyQt4.QtGui import *

app = QApplication(sys.argv) #ignore()
window = QWidget()
window.setWindowTitle("Hello World")
window.show()

# [Add widgets to the widget]

# Create some widgets (these won't appear immediately):
nameLabel = QLabel("Name:")
nameEdit = QLineEdit()
addressLabel = QLabel("Address:")
addressEdit = QTextEdit()

# Put the widgets in a layout (now they start to appear):
layout = QGridLayout(window)
layout.addWidget(nameLabel, 0, 0)
layout.addWidget(nameEdit, 0, 1)
layout.addWidget(addressLabel, 1, 0)
layout.addWidget(addressEdit, 1, 1)
layout.setRowStretch(2, 1)

# [Resizing the window]

# Let's resize the window:
window.resize(480, 160)

# The widgets are managed by the layout...
window.resize(320, 180)

# [Run the application]

# Start the event loop...
sys.exit(app.exec_())
