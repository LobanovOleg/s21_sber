QT       += core gui opengl openglwidgets

greaterThan(QT_MAJOR_VERSION, 4): QT += widgets

CONFIG += c++17 -Wno-error=deprecated-declarations

# You can make your code fail to compile if it uses deprecated APIs.
# In order to do so, uncomment the following line.
#DEFINES += QT_DISABLE_DEPRECATED_BEFORE=0x060000    # disables all the APIs deprecated before Qt 6.0.0

SOURCES += main.cpp \
    mainwindow.cpp \
    myopenglwidget.cpp \
    C/edges.c \
    C/figure.c \
    C/point.c \
    C/points.c \
    C/faces.c \
    gifimage/qgifimage.cpp \
    ./3rdParty/giflib/dgif_lib.c \
    ./3rdParty/giflib/egif_lib.c \
    ./3rdParty/giflib/gif_err.c \
    ./3rdParty/giflib/gif_font.c \
    ./3rdParty/giflib/gif_hash.c \
    ./3rdParty/giflib/gifalloc.c \
    ./3rdParty/giflib/quantize.c \



HEADERS += mainwindow.h \
    myopenglwidget.h \
    C/edges.h \
    C/figure.h \
    C/point.h \
    C/points.h \
    C/faces.h \
    C/errors.h \
    gifimage/qgifimage.h
    ./3rdParty/giflib/gif_lib.h
    ./3rdParty/giflib/gif_hash.h
    ./3rdParty/giflib/gif_lib_private.h


FORMS += \
    mainwindow.ui

INCLUDEPATH =  \
    ./ \
    ./C \
    ./gifimage
    ./3rdParty


# Default rules for deployment.
qnx: target.path = /tmp/$${TARGET}/bin
else: unix:!android: target.path = /opt/$${TARGET}/bin
!isEmpty(target.path): INSTALLS += target
