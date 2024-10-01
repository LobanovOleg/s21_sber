#ifndef MODEL_S21_TRANSFORMATIONS_H_
#define MODEL_S21_TRANSFORMATIONS_H_

#include <cmath>

namespace s21 {

/** @class Transformation
 *
 *  @brief The Transformation class manages the object's affine
 * transformations
 */
class Transformation {
 public:
  Transformation() {}
  ~Transformation() {}

  void move_x(std::vector<double> *vector_v_, double value) {
    value = value / 100;
    double del_x = value - value_move_x_prev_;
    for (auto it = (*vector_v_).begin(); it < (*vector_v_).end(); it += 3) {
      *it = *it + del_x;
    }
    value_move_x_prev_ = value;
  }

  void move_y(std::vector<double> *vector_v_, double value) {
    value = value / 100;
    double del_y = value - value_move_y_prev_;
    for (auto it = (*vector_v_).begin() + 1; it < (*vector_v_).end(); it += 3) {
      *it = *it + del_y;
    }
    value_move_y_prev_ = value;
  }

  void move_z(std::vector<double> *vector_v_, double value) {
    value = value / 100;
    double del_z = value - value_move_z_prev_;
    for (auto it = (*vector_v_).begin() + 2; it < (*vector_v_).end(); it += 3) {
      *it = *it + del_z;
    }
    value_move_z_prev_ = value;
  }

  void rotate_x(std::vector<double> *vector_v_, double value) {
    double del_x = value - value_rotate_x_prev_;
    double radians = convert_degrees_to_radians(del_x);
    double tmp_y = 0;
    double tmp_z = 0;
    for (auto it = (*vector_v_).begin(); it != (*vector_v_).end();
         it = it + 3) {
      tmp_y = *(it + 1);                                         // save y
      tmp_z = *(it + 2);                                         // save z
      *(it + 1) = tmp_y * cos(radians) + tmp_z * sin(radians);   // change y
      *(it + 2) = -tmp_y * sin(radians) + tmp_z * cos(radians);  // change z
    }
    value_rotate_x_prev_ = value;
  }

  void rotate_y(std::vector<double> *vector_v_, double value) {
    double del_y = value - value_rotate_y_prev_;
    double radians = convert_degrees_to_radians(del_y);
    double tmp_x = 0;
    double tmp_z = 0;
    for (auto it = (*vector_v_).begin(); it != (*vector_v_).end();
         it = it + 3) {
      tmp_x = *it;                                               // save x
      tmp_z = *(it + 2);                                         // save z
      *(it) = tmp_x * cos(radians) + tmp_z * sin(radians);       // change x
      *(it + 2) = -tmp_x * sin(radians) + tmp_z * cos(radians);  // change z
    }
    value_rotate_y_prev_ = value;
  }

  void rotate_z(std::vector<double> *vector_v_, double value) {
    double del_z = value - value_rotate_z_prev_;
    double radians = convert_degrees_to_radians(del_z);
    double tmp_x = 0;
    double tmp_y = 0;
    for (auto it = (*vector_v_).begin(); it != (*vector_v_).end();
         it = it + 3) {
      tmp_x = *(it);      // save x
      tmp_y = *(it + 1);  // save y
      *(it) = tmp_x * cos(radians) - tmp_y * sin(radians);
      *(it + 1) = tmp_x * sin(radians) + tmp_y * cos(radians);
    }
    value_rotate_z_prev_ = value;
  }

  double convert_degrees_to_radians(double degree) {
    return degree * M_PI / 180;
  }

  void scale(std::vector<double> *vector_v_, double value) {
    if (fabs(value) < 10e-7) return;

    mul_ = value;

    // get scale sign (+ or -)
    if (mul_ < 0) {
      mul_pos_ = 0;
    } else {
      mul_pos_ = 1;
    }

    // scaling result vector
    if (mul_pos_ == 1) {
      for (auto it = (*vector_v_).begin(); it < (*vector_v_).end(); it++) {
        *it = *it * mul_;
      }
    } else {
      for (auto it = (*vector_v_).begin(); it < (*vector_v_).end(); it++) {
        *it = *it / (-1 * mul_);
      }
    }
  }

 private:
  double value_move_x_prev_, value_move_y_prev_, value_move_z_prev_ = 0;
  double value_rotate_x_prev_, value_rotate_y_prev_, value_rotate_z_prev_ = 0;
  double mul_, mul_pos_ = 1;
};

}  // namespace s21

#endif  // MODEL_S21_TRANSFORMATIONS_H_
