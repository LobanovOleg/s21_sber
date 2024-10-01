#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>

#include "gl_widget.h"

QT_BEGIN_NAMESPACE
namespace Ui {
class MainWindow;
}
QT_END_NAMESPACE
namespace s21 {

/** @class MainWindow
 *
 *  @brief The MainWindow class is simple GUI from QT
 */
class MainWindow : public QMainWindow {
  Q_OBJECT

 public:
  MainWindow(QWidget* parent = nullptr);
  ~MainWindow();

 private slots:

  void build_new_object();
  void make_screenshot();

  void on_zoom_slider_valueChanged(int value);

  void on_zoom_nodes_slider_valueChanged(int value);
  void on_pushButton_set_nodes_color_clicked();
  void on_pushButton_set_edges_color_clicked();
  void on_edges_width_spinBox_valueChanged(int arg1);

  void on_move_scroll_bar_x_valueChanged(int value);
  void on_move_scroll_bar_y_valueChanged(int value);
  void on_move_scroll_bar_z_valueChanged(int value);

  void on_rotate_scroll_bar_x_valueChanged(int value);
  void on_rotate_scroll_bar_y_valueChanged(int value);
  void on_rotate_scroll_bar_z_valueChanged(int value);

  void on_actionOpen_triggered();
  void on_actionSave_picture_triggered();

  void on_sizeNodes_radioButton_none_clicked();
  void on_sizeNodes_radioButton_square_clicked();
  void on_sizeNodes_radioButton_circle_clicked();
  void on_edges_solid_radioButton_clicked();
  void on_edges_dashed_radioButton_clicked();

  void on_pushButton_set_bg_color_clicked();

  void saveSettings();
  void loadSettings();

  void on_pushButton_screencast_clicked();
  void startGifRecording(const QString& gif_fileName);
  void saveGifAnimation(const QString& gif_fileName,
                        const QVector<QImage>& frames);

  void onTimeout();

  void on_radioButton_central_projection_clicked();
  void on_radioButton_parallel_projection_clicked();

  void on_pushButton_openFile_clicked();

  void on_pushButton_screenshot_clicked();

 private:
  Ui::MainWindow* ui;
};

}  // namespace s21
#endif  // MAINWINDOW_H
