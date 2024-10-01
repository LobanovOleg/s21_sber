#include "s21_decimal.h"

int s21_truncate(s21_decimal value, s21_decimal *result) {
  initialize(result);
  info inf_val = {0};
  s21_decimal pow = {{10, 0, 0, 0}};
  get_exp(&inf_val, &value);
  value.bits[scale] = 0;

  if (inf_val.exponent > 28) {
    return CONVERT_ERROR;
  }
  if (!inf_val.exponent) {
    *result = value;
  } else {
    while (inf_val.exponent) {
      s21_div(value, pow, result);
      value = *result;
      inf_val.exponent--;
    }
  }
  set_info(result, inf_val.sign, 0);
  return OK;
}
