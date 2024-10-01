#include "gl_widget.h"

#include <QDebug>
#include <cmath>
#include <unordered_set>

#include "../Controller/s21_controller.h"
#include "../Model/s21_loader.h"
#include "../Model/s21_model.h"
#include "../Model/s21_transformations.h"

namespace s21 {

MeshGLWidget::~MeshGLWidget() {
  // makeCurrent();

  Cleanup();
  delete program;
}

void MeshGLWidget::initializeGL() {
  initializeOpenGLFunctions();

  glEnable(GL_DEPTH_TEST);

  initShaders();
}

void MeshGLWidget::paintGL() {
  drawBackground();
  glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);

  // Edge case. Do not draw the object if it not loaded
  if (mesh_state.is_loaded == false) return;

  CalculateMVPMatrix();

  program->bind();
  program->setUniformValue("mvp_matrix", mvp_matrix);

  vertex_array_object.bind();
  drawPointsIfNeeded();
  drawLines();
  vertex_array_object.release();

  program->release();
}

void MeshGLWidget::initShaders() {
  delete program;
  program = new QOpenGLShaderProgram();
  // Compile vertex shader
  if (!program->addShaderFromSourceFile(QOpenGLShader::Vertex,
                                        ":/shaders/vertex.glsl"))
    close();

  // Compile fragment shader
  if (!program->addShaderFromSourceFile(QOpenGLShader::Fragment,
                                        ":/shaders/fragment.glsl"))
    close();

  // Link shader pipeline
  if (!program->link()) close();

  // Bind shader pipeline for use
  if (!program->bind()) close();
}

void MeshGLWidget::LoadObjectGeometry() {
  std::vector<double> vertices = s21::Controller::Get()->GetVertices();

  double* axis_values = new double[vertices.size()];

  for (size_t i = 0; i < vertices.size(); ++i) {
    axis_values[i] = vertices[i];
  }
  vertices_ = axis_values;

  if (!indices_) {
    std::vector<int> indices = s21::Controller::Get()->GetIndices();
    unsigned int* indices_values = new unsigned int[indices.size()];

    for (std::vector<int>::size_type i = 0; i < indices.size(); i++) {
      indices_values[i] = indices[i];
    }

    indices_ = indices_values;
  }
}

void MeshGLWidget::initVertexBuffer() {
  vertex_buffer.create();
  vertex_buffer.bind();
  vertex_buffer.setUsagePattern(QOpenGLBuffer::StaticDraw);
  vertex_buffer.allocate(
      vertices_,
      sizeof(double) * s21::Controller::Get()->GetNumberOfVertices() * 3);
  vertex_buffer.release();

  // vertex_array_object.create();
  if (!vertex_array_object.isCreated()) vertex_array_object.create();
  vertex_array_object.bind();

  vertex_buffer.bind();
  glEnableVertexAttribArray(0);
  glVertexAttribPointer(0, 3, GL_DOUBLE, GL_FALSE, 0, nullptr);
  vertex_buffer.release();

  vertex_array_object.release();
}

void MeshGLWidget::initElementBuffer() {
  // Initialize variables and containers
  std::vector<std::pair<GLuint, GLuint>> mesh_lines;
  std::unordered_set<std::string> existed_lines;

  // Iterate through each polygon
  for (int i = 0; i < s21::Controller::Get()->GetNumberOfPolygons(); ++i) {
    auto indices = s21::Controller::Get()->GetPolygonIndices(i);

    // Iterate through each vertex index in the polygon
    for (size_t j = 0; j < indices.size(); ++j) {
      GLuint index1 = indices[j];
      GLuint index2 = indices[(j + 1) % indices.size()];  // Next vertex index

      // Form a line between consecutive vertices
      std::string line_key = std::to_string(std::min(index1, index2)) + "-" +
                             std::to_string(std::max(index1, index2));
      if (existed_lines.find(line_key) == existed_lines.end()) {
        mesh_lines.push_back({index1, index2});
        existed_lines.insert(line_key);
      }
    }
  }

  // Allocate and initialize element buffer
  mesh_count_lines = mesh_lines.size();
  element_buffer.create();
  element_buffer.bind();
  element_buffer.allocate(mesh_lines.data(),
                          mesh_count_lines * sizeof(GLuint) * 2);
  element_buffer.release();
}

void MeshGLWidget::drawBackground() {
  glClearColor(mesh_state.background.redF(), mesh_state.background.greenF(),
               mesh_state.background.blueF(), mesh_state.background.alphaF());
}

void MeshGLWidget::drawPointsIfNeeded() {
  if (mesh_state.points_style == PointsStyle::kNone) return;

  glPointSize(mesh_state.point_size);

  if (mesh_state.points_style == PointsStyle::kCircle) {
    glEnable(GL_POINT_SMOOTH);
  }

  if (mesh_state.points_style == PointsStyle::kSquare) {
    glDisable(GL_POINT_SMOOTH);
  }

  program->setUniformValue("FragColor", mesh_state.points_color);
  glDrawArrays(GL_POINTS, 0, s21::Controller::Get()->GetNumberOfVertices());
}

void MeshGLWidget::drawLines() {
  if (mesh_state.lines_style == LinesStyle::kDashed) {
    glEnable(GL_LINE_STIPPLE);
    glLineStipple(1, 0x000f);
  }

  if (mesh_state.lines_style == LinesStyle::kSolid) {
    glDisable(GL_LINE_STIPPLE);
  }

  glLineWidth(mesh_state.lines_width);

  program->setUniformValue("FragColor", mesh_state.lines_color);

  element_buffer.bind();
  glDrawElements(GL_LINES, mesh_count_lines * 2, GL_UNSIGNED_INT, nullptr);
  element_buffer.release();
}

void MeshGLWidget::CalculateMVPMatrix() {
  GLfloat ratio = (double)this->width() / (double)this->height();

  mvp_matrix.setToIdentity();

  mvp_matrix.ortho(-1.0, 1.0, -1.0 / ratio, 1.0 / ratio, -1.0, 1.0);

  if (mesh_state.is_perspective) {
    mvp_matrix.perspective(90.0, 1, 0.0, 100.0);
    mvp_matrix.translate(0.0, 0.0, -2.0);
  }

  mvp_matrix.scale(mesh_state.scaling);
  mvp_matrix.translate(mesh_state.position);
  mvp_matrix.rotate(mesh_state.degree.x(), 1, 0, 0);
  mvp_matrix.rotate(mesh_state.degree.y(), 0, 1, 0);
  mvp_matrix.rotate(mesh_state.degree.z(), 0, 0, 1);
}

bool MeshGLWidget::loadObject(const QString& filename) {
  s21::Controller::Get()->ProcessModel(filename.toStdString());
  int load_status = s21::Controller::Get()->GetStatus();
  bool is_loaded = (load_status == 0) ? true : false;

  if (is_loaded) {
    if (mesh_state.is_loaded) Cleanup();
    LoadObjectGeometry();
    initVertexBuffer();
    initElementBuffer();
    mesh_state.is_loaded = true;
  }

  update();
  return is_loaded;
}

void MeshGLWidget::Cleanup() {
  if (mesh_state.is_loaded == false) return;

  if (vertices_) delete[] vertices_;
  if (indices_) delete[] indices_;

  vertices_ = nullptr;
  indices_ = nullptr;

  vertex_buffer.destroy();
  element_buffer.destroy();
  vertex_array_object.destroy();

  mesh_count_lines = 0;
  mesh_state.is_loaded = false;
}

void MeshGLWidget::moveObjectX(float x) {
  mesh_state.position.setX(x);
  update();
}

void MeshGLWidget::moveObjectY(float y) {
  mesh_state.position.setY(y);
  update();
}

void MeshGLWidget::moveObjectZ(float z) {
  mesh_state.position.setZ(z);
  update();
}

void MeshGLWidget::rotateObjectX(float x) {
  mesh_state.degree.setX(x);
  update();
}

void MeshGLWidget::rotateObjectY(float y) {
  mesh_state.degree.setY(y);
  update();
}

void MeshGLWidget::rotateObjectZ(float z) {
  mesh_state.degree.setZ(z);
  update();
}

void MeshGLWidget::scaleObject(float percent) {
  mesh_state.scaling = percent / 100.0;
  update();
}

void MeshGLWidget::setLineWidth(float width) {
  mesh_state.lines_width = width;
  update();
}

void MeshGLWidget::setLineColor(QColor& color) {
  mesh_state.lines_color = color;
  update();
}

void MeshGLWidget::setLineStyle(LinesStyle style) {
  mesh_state.lines_style = style;
  update();
}
void MeshGLWidget::setPointsColor(QColor& color) {
  mesh_state.points_color = color;
  update();
}

void MeshGLWidget::setPointsSize(float size) {
  mesh_state.point_size = size;
  update();
}

void MeshGLWidget::setPointsStyle(PointsStyle style) {
  mesh_state.points_style = style;
  update();
}

void MeshGLWidget::setBackground(QColor& color) {
  mesh_state.background = color;
  update();
}

void MeshGLWidget::setCentralPerspective(bool is_central_perspective) {
  mesh_state.is_perspective = is_central_perspective;
  update();
}

GLuint MeshGLWidget::getCountNodes() {
  return (GLuint)s21::Controller::Get()->GetNumberOfVertices();
}

GLuint MeshGLWidget::getCountEdges() {
  return (GLuint)s21::Controller::Get()->GetNumberOfEdges();
}

}  // namespace s21
