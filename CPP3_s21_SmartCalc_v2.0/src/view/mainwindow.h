#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QDebug>
#include <QKeyEvent>
#include <QMainWindow>
#include <QTabBar>
#include <QTimer>
#include <QtWidgets>

#include "./../controller/smartCalculController.h"

QT_BEGIN_NAMESPACE
namespace Ui {
class MainWindow;
}
QT_END_NAMESPACE

namespace s21 {
class MainWindow : public QMainWindow {
  Q_OBJECT

 public:
  MainWindow(QWidget *parent = nullptr);
  ~MainWindow();

 protected:
  void keyPressEvent(QKeyEvent *e) override;
 private slots:
  void clickedRightWidget();
  void clickedLeftWidget();
  void bigSizeButtonActivateStyle();
  void smallSizeButtonActivateStyle();
  void PressPushButtonEqual();
  void TimerSlot();

 private:
  void decreaseMainWindowSize();
  void increaseMainWindowSize();
  void Calculation();
  void BuildGraph();
  QString CalcGraphY();
  void CalcGraphYPushToVector();
  void changeAnimationStatus(int flag_anim);
 private slots:
  void on_dial_speed_graph_valueChanged(int value);
  void clickedButtonTurn();
  void clickedButtonOff();

 private:
  Ui::MainWindow *ui;
  void setInterfaceStyle();
  s21::SmartCalculController *controller_;

  double x_begin, x_end, y_begin, y_end;
  double h = 0.1, x_input_graph, buff;
  int N;
  QVector<double> x, y;
  QTimer *timer;
  int time = 20;
  int anim_status = 0;
};
}  // namespace s21
#endif  // MAINWINDOW_H
