#ifndef MODEL_S21_LOADER_H_
#define MODEL_S21_LOADER_H_

#include <cstring>
#include <fstream>
#include <sstream>
#include <string>
#include <vector>

namespace s21 {

/** @class Loader
 *
 *  @brief The Loader class is upload objects and making parse of Verties and
 * Polygons
 */
class Loader {
 public:
  Loader() {}
  ~Loader() {}

  // getters
  std::vector<double>& GetVectorV();
  std::vector<int>& GetVectorF();
  int GetCountVertices();
  int GetCountPolygons();

  int LoadingFile(const std::string& filename);

 private:
  int Parsing(std::ifstream& file);
  // parsing and counting v-strings
  void SetVertices(const std::string& line);
  // parsing and counting polygons
  void SetPolygons(const std::string& line);

  // clearing vector_v_, vector_f_, counts of vertices and polygons. Set
  // value_max_ to -1
  void Clearing();

  // normalize to (-1..1)
  void Normalize();

  /**
   * @brief is countain valid values on input string
   * @param line input string
   * @return true/false
   */
  bool IsValidString(const std::string& line);
  std::string parseLine(const std::string& line);

  std::vector<double> vector_v_{};
  std::vector<int> vector_f_{};
  int count_vertices_ = 0;
  int count_polygons_ = 0;
  double value_max_ = -1;
};

}  // namespace s21

#endif  // MODEL_S21_LOADER_H_
