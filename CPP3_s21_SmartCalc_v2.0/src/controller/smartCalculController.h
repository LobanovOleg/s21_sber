#ifndef CPP3_SMARTCALC_SRC_SMARTCALCULCONTROLLER_H_
#define CPP3_SMARTCALC_SRC_SMARTCALCULCONTROLLER_H_

#include "./../model/smartCalculModel.h"

namespace s21 {
class SmartCalculController {
 private:
  SmartCalculModel *model_;

 public:
  SmartCalculController();
  ~SmartCalculController() { delete model_; };
  double get_result(const char *expr_input);
};
}  // namespace s21
#endif  // CPP3_SMARTCALC_SRC_SMARTCALCULCONTROLLER_H_