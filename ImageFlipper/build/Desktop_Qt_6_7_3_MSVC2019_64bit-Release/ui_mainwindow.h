/********************************************************************************
** Form generated from reading UI file 'mainwindow.ui'
**
** Created by: Qt User Interface Compiler version 6.7.3
**
** WARNING! All changes made in this file will be lost when recompiling UI file!
********************************************************************************/

#ifndef UI_MAINWINDOW_H
#define UI_MAINWINDOW_H

#include <QtCore/QVariant>
#include <QtWidgets/QApplication>
#include <QtWidgets/QLabel>
#include <QtWidgets/QMainWindow>
#include <QtWidgets/QMenuBar>
#include <QtWidgets/QPushButton>
#include <QtWidgets/QStatusBar>
#include <QtWidgets/QWidget>

QT_BEGIN_NAMESPACE

class Ui_MainWindow
{
public:
    QWidget *centralwidget;
    QPushButton *openImgButton;
    QPushButton *flipVerticalButton;
    QLabel *label;
    QPushButton *flipHorButton;
    QPushButton *flipHorVerButton;
    QPushButton *switchColorButton;
    QPushButton *saveImgButton;
    QMenuBar *menubar;
    QStatusBar *statusbar;

    void setupUi(QMainWindow *MainWindow)
    {
        if (MainWindow->objectName().isEmpty())
            MainWindow->setObjectName("MainWindow");
        MainWindow->resize(800, 600);
        centralwidget = new QWidget(MainWindow);
        centralwidget->setObjectName("centralwidget");
        openImgButton = new QPushButton(centralwidget);
        openImgButton->setObjectName("openImgButton");
        openImgButton->setGeometry(QRect(30, 20, 101, 41));
        flipVerticalButton = new QPushButton(centralwidget);
        flipVerticalButton->setObjectName("flipVerticalButton");
        flipVerticalButton->setGeometry(QRect(30, 90, 101, 41));
        label = new QLabel(centralwidget);
        label->setObjectName("label");
        label->setGeometry(QRect(280, 30, 491, 311));
        flipHorButton = new QPushButton(centralwidget);
        flipHorButton->setObjectName("flipHorButton");
        flipHorButton->setGeometry(QRect(30, 160, 101, 41));
        flipHorVerButton = new QPushButton(centralwidget);
        flipHorVerButton->setObjectName("flipHorVerButton");
        flipHorVerButton->setGeometry(QRect(30, 230, 101, 41));
        switchColorButton = new QPushButton(centralwidget);
        switchColorButton->setObjectName("switchColorButton");
        switchColorButton->setGeometry(QRect(30, 300, 161, 41));
        saveImgButton = new QPushButton(centralwidget);
        saveImgButton->setObjectName("saveImgButton");
        saveImgButton->setGeometry(QRect(30, 370, 101, 41));
        MainWindow->setCentralWidget(centralwidget);
        menubar = new QMenuBar(MainWindow);
        menubar->setObjectName("menubar");
        menubar->setGeometry(QRect(0, 0, 800, 21));
        MainWindow->setMenuBar(menubar);
        statusbar = new QStatusBar(MainWindow);
        statusbar->setObjectName("statusbar");
        MainWindow->setStatusBar(statusbar);

        retranslateUi(MainWindow);

        QMetaObject::connectSlotsByName(MainWindow);
    } // setupUi

    void retranslateUi(QMainWindow *MainWindow)
    {
        MainWindow->setWindowTitle(QCoreApplication::translate("MainWindow", "MainWindow", nullptr));
        openImgButton->setText(QCoreApplication::translate("MainWindow", "Open image", nullptr));
        flipVerticalButton->setText(QCoreApplication::translate("MainWindow", "Flip vertically", nullptr));
        label->setText(QString());
        flipHorButton->setText(QCoreApplication::translate("MainWindow", "Flip horizontally", nullptr));
        flipHorVerButton->setText(QCoreApplication::translate("MainWindow", "Flip hor/ver", nullptr));
        switchColorButton->setText(QCoreApplication::translate("MainWindow", "Switch colors (RGB <-> BGR)", nullptr));
        saveImgButton->setText(QCoreApplication::translate("MainWindow", "Save image", nullptr));
    } // retranslateUi

};

namespace Ui {
    class MainWindow: public Ui_MainWindow {};
} // namespace Ui

QT_END_NAMESPACE

#endif // UI_MAINWINDOW_H
