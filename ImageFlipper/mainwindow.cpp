#include "mainwindow.h"
#include "ui_mainwindow.h"

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
    , isRGB(true)
    , ui(new Ui::MainWindow)
{
    ui->setupUi(this);

    this->setStyleSheet("QMainWindow { background-color: #f0e0d1; }");

    ui->openImgButton->setStyleSheet("QPushButton { background-color: #3498db; color: #11191f; border: 2px solid #2980b9; border-radius: 10px; } QPushButton:hover { background-color: #2980b9; } QPushButton:pressed { background-color: #1abc9c; }");

    ui->flipVerticalButton->setEnabled(false);
    ui->flipHorButton->setEnabled(false);
    ui->flipHorVerButton->setEnabled(false);
    ui->switchColorButton->setEnabled(false);
    ui->saveImgButton->setEnabled(false);

    ui->flipVerticalButton->setStyleSheet(
        "QPushButton:disabled { background-color: #a8a8a8; color: #3b3b3b; border: 2px solid #5e5e5e; border-radius: 10px; }"
        "QPushButton:enabled { background-color: #c4894f; color: #453422; border: 2px solid #ed7700; border-radius: 10px; } QPushButton:hover { background-color: #6e5031; } QPushButton:pressed { background-color: #e6d3c1; }"
    );

    ui->flipHorButton->setStyleSheet(
        "QPushButton:disabled { background-color: #a8a8a8; color: #3b3b3b; border: 2px solid #5e5e5e; border-radius: 10px; }"
        "QPushButton:enabled { background-color: #4a90e2; color: #2c3e50; border: 2px solid #0077cc; border-radius: 10px; } QPushButton:hover { background-color: #0077cc; } QPushButton:pressed { background-color: #005fa3; }"
    );

    ui->flipHorVerButton->setStyleSheet(
        "QPushButton:disabled { background-color: #a8a8a8; color: #3b3b3b; border: 2px solid #5e5e5e; border-radius: 10px; }"
        "QPushButton:enabled { background-color: #e67e22; color: #f9c8c8; border: 2px solid #d35400; border-radius: 10px; } QPushButton:hover { background-color: #d35400; } QPushButton:pressed { background-color: #c65a1d; }"
    );

    ui->switchColorButton->setStyleSheet(
        "QPushButton:disabled { background-color: #a8a8a8; color: #3b3b3b; border: 2px solid #5e5e5e; border-radius: 10px; }"
        "QPushButton:enabled { background-color: #27ae60; color: #e8d1e7; border: 2px solid #219653; border-radius: 10px; } QPushButton:hover { background-color: #219653; } QPushButton:pressed { background-color: #1c7a4c; }"
    );

    ui->saveImgButton->setStyleSheet(
        "QPushButton:disabled { background-color: #a8a8a8; color: #3b3b3b; border: 2px solid #5e5e5e; border-radius: 10px; }"
        "QPushButton:enabled { background-color: #e74c3c; color: white; border: 2px solid #c0392b; border-radius: 10px; } QPushButton:hover { background-color: #c0392b; } QPushButton:pressed { background-color: #f39c12; }"
    );

}

MainWindow::~MainWindow()
{
    delete ui;
}

void MainWindow::updateImg() {
    QImage img = QImage((uchar*) poza.data, poza.cols, poza.rows, poza.step, QImage::Format_RGB888);

    ui->label->setPixmap(QPixmap::fromImage(img).scaled(ui->label->size(), Qt::KeepAspectRatio));
    ui->label->resize(ui->label->pixmap().size());
}

void MainWindow::on_openImgButton_clicked()
{
    QString fileName = QFileDialog::getOpenFileName(this, tr("Open image"),
                                                    ".", tr("Image Files (*.png *.jpg *.jpeg *.bmp)"));

    if (fileName.isEmpty()) {
        return;
    }

    poza = imread(fileName.toLatin1().data());

    if (poza.data) {
        ui->flipVerticalButton->setEnabled(true);
        ui->flipHorButton->setEnabled(true);
        ui->flipHorVerButton->setEnabled(true);
        ui->switchColorButton->setEnabled(true);
        ui->saveImgButton->setEnabled(true);
    }

    cvtColor(poza, poza, COLOR_BGR2RGB);

    updateImg();

    //namedWindow("Init pic", WINDOW_AUTOSIZE);
    //imshow("Init pic", poza);
}

void MainWindow::on_flipVerticalButton_clicked()
{
    flip(poza, poza, 1);

    updateImg();

    //namedWindow("Mirrored pic");
    //imshow("Mirrored pic", poza);
}

void MainWindow::on_flipHorButton_clicked()
{
    flip(poza, poza, 0);

    updateImg();
}


void MainWindow::on_flipHorVerButton_clicked()
{
    flip(poza, poza, -1);

    updateImg();
}


void MainWindow::on_switchColorButton_clicked()
{
    if (isRGB) {
        cvtColor(poza, poza, COLOR_RGB2BGR);
    } else {
        cvtColor(poza, poza, COLOR_BGR2RGB);
    }

    updateImg();

    isRGB = !isRGB;
}


void MainWindow::on_saveImgButton_clicked()
{
    QString fileName = QFileDialog::getSaveFileName(this, tr("Save Image"),
                                                    ".", tr("Image Files (*.png *.jpg *.jpeg *.bmp)"));

    if (fileName.isEmpty()) {
        return;
    }

    if (!isRGB) {
        cvtColor(poza, poza, COLOR_BGR2RGB);
    }

    if (!imwrite(fileName.toStdString(), poza)) {
        QMessageBox::warning(this, tr("Error"), tr("Failed to save the image."));
    }
}

