import cv2
import numpy as np
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import Qt, QRect, QSize
from PyQt6.QtGui import QPixmap, QImage, QColor, QPainter, QPen
from PyQt6.QtWidgets import QColorDialog, QFileDialog, QMenu, QMessageBox


class ImageLabel(QtWidgets.QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMouseTracking(True)
        self.setCursor(QtCore.Qt.CursorShape.CrossCursor)
        self.roi = QRect()
        self.selectingROI = False
        self.border_color = QColor(0, 255, 0)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.selectingROI = True
            self.roi = QRect(event.position().toPoint(), QSize())

    def mouseMoveEvent(self, event):
        if self.selectingROI:
            self.roi.setBottomRight(event.position().toPoint())
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.selectingROI = False
            self.roi = self.roi.normalized()
            self.update()

    def paintEvent(self, event):
        super().paintEvent(event)
        if not self.roi.isNull():
            painter = QPainter(self)
            painter.setPen(QPen(self.border_color, 2, Qt.PenStyle.SolidLine))
            painter.drawRect(self.roi)

    def get_roi(self):
        return self.roi

    def clear_roi(self):
        self.roi = QRect()
        self.update()

    def contextMenuEvent(self, event):
        context_menu = QMenu(self)
        clear_roi_action = context_menu.addAction("Clear ROI")
        action = context_menu.exec(self.mapToGlobal(event.pos()))

        if action == clear_roi_action:
            self.clear_roi()

class Ui_MainWindow(object):
    def __init__(self):
        super().__init__()

        self.image = None
        self.q_image = None
        self.roi = QRect()
        self.color = QColor(255, 255, 255)
        self.scaling_factor_x = 1
        self.scaling_factor_y = 1

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(600, 550)

        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.centralwidget.setStyleSheet("QWidget { background-color: #f0e0d1; }")

        self.colorLabel = QtWidgets.QLabel(parent=self.centralwidget)
        self.colorLabel.setGeometry(QtCore.QRect(20, 10, 51, 51))
        self.colorLabel.setText("")
        self.colorLabel.setObjectName("colorLabel")

        self.colorButton = QtWidgets.QPushButton(parent=self.centralwidget)
        self.colorButton.setGeometry(QtCore.QRect(90, 20, 80, 24))
        self.colorButton.setObjectName("colorButton")
        self.colorButton.setStyleSheet(
            "QPushButton { background-color: #8e44ad; color: #f0f0f0; border: 2px solid #732d91; border-radius: 10px; } "
            "QPushButton:hover { background-color: #732d91; } "
            "QPushButton:pressed { background-color: #d35400; }"
        )

        self.applyColorButton = QtWidgets.QPushButton(parent=self.centralwidget)
        self.applyColorButton.setGeometry(QtCore.QRect(200, 20, 80, 24))
        self.applyColorButton.setObjectName("applyColorButton")
        self.applyColorButton.setStyleSheet(
            "QPushButton:disabled { background-color: #a8a8a8; color: #3b3b3b; border: 2px solid #5e5e5e; border-radius: 10px; } "
            "QPushButton:enabled { background-color: #e74c3c; color: white; border: 2px solid #c0392b; border-radius: 10px; } "
            "QPushButton:hover { background-color: #c0392b; } "
            "QPushButton:pressed { background-color: #f39c12; }"
        )

        self.imgLabel = ImageLabel(parent=self.centralwidget)
        self.imgLabel.setGeometry(QtCore.QRect(20, 90, 551, 381))
        self.imgLabel.setText("")
        self.imgLabel.setObjectName("imgLabel")
        self.imgLabel.setScaledContents(True)
        self.imgLabel.setMouseTracking(True)
        self.imgLabel.setCursor(QtCore.Qt.CursorShape.CrossCursor)

        self.colorLabel.setStyleSheet("background-color: white; border: 2px solid black;")
        self.imgLabel.setStyleSheet("background-color: white; border: 2px solid black;")

        MainWindow.setCentralWidget(self.centralwidget)

        self.menubar = QtWidgets.QMenuBar(parent=MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 600, 21))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(parent=self.menubar)
        self.menuFile.setGeometry(QtCore.QRect(288, 101, 126, 96))
        self.menuFile.setObjectName("menuFile")
        MainWindow.setMenuBar(self.menubar)
        self.actionOpen_File = QtGui.QAction(parent=MainWindow)
        self.actionOpen_File.setShortcutContext(QtCore.Qt.ShortcutContext.WidgetShortcut)
        self.actionOpen_File.setObjectName("actionOpen_File")
        self.actionSave_File = QtGui.QAction(parent=MainWindow)
        self.actionSave_File.setObjectName("actionSave_File")
        self.menuFile.addAction(self.actionOpen_File)
        self.menuFile.addAction(self.actionSave_File)
        self.menubar.addAction(self.menuFile.menuAction())

        # connecting signals to slots
        self.colorButton.clicked.connect(self.choose_background_color)
        self.actionOpen_File.triggered.connect(self.openImage)
        self.actionSave_File.triggered.connect(self.saveImage)
        self.applyColorButton.clicked.connect(self.apply_color)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "ROIchanger"))
        self.colorButton.setText(_translate("MainWindow", "Choose color"))
        self.applyColorButton.setText(_translate("MainWindow", "Apply color"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.actionOpen_File.setText(_translate("MainWindow", "Open File"))
        self.actionOpen_File.setShortcut(_translate("MainWindow", "Ctrl+O"))
        self.actionOpen_File.setShortcutContext(QtCore.Qt.ShortcutContext.ApplicationShortcut)
        self.actionSave_File.setText(_translate("MainWindow", "Save File"))
        self.actionSave_File.setShortcut(_translate("MainWindow", "Ctrl+S"))

    def choose_background_color(self):
        color_dialog = QColorDialog()
        color = color_dialog.getColor()
        if color.isValid():
            self.color = color
            color_pixmap = QPixmap(250, 250)
            color_pixmap.fill(color)
            self.colorLabel.setPixmap(color_pixmap)

    def openImage(self):
        filePath, _ = QFileDialog.getOpenFileName(None, "Open Image", "", "Image Files (*.png *.jpg *.jpeg *.bmp)")

        if filePath:
            self.image = cv2.imread(filePath)
            self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
            h, w, _ = self.image.shape
            bytes_per_line = 3 * w
            self.q_image = QImage(self.image.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)

            self.scaling_factor_x = self.imgLabel.width() / w
            self.scaling_factor_y = self.imgLabel.height() / h

            self.update_pixmap()

    def update_pixmap(self):
        scaled_image = self.q_image.scaled(self.imgLabel.size(), Qt.AspectRatioMode.KeepAspectRatio)
        self.imgLabel.setPixmap(QPixmap.fromImage(scaled_image))

    def saveImage(self):
        if self.image is not None:
            filePath, _ = QFileDialog.getSaveFileName(None, "Save Image", "",
                                                      "PNG Files (*.png);;"
                                                      "JPG Files (*.jpg);;"
                                                      "JPEG Files (*.jpeg);;"
                                                      "BMP Files (*.bmp)")
            if filePath:
                cv2.imwrite(filePath, cv2.cvtColor(self.image, cv2.COLOR_RGB2BGR))

    def show_warning(self, message):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Icon.Warning)
        msg_box.setText(message)
        msg_box.setWindowTitle("Apply Color Warning")
        msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg_box.exec()

    def apply_color(self):
        if self.image is None:
            self.show_warning("Please load an image before applying the color.")
            return

        self.roi = self.imgLabel.get_roi()
        if self.roi.isNull():
            self.show_warning("Please select a region of interest (ROI) before applying the color.")
            return

        scaling_x = self.scaling_factor_x
        scaling_y = self.scaling_factor_y

        roi_x, roi_y, roi_w, roi_h = self.roi.getRect()
        roi_x = int(roi_x / scaling_x)
        roi_y = int(roi_y / scaling_y)
        roi_w = int(roi_w / scaling_x)
        roi_h = int(roi_h / scaling_y)

        roi_image = self.image[roi_y:roi_y + roi_h, roi_x:roi_x + roi_w]
        gray_roi = cv2.cvtColor(roi_image, cv2.COLOR_RGB2GRAY)

        _, thresh = cv2.threshold(gray_roi, 190, 255, cv2.THRESH_BINARY_INV)

        mask_subject = (thresh == 255)
        colored_bg = np.full_like(roi_image, self.color.getRgb()[:3], dtype=np.uint8)
        roi_image[~mask_subject] = colored_bg[~mask_subject]

        mask_subject_full = np.zeros(self.image.shape[:2], dtype=np.uint8)
        mask_subject_full[roi_y:roi_y + roi_h, roi_x:roi_x + roi_w] = mask_subject

        background_color = np.array([self.color.red(), self.color.green(), self.color.blue()])

        self.image[mask_subject_full == 0] = background_color
        self.image[roi_y:roi_y + roi_h, roi_x:roi_x + roi_w] = roi_image

        self.update_pixmap()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())
