#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include <QFileDialog>
#include <QMessageBox>
#include <QtGui>
#include <opencv2/opencv.hpp>
#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <opencv2/imgproc/imgproc.hpp>

using namespace cv;

QT_BEGIN_NAMESPACE
namespace Ui {
class MainWindow;
}
QT_END_NAMESPACE

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    MainWindow(QWidget *parent = nullptr);
    ~MainWindow();

private slots:
    void on_flipVerticalButton_clicked();

    void on_openImgButton_clicked();

    void on_flipHorButton_clicked();

    void on_flipHorVerButton_clicked();

    void on_switchColorButton_clicked();

    void on_saveImgButton_clicked();

private:
    void updateImg();
    bool isRGB;

private:
    Ui::MainWindow *ui;
    Mat poza;
};
#endif // MAINWINDOW_H
