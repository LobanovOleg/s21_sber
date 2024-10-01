#include "s21_decimal.h"

int s21_from_float_to_decimal(float src, s21_decimal *dst) {
  int status = 0;
  if (fabs(src) < 2e-28) {
    s21_clear_decimal(dst);
    status = 1;
  }
  if (fabs(src) > s21_MAXDEC) {
    status = 1;
  }
  if (dst) {
    s21_clear_decimal(dst);
    int sign = 0;
    if (src < 0) {
      sign = 1;
      src = -(src);
    }
    long int new = (long int)src;
    long int exp = 0;
    while (src - ((float)new / (long int)(pow(10, exp))) != 0) {
      exp++;
      new = src *(long int)(pow(10, exp));
    }
    s21_from_int_to_decimal(new, dst);
    if (sign) {
      s21_set_sign(dst);
    }
    dst->bits[3] += exp << 16;
  } else {
    status = 1;
  }
  return status;
}