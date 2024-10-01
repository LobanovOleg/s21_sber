#include "s21_decimal.h"

int s21_from_decimal_to_int(s21_decimal src, int *dst) {
  int status = 0;
  if (dst) {
    if (s21_get_sign(src) == 1) {
      *dst = -1 * (int)(src.bits[0] / pow(10, s21_get_exp(src)));
    } else {
      *dst = (int)(src.bits[0] / pow(10, s21_get_exp(src)));
    }
  } else {
    status = 1;
  }
  return status;
}