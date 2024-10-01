#include "s21_controller.h"

namespace s21 {
Controller *Controller::instance_ = nullptr;

Controller::Controller() { model_ = new Model(); }

Controller::~Controller() { delete model_; }

Controller *Controller::Get() {
  if (instance_ == nullptr) instance_ = new Controller;
  return instance_;
}

void Controller::ProcessModel(std::string path) {
  is_object_loaded_ = model_->LoadingModel(path);
}

std::vector<double> &Controller::GetVertices() { return model_->GetVectorV(); }
std::vector<int> &Controller::GetIndices() { return model_->GetVectorF(); }
int Controller::GetNumberOfPolygons() { return model_->GetCountPolygons(); }
int Controller::GetNumberOfVertices() { return model_->GetCountVertices(); }
int Controller::GetNumberOfEdges() {
  int count_polygons = model_->GetCountPolygons();
  int count_vertices = model_->GetCountVertices();
  return count_polygons * 3 - count_vertices + 2;
}

std::vector<int> Controller::GetPolygonIndices(int polygonIndex) {
  std::vector<int> polygonIndices;
  int count_polygons = model_->GetCountPolygons();
  // Проверяем, что индекс полигона находится в допустимых пределах
  if (polygonIndex >= 0 && polygonIndex < count_polygons) {
    // Получаем индексы вершин для заданного полигона
    polygonIndices = model_->GetPolygonVertices(polygonIndex);
  }
  return polygonIndices;
}

int Controller::GetNumberOfLines() { return model_->GetCountLines(); }

int Controller::GetStatus() { return is_object_loaded_; }

void Controller::Scale(float size) { model_->Transform("scale", "0", size); }

void Controller::Translate(double x, double y, double z) {
  if (x != 0) model_->Transform("move", "x", x);
  if (y != 0) model_->Transform("move", "y", y);
  if (z != 0) model_->Transform("move", "z", z);
}

void Controller::Rotate(double x, double y, double z) {
  if (x != 0) model_->Transform("rotate", "x", x);
  if (y != 0) model_->Transform("rotate", "y", y);
  if (z != 0) model_->Transform("rotate", "z", z);
}

}  // namespace s21
