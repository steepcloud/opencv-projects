import sys
import cv2
import numpy as np
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
    QFileDialog, QSlider, QComboBox, QWidget
)
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtCore import Qt


class ObjectCounterApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Optimized Object Counter")
        self.setGeometry(100, 100, 1200, 700)

        self.image = None
        self.processed_image = None
        self.grabcut_cache = {}

        self._initialize_ui()

    def _initialize_ui(self):
        main_layout = QHBoxLayout()
        self.input_label = self._create_image_label("Input Image")
        self.output_label = self._create_image_label("Processed Image")

        main_layout.addWidget(self.input_label)
        main_layout.addWidget(self.output_label)

        control_layout = QVBoxLayout()
        control_layout.addWidget(self._create_button("Load Image", self.load_image))
        self.save_button = self._create_button("Save Image", self.save_image, enabled=False)
        control_layout.addWidget(self.save_button)
        self.method_selector = self._create_method_selector()
        control_layout.addWidget(self.method_selector)
        self.object_count_label = QLabel("Objects Found: 0")
        control_layout.addWidget(self.object_count_label)
        self.sliders = self._initialize_sliders(control_layout)
        main_layout.addLayout(control_layout)

        widget = QWidget()
        widget.setLayout(main_layout)
        self.setCentralWidget(widget)

    def _create_image_label(self, text):
        label = QLabel(text)
        label.setFixedSize(500, 500)
        label.setStyleSheet("border: 1px solid black;")
        return label

    def _create_button(self, text, callback, enabled=True):
        button = QPushButton(text)
        button.clicked.connect(callback)
        button.setEnabled(enabled)
        return button

    def _create_method_selector(self):
        selector = QComboBox()
        selector.addItems(["GrabCut"])
        selector.currentTextChanged.connect(self.update_image)
        return selector

    def _initialize_sliders(self, layout):
        sliders = {
            "threshold": self._create_slider(layout, 0, 255, 1, "Threshold"),
            "canny_min": self._create_slider(layout, 0, 500, 100, "Canny MinVal"),
            "canny_max": self._create_slider(layout, 0, 500, 200, "Canny MaxVal"),
            "iterations": self._create_slider(layout, 1, 10, 1, "GrabCut Iterations"),
        }
        return sliders

    def _create_slider(self, layout, min_val, max_val, default_val, label):
        slider = QSlider(Qt.Orientation.Horizontal)
        slider.setRange(min_val, max_val)
        slider.setValue(default_val)
        slider_label = QLabel(f"{label}: {default_val}")
        slider.valueChanged.connect(lambda val: slider_label.setText(f"{label}: {val}"))
        slider.valueChanged.connect(self.update_image)
        slider_layout = QVBoxLayout()
        slider_layout.addWidget(slider_label)
        slider_layout.addWidget(slider)
        layout.addLayout(slider_layout)
        return slider

    def load_image(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Image File", "", "Images (*.png *.jpg *.jpeg *.bmp)")
        if file_path:
            self.image = cv2.imread(file_path)
            self.display_image(self.image, self.input_label)
            self.save_button.setEnabled(True)
            self.grabcut_cache.clear()
            self.update_image()

    def save_image(self):
        if self.processed_image is not None:
            file_path, _ = QFileDialog.getSaveFileName(self, "Save Image File", "", "Images (*.png *.jpg *.bmp)")
            if file_path:
                cv2.imwrite(file_path, self.processed_image)

    def update_image(self):
        if self.image is None:
            return
        if self.method_selector.currentText() == "GrabCut":
            self._apply_grabcut()

    def _apply_grabcut(self):
        scale_factor = 0.5
        small_image = cv2.resize(self.image, (0, 0), fx=scale_factor, fy=scale_factor)
        mask = np.zeros(small_image.shape[:2], dtype=np.uint8)
        rect = (10, 10, small_image.shape[1] - 20, small_image.shape[0] - 20)
        bgd_model = np.zeros((1, 65), dtype=np.float64)
        fgd_model = np.zeros((1, 65), dtype=np.float64)
        cv2.grabCut(small_image, mask, rect, bgd_model, fgd_model, self.sliders["iterations"].value(), cv2.GC_INIT_WITH_RECT)
        mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype("uint8")
        segmented_small = small_image * mask2[:, :, np.newaxis]
        segmented = cv2.resize(segmented_small, (self.image.shape[1], self.image.shape[0]))
        threshold_value = self.sliders["threshold"].value()
        gray = cv2.cvtColor(segmented, cv2.COLOR_BGR2GRAY)
        _, binary = cv2.threshold(gray, threshold_value, 255, cv2.THRESH_BINARY)
        self._detect_and_draw_contours(binary)

    def _detect_and_draw_contours(self, binary_image):
        contours, _ = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        result = np.zeros_like(self.image)
        object_count = 0
        for contour in contours:
            if cv2.contourArea(contour) < 100:
                continue
            color = tuple(np.random.randint(0, 255, 3).tolist())
            cv2.drawContours(result, [contour], -1, color, -1)
            moments = cv2.moments(contour)
            if moments["m00"] != 0:
                cx = int(moments["m10"] / moments["m00"])
                cy = int(moments["m01"] / moments["m00"])
                cv2.putText(result, str(object_count + 1), (cx, cy), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
            object_count += 1
        self.object_count_label.setText(f"Objects Found: {object_count}")
        self.processed_image = result
        self.display_image(result, self.output_label)

    def display_image(self, image, label):
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        qt_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)
        pixmap = QPixmap.fromImage(qt_image).scaled(label.size(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        label.setPixmap(pixmap)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ObjectCounterApp()
    window.show()
    sys.exit(app.exec())
