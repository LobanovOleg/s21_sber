#include "s21_decimal.h"

int s21_mul(s21_decimal value_1, s21_decimal value_2, s21_decimal *result) {
  initialize(result);
  info val_1 = {0};
  info val_2 = {0};
  get_exp(&val_1, &value_1);
  get_exp(&val_2, &value_2);
  if (val_1.exponent + val_2.exponent > 28) return TOO_SMALL_OR_NEG_INF;
  s21_decimal tmp = {0};
  int bit_1 = 0;
  int bit_2 = 0;
  // int tmp_mul = 1;
  for (int i = 0; i < 96; i++) {
    bit_2 = get_bit(value_2, i);
    for (int k = 0; k < 96; k++) {
      bit_1 = get_bit(value_1, k);
      set_bit_nums(&tmp.bits[k / 32], bit_1 & bit_2, k);
    }
    if (((get_bit_nums(result->bits[top], 31) == 1 && i != 95) ||
         get_bit_nums(tmp.bits[top], 31) == 1) &&
        tmp.bits[low] != 0 && tmp.bits[mid] != 0 && tmp.bits[top] != 0) {
      if (val_1.sign == val_2.sign) {
        return TOO_LARGE_OR_INF;
      } else if (val_1.sign != val_2.sign) {
        return TOO_SMALL_OR_NEG_INF;
      }
    }
    if (i != 0) {
      for (int j = 0; j < i; j++) {
        if (get_bit_nums(tmp.bits[top], 31) == 1) {
          if (val_1.sign == val_2.sign) {
            return TOO_LARGE_OR_INF;
          } else if (val_1.sign != val_2.sign) {
            return TOO_SMALL_OR_NEG_INF;
          }
        }
        shift_left(&tmp);
        // tmp_mul++;
      }
    }
    pre_add(tmp, *result, result);
    tmp.bits[low] = 0;
    tmp.bits[mid] = 0;
    tmp.bits[top] = 0;
    // if (tmp_mul == 32) tmp_mul = 1;
    if (val_1.exponent || val_2.exponent) {
      result->bits[scale] = val_1.exponent + val_2.exponent;
      result->bits[scale] <<= 16;
    }
    if (val_1.sign == val_2.sign) {
      set_bit_nums(&result->bits[scale], 0, 31);
    } else {
      set_bit_nums(&result->bits[scale], 1, 31);
    }
  }
  return OK;
}