import sys
import cv2
import numpy as np
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout,
    QWidget, QLabel, QSlider, QCheckBox, QPushButton, QColorDialog
)
from PyQt6.QtGui import QImage, QPixmap, QColor
from PyQt6.QtCore import Qt, QTimer


class WebcamDrawingApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Webcam Drawing App")
        self.current_color = (0, 255, 0)
        self._init_ui()
        self._init_webcam()

    def _init_ui(self):
        main_widget = QWidget()
        main_layout = QHBoxLayout()
        webcam_layout = QVBoxLayout()
        control_layout = QVBoxLayout()

        self.original_label = QLabel("Original Feed")
        self.threshold_label = QLabel("Threshold Feed")
        self.color_preview = QLabel("HSV Color")
        self.color_preview.setFixedSize(100, 100)

        webcam_layout.addWidget(self.original_label)
        webcam_layout.addWidget(self.threshold_label)
        webcam_layout.addWidget(self.color_preview)

        self.h_min_slider, self.h_min_label = self._create_hsv_slider("Hue Min", 0, 179, 20)
        self.h_max_slider, self.h_max_label = self._create_hsv_slider("Hue Max", 0, 179, 70)
        self.s_min_slider, self.s_min_label = self._create_hsv_slider("Saturation Min", 0, 255, 100)
        self.s_max_slider, self.s_max_label = self._create_hsv_slider("Saturation Max", 0, 255, 255)
        self.v_min_slider, self.v_min_label = self._create_hsv_slider("Value Min", 0, 255, 100)
        self.v_max_slider, self.v_max_label = self._create_hsv_slider("Value Max", 0, 255, 255)

        sliders = [
            (self.h_min_label, self.h_min_slider),
            (self.h_max_label, self.h_max_slider),
            (self.s_min_label, self.s_min_slider),
            (self.s_max_label, self.s_max_slider),
            (self.v_min_label, self.v_min_slider),
            (self.v_max_label, self.v_max_slider)
        ]
        for label, slider in sliders:
            control_layout.addWidget(label)
            control_layout.addWidget(slider)

        self.draw_checkbox = QCheckBox("Draw Mode")
        self.erase_checkbox = QCheckBox("Erase Mode")
        self.draw_checkbox.stateChanged.connect(self._toggle_mode)
        self.erase_checkbox.stateChanged.connect(self._toggle_mode)

        color_button = QPushButton("Choose Color")
        color_button.clicked.connect(self._choose_color)
        clear_button = QPushButton("Clear Canvas")
        clear_button.clicked.connect(self._clear_canvas)

        control_layout.addWidget(self.draw_checkbox)
        control_layout.addWidget(self.erase_checkbox)
        control_layout.addWidget(color_button)
        control_layout.addWidget(clear_button)

        main_layout.addLayout(webcam_layout, 2)
        main_layout.addLayout(control_layout, 1)

        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

    def _init_webcam(self):
        self.cap = cv2.VideoCapture(0)
        self.canvas = np.zeros((480, 640, 3), dtype=np.uint8)

        for slider in [self.h_min_slider, self.h_max_slider,
                       self.s_min_slider, self.s_max_slider,
                       self.v_min_slider, self.v_max_slider]:
            slider.valueChanged.connect(self._update_color_preview)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self._update_frame)
        self.timer.start(30)

    def _toggle_mode(self, state):
        sender = self.sender()
        if sender == self.draw_checkbox:
            if self.draw_checkbox.isChecked():
                self.erase_checkbox.setChecked(False)
                self.erase_checkbox.setEnabled(False)
            else:
                self.erase_checkbox.setEnabled(True)
        elif sender == self.erase_checkbox:
            if self.erase_checkbox.isChecked():
                self.draw_checkbox.setChecked(False)
                self.draw_checkbox.setEnabled(False)
            else:
                self.draw_checkbox.setEnabled(True)

    def _choose_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.current_color = (color.blue(), color.green(), color.red())

    def _create_hsv_slider(self, name, min_val, max_val, default_val=0):
        slider = QSlider(Qt.Orientation.Horizontal)
        slider.setMinimum(min_val)
        slider.setMaximum(max_val)
        slider.setValue(default_val)
        label = QLabel(f"{name}: {default_val}")
        slider.valueChanged.connect(lambda value, lbl=label, nm=name: lbl.setText(f"{nm}: {value}"))
        return slider, label

    def _update_color_preview(self):
        hsv_color = np.uint8([[[
            self.h_min_slider.value(),
            self.s_min_slider.value(),
            self.v_min_slider.value()
        ]]])
        bgr_color = cv2.cvtColor(hsv_color, cv2.COLOR_HSV2BGR)
        q_color = QColor(bgr_color[0][0][2], bgr_color[0][0][1], bgr_color[0][0][0])
        pixmap = QPixmap(100, 100)
        pixmap.fill(q_color)
        self.color_preview.setPixmap(pixmap)

    def _update_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            return

        frame = cv2.flip(frame, 1)
        lower_hsv = np.array([
            self.h_min_slider.value(),
            self.s_min_slider.value(),
            self.v_min_slider.value()
        ])
        upper_hsv = np.array([
            self.h_max_slider.value(),
            self.s_max_slider.value(),
            self.v_max_slider.value()
        ])

        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv_frame, lower_hsv, upper_hsv)
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if self.draw_checkbox.isChecked() and contours:
            largest_contour = max(contours, key=cv2.contourArea)
            M = cv2.moments(largest_contour)
            if M["m00"] != 0:
                cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])

            if not hasattr(self, 'prev_point'):
                self.prev_point = (cx, cy)

            cv2.line(self.canvas, self.prev_point, (cx, cy), self.current_color, 5)
            self.prev_point = (cx, cy)
        elif self.erase_checkbox.isChecked() and contours:
            largest_contour = max(contours, key=cv2.contourArea)
            M = cv2.moments(largest_contour)
            if M["m00"] != 0:
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])

                eraser_mask = np.zeros_like(mask)
                cv2.drawContours(eraser_mask, [largest_contour], -1, 255, thickness=cv2.FILLED)

                if np.any(eraser_mask):
                    self.canvas = cv2.bitwise_and(self.canvas, self.canvas, mask=cv2.bitwise_not(eraser_mask))
            else:
                pass
        elif hasattr(self, 'prev_point'):
            del self.prev_point

        result = cv2.addWeighted(frame, 0.3, self.canvas, 0.7, 0)
        original_pixmap = self._convert_cv_to_pixmap(result)
        threshold_pixmap = self._convert_cv_to_pixmap(mask)

        self.original_label.setPixmap(original_pixmap)
        self.threshold_label.setPixmap(threshold_pixmap)

    def _convert_cv_to_pixmap(self, cv_img):
        height, width = cv_img.shape[:2]
        if len(cv_img.shape) == 3:
            rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        else:
            rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_GRAY2RGB)

        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        q_img = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)
        return QPixmap.fromImage(q_img)

    def _clear_canvas(self):
        self.canvas = np.zeros((480, 640, 3), dtype=np.uint8)
        if self.draw_checkbox.isChecked():
            self.erase_checkbox.setEnabled(True)
            self.draw_checkbox.setChecked(False)
        if self.erase_checkbox.isChecked():
            self.draw_checkbox.setEnabled(True)
            self.erase_checkbox.setChecked(False)


def main():
    app = QApplication(sys.argv)
    window = WebcamDrawingApp()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()