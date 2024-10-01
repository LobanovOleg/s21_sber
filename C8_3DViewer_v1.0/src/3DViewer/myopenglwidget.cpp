#include "myopenglwidget.h"

#include <QMessageBox>

MyOpenGLWidget::MyOpenGLWidget(QWidget *parent) : QOpenGLWidget(parent) {
  OK = false;
  figure = NULL;
}

MyOpenGLWidget::~MyOpenGLWidget() {
  destroy_image();
  free_figure(figure);
}

figure_t *MyOpenGLWidget::get_figure() { return figure; }

figure_t *MyOpenGLWidget::get_image() { return &image; }

void MyOpenGLWidget::initializeGL() {
  initializeOpenGLFunctions();
  glClearColor(background_color.redF(), background_color.greenF(),
               background_color.blueF(), 1.0f);
}

void MyOpenGLWidget::paintGL() {
  glClearColor(background_color.redF(), background_color.greenF(),
               background_color.blueF(), 1.0f);
  glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);

  init_camera();
  if (OK) {
    draw_edges();
    draw_vertices();
  } else {
    figure = figure_init();
    init_base_image();
    OK = true;
  }
}

void MyOpenGLWidget::init_model(QString filename) {
  std::string str = filename.toStdString();
  const char *p = str.c_str();
  my_error_t rc = download_figure(figure, p);
  if (rc) {
    QMessageBox::critical(this, "Error", "Erorr while loading figure");
  } else {
    if (figure) {
      emit model_information(figure);
    }
  }
  destroy_image();
  if (init_image(figure, &image))
    QMessageBox::critical(this, "Error", "Memory allocate error");
}

void MyOpenGLWidget::init_camera() {
  glMatrixMode(GL_PROJECTION);
  glLoadIdentity();
  if (projection == PERSPECTIVE) {
    if (figure) {
      double min_x = -1.0;
      double max_x = 1.0;
      double min_y = -1.0;
      double max_y = 1.0;
      double min_z = 1.0;
      double max_z = 10.0;
      find_min_max_points(&figure->points, &min_x, &max_x, &min_y, &max_y,
                          &min_z, &max_z);

      double padding = 2.0;

      double width = max_x - min_x + 2 * padding;
      double height = max_y - min_y + 2 * padding;
      double depth = max_z - min_z + 2 * padding;

      double centerX = (max_x + min_x) / 2;
      double centerY = (max_y + min_y) / 2;
      double centerZ = (max_z + min_z) / 2;

      double halfWidth = width / 2;
      double halfHeight = height / 2;
      double halfDepth = depth / 2;

      double diagonal = sqrt(halfWidth * halfWidth + halfHeight * halfHeight +
                             halfDepth * halfDepth);

      min_x = centerX - diagonal;
      max_x = centerX + diagonal;
      min_y = centerY - diagonal;
      max_y = centerY + diagonal;
      min_z = centerZ - diagonal;
      max_z = centerZ + diagonal;

      glFrustum(min_x / 10.0, max_x / 10.0, min_y / 10.0, max_y / 10.0, 1,
                1000000);
      glTranslatef(0, 0, -fabs(min_z));
    } else
      glFrustum(-1.0, 1.0, -1.0, 1.0, 1.0, 10.0);
  } else {
    if (figure) {
      double min_x = -1.0;
      double max_x = 1.0;
      double min_y = -1.0;
      double max_y = 1.0;
      double min_z = 1.0;
      double max_z = 10.0;
      find_min_max_points(&figure->points, &min_x, &max_x, &min_y, &max_y,
                          &min_z, &max_z);
      double padding = 2.0;

      double width = max_x - min_x + 2 * padding;
      double height = max_y - min_y + 2 * padding;
      double depth = max_z - min_z + 2 * padding;

      double centerX = (max_x + min_x) / 2;
      double centerY = (max_y + min_y) / 2;
      double centerZ = (max_z + min_z) / 2;

      double halfWidth = width / 2;
      double halfHeight = height / 2;
      double halfDepth = depth / 2;

      double diagonal = sqrt(halfWidth * halfWidth + halfHeight * halfHeight +
                             halfDepth * halfDepth);

      min_x = centerX - diagonal;
      max_x = centerX + diagonal;
      min_y = centerY - diagonal;
      max_y = centerY + diagonal;
      min_z = centerZ - diagonal;
      max_z = centerZ + diagonal;

      glOrtho(min_x, max_x, min_y, max_y, 0, 1000000);
      glTranslatef(0.0f, 0.0f, -fabs(min_z));
    } else
      glOrtho(-1, 1, -1, 1, 1, 10);
  }
  glMatrixMode(GL_MODELVIEW);
  glLoadIdentity();
}

void MyOpenGLWidget::init_settings() {
  background_color.setRgbF(0.0f, 0.0f, 0.0f);
  edges_color.setRgbF(1, 0, 0);
  vertices_color.setRgbF(0, 0, 1);
  current_move_y = 0;
  current_move_z = 0;
  current_turn_x = 0;
  current_turn_y = 0;
  current_turn_z = 0;
  current_scale = 0;
  vertex_type = NONE;
  edges_type = SOLID;
}

void MyOpenGLWidget::draw_edges() {
  if (edges_type == DOTTED) {
    glEnable(GL_LINE_STIPPLE);
    glLineStipple(1, 0x00FF);
  }

  glColor3f(edges_color.redF(), edges_color.greenF(), edges_color.blueF());
  glLineWidth(edges_width);

  glBegin(GL_LINES);
  for (int i = 0; i < image.edges.size; ++i) {
    int v1 = image.edges.array_edges[i].first_point;
    int v2 = image.edges.array_edges[i].second_point;
    glVertex3f(image.points.array_points[v1].x, image.points.array_points[v1].y,
               image.points.array_points[v1].z);
    glVertex3f(image.points.array_points[v2].x, image.points.array_points[v2].y,
               image.points.array_points[v2].z);
  }
  glEnd();

  if (edges_type == DOTTED) {
    glDisable(GL_LINE_STIPPLE);
  }
}

void MyOpenGLWidget::draw_vertices() {
  if (vertex_type != NONE) {
    if (vertex_type == CIRCLE) glEnable(GL_POINT_SMOOTH);
    glColor3f(vertices_color.redF(), vertices_color.greenF(),
              vertices_color.blueF());
    glPointSize(vertices_width);
    glBegin(GL_POINTS);

    for (int i = 0; i < image.points.size; i++) {
      glVertex3f(image.points.array_points[i].x, image.points.array_points[i].y,
                 image.points.array_points[i].z);
    }

    glEnd();
    if (vertex_type == CIRCLE) glDisable(GL_POINT_SMOOTH);
  }
}

void MyOpenGLWidget::background_color_changed(QColor *new_color) {
  background_color.setRed(new_color->red());
  background_color.setGreen(new_color->green());
  background_color.setBlue(new_color->blue());
  update();
}

void MyOpenGLWidget::edges_color_changed(QColor *new_color) {
  edges_color.setRed(new_color->red());
  edges_color.setGreen(new_color->green());
  edges_color.setBlue(new_color->blue());
  update();
}

void MyOpenGLWidget::vertices_color_changed(QColor *new_color) {
  vertices_color.setRed(new_color->red());
  vertices_color.setGreen(new_color->green());
  vertices_color.setBlue(new_color->blue());
  update();
}

void MyOpenGLWidget::vertices_width_changed(float *new_width) {
  vertices_width = *new_width;
  update();
}

void MyOpenGLWidget::edges_width_changed(float *new_width) {
  edges_width = *new_width;
  update();
}

void MyOpenGLWidget::edges_type_changed(edges_type_t *new_type) {
  edges_type = *new_type;
  update();
}

void MyOpenGLWidget::vertices_type_changed(vertex_type_t *new_type) {
  vertex_type = *new_type;
  update();
}

void MyOpenGLWidget::projection_changed(projection_t *new_projection) {
  projection = *new_projection;
  update();
}

void MyOpenGLWidget::redraw() { update(); }

int MyOpenGLWidget::init_image(figure_t *src, figure_t *dst) {
  dst->faces.size = src->faces.size;
  dst->faces.capacity = src->faces.capacity;
  dst->faces.array_faces = (face_t *)malloc(src->faces.size * sizeof(face_t));
  if (!dst->faces.array_faces) return EXIT_FAILURE;

  dst->points.size = src->points.size;
  dst->points.capacity = src->points.capacity;
  dst->points.array_points =
      (point_t *)malloc(sizeof(point_t) * src->points.size);
  if (!dst->points.array_points) return EXIT_FAILURE;

  dst->edges.size = src->edges.size;
  dst->edges.capacity = src->edges.capacity;
  dst->edges.array_edges = (edge_t *)malloc(sizeof(edge_t) * src->edges.size);
  if (!dst->edges.array_edges) return EXIT_FAILURE;

  dst->points.points_table = (int **)malloc(sizeof(int *) * src->points.size);
  if (!dst->points.points_table) return EXIT_FAILURE;

  for (int i = 0; i < src->points.size; ++i) {
    dst->points.points_table[i] = (int *)malloc(sizeof(int) * src->points.size);
    if (!dst->points.points_table[i]) return EXIT_FAILURE;
  }
  copy_image(src, dst);
  return EXIT_SUCCESS;
}

void MyOpenGLWidget::copy_image(figure_t *src, figure_t *dst) {
  dst->center = src->center;
  for (int i = 0; i < src->faces.size; ++i)
    dst->faces.array_faces[i] = src->faces.array_faces[i];

  for (int i = 0; i < src->points.size; ++i)
    dst->points.array_points[i] = src->points.array_points[i];

  for (int i = 0; i < src->edges.size; ++i)
    dst->edges.array_edges[i] = src->edges.array_edges[i];

  for (int i = 0; i < src->points.size; ++i)
    for (int j = 0; j < src->points.size; ++j)
      dst->points.points_table[i][j] = src->points.points_table[i][j];
}

void MyOpenGLWidget::destroy_image() {
  if (image.edges.array_edges) free(image.edges.array_edges);
  if (image.faces.array_faces) free(image.faces.array_faces);
  if (image.points.array_points) free(image.points.array_points);
  if (image.points.points_table) free(image.points.points_table);
}

void MyOpenGLWidget::init_base_image() {
  point_default(&image.center);
  points_default(&image.points);
  edges_default(&image.edges);
  faces_default(&image.faces);
}
