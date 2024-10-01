#include "s21_decimal.h"

int s21_add(s21_decimal value_1, s21_decimal value_2, s21_decimal *result) {
  info getinfo_1 = {0};
  info getinfo_2 = {0};
  get_exp(&getinfo_1, &value_1);
  get_exp(&getinfo_2, &value_2);
  int max = 0;

  if (getinfo_1.sign == getinfo_2.sign) {
    max = equal_exp(getinfo_1.exponent, getinfo_2.exponent, &value_1, &value_2);
    if (pre_add(value_1, value_2, result) == 1) {
      if (getinfo_1.sign == 1 && max == 0) {
        return TOO_SMALL_OR_NEG_INF;
      } else if (getinfo_1.sign == 0 && max == 0) {
        return TOO_LARGE_OR_INF;
      }
    }
    set_info(result, getinfo_1.sign, max);
  } else if (getinfo_1.sign == 1) {
    set_info(&value_1, 0, getinfo_1.exponent);
    return (s21_sub(value_2, value_1, result));
  } else if (getinfo_2.sign == 1) {
    set_info(&value_2, 0, getinfo_2.exponent);
    return (s21_sub(value_1, value_2, result));
  }
  return OK;
}
