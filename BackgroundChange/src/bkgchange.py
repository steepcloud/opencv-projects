import cv2
import numpy as np
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QFileDialog, QColorDialog
from PyQt6.QtGui import QPixmap, QImage, QIntValidator


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("Background change")
        MainWindow.resize(730, 500)

        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.centralwidget.setStyleSheet("QWidget { background-color: #f0e0d1; }")

        self.inputImgLabel = QtWidgets.QLabel(parent=self.centralwidget)
        self.inputImgLabel.setGeometry(QtCore.QRect(100, 100, 71, 16))
        self.inputImgLabel.setObjectName("inputImgLabel")
        self.otherImgLabel = QtWidgets.QLabel(parent=self.centralwidget)
        self.otherImgLabel.setGeometry(QtCore.QRect(310, 100, 121, 16))
        self.otherImgLabel.setObjectName("otherImgLabel")
        self.resultLabel = QtWidgets.QLabel(parent=self.centralwidget)
        self.resultLabel.setGeometry(QtCore.QRect(575, 100, 41, 16))
        self.resultLabel.setObjectName("resultLabel")

        self.inputImgDisplayLabel = QtWidgets.QLabel(parent=self.centralwidget)
        self.inputImgDisplayLabel.setGeometry(QtCore.QRect(40, 130, 191, 191))
        self.inputImgDisplayLabel.setObjectName("inputImgDisplayLabel")
        self.bkgImgDisplayLabel = QtWidgets.QLabel(parent=self.centralwidget)
        self.bkgImgDisplayLabel.setGeometry(QtCore.QRect(270, 130, 191, 191))
        self.bkgImgDisplayLabel.setObjectName("bkgImgDisplayLabel")
        self.resultImgDisplayLabel = QtWidgets.QLabel(parent=self.centralwidget)
        self.resultImgDisplayLabel.setGeometry(QtCore.QRect(500, 130, 191, 191))
        self.resultImgDisplayLabel.setObjectName("resultImgDisplayLabel")

        self.inputImgDisplayLabel.setStyleSheet("background-color: white; border: 2px solid black;")
        self.bkgImgDisplayLabel.setStyleSheet("background-color: white; border: 2px solid black;")
        self.resultImgDisplayLabel.setStyleSheet("background-color: white; border: 2px solid black;")

        self.inputImgButton = QtWidgets.QPushButton(parent=self.centralwidget)
        self.inputImgButton.setGeometry(QtCore.QRect(20, 20, 111, 24))
        self.inputImgButton.setObjectName("inputImgButton")
        self.inputImgButton.setStyleSheet(
            "QPushButton { background-color: #3498db; color: #11191f; border: 2px solid #2980b9; border-radius: 10px; } "
            "QPushButton:hover { background-color: #2980b9; } "
            "QPushButton:pressed { background-color: #1abc9c; }"
        )

        self.bkgImgButton = QtWidgets.QPushButton(parent=self.centralwidget)
        self.bkgImgButton.setGeometry(QtCore.QRect(160, 20, 111, 24))
        self.bkgImgButton.setObjectName("bkgImgButton")
        self.bkgImgButton.setStyleSheet(
            "QPushButton { background-color: #8e44ad; color: #f0f0f0; border: 2px solid #732d91; border-radius: 10px; } "
            "QPushButton:hover { background-color: #732d91; } "
            "QPushButton:pressed { background-color: #d35400; }"
        )

        self.bkgColorButton = QtWidgets.QPushButton(parent=self.centralwidget)
        self.bkgColorButton.setGeometry(QtCore.QRect(310, 20, 111, 24))
        self.bkgColorButton.setObjectName("bkgColorButton")
        self.bkgColorButton.setStyleSheet(
            "QPushButton { background-color: #2c3e50; color: #ecf0f1; border: 2px solid #34495e; border-radius: 10px; } "
            "QPushButton:hover { background-color: #34495e; } "
            "QPushButton:pressed { background-color: #e74c3c; }"
        )

        self.threshSlider = QtWidgets.QSlider(parent=self.centralwidget)
        self.threshSlider.setGeometry(QtCore.QRect(480, 40, 160, 16))
        self.threshSlider.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.threshSlider.setRange(0, 255)
        self.threshSlider.setValue(100)
        self.threshSlider.setObjectName("threshSlider")
        self.threshSlider.setStyleSheet(
            "QSlider::groove:horizontal { border: 1px solid #bbb; background: #ddd; height: 6px; border-radius: 3px; }"
            "QSlider::handle:horizontal { background: #3498db; border: 1px solid #2980b9; width: 14px; height: 14px; border-radius: 7px; margin: -5px 0; }"
            "QSlider::handle:horizontal:hover { background: #2980b9; }"
            "QSlider::sub-page:horizontal { background: #3498db; border: 1px solid #2980b9; height: 6px; border-radius: 3px; }"
            "QSlider::add-page:horizontal { background: #ccc; border: 1px solid #aaa; height: 6px; border-radius: 3px; }"
        )

        self.threshLabel = QtWidgets.QLabel(parent=self.centralwidget)
        self.threshLabel.setGeometry(QtCore.QRect(510, 10, 101, 16))
        self.threshLabel.setObjectName("threshLabel")

        self.threshLineEdit = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.threshLineEdit.setGeometry(QtCore.QRect(650, 40, 21, 16))
        self.threshLineEdit.setObjectName("threshLineEdit")
        self.threshLineEdit.setStyleSheet("background-color: white;")
        self.threshLineEdit.setValidator(QIntValidator(0, 255))

        self.applyButton = QtWidgets.QPushButton(parent=self.centralwidget)
        self.applyButton.setGeometry(QtCore.QRect(610, 400, 80, 24))
        self.applyButton.setObjectName("applyButton")
        self.applyButton.setStyleSheet(
            "QPushButton:disabled { background-color: #a8a8a8; color: #3b3b3b; border: 2px solid #5e5e5e; border-radius: 10px; } "
            "QPushButton:enabled { background-color: #e74c3c; color: white; border: 2px solid #c0392b; border-radius: 10px; } "
            "QPushButton:hover { background-color: #c0392b; } "
            "QPushButton:pressed { background-color: #f39c12; }"
        )
        self.applyButton.setEnabled(False)

        # connecting signals to slots
        self.inputImgButton.clicked.connect(lambda: self.load_image('input'))
        self.bkgImgButton.clicked.connect(lambda: self.load_image('background'))
        self.bkgColorButton.clicked.connect(self.choose_background_color)
        self.threshSlider.valueChanged.connect(self.update_threshold_line_edit)
        self.threshLineEdit.textChanged.connect(self.update_slider_from_line_edit)
        self.applyButton.clicked.connect(self.apply_background_change)

        self.background_image = None
        self.selected_color = None

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Background change"))
        self.inputImgLabel.setText(_translate("MainWindow", "Input Image"))
        self.otherImgLabel.setText(_translate("MainWindow", "Desired image / color"))
        self.inputImgButton.setText(_translate("MainWindow", "Open Input Image"))
        self.bkgImgButton.setText(_translate("MainWindow", "Background Image"))
        self.bkgColorButton.setText(_translate("MainWindow", "Background Color"))
        self.threshLabel.setText(_translate("MainWindow", "Thresholding value"))
        self.threshLineEdit.setText(_translate("MainWindow", "100"))
        self.resultLabel.setText(_translate("MainWindow", "Result"))
        self.applyButton.setText(_translate("MainWindow", "Apply"))

    def load_image(self, img_type):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(None,
                                                   "Select Image",
                                                   "",
                                                   "Images (*.png *.jpeg *.jpg *.bmp)")

        if file_path:
            image = cv2.imread(file_path)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            h, w, channel = image.shape
            bytes_per_line = 3 * w
            q_image = QImage(image.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)
            pixmap = QPixmap.fromImage(q_image)

            if img_type == 'input':
                self.inputImgDisplayLabel.setPixmap(pixmap.scaled(self.inputImgDisplayLabel.size(),
                                                                  QtCore.Qt.AspectRatioMode.KeepAspectRatio))
                self.input_image = image
            elif img_type == 'background':
                self.bkgImgDisplayLabel.setPixmap(pixmap.scaled(self.bkgImgDisplayLabel.size(),
                                                                QtCore.Qt.AspectRatioMode.KeepAspectRatio))
                self.background_image = image
                self.selected_color = None

            self.update_apply_button_state()

    def choose_background_color(self):
        color_dialog = QColorDialog()
        color = color_dialog.getColor()
        if color.isValid():
            self.selected_color = color
            self.background_image = None
            color_pixmap = QPixmap(250, 250)
            color_pixmap.fill(color)
            self.bkgImgDisplayLabel.setPixmap(color_pixmap)
            self.update_apply_button_state()

    def update_apply_button_state(self):
        if hasattr(self, 'input_image') and (self.background_image is not None or self.selected_color is not None):
            self.applyButton.setEnabled(True)
        else:
            self.applyButton.setEnabled(False)

    def update_threshold_line_edit(self, value):
        self.threshLineEdit.setText(str(value))

    def update_slider_from_line_edit(self):
        value = int(self.threshLineEdit.text()) if self.threshLineEdit.text() else 0
        self.threshSlider.setValue(value)

    def apply_background_change(self):
        if hasattr(self, 'input_image') and (self.background_image is not None or self.selected_color is not None):
            # convert input image to grayscale and apply thresholding
            gray_image = cv2.cvtColor(self.input_image, cv2.COLOR_BGR2GRAY)

            # retrieve threshold value from the line edit
            threshold_value = int(self.threshLineEdit.text()) if self.threshLineEdit.text() else 0

            _, binary_mask = cv2.threshold(gray_image, threshold_value, 255, cv2.THRESH_BINARY_INV)

            # find contours to isolate the subject
            contours, _ = cv2.findContours(binary_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            # create a mask that covers the subject
            mask = np.zeros_like(gray_image)
            cv2.drawContours(mask, contours, -1, (255), thickness=cv2.FILLED)

            # create an inverse mask to keep the subject content intact
            mask_inv = cv2.bitwise_not(mask)

            # extracting the subject
            foreground = cv2.bitwise_and(self.input_image, self.input_image, mask=mask)

            # check if background is an image or color
            h, w = mask.shape[:2]
            if self.background_image is not None:
                background_resized = cv2.resize(self.background_image, (w, h))
                background = cv2.bitwise_and(background_resized, background_resized, mask=mask_inv)
                requires_rgb_conversion = False
                self.selected_color = None
            elif self.selected_color is not None:
                b, g, r = self.selected_color.blue(), self.selected_color.green(), self.selected_color.red()
                color_img = np.full((h, w, 3), (b, g, r), dtype=np.uint8)
                background = cv2.bitwise_and(color_img, color_img, mask=mask_inv)
                requires_rgb_conversion = True
                self.background_image = None
            else:
                QtWidgets.QMessageBox.warning(self.centralwidget, "Warning", "No background selected.")
                return

            # combine the subject with the background
            result = cv2.add(foreground, background)

            # convert result for display in QLabel
            result = cv2.cvtColor(result, cv2.COLOR_BGR2RGB) if requires_rgb_conversion else result
            h, w, channel = result.shape
            bytes_per_line = 3 * w
            q_image = QtGui.QImage(result.data, w, h, bytes_per_line, QtGui.QImage.Format.Format_RGB888)
            self.resultImgDisplayLabel.setPixmap(QtGui.QPixmap.fromImage(q_image).scaled(191, 191,
                                                QtCore.Qt.AspectRatioMode.KeepAspectRatio))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())
