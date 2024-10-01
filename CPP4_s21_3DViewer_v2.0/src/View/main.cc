#include <QApplication>

#include "../Controller/s21_controller.h"
#include "mainwindow.h"

int main(int argc, char *argv[]) {
  QApplication a(argc, argv);
  [[maybe_unused]] s21::Controller *controller = s21::Controller::Get();
  s21::MainWindow w;
  w.show();
  return a.exec();
}
