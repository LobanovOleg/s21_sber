#include "s21_loader.h"

#include <chrono>
#include <iostream>

namespace s21 {

int Loader::LoadingFile(const std::string& filename) {
  int err = 0;
  auto start = std::chrono::high_resolution_clock::now();
  // clearing before start
  Clearing();
  // err = 2 - can't open file
  std::ifstream file(filename);
  if (!file.is_open()) {
    err = 2;
    return err;
  }
  auto end = std::chrono::high_resolution_clock::now();
  auto duration =
      std::chrono::duration_cast<std::chrono::milliseconds>(end - start)
          .count();
  std::cout << "Opening time: " << duration << " milliseconds" << std::endl;

  auto start1 = std::chrono::high_resolution_clock::now();
  // fill vertex and polygon
  err = Parsing(file);
  auto end1 = std::chrono::high_resolution_clock::now();
  auto duration1 =
      std::chrono::duration_cast<std::chrono::milliseconds>(end1 - start1)
          .count();
  std::cout << "Parsing time: " << duration1 << " milliseconds" << std::endl;
  auto start2 = std::chrono::high_resolution_clock::now();
  Normalize();
  auto end2 = std::chrono::high_resolution_clock::now();
  auto duration2 =
      std::chrono::duration_cast<std::chrono::milliseconds>(end2 - start2)
          .count();
  std::cout << "Normalizing time: " << duration2 << " milliseconds"
            << std::endl;
  // if error situation drop and clear
  if (err != 0) {
    Clearing();
  }
  file.close();
  return err;
}

void Loader::Clearing() {
  vector_v_.clear();
  vector_f_.clear();
  count_vertices_ = 0;
  count_polygons_ = 0;
  value_max_ = -1;
}

int Loader::Parsing(std::ifstream& file) {
  int err = 0;
  std::string line;

  while (std::getline(file, line)) {
    // if "v_0_0_" or "f_0_0_" < 5 chars -> string incorrect, continue parsing
    if (line.length() < 5) {
      continue;
    }
    // find and parsing string start with 'v_'
    if (line[0] == 'v' && line[1] == ' ') {
      if (IsValidString(line)) {
        SetVertices(line);
      }
      // find and parsing string start with 'f_'
    } else if (line[0] == 'f' && line[1] == ' ') {
      if (IsValidString(line)) {
        SetPolygons(line);
      }
    }
  }

  // if no correct strings retrun err = 1
  if (count_vertices_ == 0 || count_polygons_ == 0) {
    err = 1;
  }
  return err;
}

bool Loader::IsValidString(const std::string& line) {
  if (line.empty()) return false;
  std::istringstream iss(line);
  std::vector<std::string> tokens;

  std::string token;
  while (iss >> token) {
    tokens.push_back(token);
  }

  std::string validChars = "+-1234567890./ ";

  if (line[0] == 'v' || line[0] == 'f') {
    for (size_t i = 1; i < line.size(); ++i) {
      if (!std::strchr(validChars.c_str(), line[i])) {
        return false;
      }
    }
    return true;
  }
  return false;
}

void Loader::SetVertices(const std::string& line) {
  bool success = false;
  double x = 0, y = 0, z = 0;

  std::stringstream iss(line);
  char ch;
  if (iss >> ch >> x >> y >> z) {
    success = true;
  } else {
    success = false;
  }

  if (success) {
    vector_v_.insert(vector_v_.end(), {x, y, z});
    if (std::abs(x) > value_max_) {
      value_max_ = std::abs(x);
    }
    if (std::abs(y) > value_max_) {
      value_max_ = std::abs(y);
    }
    if (std::abs(z) > value_max_) {
      value_max_ = std::abs(z);
    }
    count_vertices_++;
  }
}

std::string Loader::parseLine(const std::string& line) {
  std::istringstream iss(line);
  std::string result;

  std::string token;
  while (iss >> token) {
    size_t pos = token.find('/');
    if (pos != std::string::npos) {
      result += token.substr(0, pos) + " ";
    } else {
      result += token + " ";
    }
  }
  return result;
}

void Loader::SetPolygons(const std::string& line) {
  int num1 = 0, num2 = 0, num3 = 0;
  char f;

  std::string parsedLine = parseLine(line);
  std::istringstream iss(parsedLine);
  iss >> f;
  iss >> num1 >> num2 >> num3;

  if (num1 < 1 || num2 < 1 || num3 < 1) {
    std::cerr << "Invalid data: " << num1 << ", " << num2 << ", " << num3
              << std::endl;
    return;
  }
  vector_f_.push_back(num1 - 1);
  vector_f_.push_back(num2 - 1);
  vector_f_.push_back(num3 - 1);

  count_polygons_++;
}

void Loader::Normalize() {
  if (value_max_ > 1) {
    for (double& value : vector_v_) {
      value = value / value_max_;
    }
  }
}

std::vector<double>& Loader::GetVectorV() { return vector_v_; }
std::vector<int>& Loader::GetVectorF() { return vector_f_; }

int Loader::GetCountVertices() { return count_vertices_; }
int Loader::GetCountPolygons() { return count_polygons_; }
}  // namespace s21
