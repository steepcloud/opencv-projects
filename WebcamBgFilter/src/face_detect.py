import sys
import cv2
import numpy as np
from PyQt6 import QtCore, QtGui, QtWidgets


class VideoFilterApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.face_coordinates = None
        self.setWindowTitle("Webcam Background Filter")
        self.setGeometry(100, 100, 800, 600)

        layout = QtWidgets.QVBoxLayout()

        self.image_label = QtWidgets.QLabel(self)
        layout.addWidget(self.image_label)

        self.filter_combo = QtWidgets.QComboBox(self)
        self.filter_combo.addItems([ # filters
            "Gaussian Blur",
            "Bilateral Filter",
            "Box Filter",
            "Sepia Effect",
            "Invert Colors"
        ])
        self.filter_combo.currentIndexChanged.connect(self.filter_changed)
        layout.addWidget(self.filter_combo)

        # gaussian blur slider
        self.gaussianSigmaXLabel = QtWidgets.QLabel("Sigma X (Gaussian Blur):", self)
        self.gaussianSigmaXSlider = QtWidgets.QSlider(QtCore.Qt.Orientation.Horizontal, self)
        self.gaussianSigmaXSlider.setRange(1, 100)
        self.gaussianSigmaXSlider.setValue(25)
        self.gaussianSigmaXSlider.setTickInterval(5)
        self.gaussianSigmaXSlider.setTickPosition(QtWidgets.QSlider.TickPosition.TicksBelow)
        self.gaussianSigmaXSlider.valueChanged.connect(self.update_filter_parameter)
        self.gaussianSigmaXSlider.setStyleSheet(
            "QSlider::groove:horizontal { border: 1px solid #bbb; background: #ddd; height: 6px; border-radius: 3px; }"
            "QSlider::handle:horizontal { background: #3498db; border: 1px solid #2980b9; width: 14px; height: 14px; border-radius: 7px; margin: -5px 0; }"
            "QSlider::handle:horizontal:hover { background: #2980b9; }"
            "QSlider::sub-page:horizontal { background: #3498db; border: 1px solid #2980b9; height: 6px; border-radius: 3px; }"
            "QSlider::add-page:horizontal { background: #ccc; border: 1px solid #aaa; height: 6px; border-radius: 3px; }"
        )

        # bilateral filter sliders
        self.bilateralSigmaColorLabel = QtWidgets.QLabel("Sigma Color (Bilateral Filter):", self)
        self.bilateralSigmaColorSlider = QtWidgets.QSlider(QtCore.Qt.Orientation.Horizontal, self)
        self.bilateralSigmaColorSlider.setRange(1, 200)
        self.bilateralSigmaColorSlider.setValue(75)
        self.bilateralSigmaColorSlider.setTickInterval(5)
        self.bilateralSigmaColorSlider.setTickPosition(QtWidgets.QSlider.TickPosition.TicksBelow)
        self.bilateralSigmaColorSlider.valueChanged.connect(self.update_filter_parameter)
        self.bilateralSigmaColorSlider.setStyleSheet(
            "QSlider::groove:horizontal { border: 1px solid #bbb; background: #ddd; height: 6px; border-radius: 3px; }"
            "QSlider::handle:horizontal { background: #3498db; border: 1px solid #2980b9; width: 14px; height: 14px; border-radius: 7px; margin: -5px 0; }"
            "QSlider::handle:horizontal:hover { background: #2980b9; }"
            "QSlider::sub-page:horizontal { background: #3498db; border: 1px solid #2980b9; height: 6px; border-radius: 3px; }"
            "QSlider::add-page:horizontal { background: #ccc; border: 1px solid #aaa; height: 6px; border-radius: 3px; }"
        )

        self.bilateralSigmaSpaceLabel = QtWidgets.QLabel("Sigma Space (Bilateral Filter):", self)
        self.bilateralSigmaSpaceSlider = QtWidgets.QSlider(QtCore.Qt.Orientation.Horizontal, self)
        self.bilateralSigmaSpaceSlider.setRange(1, 200)
        self.bilateralSigmaSpaceSlider.setValue(75)
        self.bilateralSigmaSpaceSlider.setTickInterval(5)
        self.bilateralSigmaSpaceSlider.setTickPosition(QtWidgets.QSlider.TickPosition.TicksBelow)
        self.bilateralSigmaSpaceSlider.valueChanged.connect(self.update_filter_parameter)
        self.bilateralSigmaSpaceSlider.setStyleSheet(
            "QSlider::groove:horizontal { border: 1px solid #bbb; background: #ddd; height: 6px; border-radius: 3px; }"
            "QSlider::handle:horizontal { background: #3498db; border: 1px solid #2980b9; width: 14px; height: 14px; border-radius: 7px; margin: -5px 0; }"
            "QSlider::handle:horizontal:hover { background: #2980b9; }"
            "QSlider::sub-page:horizontal { background: #3498db; border: 1px solid #2980b9; height: 6px; border-radius: 3px; }"
            "QSlider::add-page:horizontal { background: #ccc; border: 1px solid #aaa; height: 6px; border-radius: 3px; }"
        )

        # threshold adjusting slider
        self.thresholdLabel = QtWidgets.QLabel("Threshold Value:", self)
        self.thresholdSlider = QtWidgets.QSlider(QtCore.Qt.Orientation.Horizontal, self)
        self.thresholdSlider.setRange(0, 255)
        self.thresholdSlider.setValue(180)
        self.thresholdSlider.setTickInterval(5)
        self.thresholdSlider.setTickPosition(QtWidgets.QSlider.TickPosition.TicksBelow)
        self.thresholdSlider.valueChanged.connect(self.update_threshold_value)
        self.thresholdSlider.setStyleSheet(
            "QSlider::groove:horizontal { border: 1px solid #bbb; background: #ddd; height: 6px; border-radius: 3px; }"
            "QSlider::handle:horizontal { background: #3498db; border: 1px solid #2980b9; width: 14px; height: 14px; border-radius: 7px; margin: -5px 0; }"
            "QSlider::handle:horizontal:hover { background: #2980b9; }"
            "QSlider::sub-page:horizontal { background: #3498db; border: 1px solid #2980b9; height: 6px; border-radius: 3px; }"
            "QSlider::add-page:horizontal { background: #ccc; border: 1px solid #aaa; height: 6px; border-radius: 3px; }"
        )

        self.bilateralSigmaColorLabel.setVisible(False)
        self.bilateralSigmaColorSlider.setVisible(False)
        self.bilateralSigmaSpaceLabel.setVisible(False)
        self.bilateralSigmaSpaceSlider.setVisible(False)

        layout.addWidget(self.gaussianSigmaXLabel)
        layout.addWidget(self.gaussianSigmaXSlider)
        layout.addWidget(self.bilateralSigmaColorLabel)
        layout.addWidget(self.bilateralSigmaColorSlider)
        layout.addWidget(self.bilateralSigmaSpaceLabel)
        layout.addWidget(self.bilateralSigmaSpaceSlider)

        layout.addWidget(self.thresholdLabel)
        layout.addWidget(self.thresholdSlider)

        self.setLayout(layout)

        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            raise IOError("Cannot open webcam")

        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

        self.backSub = cv2.createBackgroundSubtractorMOG2()

        self.selected_filter = "Gaussian Blur"
        self.sigmaX = 25
        self.sigmaColor = 75
        self.sigmaSpace = 75

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(60)

    def filter_changed(self):
        self.selected_filter = self.filter_combo.currentText()
        if self.selected_filter == "Gaussian Blur":
            self.gaussianSigmaXLabel.setText("Sigma X (Gaussian Blur):")
            self.bilateralSigmaColorLabel.setVisible(False)
            self.bilateralSigmaColorSlider.setVisible(False)
            self.bilateralSigmaSpaceLabel.setVisible(False)
            self.bilateralSigmaSpaceSlider.setVisible(False)
            self.gaussianSigmaXSlider.setVisible(True)
            self.thresholdSlider.setVisible(True)
            self.thresholdLabel.setVisible(True)
            self.gaussianSigmaXLabel.setVisible(True)
        elif self.selected_filter == "Bilateral Filter":
            self.gaussianSigmaXLabel.setText("Diameter (Bilateral Filter):")
            self.bilateralSigmaColorLabel.setVisible(True)
            self.bilateralSigmaColorSlider.setVisible(True)
            self.bilateralSigmaSpaceLabel.setVisible(True)
            self.bilateralSigmaSpaceSlider.setVisible(True)
            self.gaussianSigmaXSlider.setVisible(True)
            self.thresholdSlider.setVisible(True)
            self.thresholdLabel.setVisible(True)
            self.gaussianSigmaXLabel.setVisible(True)
        elif self.selected_filter == "Box Filter":
            self.gaussianSigmaXLabel.setText("Kernel Size (Box Filter):")
            self.bilateralSigmaColorLabel.setVisible(False)
            self.bilateralSigmaColorSlider.setVisible(False)
            self.bilateralSigmaSpaceLabel.setVisible(False)
            self.bilateralSigmaSpaceSlider.setVisible(False)
            self.gaussianSigmaXSlider.setVisible(True)
            self.thresholdSlider.setVisible(True)
            self.thresholdLabel.setVisible(True)
            self.gaussianSigmaXLabel.setVisible(True)
        elif self.selected_filter == "Sepia Effect":
            self.gaussianSigmaXLabel.setText("Intensity (Sepia):")
            self.bilateralSigmaColorLabel.setVisible(False)
            self.bilateralSigmaColorSlider.setVisible(False)
            self.bilateralSigmaSpaceLabel.setVisible(False)
            self.bilateralSigmaSpaceSlider.setVisible(False)
            self.gaussianSigmaXSlider.setVisible(True)
            self.thresholdSlider.setVisible(True)
            self.thresholdLabel.setVisible(True)
            self.gaussianSigmaXLabel.setVisible(True)
        elif self.selected_filter == "Invert Colors":
            self.gaussianSigmaXLabel.setVisible(False)
            self.gaussianSigmaXSlider.setVisible(False)
            self.thresholdSlider.setVisible(False)
            self.thresholdLabel.setVisible(False)
            self.bilateralSigmaColorLabel.setVisible(False)
            self.bilateralSigmaColorSlider.setVisible(False)
            self.bilateralSigmaSpaceLabel.setVisible(False)
            self.bilateralSigmaSpaceSlider.setVisible(False)

    def update_filter_parameter(self):
        self.sigmaX = self.gaussianSigmaXSlider.value()
        self.sigmaColor = self.bilateralSigmaColorSlider.value()
        self.sigmaSpace = self.bilateralSigmaSpaceSlider.value()

    def update_threshold_value(self):
        self.threshold_value = self.thresholdSlider.value()

    def update_frame(self):
        try:
            ret, frame = self.cap.read()
            if not ret:
                print("Failed to capture frame")
                return

            frame = cv2.resize(frame, (640, 480))
            original_frame = frame.copy()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            if self.timer.remainingTime() % 10 == 0 or len(self.face_coordinates) == 0:
                self.face_coordinates = self.face_cascade.detectMultiScale(
                    gray, scaleFactor=1.1, minNeighbors=5, minSize=(50, 50), flags=cv2.CASCADE_SCALE_IMAGE
                )

            mask = np.zeros(frame.shape[:2], dtype=np.uint8)
            for (x, y, w, h) in self.face_coordinates:
                rect = (x, y, w, h)

                bgdModel = np.zeros((1, 65), dtype=np.float64)
                fgdModel = np.zeros((1, 65), dtype=np.float64)

                cv2.grabCut(frame, mask, rect, bgdModel, fgdModel, iterCount=5, mode=cv2.GC_INIT_WITH_RECT)

            subject_mask = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')

            filtered_background = original_frame.copy()
            if self.selected_filter == "Gaussian Blur":
                filtered_background = cv2.GaussianBlur(filtered_background, (21, 21), self.sigmaX)
            elif self.selected_filter == "Bilateral Filter":
                filtered_background = cv2.bilateralFilter(filtered_background, 15, self.sigmaColor, self.sigmaSpace)
            elif self.selected_filter == "Box Filter":
                filtered_background = cv2.boxFilter(filtered_background, -1, (self.sigmaX, self.sigmaX))
            elif self.selected_filter == "Sepia Effect":
                filtered_background = self.apply_sepia(filtered_background)
            elif self.selected_filter == "Invert Colors":
                filtered_background = cv2.bitwise_not(filtered_background)

            result_frame = filtered_background.copy()
            result_frame[subject_mask == 1] = original_frame[subject_mask == 1]

            qimg = QtGui.QImage(result_frame.data, result_frame.shape[1], result_frame.shape[0],
                                result_frame.strides[0], QtGui.QImage.Format.Format_BGR888)
            pixmap = QtGui.QPixmap.fromImage(qimg)
            self.image_label.setPixmap(pixmap)
        except Exception as e:
            print(f"Error: {e}")

    def apply_sepia(self, frame):
        frame = frame.astype(np.float32)
        sepia_filter = np.array([[0.393, 0.769, 0.189],
                                 [0.349, 0.686, 0.168],
                                 [0.272, 0.534, 0.131]])
        frame = np.dot(frame, sepia_filter.T)
        frame = np.clip(frame, 0, 255).astype(np.uint8)
        return frame


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = VideoFilterApp()
    window.show()
    sys.exit(app.exec())
