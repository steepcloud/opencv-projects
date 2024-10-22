#include "mainwindow.h"
#include "ui_mainwindow.h"

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::MainWindow)
{
    ui->setupUi(this);

    this->setFixedSize(this->size());

    this->setWindowFlags(Qt::Window | Qt::WindowMinimizeButtonHint | Qt::WindowCloseButtonHint);

    this->setStyleSheet("QMainWindow { background-color: #f0e0d1; }");

    ui->openImgButton->setStyleSheet("QPushButton { background-color: #3498db; color: #11191f; border: 2px solid #2980b9; border-radius: 10px; } QPushButton:hover { background-color: #2980b9; } QPushButton:pressed { background-color: #1abc9c; }");

    ui->saveImgButton->setEnabled(false);

    ui->saveImgButton->setStyleSheet(
        "QPushButton:disabled { background-color: #a8a8a8; color: #3b3b3b; border: 2px solid #5e5e5e; border-radius: 10px; }"
        "QPushButton:enabled { background-color: #e74c3c; color: white; border: 2px solid #c0392b; border-radius: 10px; } QPushButton:hover { background-color: #c0392b; } QPushButton:pressed { background-color: #f39c12; }"
    );
}

MainWindow::~MainWindow()
{
    delete ui;
}

void MainWindow::on_openImgButton_clicked()
{
    srcDir = QFileDialog::getExistingDirectory(this, tr("Select Source Folder"));

    if (!srcDir.isEmpty()) {
        ui->saveImgButton->setEnabled(true);
    }
}


void MainWindow::on_saveImgButton_clicked()
{
    destDir = QFileDialog::getExistingDirectory(this, tr("Select Destination Folder"));

    if (destDir.isEmpty()) {
        return;
    }

    procImg();
}

void MainWindow::procImg() {
    if (srcDir.isEmpty() || destDir.isEmpty()) {
        QMessageBox::warning(this, tr("Error"), tr("Please select both source and destination folders."));
        return;
    }

    if (!ui->flipVerButton->isChecked() &&
        !ui->flipHorButton->isChecked() &&
        !ui->flipHorVerButton->isChecked()) {
        QMessageBox::warning(this, tr("Error"), tr("Please select a mirroring option."));
        return;
    }

    QDir dir(srcDir);
    QFileInfoList fileInfoList = dir.entryInfoList(QStringList() << "*.jpg" << "*.jpeg" << "*.png" << "*.bmp", QDir::Files);

    for (const QFileInfo &fileInfo : fileInfoList) {
        QString srcFilePath = fileInfo.absoluteFilePath();
        QString srcFileName = fileInfo.fileName();

        Mat img = imread(srcFilePath.toStdString());

        if (!img.data) {
            continue;
        }

        if (ui->flipVerButton->isChecked()) {
            flip (img, img, 1);
        }
        else if (ui->flipHorButton->isChecked()) {
            flip (img, img, 0);
        }
        else if (ui->flipHorVerButton->isChecked()) {
            flip (img, img, -1);
        }

        QString destFilePath = destDir + "/" + srcFileName;
        imwrite(destFilePath.toStdString(), img);
    }

    QMessageBox::information(this, tr("Success"), tr("Images have been saved."));
}
