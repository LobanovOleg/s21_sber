#include "mainwindow.h"

#include "qcustomplot.h"
#include "stylehelper.h"
#include "ui_mainwindow.h"

s21::MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent),
      ui(new Ui::MainWindow),
      controller_(new SmartCalculController) {
  ui->setupUi(this);
  ui->tabWidgetLeft->tabBar()->hide();
  ui->tabWidgetRight->tabBar()->hide();
  this->setMinimumSize(944, 856);
  this->setMaximumSize(944, 856);
  setInterfaceStyle();
  decreaseMainWindowSize();
  connect(ui->pushButton_0_, SIGNAL(clicked()), this,
          SLOT(clickedRightWidget()));
  connect(ui->pushButton_1_, SIGNAL(clicked()), this,
          SLOT(clickedRightWidget()));
  connect(ui->pushButton_2_, SIGNAL(clicked()), this,
          SLOT(clickedRightWidget()));
  connect(ui->pushButton_3_, SIGNAL(clicked()), this,
          SLOT(clickedRightWidget()));
  connect(ui->pushButton_4_, SIGNAL(clicked()), this,
          SLOT(clickedRightWidget()));
  connect(ui->pushButton_5_, SIGNAL(clicked()), this,
          SLOT(clickedRightWidget()));
  connect(ui->pushButton_6_, SIGNAL(clicked()), this,
          SLOT(clickedRightWidget()));
  connect(ui->pushButton_7_, SIGNAL(clicked()), this,
          SLOT(clickedRightWidget()));
  connect(ui->pushButton_8_, SIGNAL(clicked()), this,
          SLOT(clickedRightWidget()));
  connect(ui->pushButton_9_, SIGNAL(clicked()), this,
          SLOT(clickedRightWidget()));
  connect(ui->pushButton_ac_, SIGNAL(clicked()), this,
          SLOT(clickedRightWidget()));
  connect(ui->pushButton_del_, SIGNAL(clicked()), this,
          SLOT(clickedRightWidget()));
  connect(ui->pushButton_uminus_, SIGNAL(clicked()), this,
          SLOT(clickedRightWidget()));
  connect(ui->pushButton_div_, SIGNAL(clicked()), this,
          SLOT(clickedRightWidget()));
  connect(ui->pushButton_mult_, SIGNAL(clicked()), this,
          SLOT(clickedRightWidget()));
  connect(ui->pushButton_minus_, SIGNAL(clicked()), this,
          SLOT(clickedRightWidget()));
  connect(ui->pushButton_plus_, SIGNAL(clicked()), this,
          SLOT(clickedRightWidget()));
  connect(ui->pushButton_point_, SIGNAL(clicked()), this,
          SLOT(clickedRightWidget()));
  connect(ui->pushButton_equal_, SIGNAL(clicked()), this,
          SLOT(PressPushButtonEqual()));
  connect(ui->pushButton_big_size_, SIGNAL(clicked()), this,
          SLOT(bigSizeButtonActivateStyle()));
  connect(ui->pushButton_small_size_, SIGNAL(clicked()), this,
          SLOT(smallSizeButtonActivateStyle()));
  connect(ui->pushButton_bracket_right_, SIGNAL(clicked()), this,
          SLOT(clickedLeftWidget()));
  connect(ui->pushButton_bracket_left_, SIGNAL(clicked()), this,
          SLOT(clickedLeftWidget()));
  connect(ui->pushButton_x_, SIGNAL(clicked()), this,
          SLOT(clickedLeftWidget()));
  connect(ui->pushButton_mod_, SIGNAL(clicked()), this,
          SLOT(clickedLeftWidget()));
  connect(ui->pushButton_p_, SIGNAL(clicked()), this,
          SLOT(clickedLeftWidget()));
  connect(ui->pushButton_e_, SIGNAL(clicked()), this,
          SLOT(clickedLeftWidget()));
  connect(ui->pushButton_power_, SIGNAL(clicked()), this,
          SLOT(clickedLeftWidget()));
  connect(ui->pushButton_root_, SIGNAL(clicked()), this,
          SLOT(clickedLeftWidget()));
  connect(ui->pushButton_asin_, SIGNAL(clicked()), this,
          SLOT(clickedLeftWidget()));
  connect(ui->pushButton_sin_, SIGNAL(clicked()), this,
          SLOT(clickedLeftWidget()));
  connect(ui->pushButton_log_, SIGNAL(clicked()), this,
          SLOT(clickedLeftWidget()));
  connect(ui->pushButton_ln_, SIGNAL(clicked()), this,
          SLOT(clickedLeftWidget()));
  connect(ui->pushButton_acos_, SIGNAL(clicked()), this,
          SLOT(clickedLeftWidget()));
  connect(ui->pushButton_cos_, SIGNAL(clicked()), this,
          SLOT(clickedLeftWidget()));
  connect(ui->pushButton_atan_, SIGNAL(clicked()), this,
          SLOT(clickedLeftWidget()));
  connect(ui->pushButton_tan_, SIGNAL(clicked()), this,
          SLOT(clickedLeftWidget()));
  connect(ui->pushButton_graph_, SIGNAL(clicked()), this,
          SLOT(clickedLeftWidget()));
  connect(ui->pushButton_back_, SIGNAL(clicked()), this,
          SLOT(clickedLeftWidget()));
  connect(ui->pushButton_animation_turn, SIGNAL(clicked()), this,
          SLOT(clickedButtonTurn()));
  connect(ui->pushButton_animation_off, SIGNAL(clicked()), this,
          SLOT(clickedButtonOff()));
}

s21::MainWindow::~MainWindow() {
  delete ui;
  delete controller_;
}

void s21::MainWindow::keyPressEvent(QKeyEvent *e) {
  QString currentValueDeisplay = ui->display_input->text();
  if (e->key() >= Qt::Key_0 && e->key() <= Qt::Key_9) {
    ui->display_input->setText(currentValueDeisplay + (char)e->key());
  } else if (e->key() == Qt::Key_Delete) {
  }
}

void s21::MainWindow::setInterfaceStyle() {
  ui->widget->setBackground(Qt::GlobalColor::transparent);
  ui->tabWidgetLeft->setDocumentMode(true);
  ui->tabWidgetRight->setDocumentMode(true);
  ui->widget->xAxis->setTickLabelColor(Qt::white);
  ui->widget->yAxis->setTickLabelColor(Qt::white);

  ui->display_input->setStyleSheet(StyleHelper::getInputDisplayLabelStyle());
  ui->label_draw_speed->setStyleSheet(StyleHelper::getInputDisplayLabelStyle());
  ui->tabWidgetRight->setStyleSheet(StyleHelper::getRightWidgetButtonsStyle());
  ui->tabWidgetLeft->setStyleSheet(StyleHelper::getLeftWidgetButtonsStyle());
  ui->centralwidget->setStyleSheet(StyleHelper::getMainBackground());
  ui->pushButton_big_size_->setStyleSheet(
      StyleHelper::getSizeNonActiveButtonStyle());
  ui->pushButton_small_size_->setStyleSheet(
      StyleHelper::getSizeActiveButtonStyle());

  ui->label_xmax->setStyleSheet(StyleHelper::getGraphLabelXYStyle());
  ui->label_xmin->setStyleSheet(StyleHelper::getGraphLabelXYStyle());
  ui->label_ymax->setStyleSheet(StyleHelper::getGraphLabelXYStyle());
  ui->label_ymin->setStyleSheet(StyleHelper::getGraphLabelXYStyle());
  ui->spinBox_xmax_number->setButtonSymbols(QAbstractSpinBox::NoButtons);
  ui->spinBox_xmax_number->setStyleSheet(
      StyleHelper::getGraphLabelXYNumberStyle());
  ui->spinBox_xmin_number->setButtonSymbols(QAbstractSpinBox::NoButtons);
  ui->spinBox_xmin_number->setStyleSheet(
      StyleHelper::getGraphLabelXYNumberStyle());
  ui->spinBox_ymax_number->setButtonSymbols(QAbstractSpinBox::NoButtons);
  ui->spinBox_ymax_number->setStyleSheet(
      StyleHelper::getGraphLabelXYNumberStyle());
  ui->spinBox_ymin_number->setButtonSymbols(QAbstractSpinBox::NoButtons);
  ui->spinBox_ymin_number->setStyleSheet(
      StyleHelper::getGraphLabelXYNumberStyle());
  ui->widget_speed_graph->setStyleSheet(StyleHelper::getWidgetDrawSpeedStyle());

  ui->pushButton_animation_turn->setStyleSheet(
      StyleHelper::getAnimationTurnButtonStyle());
  ui->pushButton_animation_off->setStyleSheet(
      StyleHelper::getAnimationOffActiveButtonStyle());
}

void s21::MainWindow::clickedRightWidget() {
  QPushButton *button = (QPushButton *)sender();
  QString buttonValue = button->text();
  QString currentValueDeisplay = ui->display_input->text();
  size_t length_string = currentValueDeisplay.length();
  if (buttonValue == "⌫") {
    ui->display_input->setText(currentValueDeisplay.left(length_string - 1));
  } else if (buttonValue == "+/-") {
    if (length_string == 0) {
    } else if (length_string > 2 && currentValueDeisplay[0] == '-' &&
               currentValueDeisplay[1] == '(' &&
               currentValueDeisplay[length_string - 1] == ')') {
      ui->display_input->setText(
          currentValueDeisplay.mid(2, length_string - 3));
    } else {
      ui->display_input->setText("-(" + currentValueDeisplay + ')');
    }
  } else if (buttonValue == "AC") {
    ui->display_input->clear();
  } else if (buttonValue == "÷") {
    if (length_string != 0) {
      if (QString::compare(currentValueDeisplay[length_string - 1],
                           QString("/")[0], Qt::CaseInsensitive)) {
        ui->display_input->setText(currentValueDeisplay + '/');
      }
    } else {
      ui->display_input->setText(currentValueDeisplay + '/');
    }
  } else if (buttonValue == 'x') {
    if (length_string != 0) {
      if (QString::compare(currentValueDeisplay[length_string - 1],
                           QString("*")[0], Qt::CaseInsensitive)) {
        ui->display_input->setText(currentValueDeisplay + '*');
      }
    } else {
      ui->display_input->setText(currentValueDeisplay + '*');
    }
  } else if (buttonValue == '-') {
    if (length_string != 0) {
      if (QString::compare(currentValueDeisplay[length_string - 1],
                           QString("-")[0], Qt::CaseInsensitive)) {
        ui->display_input->setText(currentValueDeisplay + buttonValue);
      }
    } else {
      ui->display_input->setText(currentValueDeisplay + buttonValue);
    }
  } else if (buttonValue == '+') {
    if (length_string != 0) {
      if (QString::compare(currentValueDeisplay[length_string - 1],
                           QString("+")[0], Qt::CaseInsensitive)) {
        ui->display_input->setText(currentValueDeisplay + buttonValue);
      }
    } else {
      ui->display_input->setText(currentValueDeisplay + buttonValue);
    }
  } else if (buttonValue == '.') {
    for (size_t i = (length_string - 1); i >= 0 && i < length_string; --i) {
      if (currentValueDeisplay[i] == QString(".")[0]) {
        break;
      } else if (currentValueDeisplay[i] >= QString("0")[0] &&
                 currentValueDeisplay[i] <= QString("9")[0] && i == 0) {
        ui->display_input->setText(currentValueDeisplay + buttonValue);
      } else if (currentValueDeisplay[i] >= QString("0")[0] &&
                 currentValueDeisplay[i] <= QString("9")[0]) {
        continue;
      } else {
        ui->display_input->setText(currentValueDeisplay + buttonValue);
        break;
      }
    }
  } else {
    ui->display_input->setText(currentValueDeisplay + buttonValue);
  }
}

void s21::MainWindow::clickedLeftWidget() {
  QPushButton *button = (QPushButton *)sender();
  QString buttonValue = button->text();
  QString currentValueDeisplay = ui->display_input->text();
  if (buttonValue == "asin" || buttonValue == "sin" || buttonValue == "acos" ||
      buttonValue == "cos" || buttonValue == "atan" || buttonValue == "tan" ||
      buttonValue == "log" || buttonValue == "ln") {
    ui->display_input->setText(currentValueDeisplay + buttonValue + '(');
  } else if (buttonValue == "f(x)") {
    ui->display_input->setText(currentValueDeisplay + 'X');
  } else if (buttonValue == "Graph \n settings") {
    ui->tabWidgetLeft->setCurrentIndex(1);
  } else if (buttonValue == "BACK") {
    ui->tabWidgetLeft->setCurrentIndex(0);
  } else {
    ui->display_input->setText(currentValueDeisplay + buttonValue);
  }
}

void s21::MainWindow::decreaseMainWindowSize() {
  ui->widget->setMinimumSize(0, 0);
  ui->widget->setMaximumSize(0, 0);
  ui->tabWidgetLeft->setMinimumSize(0, 0);
  ui->tabWidgetLeft->setMaximumSize(0, 0);
  this->setMinimumSize(500, 500);
  this->setMaximumSize(500, 500);
  ui->display_input->setMinimumSize(450, 60);
  ui->display_input->setMaximumSize(450, 60);
}

void s21::MainWindow::increaseMainWindowSize() {
  ui->widget->setMinimumSize(918, 372);
  ui->widget->setMaximumSize(918, 372);
  ui->tabWidgetLeft->setMinimumSize(454, 304);
  ui->tabWidgetLeft->setMaximumSize(16777215, 16777215);
  this->setMinimumSize(944, 856);
  this->setMaximumSize(944, 856);
  ui->display_input->setMinimumSize(918, 60);
  ui->display_input->setMaximumSize(918, 60);
}

void s21::MainWindow::bigSizeButtonActivateStyle() {
  increaseMainWindowSize();
  ui->pushButton_big_size_->setStyleSheet(
      StyleHelper::getSizeActiveButtonStyle());
  ui->pushButton_small_size_->setStyleSheet(
      StyleHelper::getSizeNonActiveButtonStyle());
}

void s21::MainWindow::smallSizeButtonActivateStyle() {
  decreaseMainWindowSize();
  ui->pushButton_big_size_->setStyleSheet(
      StyleHelper::getSizeNonActiveButtonStyle());
  ui->pushButton_small_size_->setStyleSheet(
      StyleHelper::getSizeActiveButtonStyle());
}

void s21::MainWindow::PressPushButtonEqual() {
  QString current_value_display = ui->display_input->text();
  if (current_value_display.contains("ERROR")) {
  } else if (current_value_display.contains("X")) {
    BuildGraph();
  } else {
    Calculation();
  }
}

void s21::MainWindow::Calculation() {
  try {
    QString current_value_display = ui->display_input->text();
    QByteArray inBytes = current_value_display.toUtf8();
    double result = controller_->get_result(inBytes.constData());
    QString resultString = QString::number(result);
    ui->display_input->setText(resultString);
  } catch (std::invalid_argument const &excep) {
    ui->display_input->setText(excep.what());
  }
}

void s21::MainWindow::BuildGraph() {
  x_begin = ui->spinBox_xmin_number->text().toDouble();
  x_end = ui->spinBox_xmax_number->text().toDouble() + h;
  y_begin = ui->spinBox_ymin_number->text().toDouble();
  y_end = ui->spinBox_ymax_number->text().toDouble();

  x_input_graph = x_begin;
  x.clear();
  y.clear();
  ui->widget->clearGraphs();

  if (anim_status == 1) {
    N = (x_end - x_begin) / h + 2;

    timer = new QTimer(this);
    connect(timer, SIGNAL(timeout()), this, SLOT(TimerSlot()));
    timer->start(20);

    ui->widget->clearGraphs();
    x.clear();
    y.clear();
  } else {
    h = 0.1;
    ui->widget->addGraph();
    while (x_input_graph <= x_end) {
      CalcGraphYPushToVector();
    }
    ui->widget->graph(0)->addData(x, y);
    ui->widget->rescaleAxes();
    ui->widget->graph()->setPen(QPen(Qt::yellow));
    ui->widget->replot();

    ui->widget->setInteraction(QCP::iRangeZoom, true);
    ui->widget->setInteraction(QCP::iRangeDrag, true);

    x.clear();
    y.clear();
  }
}

void s21::MainWindow::TimerSlot() {
  if (time <= 20 * N) {
    if (x_input_graph <= x_end) {
      CalcGraphYPushToVector();
    }
    time += 20;
  } else {
    time = 20;
    timer->stop();
    delete timer;
    timer = nullptr;
  }
  ui->widget->addGraph();
  ui->widget->graph(0)->addData(x, y);
  ui->widget->rescaleAxes();
  ui->widget->graph()->setPen(QPen(Qt::yellow));
  ui->widget->replot();

  ui->widget->setInteraction(QCP::iRangeZoom, true);
  ui->widget->setInteraction(QCP::iRangeDrag, true);
}

QString s21::MainWindow::CalcGraphY() {
  QString line = ui->display_input->text();
  while (true) {
    QString str_x;
    int index = line.indexOf('X');
    if (index > -1) {
      if (x_input_graph < 0) {
        str_x = "(" + QString::number(x_input_graph) + ")";
      } else {
        str_x = QString::number(x_input_graph);
      }
      line.replace(index, 1, str_x);
    } else {
      break;
    }
  }
  try {
    QString current_value_display = line;
    QByteArray inBytes = current_value_display.toUtf8();
    double result = controller_->get_result(inBytes.constData());
    QString resultString = QString::number(result);
    return resultString;
  } catch (std::invalid_argument const &excep) {
    return excep.what();
  }
}

void s21::MainWindow::CalcGraphYPushToVector() {
  QString z = CalcGraphY();
  x_input_graph = QString::number(x_input_graph, 'f', 1).toDouble();
  double buff = z.toDouble();
  if (!z.contains("ERROR") && buff >= y_begin && buff <= y_end) {
    buff = QString::number(buff, 'f', 2).toDouble();
    x.push_back(x_input_graph);
    y.push_back(buff);
  } else {
    x.push_back(qQNaN());
    y.push_back(qQNaN());
  }
  x_input_graph += h;
}

void s21::MainWindow::on_dial_speed_graph_valueChanged(int value) {
  h = double(value) / 1000;
}

void s21::MainWindow::changeAnimationStatus(int flag_anim) {
  if (flag_anim == 1) {
    anim_status = 1;
    ui->pushButton_animation_turn->setStyleSheet(
        StyleHelper::getAnimationTurnActiveButtonStyle());
    ui->pushButton_animation_off->setStyleSheet(
        StyleHelper::getAnimationOffButtonStyle());
  } else {
    anim_status = 0;
    ui->pushButton_animation_turn->setStyleSheet(
        StyleHelper::getAnimationTurnButtonStyle());
    ui->pushButton_animation_off->setStyleSheet(
        StyleHelper::getAnimationOffActiveButtonStyle());
  }
}

void s21::MainWindow::clickedButtonTurn() { changeAnimationStatus(1); }

void s21::MainWindow::clickedButtonOff() { changeAnimationStatus(0); }
