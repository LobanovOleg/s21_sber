#ifndef CPP3_SMARTCALC_SRC_SMARTCALCULMODEL_H_
#define CPP3_SMARTCALC_SRC_SMARTCALCULMODEL_H_

#include <cmath>
#include <cstring>
#include <iostream>
#include <stack>
#include <string>

enum Operation {
  Empty,
  Plus,
  Minus,
  Mult,
  Div,
  Mod,
  Pow,
  UMinus,
  Cos,
  Sin,
  Tan,
  Acos,
  Asin,
  Atan,
  Sqrt,
  Ln,
  Log,
  LeftBracket = -1,
  RightBracket = -2
};

enum Priority { LowMin, Low, LowMax, MiddleMin, Middle, MiddleMax, High };

namespace s21 {
class SmartCalculModel {
 private:
  std::stack<Operation> container_operators_;
  std::stack<double> container_numbers_;

 public:
  SmartCalculModel() : container_operators_(), container_numbers_(){};
  ~SmartCalculModel() noexcept = default;

 public:
  void calculOneOperation();

 public:
  void GetStringFromCalculator(const char *expr_input);
  void GeneralCalculation(const char *expr_input);
  int MoveToNextSymbolInString(const char **expr_input, Operation opr);
  Operation CheckOperationType(const char **expr_input, int &index_string);
  double CheckNumber(const char **expr_input, int &index_string);
  bool AddOrReturnOperation(Operation opr);
  Priority CheckPriority(Operation opr);
  void DoBinaryOperation(Operation opr);
  void DoUnaryOperation(Operation opr);
  double get_container_numbers();
  void CheckExcVariabPushContainerNumbers(double tmp_result);
  void ClearAllContainers() noexcept;
};
}  // namespace s21
#endif  // CPP3_SMARTCALC_SRC_SMARTCALCULMODEL_H_