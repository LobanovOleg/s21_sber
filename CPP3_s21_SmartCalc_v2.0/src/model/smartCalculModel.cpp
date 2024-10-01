#include "smartCalculModel.h"

void s21::SmartCalculModel::calculOneOperation() {
  bool doCalcul = true;
  bool bracket = false;
  while (doCalcul) {
    if (!container_operators_.empty() &&
        container_operators_.top() == LeftBracket) {
      container_operators_.pop();
      doCalcul = false;
      bracket = false;
    } else if (!container_operators_.empty() &&
               container_operators_.top() == RightBracket) {
      container_operators_.pop();
      bracket = true;
    } else if (!container_operators_.empty() &&
               container_operators_.top() >= Plus &&
               container_operators_.top() <= Pow) {
      DoBinaryOperation(container_operators_.top());
      container_operators_.pop();
      if (bracket != true) {
        doCalcul = false;
      }
    } else if (!container_operators_.empty() &&
               container_operators_.top() >= UMinus &&
               container_operators_.top() <= Log) {
      DoUnaryOperation(container_operators_.top());
      container_operators_.pop();
      if (bracket != true) {
        doCalcul = false;
      }
    } else {
      ClearAllContainers();
      throw std::invalid_argument("ERROR!");
    }
  }
}

void s21::SmartCalculModel::GetStringFromCalculator(const char *expr_input) {
  if (strlen(expr_input) == 0) {
    throw std::invalid_argument("ERROR! Input string is empty.");
  }
  GeneralCalculation(expr_input);
}

void s21::SmartCalculModel::GeneralCalculation(const char *expr_input) {
  int index_string = 0;
  while (*expr_input) {
    Operation type_operation = CheckOperationType(&expr_input, index_string);
    if (type_operation != Empty) {
      index_string += MoveToNextSymbolInString(&expr_input, type_operation);
      bool add_to_stack = AddOrReturnOperation(type_operation);
      while (add_to_stack == false) {
        calculOneOperation();
        add_to_stack = AddOrReturnOperation(type_operation);
      }
    } else {
      double number = CheckNumber(&expr_input, index_string);
      container_numbers_.push(number);
    }
  }
  while (!container_operators_.empty()) {
    calculOneOperation();
  }
  if (container_numbers_.size() > 1) {
    ClearAllContainers();
    throw std::invalid_argument("ERROR!");
  }
}

int s21::SmartCalculModel::MoveToNextSymbolInString(const char **expr_input,
                                                    Operation opr) {
  int move_string_point = 1;
  if (opr == Mod || opr == Sin || opr == Cos || opr == Tan || opr == Sqrt ||
      opr == Log) {
    move_string_point += 2;
  } else if (opr == Acos || opr == Asin || opr == Atan) {
    move_string_point += 3;
  } else if (opr == Ln) {
    move_string_point += 1;
  }
  *expr_input += move_string_point;
  return move_string_point;
}

Operation s21::SmartCalculModel::CheckOperationType(const char **expr_input,
                                                    int &index_string) {
  Operation opr = Empty;
  //    When '-' and next LeftBracket or number -> UMinus
  if (**expr_input == '-' && (*(*expr_input + 1) == '(' || index_string == 0) &&
      *(*expr_input - 1) != ')') {
    return UMinus;
  } else if (**expr_input == '-' && index_string != 0 &&
             *(*expr_input - 1) != '(' &&
             ((*(*expr_input - 1) >= 48 && *(*expr_input - 1) <= 57) ||
              *(*expr_input - 1) == '.' || *(*expr_input - 1) == ')')) {
    return Minus;
  } else if (**expr_input == '-') {
    return UMinus;
  } else if (**expr_input == '+') {
    return Plus;
  } else if (**expr_input == '*') {
    return Mult;
  } else if (**expr_input == '/') {
    return Div;
  } else if (**expr_input == '^') {
    return Pow;
  } else if (**expr_input == '(') {
    return LeftBracket;
  } else if (**expr_input == ')') {
    return RightBracket;
  } else if (strncmp(*expr_input, "√", 3) == 0) {
    return Sqrt;
  } else if (strncmp(*expr_input, "mod", 3) == 0) {
    return Mod;
  } else if (strncmp(*expr_input, "sin", 3) == 0) {
    return Sin;
  } else if (strncmp(*expr_input, "cos", 3) == 0) {
    return Cos;
  } else if (strncmp(*expr_input, "tan", 3) == 0) {
    return Tan;
  } else if (strncmp(*expr_input, "log", 3) == 0) {
    return Log;
  } else if (strncmp(*expr_input, "ln", 2) == 0) {
    return Ln;
  } else if (strncmp(*expr_input, "acos", 4) == 0) {
    return Acos;
  } else if (strncmp(*expr_input, "asin", 4) == 0) {
    return Asin;
  } else if (strncmp(*expr_input, "atan", 4) == 0) {
    return Atan;
  }
  return opr;
}

double s21::SmartCalculModel::CheckNumber(const char **expr_input,
                                          int &index_string) {
  if (strncmp(*expr_input, "π", 2) == 0) {
    *expr_input += 2;
    index_string += 1;
    return M_PI;
  } else if (**expr_input == 'e') {
    *expr_input += 1;
    index_string += 1;
    return M_E;
  }
  char *end = nullptr;
  double number = strtod(*expr_input, &end);
  if (**expr_input == '.') {
    *expr_input += 1;
    index_string += 1;
  } else if (*expr_input != end) {
    *expr_input = end;
    index_string += (int)std::to_string(number).size();
  } else {
    ClearAllContainers();
    throw std::invalid_argument("ERROR!");
  }
  return number;
}

bool s21::SmartCalculModel::AddOrReturnOperation(Operation opr) {
  Priority prior_new = CheckPriority(opr);
  if (opr == UMinus) {
    container_operators_.push(opr);
    return true;
  } else if (container_operators_.empty() || prior_new == LowMin ||
             prior_new == MiddleMax ||
             CheckPriority(container_operators_.top()) < prior_new ||
             (prior_new == MiddleMin &&
              CheckPriority(container_operators_.top()) == MiddleMin)) {
    container_operators_.push(opr);
    return true;
  }
  return false;
}

Priority s21::SmartCalculModel::CheckPriority(Operation opr) {
  if (opr == LeftBracket) {
    return LowMin;
  } else if (opr == Plus || opr == Minus) {
    return Low;
  } else if (opr >= Mult && opr <= Mod) {
    return LowMax;
  } else if (opr == Pow) {
    return MiddleMin;
  } else if (opr == UMinus) {
    return Middle;
  } else if (opr >= Cos && opr <= Log) {
    return MiddleMax;
  } else if (opr == RightBracket) {
    return High;
  }
  return LowMin;
}

void s21::SmartCalculModel::DoBinaryOperation(Operation opr) {
  if (container_numbers_.size() < 2) {
    ClearAllContainers();
    throw std::invalid_argument("ERROR! Not enough numbers.");
  }
  double second_number = container_numbers_.top();
  container_numbers_.pop();
  double first_number = container_numbers_.top();
  container_numbers_.pop();
  double tmp_result = 0;
  if (opr == Plus) {
    tmp_result = first_number + second_number;
  } else if (opr == Minus) {
    tmp_result = first_number - second_number;
  } else if (opr == Mult) {
    tmp_result = first_number * second_number;
  } else if (opr == Div) {
    tmp_result = first_number / second_number;
  } else if (opr == Mod) {
    tmp_result = std::fmod(first_number, second_number);
  } else if (opr == Pow) {
    tmp_result = std::pow(first_number, second_number);
  }
  CheckExcVariabPushContainerNumbers(tmp_result);
}

void s21::SmartCalculModel::DoUnaryOperation(Operation opr) {
  if (container_numbers_.empty()) {
    ClearAllContainers();
    throw std::invalid_argument("ERROR! Not enough numbers.");
  }
  double number = container_numbers_.top();
  container_numbers_.pop();
  double tmp_result = 0;
  if (opr == UMinus) {
    tmp_result = -1 * number;
  } else if (opr == Cos) {
    tmp_result = std::cos(number);
  } else if (opr == Sin) {
    tmp_result = std::sin(number);
  } else if (opr == Tan) {
    tmp_result = std::tan(number);
  } else if (opr == Acos) {
    tmp_result = std::acos(number);
  } else if (opr == Asin) {
    tmp_result = std::asin(number);
  } else if (opr == Atan) {
    tmp_result = std::atan(number);
  } else if (opr == Sqrt) {
    tmp_result = std::sqrt(number);
  } else if (opr == Ln) {
    tmp_result = std::log(number);
  } else if (opr == Log) {
    tmp_result = std::log10(number);
  }
  CheckExcVariabPushContainerNumbers(tmp_result);
}

void s21::SmartCalculModel::CheckExcVariabPushContainerNumbers(
    double tmp_result) {
  if (std::isnan(tmp_result) || std::isinf(tmp_result)) {
    ClearAllContainers();
    throw std::invalid_argument("ERROR!");
  } else {
    container_numbers_.push(tmp_result);
  }
}

double s21::SmartCalculModel::get_container_numbers() {
  if (container_numbers_.empty()) {
    ClearAllContainers();
    throw std::out_of_range("ERROR!");
  } else {
    double tmp_result = container_numbers_.top();
    ClearAllContainers();
    return tmp_result;
  }
}

void s21::SmartCalculModel::ClearAllContainers() noexcept {
  while (!container_operators_.empty()) {
    container_operators_.pop();
  }
  while (!container_numbers_.empty()) {
    container_numbers_.pop();
  }
}