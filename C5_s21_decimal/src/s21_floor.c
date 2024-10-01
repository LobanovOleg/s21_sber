#include "s21_decimal.h"

int s21_floor(s21_decimal value, s21_decimal *result) {
  initialize(result);
  info ssign = {0};
  get_exp(&ssign, &value);
  if (ssign.sign == 1) {
    s21_negate(value, &value);
  }
  s21_truncate(value, result);
  s21_decimal one = {{1, 0, 0, 0}};
  if (ssign.sign == 1) {
    s21_add(*result, one, result);
  }
  set_exp(result, 0);
  if (ssign.sign == 1) {
    s21_negate(*result, result);
  }
  return 0;
}
