#include "s21_decimal.h"

int s21_is_equal(s21_decimal value_1, s21_decimal value_2) {
  if (both_zeroes(value_1, value_2)) return 1;
  info getinfo_1 = {0};
  info getinfo_2 = {0};
  get_exp(&getinfo_1, &value_1);
  get_exp(&getinfo_2, &value_2);
  if (getinfo_1.sign != getinfo_2.sign) return COMPAR_FALSE;
  equal_exp(getinfo_1.exponent, getinfo_2.exponent, &value_1, &value_2);
  if (bits_eq(value_1.bits, value_2.bits)) {
    return COMPAR_TRUE;
  } else {
    return COMPAR_FALSE;
  }
}
