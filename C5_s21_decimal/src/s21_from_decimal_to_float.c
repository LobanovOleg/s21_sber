#include "s21_decimal.h"

int s21_from_decimal_to_float(s21_decimal src, float *dst) {
  int status = 0;
  *dst = 0;
  if (dst == NULL) {
  } else {
    int minus = 1;
    long double result = 0, two = 1;
    int exp = s21_get_exp(src);
    if (s21_get_sign(src) == 1) minus = -1;
    for (int k = 0; k < 96; k++) {
      if (checkBit(&src, k)) {
        result += two;
      }
      two *= 2;
    }
    for (int k = 0; k < exp; k++) {
      result /= 10;
    }
    *dst = minus * result;
  }
  return status;
}