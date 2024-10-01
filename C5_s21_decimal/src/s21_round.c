#include "s21_decimal.h"

int s21_round(s21_decimal value, s21_decimal *result) {
  s21_decimal ostatok = {{5, 0, 0, 0}};
  s21_decimal mod_res = {0};
  s21_decimal one = {{1, 0, 0, 0}};
  initialize(result);
  info ssign = {0};
  get_exp(&ssign, &value);
  if (ssign.sign == 1) {
    s21_negate(value, &value);
  }
  s21_truncate(value, result);
  s21_decimal for_mod = {{pow(10, ssign.exponent), 0, 0, 0}};
  s21_mod(value, for_mod, &mod_res);
  set_exp(&ostatok, 1);
  if (s21_is_less_or_equal(ostatok, mod_res)) {
    s21_add(*result, one, result);
  }
  info res = {0};
  get_exp(&res, result);
  res.exponent = 0;
  set_exp(result, res.exponent);
  if (ssign.sign) {
    s21_negate(*result, result);
  }
  return 0;
}
