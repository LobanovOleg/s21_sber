QT       += core gui printsupport

greaterThan(QT_MAJOR_VERSION, 4): QT += widgets

CONFIG += c++17

# You can make your code fail to compile if it uses deprecated APIs.
# In order to do so, uncomment the following line.
#DEFINES += QT_DISABLE_DEPRECATED_BEFORE=0x060000    # disables all the APIs deprecated before Qt 6.0.0

SOURCES += \
    ../smart_calc_controller.c \
    ../mechanic/calculate.c \
    ../mechanic/deposit_calc.c \
    ../mechanic/input_validation.c \
    ../mechanic/loan_calc.c \
    ../mechanic/shunting_yard.c \
    ../mechanic/stack.c \
    ../mechanic/tokens_devider.c \
    about.cpp \
    credit.cpp \
    deposit.cpp \
    main.cpp \
    mainwindow.cpp \
    plot.cpp \
    qcustomplot.cpp \
    rpn.cpp

HEADERS += \
    ../smart_calc_controller.h \
    ../mechanic/calculate.h \
    ../mechanic/deposit_calc.h \
    ../mechanic/input_validation.h \
    ../mechanic/loan_calc.h \
    ../mechanic/shunting_yard.h \
    ../mechanic/stack.h \
    ../mechanic/tokens_devider.h \
    about.h \
    credit.h \
    deposit.h \
    mainwindow.h \
    plot.h \
    qcustomplot.h \
    rpn.h

FORMS += \
    about.ui \
    credit.ui \
    deposit.ui \
    mainwindow.ui \
    plot.ui \
    rpn.ui

# Default rules for deployment.
qnx: target.path = /tmp/$${TARGET}/bin
else: unix:!android: target.path = /opt/$${TARGET}/bin
!isEmpty(target.path): INSTALLS += target

RESOURCES += \
    fonts.qrc \
    resourses.qrc

DISTFILES +=