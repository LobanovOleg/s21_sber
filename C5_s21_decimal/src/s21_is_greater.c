#include "s21_decimal.h"

int s21_is_greater(s21_decimal value_1, s21_decimal value_2) {
  if (both_zeroes(value_1, value_2))
    return 0;
  else
    return s21_is_less(value_2, value_1);
}