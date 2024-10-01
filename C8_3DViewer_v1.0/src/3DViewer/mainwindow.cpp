#include "mainwindow.h"

#include <qgifimage.h>

#include <QFileDialog>
#include <QMessageBox>
#include <QSettings>

QTimer *screenshotTimer;
QGifImage *gif;

#include "myopenglwidget.h"
#include "ui_mainwindow.h"

QColor color_from_index(int index) {
  if (index == 0) return QColor::fromRgb(BLACK);
  if (index == 1) return QColor::fromRgb(WHITE);
  if (index == 2) return QColor::fromRgb(RED);
  if (index == 3) return QColor::fromRgb(ORANGE);
  if (index == 4) return QColor::fromRgb(YELLOW);
  if (index == 5) return QColor::fromRgb(GREEN);
  if (index == 6) return QColor::fromRgb(BLUE);
  if (index == 7) return QColor::fromRgb(PURPLE);
  if (index == 8) return QColor::fromRgb(PINK);

  return QColor::fromRgb(0, 0, 0);
}

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent), ui(new Ui::MainWindow) {
  ui->setupUi(this);

  connect(this, SIGNAL(background_color_changed(QColor *)), ui->picture,
          SLOT(background_color_changed(QColor *)));
  connect(this, SIGNAL(edges_color_changed(QColor *)), ui->picture,
          SLOT(edges_color_changed(QColor *)));
  connect(this, SIGNAL(vertices_color_changed(QColor *)), ui->picture,
          SLOT(vertices_color_changed(QColor *)));
  connect(this, SIGNAL(vertices_width_changed(float *)), ui->picture,
          SLOT(vertices_width_changed(float *)));
  connect(this, SIGNAL(edges_width_changed(float *)), ui->picture,
          SLOT(edges_width_changed(float *)));
  connect(this, SIGNAL(edges_type_changed(edges_type_t *)), ui->picture,
          SLOT(edges_type_changed(edges_type_t *)));
  connect(this, SIGNAL(vertices_type_changed(vertex_type_t *)), ui->picture,
          SLOT(vertices_type_changed(vertex_type_t *)));
  connect(this, SIGNAL(projection_changed(projection_t *)), ui->picture,
          SLOT(projection_changed(projection_t *)));
  connect(this, SIGNAL(init_model(QString)), ui->picture,
          SLOT(init_model(QString)));
  connect(this, SIGNAL(scale_changed()), ui->picture, SLOT(redraw()));
  connect(this, SIGNAL(turn_changed()), ui->picture, SLOT(redraw()));
  connect(this, SIGNAL(move_changed()), ui->picture, SLOT(redraw()));
  connect(ui->picture, SIGNAL(model_information(figure_t *)), this,
          SLOT(model_information(figure_t *)));

  edges_width = 1.0;
  vertices_width = 1.0;
  vertices_type = NONE;
  edges_type = SOLID;

  QSettings settings("team", "3DViewer");
  ui->moveXSlider->setValue(settings.value("moveXSlider").toInt());
  ui->moveYSlider->setValue(settings.value("moveYSlider").toInt());
  ui->moveZSlider->setValue(settings.value("moveZSlider").toInt());
  ui->moveXBox->setValue(settings.value("moveXBox").toInt());
  ui->moveYBox->setValue(settings.value("moveYBox").toInt());
  ui->moveZBox->setValue(settings.value("moveZBox").toInt());

  ui->turnXBox->setValue(settings.value("turnXBox").toInt());
  ui->turnYBox->setValue(settings.value("turnYBox").toInt());
  ui->turnZBox->setValue(settings.value("turnZBox").toInt());
  ui->turnXSlider->setValue(settings.value("turnXSlider").toInt());
  ui->turnYSlider->setValue(settings.value("turnYSlider").toInt());
  ui->turnZSlider->setValue(settings.value("turnZSlider").toInt());

  ui->scaleBox->setValue(settings.value("scaleBox").toInt());
  ui->scaleSlider->setValue(settings.value("scaleSlider").toInt());

  ui->slider_edges_width->setValue(
      settings.value("slider_edges_width").toInt());
  ui->slider_vertices_width->setValue(
      settings.value("slider_vertices_width").toInt());

  ui->button_parallel->setChecked(!settings.value("RB1").toInt());
  ui->button_perspective->setChecked(settings.value("RB1").toInt());

  ui->box_edges_type->setCurrentIndex(settings.value("box_edges_type").toInt());
  ui->box_vertices_type->setCurrentIndex(
      settings.value("box_vertices_type").toInt());

  ui->vertices_color->setCurrentIndex(settings.value("vertices_color").toInt());
  ui->edges_color->setCurrentIndex(settings.value("edges_color").toInt());
  ui->background_color->setCurrentIndex(
      settings.value("background_color").toInt());

  scale = ui->scaleBox->value();
  rotate_x = ui->turnXBox->value();
  rotate_y = ui->turnYBox->value();
  rotate_z = ui->turnZBox->value();
  move_x = ui->moveXBox->value();
  move_y = ui->moveYBox->value();
  move_z = ui->moveZBox->value();
  if (ui->button_parallel->isChecked())
    on_button_parallel_clicked();
  else
    on_button_perspective_clicked();
}

MainWindow::~MainWindow() {
  QSettings settings("team", "3DViewer");
  settings.setValue("moveXSlider", ui->moveXSlider->value());
  settings.setValue("moveYSlider", ui->moveYSlider->value());
  settings.setValue("moveZSlider", ui->moveYSlider->value());

  settings.setValue("moveXBox", ui->moveXBox->value());
  settings.setValue("moveYBox", ui->moveYBox->value());
  settings.setValue("moveZBox", ui->moveZBox->value());

  settings.setValue("turnXSlider", ui->turnXSlider->value());
  settings.setValue("turnYSlider", ui->turnYSlider->value());
  settings.setValue("turnZSlider", ui->turnYSlider->value());

  settings.setValue("turnXBox", ui->turnXBox->value());
  settings.setValue("turnYBox", ui->turnYBox->value());
  settings.setValue("turnZBox", ui->turnZBox->value());

  settings.setValue("scaleBox", ui->scaleBox->value());
  settings.setValue("scaleSlider", ui->scaleSlider->value());

  settings.setValue("slider_edges_width", ui->slider_edges_width->value());
  settings.setValue("slider_vertices_width",
                    ui->slider_vertices_width->value());

  settings.setValue("box_vertices_type", ui->box_vertices_type->currentIndex());
  settings.setValue("box_edges_type", ui->box_edges_type->currentIndex());

  settings.setValue("edges_color", ui->edges_color->currentIndex());
  settings.setValue("background_color", ui->background_color->currentIndex());
  settings.setValue("vertices_color", ui->vertices_color->currentIndex());

  if (ui->button_parallel->isChecked())
    settings.setValue("RB1", "0");
  else
    settings.setValue("RB1", "1");

  delete ui;
}

void MainWindow::on_slider_vertices_width_valueChanged(int value) {
  vertices_width = value / 10;
  emit vertices_width_changed(&vertices_width);
}

void MainWindow::on_slider_edges_width_valueChanged(int value) {
  edges_width = value / 10;
  emit edges_width_changed(&edges_width);
}

void MainWindow::on_box_edges_type_currentIndexChanged(int index) {
  if (index == 0) {
    edges_type = SOLID;
  } else if (index == 1) {
    edges_type = DOTTED;
  }
  emit edges_type_changed(&edges_type);
}

void MainWindow::on_box_vertices_type_currentIndexChanged(int index) {
  if (index == 0) {
    vertices_type = NONE;
  } else if (index == 1) {
    vertices_type = SQUARE;
  } else if (index == 2) {
    vertices_type = CIRCLE;
  }
  emit vertices_type_changed(&vertices_type);
}

void MainWindow::on_button_parallel_clicked() {
  projection = PARALLEL;
  emit projection_changed(&projection);
}

void MainWindow::on_button_perspective_clicked() {
  projection = PERSPECTIVE;
  emit projection_changed(&projection);
}

void MainWindow::on_actionLoad_file_triggered() {
  file_name = QFileDialog::getOpenFileName(this, "Select object file",
                                           QDir::homePath(), "*.obj");
  if (file_name.isEmpty()) {
    QMessageBox::critical(this, "cannot open file", "cannot open file");
  } else {
    emit init_model(file_name);

    turn_prev();
    scale_prev();
    move_prev();
  }
}

void MainWindow::on_actionbmp_triggered() {
  QPixmap screenshot = ui->picture->grab();
  QString filename = QFileDialog::getSaveFileName(this, "Save file",
                                                  QDir::homePath(), "*.bmp");
  QFile file(filename);

  if (file.open(QIODevice::WriteOnly)) {
    screenshot.save(&file, "BMP");
    file.close();
  }
}

void MainWindow::on_actionjpeg_triggered() {
  QPixmap screenshot = ui->picture->grab();
  QString filename = QFileDialog::getSaveFileName(this, "Save file",
                                                  QDir::homePath(), "*.jpeg");
  QFile file(filename);
  if (file.open(QIODevice::WriteOnly)) {
    screenshot.save(&file, "jpeg");
    file.close();
  }
}

void MainWindow::takeFrame() {
  QImage frame = ui->picture->grabFramebuffer();
  gif->addFrame(frame.scaled(640, 480), 0);
  if (gif->frameCount() == 50) {
    screenshotTimer->stop();
    QString pathGIF = QFileDialog::getSaveFileName(
        this, ("Save as GIF"), "image.gif", "GIF Image Files (*.gif)");
    gif->save(pathGIF);
    delete screenshotTimer;
    delete gif;
  }
}

void MainWindow::on_actionMake_video_triggered() {
  gif = new QGifImage;
  screenshotTimer = new QTimer(this);
  gif->setDefaultDelay(100);
  screenshotTimer->start(100);
  connect(screenshotTimer, SIGNAL(timeout()), this, SLOT(takeFrame()));
}

void MainWindow::move_prev() {
  move_t move_tmp;
  if (projection == PERSPECTIVE)
    move_tmp = {.dx = move_x * 10, .dy = move_y * 10, .dz = move_z};
  else
    move_tmp = {.dx = move_x, .dy = move_y, .dz = move_z};

  move_figure(ui->picture->get_image(), &move_tmp);
  emit move_changed();
}

void MainWindow::turn_prev() {
  rotate_t rotate_tmp = {
      .angle_x = rotate_x, .angle_y = rotate_y, .angle_z = rotate_z};
  rotate_figure(ui->picture->get_image(), &rotate_tmp);
  emit turn_changed();
}

void MainWindow::scale_prev() {
  scale_t scale_tmp = {.kx = scale, .ky = scale, .kz = scale};
  scale_figure(ui->picture->get_image(), &scale_tmp);
  emit scale_changed();
}

void MainWindow::on_moveXSlider_sliderMoved(int position) {
  ui->moveXBox->setValue(position / 100.0);
  ui->picture->copy_image(ui->picture->get_figure(), ui->picture->get_image());
  move_t move_tmp;
  if (projection == PERSPECTIVE)
    move_tmp = {.dx = double(ui->moveXBox->value()) * 10,
                .dy = move_y * 10,
                .dz = move_z};
  else
    move_tmp = {
        .dx = double(ui->moveXBox->value()), .dy = move_y, .dz = move_z};
  move_figure(ui->picture->get_image(), &move_tmp);
  move_x = double(ui->moveXBox->value());
  emit move_changed();

  turn_prev();
  scale_prev();
}

void MainWindow::on_moveYSlider_sliderMoved(int position) {
  ui->moveYBox->setValue(position / 100.0);
  ui->picture->copy_image(ui->picture->get_figure(), ui->picture->get_image());
  move_t move_tmp;
  if (projection == PERSPECTIVE)
    move_tmp = {.dx = move_x * 10,
                .dy = double(ui->moveYBox->value()) * 10,
                .dz = move_z};
  else
    move_tmp = {
        .dx = move_x, .dy = double(ui->moveYBox->value()), .dz = move_z};
  move_figure(ui->picture->get_image(), &move_tmp);
  move_y = double(ui->moveYBox->value());
  emit move_changed();

  turn_prev();
  scale_prev();
}

void MainWindow::on_moveZSlider_sliderMoved(int position) {
  ui->moveZBox->setValue(position / 100.0);
  ui->picture->copy_image(ui->picture->get_figure(), ui->picture->get_image());
  move_t move_tmp;
  if (projection == PERSPECTIVE)
    move_tmp = {.dx = move_x * 10,
                .dy = move_y * 10,
                .dz = double(ui->moveZBox->value())};
  else
    move_tmp = {
        .dx = move_x, .dy = move_y, .dz = double(ui->moveZBox->value())};
  move_figure(ui->picture->get_image(), &move_tmp);
  move_z = double(ui->moveZBox->value());
  emit move_changed();

  turn_prev();
  scale_prev();
}

void MainWindow::on_moveXBox_editingFinished() {
  ui->moveXSlider->setValue(ui->moveXBox->value() * 100);
  ui->picture->copy_image(ui->picture->get_figure(), ui->picture->get_image());
  move_t move_tmp;
  if (projection == PERSPECTIVE)
    move_tmp = {.dx = double(ui->moveXBox->value()) * 10,
                .dy = move_y * 10,
                .dz = move_z};
  else
    move_tmp = {
        .dx = double(ui->moveXBox->value()), .dy = move_y, .dz = move_z};
  move_figure(ui->picture->get_image(), &move_tmp);
  move_x = double(ui->moveXBox->value());
  emit move_changed();

  turn_prev();
  scale_prev();
}

void MainWindow::on_moveYBox_editingFinished() {
  ui->moveYSlider->setValue(ui->moveYBox->value() * 100);
  ui->picture->copy_image(ui->picture->get_figure(), ui->picture->get_image());
  move_t move_tmp;
  if (projection == PERSPECTIVE)
    move_tmp = {.dx = move_x * 10,
                .dy = double(ui->moveYBox->value()) * 10,
                .dz = move_z};
  else
    move_tmp = {
        .dx = move_x, .dy = double(ui->moveYBox->value()), .dz = move_z};

  move_figure(ui->picture->get_image(), &move_tmp);
  move_y = double(ui->moveYBox->value());
  emit move_changed();

  turn_prev();

  scale_t scale_tmp = {.kx = scale, .ky = scale, .kz = scale};
  scale_figure(ui->picture->get_image(), &scale_tmp);
  emit scale_changed();
}

void MainWindow::on_moveZBox_editingFinished() {
  ui->moveZSlider->setValue(ui->moveZBox->value() * 100);
  ui->picture->copy_image(ui->picture->get_figure(), ui->picture->get_image());
  move_t move_tmp;
  if (projection == PERSPECTIVE)
    move_tmp = {.dx = double(ui->moveXBox->value()) * 10,
                .dy = move_y * 10,
                .dz = move_z};
  else
    move_tmp = {
        .dx = double(ui->moveXBox->value()), .dy = move_y, .dz = move_z};
  move_figure(ui->picture->get_image(), &move_tmp);
  move_x = double(ui->moveXBox->value());
  emit move_changed();

  turn_prev();
  scale_prev();
}

void MainWindow::on_turnXSlider_sliderMoved(int position) {
  ui->turnXBox->setValue(position);
  ui->picture->copy_image(ui->picture->get_figure(), ui->picture->get_image());
  rotate_t rotate_tmp = {.angle_x = double(ui->turnXBox->value()),
                         .angle_y = rotate_y,
                         .angle_z = rotate_z};
  rotate_figure(ui->picture->get_image(), &rotate_tmp);
  rotate_x = double(ui->turnXBox->value());
  emit turn_changed();

  move_prev();
  scale_prev();
}

void MainWindow::on_turnYSlider_sliderMoved(int position) {
  ui->turnYBox->setValue(position);
  ui->picture->copy_image(ui->picture->get_figure(), ui->picture->get_image());
  rotate_t rotate_tmp = {.angle_x = rotate_x,
                         .angle_y = double(ui->turnYBox->value()),
                         .angle_z = rotate_z};
  rotate_figure(ui->picture->get_image(), &rotate_tmp);
  rotate_y = double(ui->turnYBox->value());
  emit turn_changed();

  move_prev();
  scale_prev();
}

void MainWindow::on_turnZSlider_sliderMoved(int position) {
  ui->turnZBox->setValue(position);
  ui->picture->copy_image(ui->picture->get_figure(), ui->picture->get_image());
  rotate_t rotate_tmp = {.angle_x = rotate_x,
                         .angle_y = rotate_y,
                         .angle_z = double(ui->turnZBox->value())};
  rotate_figure(ui->picture->get_image(), &rotate_tmp);
  rotate_z = double(ui->turnZBox->value());
  emit turn_changed();

  move_prev();
  scale_prev();
}

void MainWindow::on_turnXBox_editingFinished() {
  ui->turnXSlider->setValue(ui->turnXBox->value());
  ui->picture->copy_image(ui->picture->get_figure(), ui->picture->get_image());
  rotate_t rotate_tmp = {.angle_x = double(ui->turnXBox->value()),
                         .angle_y = rotate_y,
                         .angle_z = rotate_z};
  rotate_figure(ui->picture->get_image(), &rotate_tmp);
  rotate_x = double(ui->turnXBox->value());
  emit turn_changed();

  move_prev();
  scale_prev();
}

void MainWindow::on_turnYBox_editingFinished() {
  ui->turnYSlider->setValue(ui->turnYBox->value());
  ui->picture->copy_image(ui->picture->get_figure(), ui->picture->get_image());
  rotate_t rotate_tmp = {.angle_x = rotate_x,
                         .angle_y = double(ui->turnYBox->value()),
                         .angle_z = rotate_z};
  rotate_figure(ui->picture->get_image(), &rotate_tmp);
  rotate_y = double(ui->turnYBox->value());
  emit turn_changed();

  move_prev();
  scale_prev();
}

void MainWindow::on_turnZBox_editingFinished() {
  ui->turnZSlider->setValue(ui->turnZBox->value());
  ui->picture->copy_image(ui->picture->get_figure(), ui->picture->get_image());
  rotate_t rotate_tmp = {.angle_x = rotate_x,
                         .angle_y = rotate_y,
                         .angle_z = double(ui->turnZBox->value())};
  rotate_figure(ui->picture->get_image(), &rotate_tmp);
  rotate_z = double(ui->turnZBox->value());
  emit turn_changed();

  move_prev();
  scale_prev();
}

void MainWindow::on_scaleSlider_sliderMoved(int position) {
  if (position > 50) {
    ui->scaleBox->setValue((position - 46) * 0.2);
  } else if (position == 50) {
    ui->scaleBox->setValue(1);
  } else {
    ui->scaleBox->setValue(position / 50.0);
  }
  ui->picture->copy_image(ui->picture->get_figure(), ui->picture->get_image());
  scale_t scale_tmp = {.kx = ui->scaleBox->value(),
                       .ky = ui->scaleBox->value(),
                       .kz = ui->scaleBox->value()};
  scale_figure(ui->picture->get_image(), &scale_tmp);
  scale = ui->scaleBox->value();
  emit scale_changed();

  turn_prev();
  move_prev();
}

void MainWindow::on_scaleBox_editingFinished() {
  double value = ui->scaleBox->value();
  if (value > 1) {
    ui->scaleSlider->setValue(value * 5 + 46);
  } else if (value == 1) {
    ui->scaleSlider->setValue(50);
  } else {
    ui->scaleSlider->setValue(value * 50);
  }

  ui->picture->copy_image(ui->picture->get_figure(), ui->picture->get_image());
  scale_t scale_tmp = {.kx = ui->scaleBox->value(),
                       .ky = ui->scaleBox->value(),
                       .kz = ui->scaleBox->value()};
  scale_figure(ui->picture->get_image(), &scale_tmp);
  scale = ui->scaleBox->value();
  emit scale_changed();

  turn_prev();
  move_prev();
}

void MainWindow::on_background_color_currentIndexChanged(int index) {
  background_color = color_from_index(index);
  emit background_color_changed(&background_color);
}

void MainWindow::on_vertices_color_currentIndexChanged(int index) {
  vertices_color = color_from_index(index);
  emit vertices_color_changed(&vertices_color);
}

void MainWindow::on_edges_color_currentIndexChanged(int index) {
  edges_color = color_from_index(index);
  emit edges_color_changed(&edges_color);
}

void MainWindow::model_information(figure_t *figure) {
  QString info = "File: " + file_name.last(file_name.length() -
                                           file_name.lastIndexOf('/') - 1);
  info += "; Vertices: " + QString::number(figure->points.size);
  info += "; Edges: " + QString::number(figure->edges.size) + ".";
  ui->statusbar->showMessage(info);
}
