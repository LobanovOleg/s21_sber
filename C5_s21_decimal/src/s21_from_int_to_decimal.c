#include "s21_decimal.h"

int s21_from_int_to_decimal(int src, s21_decimal *dst) {
  int status = 0;
  if (abs(src) > s21_MAXDEC) {
    status = 1;
  }
  s21_clear_decimal(dst);
  if (src < 0) {
    src = -1 * src;
    s21_get_sign(*dst);
  }
  dst->bits[0] = src;
  return status;
}