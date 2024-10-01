#include "s21_decimal.h"

int s21_div(s21_decimal value_1, s21_decimal value_2, s21_decimal *result) {
  if (value_2.bits[low] == 0 && value_2.bits[mid] == 0 &&
      value_2.bits[top] == 0)
    return DIV_BY_ZERO;
  initialize(result);
  info val_1 = {0};
  info val_2 = {0};
  get_exp(&val_1, &value_1);
  get_exp(&val_2, &value_2);
  if (val_1.exponent || val_2.exponent) {
    result->bits[scale] = val_1.exponent - val_2.exponent;
    result->bits[scale] <<= 16;
  }
  if (val_1.sign == val_2.sign) {
    set_bit_nums(&result->bits[scale], 0, 31);
  } else {
    set_bit_nums(&result->bits[scale], 1, 31);
  }
  if (value_2.bits[scale] > 0) {
    for (int k = 0; k < 32; k++) {
      set_bit_nums(&value_2.bits[scale], 0, k % 32);
    }
  }
  int i = 95;
  while (get_bit(value_1, i) == 0) i--;
  int sub_times = 0;
  s21_decimal tmp = {0};
  for (; i >= 0; i--) {
    shift_left(&tmp);
    set_bit(&tmp, get_bit(value_1, i), 0);
    if (s21_is_greater_or_equal(tmp, value_2)) {
      sub_times += 1;
      shift_left(result);
      set_bit(result, 1, 0);
      s21_sub(tmp, value_2, &tmp);
    } else if (sub_times != 0) {
      shift_left(result);
    }
  }
  return OK;
}