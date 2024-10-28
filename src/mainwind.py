from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QFileDialog, QColorDialog, QLabel, QLineEdit, QScrollArea
from PyQt6.QtGui import QPixmap, QPainter, QPen, QIntValidator, QColor, QFont
from PyQt6.QtCore import Qt, QPoint

class TransparentLineEdit(QLineEdit):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setMouseTracking(True)
        self.isResizing = False
        self.current_color = QColor("black")
        self.setStyleSheet("background: transparent; border: 2px solid transparent;")
        self.resize_direction = None
        self.resize_start_pos = None
        self.resize_start_size = None

    def focusInEvent(self, event):
        self.setStyleSheet(f"background: transparent; border: 2px solid black; color: {self.current_color.name()};")
        super().focusInEvent(event)

    def focusOutEvent(self, event):
        self.setStyleSheet(f"background: transparent; border: 2px solid transparent; color: {self.current_color.name()};")
        super().focusOutEvent(event)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            margins = 5
            if abs(event.pos().x() - self.width()) < margins:
                self.isResizing = True
                self.resize_direction = "horizontal"
            elif abs(event.pos().y() - self.height()) < margins:
                self.isResizing = True
                self.resize_direction = "vertical"
            if self.isResizing:
                self.resize_start_pos = event.pos()
                self.resize_start_size = self.size()
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        margins = 5
        if not self.isResizing:
            if abs(event.pos().x() - self.width()) < margins:
                self.setCursor(Qt.CursorShape.SizeHorCursor)
            elif abs(event.pos().y() - self.height()) < margins:
                self.setCursor(Qt.CursorShape.SizeVerCursor)
            else:
                self.setCursor(Qt.CursorShape.IBeamCursor)
        else:
            delta = event.pos() - self.resize_start_pos
            if self.resize_direction == "horizontal":
                new_width = self.resize_start_size.width() + delta.x()
                self.setFixedWidth(max(30, new_width))
            elif self.resize_direction == "vertical":
                new_height = self.resize_start_size.height() + delta.y()
                self.setFixedHeight(max(20, new_height))

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.isResizing = False
        super().mouseReleaseEvent(event)

    def setTextColor(self, color):
        self.current_color = color
        self.setStyleSheet(f"color: {self.current_color.name()}; background: transparent; border: 2px solid transparent;"
                           f"color: {self.current_color.name()};")

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):

        MainWindow.setObjectName("Frame")
        MainWindow.resize(650, 550)

        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.centralwidget.setStyleSheet("QWidget { background-color: #f0e0d1; }")

        self.sizeSlider = QtWidgets.QSlider(parent=self.centralwidget)
        self.sizeSlider.setGeometry(QtCore.QRect(540, 20, 16, 160))
        self.sizeSlider.setOrientation(QtCore.Qt.Orientation.Vertical)
        self.sizeSlider.setObjectName("sizeSlider")

        self.thicknessSlider = QtWidgets.QSlider(parent=self.centralwidget)
        self.thicknessSlider.setGeometry(QtCore.QRect(600, 20, 16, 160))
        self.thicknessSlider.setOrientation(QtCore.Qt.Orientation.Vertical)
        self.thicknessSlider.setObjectName("thicknessSlider")

        self.sizeLabel = QtWidgets.QLabel(parent=self.centralwidget)
        self.sizeLabel.setGeometry(QtCore.QRect(540, 0, 21, 20))
        self.sizeLabel.setObjectName("sizeLabel")

        self.thicknessLabel = QtWidgets.QLabel(parent=self.centralwidget)
        self.thicknessLabel.setGeometry(QtCore.QRect(580, 0, 51, 21))
        self.thicknessLabel.setObjectName("thicknessLabel")

        self.sizeLineEdit = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.sizeLineEdit.setGeometry(QtCore.QRect(540, 180, 16, 16))
        self.sizeLineEdit.setObjectName("sizeLineEdit")

        # setting the min / max value for size slider
        self.sizeSlider.setMinimum(1)
        self.sizeSlider.setMaximum(50)
        self.sizeLineEdit.setValidator(QIntValidator(1, 50, self.sizeLineEdit))
        
        self.thicknessLineEdit = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.thicknessLineEdit.setGeometry(QtCore.QRect(600, 180, 16, 16))
        self.thicknessLineEdit.setObjectName("thicknessLineEdit")

        # setting the min / max value for thickness slider
        self.thicknessSlider.setMinimum(1)
        self.thicknessSlider.setMaximum(10)
        self.thicknessLineEdit.setValidator(QIntValidator(1, 10, self.thicknessLineEdit))

        self.textColorButton = QtWidgets.QPushButton(parent=self.centralwidget)
        self.textColorButton.setGeometry(QtCore.QRect(530, 210, 101, 31))
        self.textColorButton.setObjectName("textColorButton")
        self.textColorButton.setStyleSheet(
            "QPushButton { background-color: #3498db; color: #11191f; border: 2px solid #2980b9; border-radius: 10px; } "
            "QPushButton:hover { background-color: #2980b9; } "
            "QPushButton:pressed { background-color: #1abc9c; }"
        )

        self.saveImgButton = QtWidgets.QPushButton(parent=self.centralwidget)
        self.saveImgButton.setGeometry(QtCore.QRect(530, 250, 101, 31))
        self.saveImgButton.setObjectName("saveImgButton")
        self.saveImgButton.setStyleSheet(
            "QPushButton:disabled { background-color: #a8a8a8; color: #3b3b3b; border: 2px solid #5e5e5e; border-radius: 10px; } "
            "QPushButton:enabled { background-color: #e74c3c; color: white; border: 2px solid #c0392b; border-radius: 10px; } "
            "QPushButton:hover { background-color: #c0392b; } "
            "QPushButton:pressed { background-color: #f39c12; }"
        )
        self.saveImgButton.setEnabled(False)

        self.imgWidget = QtWidgets.QWidget(parent=self.centralwidget)
        self.imgWidget.setGeometry(QtCore.QRect(10, 20, 491, 471))
        self.imgWidget.setObjectName("imgWidget")

        # image label for imgWidget
        self.image_label = QLabel()

        self.scrollArea = QScrollArea(self.imgWidget)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setContentsMargins(0, 0, 0, 0)

        self.scrollArea.setWidget(self.image_label)
        self.scrollArea.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout = QtWidgets.QVBoxLayout(self.imgWidget)
        layout.addWidget(self.scrollArea)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.imgWidget.setLayout(layout)

        self.scrollArea.hide()

        self.imgWidget.setStyleSheet("border: 1px solid black;")

        MainWindow.setCentralWidget(self.centralwidget)

        self.menubar = QtWidgets.QMenuBar(parent=MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 650, 21))
        self.menubar.setObjectName("menubar")

        self.menuFile = QtWidgets.QMenu(parent=self.menubar)
        self.menuFile.setObjectName("menuFile")
        MainWindow.setMenuBar(self.menubar)

        self.actionOpen_File = QtGui.QAction(parent=MainWindow)
        self.actionOpen_File.setShortcutContext(QtCore.Qt.ShortcutContext.WidgetWithChildrenShortcut)
        self.actionOpen_File.setObjectName("actionOpen_File")

        self.actionExit = QtGui.QAction(parent=MainWindow)
        self.actionExit.setObjectName("actionExit")

        self.menuFile.addAction(self.actionOpen_File)
        self.menuFile.addAction(self.actionExit)

        self.menubar.addAction(self.menuFile.menuAction())

        self.sizeSlider.valueChanged.connect(self.updateSize)
        self.sizeSlider.valueChanged.connect(lambda val: self.sizeLineEdit.setText(str(val)))
        self.sizeLineEdit.textChanged.connect(self.updateSizeFromLineEdit)

        self.thicknessSlider.valueChanged.connect(self.updateThickness)
        self.thicknessSlider.valueChanged.connect(lambda val: self.thicknessLineEdit.setText(str(val)))
        self.thicknessLineEdit.textChanged.connect(self.updateThicknessFromLineEdit)

        self.size = 1
        self.thickness = 1
        self.textColor = QColor("black")
        self.image = None
        self.painter = QPainter()
        self.textBoxes = []

        self.textColorButton.clicked.connect(self.selectTextColor)
        self.saveImgButton.clicked.connect(self.saveImage)

        self.actionOpen_File.triggered.connect(self.openImage)
        self.actionExit.triggered.connect(MainWindow.close)

        self.imgWidget.mousePressEvent = self.addTextBox

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def updateSize(self, value):
        self.size = value

        for box in self.textBoxes:
            font = box.font()
            font.setPointSize(value)
            box.setFont(font)

    def updateSizeFromLineEdit(self):
        value = int(self.sizeLineEdit.text()) if self.sizeLineEdit.text() else 1
        self.size = value
        self.sizeSlider.setValue(value)

    def updateThickness(self, value: int):
        self.thickness = value
        font_weight = value * 100

        for box in self.textBoxes:
            font = box.font()
            font.setWeight(font_weight)
            box.setFont(font)

    def updateThicknessFromLineEdit(self):
        value = int(self.thicknessLineEdit.text()) if self.thicknessLineEdit.text() else 1
        self.thickness = value
        self.thicknessSlider.setValue(value)

    def selectTextColor(self):
        color = QColorDialog.getColor()

        if color.isValid():
            self.textColor = color

            for box in self.textBoxes:
                box.setTextColor(color)

    def openImage(self):
        filePath, _ = QFileDialog.getOpenFileName(None, "Open Image", "", "Image Files (*.png *.jpg *.jpeg *.bmp)")

        if filePath:
            self.image = QPixmap(filePath)

            if self.image.isNull() or self.image.size().isEmpty():
                return

            self.scrollArea.setStyleSheet("border: none;")

            # scaling the image to fully occupy imgWidget's space
            scaled_pixmap = self.image.scaled(self.imgWidget.width(), self.imgWidget.height(),
                                              Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                                              Qt.TransformationMode.SmoothTransformation)

            # setting the scaled pixmap to the image label
            self.image_label.setPixmap(scaled_pixmap)
            self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

            self.scrollArea.show()
            self.textBoxes.clear()
            self.saveImgButton.setEnabled(True)

    def addTextBox(self, event):
        if self.image is None:
            return

        x, y = event.pos().x(), event.pos().y()
        if x > self.image.width() or y > self.image.height():
            return

        textBox = TransparentLineEdit(self.imgWidget)
        font = QtGui.QFont()
        font.setPointSize(self.size)
        font.setWeight(self.thickness * 100)
        textBox.setFont(font)
        textBox.setTextColor(self.textColor)
        textBox.move(event.pos())
        textBox.setFocus()
        textBox.returnPressed.connect(lambda: self.renderText(textBox))
        textBox.show()
        self.textBoxes.append(textBox)

    def renderText(self, textBox):
        if self.image:
            painter = QPainter(self.image)
            pen = QPen(self.textColor, self.thickness)
            painter.setPen(pen)
            font = painter.font()
            font.setPointSize(self.size)
            font.setWeight(self.thickness * 10)
            painter.setFont(font)
            textBox_pos = textBox.mapToParent(textBox.pos())
            painter.drawText(textBox_pos, textBox.text())
            painter.end()
            textBox.hide()
            self.image_label.setPixmap(self.image)

    def saveImage(self):
        if self.image is None:
            return

        filePath, _ = QFileDialog.getSaveFileName(None, "Save Image", "",
                                                  "PNG Files (*.png);;"
                                                  "JPG Files (*.jpg);;"
                                                  "JPEG Files (*.jpeg);;"
                                                  "BMP Files (*.bmp)")

        if filePath:
            temp_image = self.image.copy()
            try:
                painter = QPainter(temp_image)

                displayed_pixmap = self.image_label.pixmap()
                if displayed_pixmap.isNull():
                    return

                scale_y = self.image.height() / displayed_pixmap.height()

                for box in self.textBoxes:
                    if box is None:
                        continue

                    font = box.font()
                    color = box.current_color

                    # setting the painter's font size according to the original size
                    adjusted_font_size = int(font.pointSize() * scale_y)
                    painter.setFont(QFont(font.family(), adjusted_font_size, font.weight()))

                    # scaling the position of the text box
                    box_pos = box.mapToParent(box.pos())

                    painter.setPen(QPen(color, self.thickness))

                    painter.drawText(QPoint(box_pos.x(), box_pos.y()), box.text())

                painter.end()
                temp_image.save(filePath)

            except Exception as e:
                print(f"Error while saving image: {e}")


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("Frame", "Frame"))
        self.sizeLabel.setText(_translate("Frame", "Size"))
        self.thicknessLabel.setText(_translate("Frame", "Thickness"))
        self.sizeLineEdit.setText(_translate("Frame", "1"))
        self.thicknessLineEdit.setText(_translate("Frame", "1"))
        self.textColorButton.setText(_translate("Frame", "Select Text Color"))
        self.saveImgButton.setText(_translate("Frame", "Save Image"))
        self.menuFile.setTitle(_translate("Frame", "File"))
        self.actionOpen_File.setText(_translate("Frame", "Open File"))
        self.actionOpen_File.setShortcut(_translate("Frame", "Ctrl+O"))
        self.actionOpen_File.setShortcutContext(QtCore.Qt.ShortcutContext.ApplicationShortcut)
        self.actionExit.setText(_translate("Frame", "Exit"))
        self.actionExit.setShortcut(_translate("Frame", "Ctrl+E"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())
