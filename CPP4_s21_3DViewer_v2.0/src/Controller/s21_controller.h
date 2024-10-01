#ifndef CONTROLLER_S21_CONTROLLER_H_
#define CONTROLLER_S21_CONTROLLER_H_

#include "../Model/s21_model.h"

namespace s21 {
/** @class Controller
 *
 *  @brief The Controller class manages the application's logic and serves as
 * the global access point.
 */

class Controller {
 public:
  Controller(Controller const &other) = delete;  /// Should't be cloned.
  void operator=(const Controller &) = delete;   /// Should't be assignable.
  ~Controller();

  static Controller *Get();

  void ProcessModel(std::string path);
  std::vector<double> &GetVertices();
  std::vector<int> &GetIndices();
  int GetNumberOfPolygons();
  int GetNumberOfVertices();
  int GetNumberOfEdges();
  int GetNumberOfLines();
  int GetStatus();
  void Scale(float size);
  void Translate(double x, double y, double z);
  void Rotate(double x, double y, double z);

  std::vector<int> GetPolygonIndices(int polygonIndex);

 protected:
  Controller();

 private:
  static Controller *instance_;
  Model *model_;
  int is_object_loaded_;
};

}  // namespace s21
#endif  // CONTROLLER_S21_CONTROLLER_H_
