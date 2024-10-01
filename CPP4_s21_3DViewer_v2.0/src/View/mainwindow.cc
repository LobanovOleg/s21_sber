#include "mainwindow.h"

#include <QButtonGroup>
#include <QColorDialog>
#include <QFileDialog>
#include <QFileInfo>
#include <QResizeEvent>
#include <QtGlobal>

#include "./ui_mainwindow.h"

// 3rd bonus task
#include <QFileDialog>
#include <QImage>
#include <QImageWriter>
#include <QSettings>
#include <QTimer>
#include <QVector>
#include <cstdint>
#include <vector>

#include "extern/gif-h/gif.h"

inline void initModelViewerResources() { Q_INIT_RESOURCE(resources); }
namespace s21 {

void saveImageToFile(const QImage &image, const QString &filePath) {
  image.save(filePath);
}

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent), ui(new Ui::MainWindow) {
  initModelViewerResources();  // add resources

  ui->setupUi(this);

  QLabel *buildStatusLabel = ui->build_status_label;
  QLabel *nodesValueLabel = ui->nodes_value_label;
  QLabel *edgesValueLabel = ui->edges_value_label;
  QLabel *fileNameLabel = ui->file_name_label;

  QStatusBar *statusBar = QMainWindow::statusBar();  // get pointer to statusBar
  statusBar->addWidget(buildStatusLabel);
  statusBar->addPermanentWidget(fileNameLabel);
  statusBar->addPermanentWidget(nodesValueLabel);
  statusBar->addPermanentWidget(edgesValueLabel);

  // set background color on palette widgets (before choosing color)
  QPalette palette = ui->color_nodes_widget->palette();

  palette.setColor(QPalette::Window, "white");
  ui->color_nodes_widget->setPalette(palette);
  ui->color_nodes_widget->setAutoFillBackground(true);

  ui->color_edges_widget->setPalette(palette);
  ui->color_edges_widget->setAutoFillBackground(true);

  palette.setColor(QPalette::Window, "black");
  ui->color_bg_widget->setPalette(palette);
  ui->color_bg_widget->setAutoFillBackground(true);

  QButtonGroup *buttonGroup1 = new QButtonGroup(this);
  buttonGroup1->addButton(ui->radioButton_central_projection);
  buttonGroup1->addButton(ui->radioButton_parallel_projection);

  QButtonGroup *buttonGroup2 = new QButtonGroup(this);
  buttonGroup2->addButton(ui->sizeNodes_radioButton_circle);
  buttonGroup2->addButton(ui->sizeNodes_radioButton_square);
  buttonGroup2->addButton(ui->sizeNodes_radioButton_none);

  QButtonGroup *buttonGroup3 = new QButtonGroup(this);
  buttonGroup3->addButton(ui->edges_dashed_radioButton);
  buttonGroup3->addButton(ui->edges_solid_radioButton);

  loadSettings();
}

MainWindow::~MainWindow() {
  saveSettings();
  delete ui;
}

void MainWindow::on_actionOpen_triggered() { build_new_object(); }

void MainWindow::on_pushButton_openFile_clicked() { build_new_object(); }

void MainWindow::on_actionSave_picture_triggered() { make_screenshot(); }

void MainWindow::on_pushButton_screenshot_clicked() { make_screenshot(); }

void MainWindow::make_screenshot() {
  // Grab a screenshot of the MeshGLWidget
  QPixmap screenshot = ui->MeshGLWidget->grab();

  // Link to save image
  QString filePath = QFileDialog::getSaveFileName(
      this, "Save Image", ".", "BMP Files (*.bmp);;JPEG Files (*.jpg)");

  // Save image
  if (!filePath.isEmpty()) {
    screenshot.save(filePath);
  }
}

void MainWindow::build_new_object() {
  QString filename = QFileDialog::getOpenFileName(
      this, "Choose .obj...", "../src/obj_examples", "OBJ File (*.obj)");

  QLabel *buildStatusPicLabel = ui->build_status_pic_label;
  QLabel *nodesValueLabel = ui->nodes_value_label;
  QLabel *edgesValueLabel = ui->edges_value_label;
  QLabel *buildStatusLabel = ui->build_status_label;

  int width_status_image = ui->build_status_pic_label->width();
  int height_status_image = ui->build_status_pic_label->height();

  statusBar()->addWidget(buildStatusPicLabel);
  statusBar()->addPermanentWidget(nodesValueLabel);
  statusBar()->addPermanentWidget(edgesValueLabel);

  if (filename.isEmpty()) {
    ui->file_name_label->setText("");
    ui->build_status_label->setStyleSheet("color: white");
    ui->build_status_label->setText(QString("Canceled"));
    buildStatusPicLabel->clear();
    return;
  }

  bool is_loaded = ui->MeshGLWidget->loadObject(filename);
  if (is_loaded) {
    QFileInfo fileInfo(filename);
    QString baseName = fileInfo.fileName();
    ui->file_name_label->setText(baseName);

    GLuint edges = ui->MeshGLWidget->getCountEdges() / 2;
    GLuint nodes = ui->MeshGLWidget->getCountNodes();
    nodesValueLabel->setText("Nodes: " + QString::number(nodes));
    edgesValueLabel->setText("Edges: " + QString::number(edges));

    ui->build_status_label->setStyleSheet("color: green");
    buildStatusLabel->setText(QString("Success"));

    QPixmap pixmap(":/images/success.png");
    pixmap = pixmap.scaled(width_status_image, height_status_image,
                           Qt::KeepAspectRatio);  // scaling status image
    buildStatusPicLabel->setPixmap(pixmap);
  } else {
    ui->file_name_label->setText("");

    ui->build_status_label->setStyleSheet("color: red");
    buildStatusLabel->setText(QString("Error"));

    QPixmap pixmap(":/images/error.png");
    pixmap = pixmap.scaled(width_status_image, height_status_image,
                           Qt::KeepAspectRatio);  // scaling status image
    buildStatusPicLabel->setPixmap(pixmap);
  }
}

void MainWindow::on_zoom_slider_valueChanged(int value) {
  ui->zoom_value_label->setText(QString::number(value) + "%");
  ui->MeshGLWidget->scaleObject(value);
}

void MainWindow::on_zoom_nodes_slider_valueChanged(int value) {
  ui->zoom_nodes_value_label->setText(QString::number(value) + "%");
  ui->MeshGLWidget->setPointsSize(value / 2.0);
}

void MainWindow::on_pushButton_set_bg_color_clicked() {
  QColorDialog bg_dialog;
  QColor color = bg_dialog.getColor();
  if (color.isValid()) {
    QPalette palette = ui->color_bg_widget->palette();
    palette.setColor(QPalette::Window, color);
    ui->color_bg_widget->setPalette(palette);
    ui->color_bg_widget->setAutoFillBackground(true);

    ui->MeshGLWidget->setBackground(color);
  }
}

void MainWindow::on_pushButton_set_nodes_color_clicked() {
  QColorDialog nodes_dialog;
  QColor color = nodes_dialog.getColor();

  if (color.isValid()) {
    QPalette palette = ui->color_nodes_widget->palette();
    palette.setColor(QPalette::Window, color);
    ui->color_nodes_widget->setPalette(palette);
    ui->color_nodes_widget->setAutoFillBackground(true);

    ui->MeshGLWidget->setPointsColor(color);
  }
}

void MainWindow::on_pushButton_set_edges_color_clicked() {
  QColorDialog edges_dialog;
  QColor color = edges_dialog.getColor();

  if (color.isValid()) {
    QPalette palette = ui->color_edges_widget->palette();
    palette.setColor(QPalette::Window, color);
    ui->color_edges_widget->setPalette(palette);
    ui->color_edges_widget->setAutoFillBackground(true);

    ui->MeshGLWidget->setLineColor(color);
  }
}

void MainWindow::on_edges_width_spinBox_valueChanged(int value) {
  ui->MeshGLWidget->setLineWidth(value);
}

void MainWindow::on_move_scroll_bar_x_valueChanged(int value) {
  float position = static_cast<float>(value / 20.0);
  ui->label_move_value_x->setText(QString::number(position, 'f', 2));
  ui->MeshGLWidget->moveObjectX(position);
}

void MainWindow::on_move_scroll_bar_y_valueChanged(int value) {
  float position = static_cast<float>(value / 20.0);
  ui->label_move_value_y->setText(QString::number(position, 'f', 2));
  ui->MeshGLWidget->moveObjectY(position);
}

void MainWindow::on_move_scroll_bar_z_valueChanged(int value) {
  float position = static_cast<float>(value / 20.0);
  ui->label_move_value_z->setText(QString::number(position, 'f', 2));
  ui->MeshGLWidget->moveObjectZ(position);
}

void MainWindow::on_rotate_scroll_bar_x_valueChanged(int value) {
  ui->label_rotate_value_x->setText(QString::number(value) + "°");
  ui->MeshGLWidget->rotateObjectX(value);
}

void MainWindow::on_rotate_scroll_bar_y_valueChanged(int value) {
  ui->label_rotate_value_y->setText(QString::number(value) + "°");
  ui->MeshGLWidget->rotateObjectY(value);
}

void MainWindow::on_rotate_scroll_bar_z_valueChanged(int value) {
  ui->label_rotate_value_z->setText(QString::number(value) + "°");
  ui->MeshGLWidget->rotateObjectZ(value);
}

void MainWindow::on_sizeNodes_radioButton_none_clicked() {
  ui->MeshGLWidget->setPointsStyle(PointsStyle::kNone);
}

void MainWindow::on_sizeNodes_radioButton_square_clicked() {
  ui->MeshGLWidget->setPointsStyle(PointsStyle::kSquare);
}

void MainWindow::on_sizeNodes_radioButton_circle_clicked() {
  ui->MeshGLWidget->setPointsStyle(PointsStyle::kCircle);
}

void MainWindow::on_edges_solid_radioButton_clicked() {
  ui->MeshGLWidget->setLineStyle(LinesStyle::kSolid);
}

void MainWindow::on_edges_dashed_radioButton_clicked() {
  ui->MeshGLWidget->setLineStyle(LinesStyle::kDashed);
}

void MainWindow::on_radioButton_central_projection_clicked() {
  ui->MeshGLWidget->setCentralPerspective(true);
}

void MainWindow::on_radioButton_parallel_projection_clicked() {
  ui->MeshGLWidget->setCentralPerspective(false);
}

void MainWindow::saveSettings() {
  QSettings settings("3D_Viewer_Settings", "3d_viewer", this);

  int lineStyle = ui->edges_solid_radioButton->isChecked()
                      ? 0
                      : 1;  // 0 - solid, 1 - dashed
  settings.setValue("lineStyle", lineStyle);

  int edgesWidth = ui->edges_width_spinBox->value();
  settings.setValue("edgesWidth", edgesWidth);

  int nodeStyle = 0;
  if (ui->sizeNodes_radioButton_square->isChecked()) {
    nodeStyle = 1;
  } else if (ui->sizeNodes_radioButton_circle->isChecked()) {
    nodeStyle = 2;
  }
  settings.setValue("nodeStyle", nodeStyle);

  int nodeSize = ui->zoom_nodes_slider->value();
  settings.setValue("nodeSize", nodeSize);

  QColor bgColor = ui->color_bg_widget->palette().color(QPalette::Window);
  int bgRed = bgColor.red();
  int bgGreen = bgColor.green();
  int bgBlue = bgColor.blue();
  settings.setValue("bgRed", bgRed);
  settings.setValue("bgGreen", bgGreen);
  settings.setValue("bgBlue", bgBlue);

  QColor edgesColor = ui->color_edges_widget->palette().color(QPalette::Window);
  int edgesRed = edgesColor.red();
  int edgesGreen = edgesColor.green();
  int edgesBlue = edgesColor.blue();
  settings.setValue("edgesRed", edgesRed);
  settings.setValue("edgesGreen", edgesGreen);
  settings.setValue("edgesBlue", edgesBlue);

  QColor nodesColor = ui->color_nodes_widget->palette().color(QPalette::Window);
  int nodesRed = nodesColor.red();
  int nodesGreen = nodesColor.green();
  int nodesBlue = nodesColor.blue();
  settings.setValue("nodesRed", nodesRed);
  settings.setValue("nodesGreen", nodesGreen);
  settings.setValue("nodesBlue", nodesBlue);

  int projectionPerspective =
      ui->radioButton_central_projection->isChecked() ? 0 : 1;
  settings.setValue("projectionPerspective", projectionPerspective);
}

void MainWindow::loadSettings() {
  QSettings settings("3D_Viewer_Settings", "3d_viewer", this);
  QColor loaded_color = QColor();

  // Load lines style. If not set use solid lines
  int lineStyle = settings.value("lineStyle", 0).toInt();
  if (lineStyle == 1) {
    ui->MeshGLWidget->setLineStyle(LinesStyle::kDashed);
    ui->edges_dashed_radioButton->setChecked(lineStyle == 1);
  } else {
    ui->MeshGLWidget->setLineStyle(LinesStyle::kSolid);
    ui->edges_solid_radioButton->setChecked(lineStyle == 0);
  }

  int edgesWidth = settings.value("edgesWidth", 1).toInt();
  ui->edges_width_spinBox->setValue(edgesWidth);
  ui->MeshGLWidget->setLineWidth(edgesWidth);

  int nodeStyle = settings.value("nodeStyle", 0).toInt();
  if (nodeStyle == 0) {
    ui->MeshGLWidget->setPointsStyle(PointsStyle::kNone);
    ui->sizeNodes_radioButton_none->setChecked(nodeStyle == 0);
  } else if (nodeStyle == 2) {
    ui->MeshGLWidget->setPointsStyle(PointsStyle::kCircle);
    ui->sizeNodes_radioButton_circle->setChecked(nodeStyle == 2);
  } else {
    ui->MeshGLWidget->setPointsStyle(PointsStyle::kSquare);
    ui->sizeNodes_radioButton_square->setChecked(nodeStyle == 1);
  }

  int nodeSize = settings.value("nodeSize", 1).toInt();
  ui->MeshGLWidget->setPointsSize(nodeSize / 2.0);
  ui->zoom_nodes_value_label->setText(QString::number(nodeSize) + "%");
  ui->zoom_nodes_slider->setValue(nodeSize);

  // Load background color
  loaded_color = QColor(settings.value("bgRed", 0).toInt(),
                        settings.value("bgGreen", 0).toInt(),
                        settings.value("bgBlue", 0).toInt());
  ui->MeshGLWidget->setBackground(loaded_color);
  QPalette palette;
  palette.setColor(QPalette::Window, loaded_color);
  ui->color_bg_widget->setPalette(palette);
  ui->color_bg_widget->setAutoFillBackground(true);

  loaded_color = QColor(settings.value("edgesRed", 255).toInt(),
                        settings.value("edgesGreen", 255).toInt(),
                        settings.value("edgesBlue", 255).toInt());
  ui->MeshGLWidget->setLineColor(loaded_color);
  palette.setColor(QPalette::Window, loaded_color);
  ui->color_edges_widget->setPalette(palette);
  ui->color_edges_widget->setAutoFillBackground(true);

  loaded_color = QColor(settings.value("nodesRed", 255).toInt(),
                        settings.value("nodesGreen", 0).toInt(),
                        settings.value("nodesBlue", 0).toInt());
  ui->MeshGLWidget->setPointsColor(loaded_color);
  palette.setColor(QPalette::Window, loaded_color);
  ui->color_nodes_widget->setPalette(palette);
  ui->color_nodes_widget->setAutoFillBackground(true);

  int projectionPerspective =
      settings.value("projectionPerspective", 0).toInt();
  if (projectionPerspective == 1) {
    ui->MeshGLWidget->setCentralPerspective(false);
    ui->radioButton_parallel_projection->setChecked(projectionPerspective == 1);
  } else {
    ui->MeshGLWidget->setCentralPerspective(true);
    ui->radioButton_central_projection->setChecked(projectionPerspective == 0);
  }
}

void MainWindow::on_pushButton_screencast_clicked() {
  ui->pushButton_screencast->setDisabled(true);
  ui->pushButton_screencast->setText("In progress...");

  QString gif_fileName = QFileDialog::getSaveFileName(this, tr("Save gif"), ".",
                                                      tr("GIF files (*.gif)"));

  if (!gif_fileName.isEmpty()) {
    // Запуск процесса записи GIF
    startGifRecording(gif_fileName);
  } else {
    ui->pushButton_screencast->setDisabled(false);
    ui->pushButton_screencast->setText("Screencast");
  }
}

void MainWindow::startGifRecording(const QString &gif_fileName) {
  QVector<QImage> frames;

  const int targetFrameCount = 10 * 5;  // 10 frames per second during 5 sec
  const int gif_width = 640;
  const int gif_height = 480;

  QTimer *timer = new QTimer(this);
  connect(timer, &QTimer::timeout, this,
          [this, frames, gif_fileName, timer]() mutable {
            if (frames.size() < targetFrameCount) {
              QImage frame = ui->MeshGLWidget->grabFramebuffer();
              frame = frame.scaled(gif_width, gif_height, Qt::KeepAspectRatio);
              frames.push_back(frame);

            } else {
              timer->stop();
              ui->pushButton_screencast->setDisabled(false);
              ui->pushButton_screencast->setText("Screencast");

              saveGifAnimation(gif_fileName, frames);

              // Clear framebuffers
              frames.clear();
            }
          });

  // Запуск таймера
  timer->start(100);
}

void MainWindow::saveGifAnimation(const QString &gif_fileName,
                                  const QVector<QImage> &frames) {
  GifWriter gifWriter;

  int output_width = frames.first().width();
  int output_height = frames.first().height();

  GifBegin(&gifWriter, gif_fileName.toStdString().c_str(), output_width,
           output_height, 10);

  for (const QImage &frame : frames) {
    std::vector<uint8_t> rgbaPixels(output_width * output_height * 4, 0);

    // Конвертация RGBA пикселей в вектор uint8_t
    for (int y = 0; y != output_height; ++y) {
      for (int x = 0; x != output_width; ++x) {
        QRgb pixel = frame.pixel(x, y);
        rgbaPixels[(y * output_width + x) * 4 + 0] = qRed(pixel);
        rgbaPixels[(y * output_width + x) * 4 + 1] = qGreen(pixel);
        rgbaPixels[(y * output_width + x) * 4 + 2] = qBlue(pixel);
        rgbaPixels[(y * output_width + x) * 4 + 3] = 0;  // ignoring by gif.h :D
      }
    }

    GifWriteFrame(&gifWriter, rgbaPixels.data(), output_width, output_height,
                  10);
  }

  GifEnd(&gifWriter);
}

void MainWindow::onTimeout() {
  ui->pushButton_screencast->setText("Screencast");
  ui->pushButton_screencast->setDisabled(false);
}

}  // namespace s21
