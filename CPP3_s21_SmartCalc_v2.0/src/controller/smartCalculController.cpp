#include "smartCalculController.h"

s21::SmartCalculController::SmartCalculController()
    : model_(new s21::SmartCalculModel) {}

double s21::SmartCalculController::get_result(const char *expr_input) {
  model_->GetStringFromCalculator(expr_input);
  return model_->get_container_numbers();
}