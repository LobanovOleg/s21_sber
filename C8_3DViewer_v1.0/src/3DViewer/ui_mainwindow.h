/********************************************************************************
** Form generated from reading UI file 'mainwindow.ui'
**
** Created by: Qt User Interface Compiler version 6.2.3
**
** WARNING! All changes made in this file will be lost when recompiling UI file!
********************************************************************************/

#ifndef UI_MAINWINDOW_H
#define UI_MAINWINDOW_H

#include <QtCore/QVariant>
#include <QtGui/QAction>
#include <QtWidgets/QApplication>
#include <QtWidgets/QComboBox>
#include <QtWidgets/QDoubleSpinBox>
#include <QtWidgets/QGridLayout>
#include <QtWidgets/QGroupBox>
#include <QtWidgets/QHBoxLayout>
#include <QtWidgets/QLabel>
#include <QtWidgets/QMainWindow>
#include <QtWidgets/QMenu>
#include <QtWidgets/QMenuBar>
#include <QtWidgets/QRadioButton>
#include <QtWidgets/QSlider>
#include <QtWidgets/QSpinBox>
#include <QtWidgets/QStatusBar>
#include <QtWidgets/QVBoxLayout>
#include <QtWidgets/QWidget>
#include <myopenglwidget.h>

QT_BEGIN_NAMESPACE

class Ui_MainWindow
{
public:
    QAction *actionLoad_file;
    QAction *actionbmp;
    QAction *actionjpeg;
    QAction *actionMake_video;
    QWidget *centralwidget;
    QHBoxLayout *horizontalLayout;
    QGroupBox *verticalGroupBox;
    QVBoxLayout *verticalLayout;
    QGroupBox *gridGroupBox_2;
    QGridLayout *gridLayout_2;
    QSlider *moveYSlider;
    QSpinBox *turnXBox;
    QSlider *turnYSlider;
    QLabel *label_6;
    QSlider *turnXSlider;
    QLabel *label_5;
    QSlider *moveXSlider;
    QLabel *label_7;
    QSpinBox *turnZBox;
    QDoubleSpinBox *moveZBox;
    QLabel *label_4;
    QLabel *label_2;
    QLabel *label_3;
    QDoubleSpinBox *scaleBox;
    QSlider *scaleSlider;
    QDoubleSpinBox *moveXBox;
    QLabel *label;
    QDoubleSpinBox *moveYBox;
    QSlider *turnZSlider;
    QSpinBox *turnYBox;
    QSlider *moveZSlider;
    QGroupBox *horizontalGroupBox;
    QHBoxLayout *horizontalLayout_2;
    QLabel *label_projection;
    QRadioButton *button_parallel;
    QRadioButton *button_perspective;
    QGroupBox *gridGroupBox;
    QGridLayout *gridLayout_3;
    QLabel *label_edges_width;
    QSlider *slider_edges_width;
    QLabel *label_vertices_type;
    QLabel *label_vertices_width;
    QSlider *slider_vertices_width;
    QLabel *label_edges_type;
    QComboBox *box_vertices_type;
    QComboBox *box_edges_type;
    QGroupBox *gridGroupBox1;
    QGridLayout *gridLayout;
    QLabel *label_9;
    QComboBox *vertices_color;
    QComboBox *edges_color;
    QLabel *label_8;
    QLabel *labelRed;
    QComboBox *background_color;
    MyOpenGLWidget *picture;
    QMenuBar *menubar;
    QMenu *menuMenu;
    QMenu *menuMake_screenshot;
    QStatusBar *statusbar;

    void setupUi(QMainWindow *MainWindow)
    {
        if (MainWindow->objectName().isEmpty())
            MainWindow->setObjectName(QString::fromUtf8("MainWindow"));
        MainWindow->resize(1200, 804);
        actionLoad_file = new QAction(MainWindow);
        actionLoad_file->setObjectName(QString::fromUtf8("actionLoad_file"));
        actionbmp = new QAction(MainWindow);
        actionbmp->setObjectName(QString::fromUtf8("actionbmp"));
        actionjpeg = new QAction(MainWindow);
        actionjpeg->setObjectName(QString::fromUtf8("actionjpeg"));
        actionMake_video = new QAction(MainWindow);
        actionMake_video->setObjectName(QString::fromUtf8("actionMake_video"));
        centralwidget = new QWidget(MainWindow);
        centralwidget->setObjectName(QString::fromUtf8("centralwidget"));
        horizontalLayout = new QHBoxLayout(centralwidget);
        horizontalLayout->setObjectName(QString::fromUtf8("horizontalLayout"));
        verticalGroupBox = new QGroupBox(centralwidget);
        verticalGroupBox->setObjectName(QString::fromUtf8("verticalGroupBox"));
        QSizePolicy sizePolicy(QSizePolicy::Preferred, QSizePolicy::Preferred);
        sizePolicy.setHorizontalStretch(1);
        sizePolicy.setVerticalStretch(0);
        sizePolicy.setHeightForWidth(verticalGroupBox->sizePolicy().hasHeightForWidth());
        verticalGroupBox->setSizePolicy(sizePolicy);
        verticalLayout = new QVBoxLayout(verticalGroupBox);
        verticalLayout->setObjectName(QString::fromUtf8("verticalLayout"));
        gridGroupBox_2 = new QGroupBox(verticalGroupBox);
        gridGroupBox_2->setObjectName(QString::fromUtf8("gridGroupBox_2"));
        QSizePolicy sizePolicy1(QSizePolicy::Preferred, QSizePolicy::Preferred);
        sizePolicy1.setHorizontalStretch(0);
        sizePolicy1.setVerticalStretch(3);
        sizePolicy1.setHeightForWidth(gridGroupBox_2->sizePolicy().hasHeightForWidth());
        gridGroupBox_2->setSizePolicy(sizePolicy1);
        gridLayout_2 = new QGridLayout(gridGroupBox_2);
        gridLayout_2->setObjectName(QString::fromUtf8("gridLayout_2"));
        moveYSlider = new QSlider(gridGroupBox_2);
        moveYSlider->setObjectName(QString::fromUtf8("moveYSlider"));
        moveYSlider->setMinimum(-200);
        moveYSlider->setMaximum(200);
        moveYSlider->setOrientation(Qt::Horizontal);

        gridLayout_2->addWidget(moveYSlider, 1, 1, 1, 1);

        turnXBox = new QSpinBox(gridGroupBox_2);
        turnXBox->setObjectName(QString::fromUtf8("turnXBox"));
        turnXBox->setMinimum(-360);
        turnXBox->setMaximum(360);

        gridLayout_2->addWidget(turnXBox, 3, 2, 1, 1);

        turnYSlider = new QSlider(gridGroupBox_2);
        turnYSlider->setObjectName(QString::fromUtf8("turnYSlider"));
        turnYSlider->setMinimum(-360);
        turnYSlider->setMaximum(360);
        turnYSlider->setOrientation(Qt::Horizontal);

        gridLayout_2->addWidget(turnYSlider, 4, 1, 1, 1);

        label_6 = new QLabel(gridGroupBox_2);
        label_6->setObjectName(QString::fromUtf8("label_6"));

        gridLayout_2->addWidget(label_6, 5, 0, 1, 1);

        turnXSlider = new QSlider(gridGroupBox_2);
        turnXSlider->setObjectName(QString::fromUtf8("turnXSlider"));
        turnXSlider->setMinimum(-360);
        turnXSlider->setMaximum(360);
        turnXSlider->setOrientation(Qt::Horizontal);

        gridLayout_2->addWidget(turnXSlider, 3, 1, 1, 1);

        label_5 = new QLabel(gridGroupBox_2);
        label_5->setObjectName(QString::fromUtf8("label_5"));

        gridLayout_2->addWidget(label_5, 4, 0, 1, 1);

        moveXSlider = new QSlider(gridGroupBox_2);
        moveXSlider->setObjectName(QString::fromUtf8("moveXSlider"));
        moveXSlider->setMinimum(-200);
        moveXSlider->setMaximum(200);
        moveXSlider->setOrientation(Qt::Horizontal);

        gridLayout_2->addWidget(moveXSlider, 0, 1, 1, 1);

        label_7 = new QLabel(gridGroupBox_2);
        label_7->setObjectName(QString::fromUtf8("label_7"));

        gridLayout_2->addWidget(label_7, 6, 0, 1, 1);

        turnZBox = new QSpinBox(gridGroupBox_2);
        turnZBox->setObjectName(QString::fromUtf8("turnZBox"));
        turnZBox->setMinimum(-360);
        turnZBox->setMaximum(360);

        gridLayout_2->addWidget(turnZBox, 5, 2, 1, 1);

        moveZBox = new QDoubleSpinBox(gridGroupBox_2);
        moveZBox->setObjectName(QString::fromUtf8("moveZBox"));
        moveZBox->setMinimum(-2.000000000000000);
        moveZBox->setMaximum(2.000000000000000);
        moveZBox->setSingleStep(0.010000000000000);

        gridLayout_2->addWidget(moveZBox, 2, 2, 1, 1);

        label_4 = new QLabel(gridGroupBox_2);
        label_4->setObjectName(QString::fromUtf8("label_4"));

        gridLayout_2->addWidget(label_4, 3, 0, 1, 1);

        label_2 = new QLabel(gridGroupBox_2);
        label_2->setObjectName(QString::fromUtf8("label_2"));

        gridLayout_2->addWidget(label_2, 1, 0, 1, 1);

        label_3 = new QLabel(gridGroupBox_2);
        label_3->setObjectName(QString::fromUtf8("label_3"));

        gridLayout_2->addWidget(label_3, 2, 0, 1, 1);

        scaleBox = new QDoubleSpinBox(gridGroupBox_2);
        scaleBox->setObjectName(QString::fromUtf8("scaleBox"));
        scaleBox->setDecimals(2);
        scaleBox->setMinimum(0.010000000000000);
        scaleBox->setMaximum(10.000000000000000);
        scaleBox->setSingleStep(0.010000000000000);
        scaleBox->setValue(1.000000000000000);

        gridLayout_2->addWidget(scaleBox, 6, 2, 1, 1);

        scaleSlider = new QSlider(gridGroupBox_2);
        scaleSlider->setObjectName(QString::fromUtf8("scaleSlider"));
        scaleSlider->setMaximum(100);
        scaleSlider->setValue(50);
        scaleSlider->setOrientation(Qt::Horizontal);

        gridLayout_2->addWidget(scaleSlider, 6, 1, 1, 1);

        moveXBox = new QDoubleSpinBox(gridGroupBox_2);
        moveXBox->setObjectName(QString::fromUtf8("moveXBox"));
        moveXBox->setMinimum(-2.000000000000000);
        moveXBox->setMaximum(2.000000000000000);
        moveXBox->setSingleStep(0.010000000000000);

        gridLayout_2->addWidget(moveXBox, 0, 2, 1, 1);

        label = new QLabel(gridGroupBox_2);
        label->setObjectName(QString::fromUtf8("label"));

        gridLayout_2->addWidget(label, 0, 0, 1, 1);

        moveYBox = new QDoubleSpinBox(gridGroupBox_2);
        moveYBox->setObjectName(QString::fromUtf8("moveYBox"));
        moveYBox->setMinimum(-2.000000000000000);
        moveYBox->setMaximum(2.000000000000000);
        moveYBox->setSingleStep(0.010000000000000);

        gridLayout_2->addWidget(moveYBox, 1, 2, 1, 1);

        turnZSlider = new QSlider(gridGroupBox_2);
        turnZSlider->setObjectName(QString::fromUtf8("turnZSlider"));
        turnZSlider->setMinimum(-360);
        turnZSlider->setMaximum(360);
        turnZSlider->setOrientation(Qt::Horizontal);

        gridLayout_2->addWidget(turnZSlider, 5, 1, 1, 1);

        turnYBox = new QSpinBox(gridGroupBox_2);
        turnYBox->setObjectName(QString::fromUtf8("turnYBox"));
        turnYBox->setMinimum(-360);
        turnYBox->setMaximum(360);

        gridLayout_2->addWidget(turnYBox, 4, 2, 1, 1);

        moveZSlider = new QSlider(gridGroupBox_2);
        moveZSlider->setObjectName(QString::fromUtf8("moveZSlider"));
        moveZSlider->setMinimum(-200);
        moveZSlider->setMaximum(200);
        moveZSlider->setOrientation(Qt::Horizontal);

        gridLayout_2->addWidget(moveZSlider, 2, 1, 1, 1);


        verticalLayout->addWidget(gridGroupBox_2);

        horizontalGroupBox = new QGroupBox(verticalGroupBox);
        horizontalGroupBox->setObjectName(QString::fromUtf8("horizontalGroupBox"));
        horizontalLayout_2 = new QHBoxLayout(horizontalGroupBox);
        horizontalLayout_2->setObjectName(QString::fromUtf8("horizontalLayout_2"));
        label_projection = new QLabel(horizontalGroupBox);
        label_projection->setObjectName(QString::fromUtf8("label_projection"));

        horizontalLayout_2->addWidget(label_projection);

        button_parallel = new QRadioButton(horizontalGroupBox);
        button_parallel->setObjectName(QString::fromUtf8("button_parallel"));
        button_parallel->setChecked(true);

        horizontalLayout_2->addWidget(button_parallel);

        button_perspective = new QRadioButton(horizontalGroupBox);
        button_perspective->setObjectName(QString::fromUtf8("button_perspective"));
        button_perspective->setChecked(false);

        horizontalLayout_2->addWidget(button_perspective);


        verticalLayout->addWidget(horizontalGroupBox);

        gridGroupBox = new QGroupBox(verticalGroupBox);
        gridGroupBox->setObjectName(QString::fromUtf8("gridGroupBox"));
        gridLayout_3 = new QGridLayout(gridGroupBox);
        gridLayout_3->setObjectName(QString::fromUtf8("gridLayout_3"));
        label_edges_width = new QLabel(gridGroupBox);
        label_edges_width->setObjectName(QString::fromUtf8("label_edges_width"));

        gridLayout_3->addWidget(label_edges_width, 1, 0, 1, 1);

        slider_edges_width = new QSlider(gridGroupBox);
        slider_edges_width->setObjectName(QString::fromUtf8("slider_edges_width"));
        slider_edges_width->setMinimum(10);
        slider_edges_width->setMaximum(250);
        slider_edges_width->setValue(10);
        slider_edges_width->setOrientation(Qt::Horizontal);

        gridLayout_3->addWidget(slider_edges_width, 1, 1, 1, 1);

        label_vertices_type = new QLabel(gridGroupBox);
        label_vertices_type->setObjectName(QString::fromUtf8("label_vertices_type"));

        gridLayout_3->addWidget(label_vertices_type, 2, 0, 1, 1);

        label_vertices_width = new QLabel(gridGroupBox);
        label_vertices_width->setObjectName(QString::fromUtf8("label_vertices_width"));

        gridLayout_3->addWidget(label_vertices_width, 0, 0, 1, 1);

        slider_vertices_width = new QSlider(gridGroupBox);
        slider_vertices_width->setObjectName(QString::fromUtf8("slider_vertices_width"));
        slider_vertices_width->setMinimum(10);
        slider_vertices_width->setMaximum(1000);
        slider_vertices_width->setValue(10);
        slider_vertices_width->setOrientation(Qt::Horizontal);

        gridLayout_3->addWidget(slider_vertices_width, 0, 1, 1, 1);

        label_edges_type = new QLabel(gridGroupBox);
        label_edges_type->setObjectName(QString::fromUtf8("label_edges_type"));

        gridLayout_3->addWidget(label_edges_type, 3, 0, 1, 1);

        box_vertices_type = new QComboBox(gridGroupBox);
        box_vertices_type->addItem(QString());
        box_vertices_type->addItem(QString());
        box_vertices_type->addItem(QString());
        box_vertices_type->setObjectName(QString::fromUtf8("box_vertices_type"));

        gridLayout_3->addWidget(box_vertices_type, 2, 1, 1, 1);

        box_edges_type = new QComboBox(gridGroupBox);
        box_edges_type->addItem(QString());
        box_edges_type->addItem(QString());
        box_edges_type->setObjectName(QString::fromUtf8("box_edges_type"));

        gridLayout_3->addWidget(box_edges_type, 3, 1, 1, 1);


        verticalLayout->addWidget(gridGroupBox);

        gridGroupBox1 = new QGroupBox(verticalGroupBox);
        gridGroupBox1->setObjectName(QString::fromUtf8("gridGroupBox1"));
        QSizePolicy sizePolicy2(QSizePolicy::Preferred, QSizePolicy::Preferred);
        sizePolicy2.setHorizontalStretch(0);
        sizePolicy2.setVerticalStretch(2);
        sizePolicy2.setHeightForWidth(gridGroupBox1->sizePolicy().hasHeightForWidth());
        gridGroupBox1->setSizePolicy(sizePolicy2);
        gridLayout = new QGridLayout(gridGroupBox1);
        gridLayout->setObjectName(QString::fromUtf8("gridLayout"));
        label_9 = new QLabel(gridGroupBox1);
        label_9->setObjectName(QString::fromUtf8("label_9"));

        gridLayout->addWidget(label_9, 2, 0, 1, 1);

        vertices_color = new QComboBox(gridGroupBox1);
        vertices_color->addItem(QString());
        vertices_color->addItem(QString());
        vertices_color->addItem(QString());
        vertices_color->addItem(QString());
        vertices_color->addItem(QString());
        vertices_color->addItem(QString());
        vertices_color->addItem(QString());
        vertices_color->addItem(QString());
        vertices_color->addItem(QString());
        vertices_color->setObjectName(QString::fromUtf8("vertices_color"));

        gridLayout->addWidget(vertices_color, 1, 1, 1, 1);

        edges_color = new QComboBox(gridGroupBox1);
        edges_color->addItem(QString());
        edges_color->addItem(QString());
        edges_color->addItem(QString());
        edges_color->addItem(QString());
        edges_color->addItem(QString());
        edges_color->addItem(QString());
        edges_color->addItem(QString());
        edges_color->addItem(QString());
        edges_color->addItem(QString());
        edges_color->setObjectName(QString::fromUtf8("edges_color"));

        gridLayout->addWidget(edges_color, 2, 1, 1, 1);

        label_8 = new QLabel(gridGroupBox1);
        label_8->setObjectName(QString::fromUtf8("label_8"));

        gridLayout->addWidget(label_8, 1, 0, 1, 1);

        labelRed = new QLabel(gridGroupBox1);
        labelRed->setObjectName(QString::fromUtf8("labelRed"));

        gridLayout->addWidget(labelRed, 0, 0, 1, 1);

        background_color = new QComboBox(gridGroupBox1);
        background_color->addItem(QString());
        background_color->addItem(QString());
        background_color->addItem(QString());
        background_color->addItem(QString());
        background_color->addItem(QString());
        background_color->addItem(QString());
        background_color->addItem(QString());
        background_color->addItem(QString());
        background_color->addItem(QString());
        background_color->setObjectName(QString::fromUtf8("background_color"));

        gridLayout->addWidget(background_color, 0, 1, 1, 1);


        verticalLayout->addWidget(gridGroupBox1);


        horizontalLayout->addWidget(verticalGroupBox);

        picture = new MyOpenGLWidget(centralwidget);
        picture->setObjectName(QString::fromUtf8("picture"));
        QSizePolicy sizePolicy3(QSizePolicy::Preferred, QSizePolicy::Preferred);
        sizePolicy3.setHorizontalStretch(3);
        sizePolicy3.setVerticalStretch(0);
        sizePolicy3.setHeightForWidth(picture->sizePolicy().hasHeightForWidth());
        picture->setSizePolicy(sizePolicy3);

        horizontalLayout->addWidget(picture);

        MainWindow->setCentralWidget(centralwidget);
        menubar = new QMenuBar(MainWindow);
        menubar->setObjectName(QString::fromUtf8("menubar"));
        menubar->setGeometry(QRect(0, 0, 1200, 24));
        menuMenu = new QMenu(menubar);
        menuMenu->setObjectName(QString::fromUtf8("menuMenu"));
        menuMake_screenshot = new QMenu(menuMenu);
        menuMake_screenshot->setObjectName(QString::fromUtf8("menuMake_screenshot"));
        MainWindow->setMenuBar(menubar);
        statusbar = new QStatusBar(MainWindow);
        statusbar->setObjectName(QString::fromUtf8("statusbar"));
        MainWindow->setStatusBar(statusbar);

        menubar->addAction(menuMenu->menuAction());
        menuMenu->addAction(actionLoad_file);
        menuMenu->addAction(menuMake_screenshot->menuAction());
        menuMenu->addAction(actionMake_video);
        menuMake_screenshot->addAction(actionbmp);
        menuMake_screenshot->addAction(actionjpeg);

        retranslateUi(MainWindow);

        vertices_color->setCurrentIndex(1);
        edges_color->setCurrentIndex(2);


        QMetaObject::connectSlotsByName(MainWindow);
    } // setupUi

    void retranslateUi(QMainWindow *MainWindow)
    {
        MainWindow->setWindowTitle(QCoreApplication::translate("MainWindow", "MainWindow", nullptr));
        actionLoad_file->setText(QCoreApplication::translate("MainWindow", "Load file", nullptr));
        actionbmp->setText(QCoreApplication::translate("MainWindow", "bmp", nullptr));
        actionjpeg->setText(QCoreApplication::translate("MainWindow", "jpeg", nullptr));
        actionMake_video->setText(QCoreApplication::translate("MainWindow", "Make video", nullptr));
        label_6->setText(QCoreApplication::translate("MainWindow", "Turn z", nullptr));
        label_5->setText(QCoreApplication::translate("MainWindow", "Turn y", nullptr));
        label_7->setText(QCoreApplication::translate("MainWindow", "Scale", nullptr));
        label_4->setText(QCoreApplication::translate("MainWindow", "Turn x", nullptr));
        label_2->setText(QCoreApplication::translate("MainWindow", "Move y", nullptr));
        label_3->setText(QCoreApplication::translate("MainWindow", "Move z", nullptr));
        label->setText(QCoreApplication::translate("MainWindow", "Move x", nullptr));
        label_projection->setText(QCoreApplication::translate("MainWindow", "Projection", nullptr));
        button_parallel->setText(QCoreApplication::translate("MainWindow", "Parallel", nullptr));
        button_perspective->setText(QCoreApplication::translate("MainWindow", "Perspective", nullptr));
        label_edges_width->setText(QCoreApplication::translate("MainWindow", "Edges width", nullptr));
        label_vertices_type->setText(QCoreApplication::translate("MainWindow", "Vertices type", nullptr));
        label_vertices_width->setText(QCoreApplication::translate("MainWindow", "Vertices width", nullptr));
        label_edges_type->setText(QCoreApplication::translate("MainWindow", "Edges type", nullptr));
        box_vertices_type->setItemText(0, QCoreApplication::translate("MainWindow", "None", nullptr));
        box_vertices_type->setItemText(1, QCoreApplication::translate("MainWindow", "Square", nullptr));
        box_vertices_type->setItemText(2, QCoreApplication::translate("MainWindow", "Circle", nullptr));

        box_edges_type->setItemText(0, QCoreApplication::translate("MainWindow", "Solid", nullptr));
        box_edges_type->setItemText(1, QCoreApplication::translate("MainWindow", "Dotted", nullptr));

        label_9->setText(QCoreApplication::translate("MainWindow", "Edges", nullptr));
        vertices_color->setItemText(0, QCoreApplication::translate("MainWindow", "Black", nullptr));
        vertices_color->setItemText(1, QCoreApplication::translate("MainWindow", "White", nullptr));
        vertices_color->setItemText(2, QCoreApplication::translate("MainWindow", "Red", nullptr));
        vertices_color->setItemText(3, QCoreApplication::translate("MainWindow", "Orange", nullptr));
        vertices_color->setItemText(4, QCoreApplication::translate("MainWindow", "Yellow", nullptr));
        vertices_color->setItemText(5, QCoreApplication::translate("MainWindow", "Green", nullptr));
        vertices_color->setItemText(6, QCoreApplication::translate("MainWindow", "Blue", nullptr));
        vertices_color->setItemText(7, QCoreApplication::translate("MainWindow", "Purple", nullptr));
        vertices_color->setItemText(8, QCoreApplication::translate("MainWindow", "Pink", nullptr));

        edges_color->setItemText(0, QCoreApplication::translate("MainWindow", "Black", nullptr));
        edges_color->setItemText(1, QCoreApplication::translate("MainWindow", "White", nullptr));
        edges_color->setItemText(2, QCoreApplication::translate("MainWindow", "Red", nullptr));
        edges_color->setItemText(3, QCoreApplication::translate("MainWindow", "Orange", nullptr));
        edges_color->setItemText(4, QCoreApplication::translate("MainWindow", "Yellow", nullptr));
        edges_color->setItemText(5, QCoreApplication::translate("MainWindow", "Green", nullptr));
        edges_color->setItemText(6, QCoreApplication::translate("MainWindow", "Blue", nullptr));
        edges_color->setItemText(7, QCoreApplication::translate("MainWindow", "Purple", nullptr));
        edges_color->setItemText(8, QCoreApplication::translate("MainWindow", "Pink", nullptr));

        label_8->setText(QCoreApplication::translate("MainWindow", "Vertices", nullptr));
        labelRed->setText(QCoreApplication::translate("MainWindow", "Background", nullptr));
        background_color->setItemText(0, QCoreApplication::translate("MainWindow", "Black", nullptr));
        background_color->setItemText(1, QCoreApplication::translate("MainWindow", "White", nullptr));
        background_color->setItemText(2, QCoreApplication::translate("MainWindow", "Red", nullptr));
        background_color->setItemText(3, QCoreApplication::translate("MainWindow", "Orange", nullptr));
        background_color->setItemText(4, QCoreApplication::translate("MainWindow", "Yellow", nullptr));
        background_color->setItemText(5, QCoreApplication::translate("MainWindow", "Green", nullptr));
        background_color->setItemText(6, QCoreApplication::translate("MainWindow", "Blue", nullptr));
        background_color->setItemText(7, QCoreApplication::translate("MainWindow", "Purple", nullptr));
        background_color->setItemText(8, QCoreApplication::translate("MainWindow", "Pink", nullptr));

        menuMenu->setTitle(QCoreApplication::translate("MainWindow", "Menu", nullptr));
        menuMake_screenshot->setTitle(QCoreApplication::translate("MainWindow", "Make screenshot", nullptr));
    } // retranslateUi

};

namespace Ui {
    class MainWindow: public Ui_MainWindow {};
} // namespace Ui

QT_END_NAMESPACE

#endif // UI_MAINWINDOW_H
