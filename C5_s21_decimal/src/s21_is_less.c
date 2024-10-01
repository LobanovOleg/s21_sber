#include "s21_decimal.h"

int s21_is_less(s21_decimal value_1, s21_decimal value_2) {
  if (both_zeroes(value_1, value_2)) return 0;
  if ((lessnes(value_1, value_2) == 1) &&
      (get_bit_nums(value_1.bits[scale], 31) == 1) &&
      (get_bit_nums(value_2.bits[scale], 31) == 1))
    return 0;
  else if ((lessnes(value_1, value_2) == 0) &&
           (get_bit_nums(value_1.bits[scale], 31) == 1) &&
           (get_bit_nums(value_2.bits[scale], 31) == 1))
    return 1;
  else
    return lessnes(value_1, value_2);
}
