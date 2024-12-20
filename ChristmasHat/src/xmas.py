import sys
import cv2
import numpy as np
import time
from mtcnn import MTCNN
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QPushButton, QLabel, QFileDialog,
                             QSlider, QLineEdit)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QImage


class ImageProcessor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.detector = MTCNN()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Christmas Hat')
        self.setGeometry(100, 100, 1200, 800)

        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout()

        image_layout = QHBoxLayout()

        self.original_image_label = QLabel()
        self.processed_image_label = QLabel()
        self.original_image_label.setMinimumSize(500, 400)
        self.processed_image_label.setMinimumSize(500, 400)
        image_layout.addWidget(self.original_image_label)
        image_layout.addWidget(self.processed_image_label)

        layout.addLayout(image_layout)

        button_layout = QHBoxLayout()
        self.load_button = QPushButton('Load Image')
        self.save_button = QPushButton('Save Image')
        self.load_hat_button = QPushButton('Load Hat')
        button_layout.addWidget(self.load_button)
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.load_hat_button)
        layout.addLayout(button_layout)

        sliders_layout = QVBoxLayout()

        hat_width_layout = QHBoxLayout()
        hat_width_layout.addWidget(QLabel('Hat Width:'))
        self.hat_width_slider = QSlider(Qt.Orientation.Horizontal)
        self.hat_width_slider.setRange(15, 50)
        self.hat_width_slider.setValue(25)
        self.hat_width_edit = QLineEdit()
        self.hat_width_edit.setMaximumWidth(50)
        hat_width_layout.addWidget(self.hat_width_slider)
        hat_width_layout.addWidget(self.hat_width_edit)
        sliders_layout.addLayout(hat_width_layout)

        y_offset_top_layout = QHBoxLayout()
        y_offset_top_layout.addWidget(QLabel('Y Offset Top:'))
        self.y_offset_top_slider = QSlider(Qt.Orientation.Horizontal)
        self.y_offset_top_slider.setRange(0, 500)
        self.y_offset_top_slider.setValue(30)
        self.y_offset_top_edit = QLineEdit()
        self.y_offset_top_edit.setMaximumWidth(50)
        y_offset_top_layout.addWidget(self.y_offset_top_slider)
        y_offset_top_layout.addWidget(self.y_offset_top_edit)
        sliders_layout.addLayout(y_offset_top_layout)

        y_offset_bottom_layout = QHBoxLayout()
        y_offset_bottom_layout.addWidget(QLabel('Y Offset Bottom:'))
        self.y_offset_bottom_slider = QSlider(Qt.Orientation.Horizontal)
        self.y_offset_bottom_slider.setRange(0, 500)
        self.y_offset_bottom_slider.setValue(75)
        self.y_offset_bottom_edit = QLineEdit()
        self.y_offset_bottom_edit.setMaximumWidth(50)
        y_offset_bottom_layout.addWidget(self.y_offset_bottom_slider)
        y_offset_bottom_layout.addWidget(self.y_offset_bottom_edit)
        sliders_layout.addLayout(y_offset_bottom_layout)

        layout.addLayout(sliders_layout)

        self.faces_label = QLabel('Number of faces detected: 0')
        self.time_label = QLabel('Detection time: 0.0000 seconds')
        layout.addWidget(self.faces_label)
        layout.addWidget(self.time_label)

        main_widget.setLayout(layout)

        self.load_button.clicked.connect(self.load_image)
        self.save_button.clicked.connect(self.save_image)
        self.load_hat_button.clicked.connect(self.load_hat)
        self.hat_width_slider.valueChanged.connect(lambda value: (
            self.update_hat_width_edit(value),
            self.process_image()
        ))
        self.y_offset_top_slider.valueChanged.connect(lambda value: (
            self.update_y_offset_top_edit(value),
            self.process_image()
        ))
        self.y_offset_bottom_slider.valueChanged.connect(lambda value: (
            self.update_y_offset_bottom_edit(value),
            self.process_image()
        ))
        self.hat_width_edit.textChanged.connect(self.update_hat_width_slider)
        self.y_offset_top_edit.textChanged.connect(self.update_y_offset_top_slider)
        self.y_offset_bottom_edit.textChanged.connect(self.update_y_offset_bottom_slider)

        self.current_image = None
        self.hat_image = None
        self.detected_faces = None

        self.update_hat_width_edit(25)
        self.update_y_offset_top_edit(30)
        self.update_y_offset_bottom_edit(75)

    def load_image(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Image File", "",
                                                   "Images (*.png *.xpm *.jpg *.bmp)")
        if file_name:
            self.current_image = cv2.imread(file_name)
            self.display_image(self.current_image, self.original_image_label)
            self.process_image()

    def load_hat(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Hat Image File", "",
                                                   "Images (*.png *.xpm *.jpg *.bmp)")
        if file_name:
            self.hat_image = cv2.imread(file_name)
            if self.current_image is not None:
                self.process_image()

    def save_image(self):
        if hasattr(self, 'processed_image'):
            file_name, _ = QFileDialog.getSaveFileName(self, "Save Image File", "",
                                                       "Images (*.png *.xpm *.jpg *.bmp)")
            if file_name:
                cv2.imwrite(file_name, self.processed_image)

    def process_hat(self, hat_image):
        hat_gray = cv2.cvtColor(hat_image, cv2.COLOR_BGR2GRAY)
        _, mask = cv2.threshold(hat_gray, 5, 255, cv2.THRESH_BINARY)

        kernel = np.ones((3, 3), np.uint8)
        mask = cv2.erode(mask, kernel, iterations=2)
        mask = cv2.dilate(mask, kernel, iterations=1)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        refined_mask = np.zeros_like(mask)
        cv2.drawContours(refined_mask, contours, -1, (255), thickness=cv2.FILLED)
        refined_mask = cv2.dilate(refined_mask, kernel, iterations=1)

        return refined_mask

    def process_image(self):
        if self.current_image is None:
            return

        image_rgb = cv2.cvtColor(self.current_image, cv2.COLOR_BGR2RGB)

        start_time = time.time()
        self.detected_faces = self.detector.detect_faces(image_rgb)
        end_time = time.time()

        detection_time = end_time - start_time
        self.faces_label.setText(f"Number of faces detected: {len(self.detected_faces)}")
        self.time_label.setText(f"Detection time: {detection_time:.4f} seconds")

        processed_image = self.current_image.copy()

        if self.hat_image is not None and len(self.detected_faces) > 0:
            refined_mask = self.process_hat(self.hat_image)

            for face in self.detected_faces:
                x, y, w, h = face['box']

                hat_width_scale = self.hat_width_slider.value() / 10
                y_offset_top = self.y_offset_top_slider.value()
                y_offset_bottom = self.y_offset_bottom_slider.value()

                center_x = x + w // 2
                center_y = y + h // 4
                hat_width = int(w * hat_width_scale)
                hat_height = int(h / 2)

                y1_roi = max(center_y - hat_height - y_offset_top, 0)
                y2_roi = min(center_y + y_offset_bottom, processed_image.shape[0])
                x1_roi = max(center_x - hat_width // 3, 0)
                x2_roi = min(center_x + hat_width // 3 * 2, processed_image.shape[1])

                roi_bg = processed_image[y1_roi:y2_roi, x1_roi:x2_roi]

                if roi_bg.size == 0:
                    continue

                resized_hat = cv2.resize(self.hat_image, (roi_bg.shape[1], roi_bg.shape[0]))
                resized_mask = cv2.resize(refined_mask, (roi_bg.shape[1], roi_bg.shape[0]))
                mask_inv = cv2.bitwise_not(resized_mask)
                mask_inv_triplet = cv2.merge((mask_inv, mask_inv, mask_inv))
                masked_roi = cv2.bitwise_and(roi_bg, mask_inv_triplet)
                hat_mask = cv2.merge((resized_mask, resized_mask, resized_mask))
                masked_hat = cv2.bitwise_and(resized_hat, hat_mask)
                combined_roi = cv2.add(masked_roi, masked_hat)
                processed_image[y1_roi:y2_roi, x1_roi:x2_roi] = combined_roi

        self.processed_image = processed_image
        self.display_image(processed_image, self.processed_image_label)

    def display_image(self, image, label):
        h, w = image.shape[:2]
        label_size = label.size()

        scale_w = label_size.width() / w
        scale_h = label_size.height() / h

        scale = min(scale_w, scale_h)
        new_size = (int(w * scale), int(h * scale))
        resized_image = cv2.resize(image, new_size)
        bytes_per_line = 3 * new_size[0]
        qt_image = QImage(cv2.cvtColor(resized_image, cv2.COLOR_BGR2RGB).data,
                          new_size[0], new_size[1], bytes_per_line, QImage.Format.Format_RGB888)
        label.setPixmap(QPixmap.fromImage(qt_image))

    def update_hat_width_edit(self, value):
        self.hat_width_edit.setText(f"{value / 10:.1f}")

    def update_y_offset_top_edit(self, value):
        self.y_offset_top_edit.setText(str(value))

    def update_y_offset_bottom_edit(self, value):
        self.y_offset_bottom_edit.setText(str(value))

    def update_hat_width_slider(self):
        try:
            value = float(self.hat_width_edit.text()) * 10
            self.hat_width_slider.setValue(int(value))
        except ValueError:
            pass

    def update_y_offset_top_slider(self):
        try:
            value = int(self.y_offset_top_edit.text())
            self.y_offset_top_slider.setValue(value)
        except ValueError:
            pass

    def update_y_offset_bottom_slider(self):
        try:
            value = int(self.y_offset_bottom_edit.text())
            self.y_offset_bottom_slider.setValue(value)
        except ValueError:
            pass


def main():
    app = QApplication(sys.argv)
    window = ImageProcessor()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()