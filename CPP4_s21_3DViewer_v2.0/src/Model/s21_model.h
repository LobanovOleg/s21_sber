#ifndef MODEL_S21_MODEL_H_
#define MODEL_S21_MODEL_H_

#include "s21_loader.h"
#include "s21_transformations.h"

namespace s21 {

/** @class Model
 *
 *  @brief The Model class using Loader to upload files, manage
 * transformations, counting everything
 */
class Model {
 public:
  Model() {}
  ~Model() {}

  int LoadingModel(const std::string &file_name) {
    int err = loader_.LoadingFile(file_name);
    vector_v_ = loader_.GetVectorV();
    vector_f_ = loader_.GetVectorF();
    count_vertices_ = loader_.GetCountVertices();
    count_polygons_ = loader_.GetCountPolygons();
    return err;
  }

  std::vector<double> &GetVectorV() { return vector_v_; }
  std::vector<int> &GetVectorF() { return vector_f_; }
  int GetCountVertices() { return count_vertices_; }
  int GetCountPolygons() { return count_polygons_; }
  int GetCountLines() { return vector_f_.size(); }

  void Transform(std::string action, std::string axis, double value) {
    if (action == "scale" && axis == "0") {
      transformation_.scale(&vector_v_, value);
    } else if (action == "move" && axis == "x") {
      transformation_.move_x(&vector_v_, value);
    } else if (action == "move" && axis == "y") {
      transformation_.move_y(&vector_v_, value);
    } else if (action == "move" && axis == "z") {
      transformation_.move_z(&vector_v_, value);
    } else if (action == "rotate" && axis == "x") {
      transformation_.rotate_x(&vector_v_, value);
    } else if (action == "rotate" && axis == "y") {
      transformation_.rotate_y(&vector_v_, value);
    } else if (action == "rotate" && axis == "z") {
      transformation_.rotate_z(&vector_v_, value);
    }
  }

  std::vector<int> GetPolygonVertices(int polygonIndex) const {
    std::vector<int> polygonVertices;
    if (polygonIndex >= 0 &&
        static_cast<size_t>(polygonIndex) < vector_f_.size()) {
      // Получаем индексы вершин для заданного полигона
      int startIndex = polygonIndex * 3;  // Полигон имеет три вершины
      polygonVertices = {vector_f_[startIndex], vector_f_[startIndex + 1],
                         vector_f_[startIndex + 2]};
    }
    return polygonVertices;
  }

 private:
  std::vector<double> vector_v_{};
  std::vector<int> vector_f_{};
  int count_vertices_ = 0;
  int count_polygons_ = 0;
  Loader loader_;
  Transformation transformation_;
};

}  // namespace s21

#endif  // MODEL_S21_MODEL_H_
