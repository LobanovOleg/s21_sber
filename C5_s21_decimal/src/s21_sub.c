#include "s21_decimal.h"

int s21_sub(s21_decimal value_1, s21_decimal value_2, s21_decimal *result) {
  info inf_value_1 = {0};
  info inf_value_2 = {0};
  int res = OK;
  int flag = 0;
  int max = 0;
  int sign = 0;
  if (lessnes(value_1, value_2) && get_bit_nums(value_1.bits[scale], 31) ==
                                       get_bit_nums(value_2.bits[scale], 31)) {
    swap(&value_1, &value_2);
    flag = 1;
    if (get_bit_nums(value_1.bits[scale], 31)) {
      sign = 1;
    }
  }
  get_exp(&inf_value_1, &value_1);
  get_exp(&inf_value_2, &value_2);
  if (inf_value_1.sign == 0 && inf_value_2.sign == 0) {
    max = equal_exp(inf_value_1.exponent, inf_value_2.exponent, &value_1,
                    &value_2);
    if (pre_sub(value_1, value_2, result) == 2) {
      return TOO_SMALL_OR_NEG_INF;
    }
    set_info(result, inf_value_1.sign, max);
    if (flag == 1) {
      set_sign(result, 1);
    }
  }
  if (inf_value_1.sign == 0 && inf_value_2.sign == 1) {
    set_bit_nums(&value_2.bits[scale], 0, 31);
    if ((s21_add(value_1, value_2, result)) == 1) {
      return TOO_LARGE_OR_INF;
    }
  }
  if (inf_value_1.sign == 1 && inf_value_2.sign == 0) {
    set_bit_nums(&value_1.bits[scale], 0, 31);
    if ((s21_add(value_1, value_2, result)) == 1) {
      return TOO_SMALL_OR_NEG_INF;
    }
    set_sign(result, 1);
  }
  if (inf_value_1.sign == 1 && inf_value_2.sign == 1) {
    max = equal_exp(inf_value_1.exponent, inf_value_2.exponent, &value_1,
                    &value_2);
    if (pre_sub(value_1, value_2, result) == 2) {
      return TOO_SMALL_OR_NEG_INF;
    }
    set_exp(result, max);
    if (s21_is_less(value_1, value_2) && flag == 0) {
      set_bit_nums(&result->bits[scale], 1, 31);
    } else if (s21_is_less(value_2, value_1)) {
      if (sign == 1) {
        set_bit_nums(&result->bits[scale], 0, 31);
      } else {
        set_bit_nums(&result->bits[scale], 1, 31);
      }
    }
  }
  return res;
}