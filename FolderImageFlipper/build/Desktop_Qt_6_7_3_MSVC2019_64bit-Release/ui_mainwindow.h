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
#include <QtWidgets/QGroupBox>
#include <QtWidgets/QMainWindow>
#include <QtWidgets/QMenuBar>
#include <QtWidgets/QPushButton>
#include <QtWidgets/QRadioButton>
#include <QtWidgets/QStatusBar>
#include <QtWidgets/QWidget>

QT_BEGIN_NAMESPACE

class Ui_MainWindow
{
public:
    QWidget *centralwidget;
    QPushButton *openImgButton;
    QPushButton *saveImgButton;
    QGroupBox *groupBox;
    QRadioButton *flipVerButton;
    QRadioButton *flipHorButton;
    QRadioButton *flipHorVerButton;
    QMenuBar *menubar;
    QStatusBar *statusbar;

    void setupUi(QMainWindow *MainWindow)
    {
        if (MainWindow->objectName().isEmpty())
            MainWindow->setObjectName("MainWindow");
        MainWindow->resize(800, 427);
        MainWindow->setCursor(QCursor(Qt::CursorShape::ArrowCursor));
        MainWindow->setIconSize(QSize(24, 24));
        centralwidget = new QWidget(MainWindow);
        centralwidget->setObjectName("centralwidget");
        openImgButton = new QPushButton(centralwidget);
        openImgButton->setObjectName("openImgButton");
        openImgButton->setGeometry(QRect(340, 70, 121, 41));
        saveImgButton = new QPushButton(centralwidget);
        saveImgButton->setObjectName("saveImgButton");
        saveImgButton->setGeometry(QRect(330, 280, 141, 41));
        groupBox = new QGroupBox(centralwidget);
        groupBox->setObjectName("groupBox");
        groupBox->setGeometry(QRect(160, 140, 491, 80));
        groupBox->setAutoFillBackground(false);
        groupBox->setCheckable(false);
        flipVerButton = new QRadioButton(groupBox);
        flipVerButton->setObjectName("flipVerButton");
        flipVerButton->setGeometry(QRect(50, 40, 91, 22));
        flipHorButton = new QRadioButton(groupBox);
        flipHorButton->setObjectName("flipHorButton");
        flipHorButton->setGeometry(QRect(190, 40, 101, 22));
        flipHorVerButton = new QRadioButton(groupBox);
        flipHorVerButton->setObjectName("flipHorVerButton");
        flipHorVerButton->setGeometry(QRect(340, 40, 101, 21));
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
        openImgButton->setText(QCoreApplication::translate("MainWindow", "Select Source Folder", nullptr));
        saveImgButton->setText(QCoreApplication::translate("MainWindow", "Select Destination Folder", nullptr));
        groupBox->setTitle(QString());
        flipVerButton->setText(QCoreApplication::translate("MainWindow", "Vertical Flip", nullptr));
        flipHorButton->setText(QCoreApplication::translate("MainWindow", "Horizontal Flip", nullptr));
        flipHorVerButton->setText(QCoreApplication::translate("MainWindow", "Flip Both Ways", nullptr));
    } // retranslateUi

};

namespace Ui {
    class MainWindow: public Ui_MainWindow {};
} // namespace Ui

QT_END_NAMESPACE

#endif // UI_MAINWINDOW_H
