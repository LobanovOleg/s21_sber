#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include <QTimer>
#include <QPixmap>
#include <QProcess>
#include <QStandardPaths>
#include "figure.h"

#define BLACK 0, 0, 0
#define WHITE 255, 255, 255
#define RED 217, 85, 65
#define ORANGE 217, 146, 65
#define YELLOW 252, 244, 88
#define GREEN 132, 222, 84
#define BLUE 84, 210, 222
#define PURPLE 171, 84, 222
#define PINK 232, 130, 178

QT_BEGIN_NAMESPACE
namespace Ui { class MainWindow; }
QT_END_NAMESPACE

typedef enum { BACKGROUND, EDGES, VERTICES } current_object;
typedef enum { SOLID, DOTTED } edges_type_t;
typedef enum { NONE, SQUARE, CIRCLE } vertex_type_t;
typedef enum { PARALLEL, PERSPECTIVE} projection_t;

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    MainWindow(QWidget *parent = nullptr);
    ~MainWindow();

private slots:
    void on_slider_vertices_width_valueChanged(int value);
    void on_slider_edges_width_valueChanged(int value);
    void on_box_edges_type_currentIndexChanged(int index);
    void on_box_vertices_type_currentIndexChanged(int index);

    void on_button_parallel_clicked();
    void on_button_perspective_clicked();

    void on_actionLoad_file_triggered();
    void on_actionbmp_triggered();
    void on_actionjpeg_triggered();
    void takeFrame();

    void on_actionMake_video_triggered();
    void on_moveXSlider_sliderMoved(int position);
    void on_moveYSlider_sliderMoved(int position);
    void on_moveZSlider_sliderMoved(int position);
    void on_moveXBox_editingFinished();
    void on_moveYBox_editingFinished();
    void on_moveZBox_editingFinished();
    void on_turnXSlider_sliderMoved(int position);
    void on_turnYSlider_sliderMoved(int position);
    void on_turnZSlider_sliderMoved(int position);
    void on_turnXBox_editingFinished();
    void on_turnYBox_editingFinished();
    void on_turnZBox_editingFinished();
    void on_scaleSlider_sliderMoved(int position);
    void on_scaleBox_editingFinished();

    void on_background_color_currentIndexChanged(int index);
    void on_vertices_color_currentIndexChanged(int index);
    void on_edges_color_currentIndexChanged(int index);

    void model_information(figure_t*);

private:
    Ui::MainWindow *ui;
    QColor vertices_color;
    QColor edges_color;
    QColor background_color;

    edges_type_t edges_type;
    vertex_type_t vertices_type;
    projection_t projection;

    QString file_name;

    float vertices_width;
    float edges_width;

    double scale;
    double rotate_x;
    double rotate_y;
    double rotate_z;
    double move_x;
    double move_y;
    double move_z;

    void scale_prev();
    void move_prev();
    void turn_prev();


signals:
    void background_color_changed(QColor *current_color);
    void edges_color_changed(QColor *current_color);
    void vertices_color_changed(QColor *current_color);
    void vertices_width_changed(float *current_width);
    void edges_width_changed(float *current_width);
    void edges_type_changed(edges_type_t *current_type);
    void vertices_type_changed(vertex_type_t *current_tupe);
    void projection_changed(projection_t *current_projection);
    void init_model(QString file_name);
    void scale_changed();
    void turn_changed();
    void move_changed();
};
#endif // MAINWINDOW_H
