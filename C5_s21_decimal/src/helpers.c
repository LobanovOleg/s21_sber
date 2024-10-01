#include "s21_decimal.h"

void get_exp(info *bits, s21_decimal *src) {
  int j = 0;
  for (int i = 16; i <= 23; i++) {
    set_bit_nums((unsigned *)&bits->exponent, get_bit_nums(src->bits[3], i), j);
    j++;
  }
  bits->sign = ((src->bits[3] >> 31) & 1);
}

void set_sign(s21_decimal *result, int flag) {
  if (flag == 1) {
    set_bit_nums(&result->bits[scale], 1, 31);
  } else {
    set_bit_nums(&result->bits[scale], 0, 31);
  }
}

bool get_sign(s21_decimal decimal) { return ((decimal.bits[3] >> 31) & 1); }

int get_bit(s21_decimal num, int pos) {
  int result = (num.bits[pos / 32] >> (pos % 32)) & 1;
  return result;
}

void set_bit(s21_decimal *val, int bit, int pos) {
  if (bit != 0) {
    val->bits[pos / 32] = val->bits[pos / 32] | (bit << pos);
  } else if (bit == 0) {
    val->bits[pos / 32] = val->bits[pos / 32] & ~((bit + 1) << pos);
  }
}

int get_bit_nums(unsigned int num, int pos) {
  int result = (num >> (pos % 32)) & 1;
  return result;
}

void set_bit_nums(unsigned int *val, int bit, int pos) {
  if (bit != 0 && get_bit_nums(*val, pos) == 0) {
    *val = *val | (bit << pos);
  } else if (bit == 0 && get_bit_nums(*val, pos) == 1) {
    *val = *val & ~((bit + 1) << pos);
  }
}

bool bits_eq(const unsigned bits_a[4], const unsigned bits_b[4]) {
  return bits_a[low] == bits_b[low] && bits_a[mid] == bits_b[mid] &&
         bits_a[top] == bits_b[top] && bits_a[scale] == bits_b[scale];
}

void swap(s21_decimal *val_1, s21_decimal *val_2) {
  s21_decimal x = {0};
  x = *val_1;
  *val_1 = *val_2;
  *val_2 = x;
}

void shift_left(s21_decimal *val) {
  int bit_1 = 0;
  int bit_2 = 0;
  if (get_bit_nums(val->bits[low], 31) == 1) bit_1 = 1;
  if (get_bit_nums(val->bits[mid], 31) == 1) bit_2 = 1;
  val->bits[low] <<= 1;
  val->bits[mid] <<= 1;
  val->bits[top] <<= 1;
  if (bit_1 == 1) set_bit_nums(&val->bits[mid], 1, 0);
  if (bit_2 == 1) set_bit_nums(&val->bits[top], 1, 0);
}

void shift_right(s21_decimal *val) {
  int bit_1 = 0;
  int bit_2 = 0;
  if (get_bit_nums(val->bits[mid], 0) == 1) bit_1 = 1;
  if (get_bit_nums(val->bits[top], 0) == 1) bit_2 = 1;
  val->bits[low] >>= 1;
  val->bits[mid] >>= 1;
  val->bits[top] >>= 1;
  if (bit_1 == 1) set_bit_nums(&val->bits[low], 1, 31);
  if (bit_2 == 1) set_bit_nums(&val->bits[mid], 1, 31);
}

void initialize(s21_decimal *result) {
  result->bits[low] = 0;
  result->bits[mid] = 0;
  result->bits[top] = 0;
  result->bits[scale] = 0;
}

int pre_add(s21_decimal value_1, s21_decimal value_2, s21_decimal *result) {
  initialize(result);
  int flag = 0;
  int i = 0;
  int n = get_bit(value_1, i);
  int m = get_bit(value_2, i);
  int res = n ^ m;

  if (n == 1 && m == 1) flag = 1;
  set_bit(result, res, i);
  i++;

  while (i < 96) {
    n = get_bit(value_1, i);
    m = get_bit(value_2, i);
    res = n ^ m;
    if (res == 1 && flag == 1) {
      res = res ^ flag;
    } else if (flag == 1) {
      res = res ^ flag;
      flag = 0;
    }
    if (n == 1 && m == 1) flag = 1;
    set_bit(result, res, i);
    i++;
  }
  return flag;
}

int pre_sub(s21_decimal value_1, s21_decimal value_2, s21_decimal *result) {
  int res = OK;
  int i = 0;
  while (i < 96) {
    int a = get_bit(value_1, i);
    int b = get_bit(value_2, i);
    if (b && !a) {
      int j;
      for (j = i + 1; !get_bit(value_1, j) && j < 96;) j++;
      set_bit_nums(&value_1.bits[j / 32], low, j);
      j--;
      while (j != i) {
        set_bit_nums(&value_1.bits[j / 32], mid, j);
        j--;
      }
      set_bit_nums(&result->bits[i / 32], mid, i);
    } else {
      set_bit_nums(&result->bits[i / 32], a ^ b, i);
    }
    i++;
  }
  return res;
}

int mul10(s21_decimal *value_1, int exp) {
  s21_decimal ten = {0};
  if (value_1->bits[top] >= 429496730) {
    return TOO_LARGE_OR_INF;
  }
  ten.bits[low] = 10;
  while (exp > 0) {
    s21_mul(ten, *value_1, value_1);
    exp--;
  }
  return OK;
}

void set_info(s21_decimal *result, int sign, int exp) {
  int i = 16;
  int k = 0;
  set_bit_nums(&result->bits[scale], sign, 31);
  while (i < 23) {
    set_bit_nums(&result->bits[scale], get_bit_nums(exp, k), i);
    i++;
    k++;
  }
}

void set_exp(s21_decimal *result, int exp) {
  int i = 16;
  int k = 0;
  while (i < 23) {
    set_bit_nums(&result->bits[scale], get_bit_nums(exp, k), i);
    i++;
    k++;
  }
}

int both_zeroes(s21_decimal value_1, s21_decimal value_2) {
  if (value_1.bits[0] == 0 && value_1.bits[1] == 0 && value_1.bits[2] == 0 &&
      value_2.bits[0] == 0 && value_2.bits[1] == 0 && value_2.bits[2] == 0) {
    return 1;
  } else {
    return 0;
  }
}

int lessnes(s21_decimal value_1, s21_decimal value_2) {
  int i = 95;
  info getinfo_1 = {0};
  info getinfo_2 = {0};
  get_exp(&getinfo_1, &value_1);
  get_exp(&getinfo_2, &value_2);
  int res = 0;
  int n = 0;
  int m = 0;

  if (getinfo_2.sign > getinfo_1.sign) {
    res = 0;
  } else if (getinfo_1.sign > getinfo_2.sign) {
    res = 1;
  } else {
    equal_exp(getinfo_1.exponent, getinfo_2.exponent, &value_1, &value_2);
    while (i > -1) {
      n = get_bit(value_1, i);
      m = get_bit(value_2, i);
      if (n == 0 && m == 1) {
        res = 1;
        break;
      }
      if (n == 1 && m == 0) {
        res = 0;
        break;
      }
      i--;
    }
  }
  return res;
}

int s21_get_sign(s21_decimal value) {
  return (value.bits[3] & 0x80000000) >> 31;
}

int s21_get_exp(s21_decimal value) {
  return (value.bits[3] & 0x00FF0000) >> 16;
}

int s21_set_sign(s21_decimal *value) {
  value->bits[3] = value->bits[3] | ((unsigned long)1 << (31));
  return 0;
}

int s21_clear_decimal(s21_decimal *value) {
  value->bits[0] = 0;
  value->bits[1] = 0;
  value->bits[2] = 0;
  value->bits[3] = 0;
  return 0;
}

int checkPow(s21_decimal check) {
  int num = 0;
  if (get_sign(check) == 1) {
    check.bits[3] = check.bits[3] >> 2;
    check.bits[3] = check.bits[3] - pow(2, 29);
    check.bits[3] = check.bits[3] << 2;
    num = check.bits[3] >> 16;
    if (num < 0) {
      num = abs(num);
    }
  } else {
    num = check.bits[3] >> 16;
  }
  return num;
}

void Min(s21_decimal *check) {
  if (checkBit(check, 31) == 0) {
    check->bits[3] = check->bits[3] >> 2;
    check->bits[3] = check->bits[3] + pow(2, 29);
    check->bits[3] = check->bits[3] << 2;
  }
}

int checkBit(s21_decimal *check, int num) {
  return !!(check->bits[num / 32] & (1u << (num % 32)));
}

void Plus(s21_decimal *check) {
  if (checkBit(check, 31) != 1) {
    check->bits[3] = check->bits[3] >> 2;
    check->bits[3] = check->bits[3] - pow(2, 29);
    check->bits[3] = check->bits[3] << 2;
  }
}

int not_zero(s21_decimal check) {
  int result = 0;
  if (check.bits[0] == 0 && check.bits[1] == 0 && check.bits[2] == 0) {
    result = 1;
  }
  return result;
}

void s21_bank_round(s21_decimal value, s21_decimal *result) {
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
  unsigned int tmp = mod_res.bits[0], k = 0;
  set_exp(&ostatok, ssign.exponent);
  while (tmp != 0) {
    k += 1;
    tmp /= 10;
  }
  s21_decimal for_mul = {{pow(10, k - 1), 0, 0, 0}};
  s21_mul(for_mul, ostatok, &ostatok);
  if (s21_is_less(ostatok, mod_res)) {
    s21_add(*result, one, result);
  }
  info res = {0};
  get_exp(&res, result);
  res.exponent = 0;
  set_exp(result, res.exponent);
  if (ssign.sign) {
    s21_negate(*result, result);
  }
}

int equal_exp(unsigned exp1, unsigned exp2, s21_decimal *value_1,
              s21_decimal *value_2) {
  int max = 0;
  int exp_diff = 0;
  s21_decimal buff = {0};

  if (exp1 == exp2) {
    return max = exp1;
  }

  if ((exp1 || exp2) && exp1 > exp2) {
    max = exp1;
    exp_diff = exp1 - exp2;
    while (exp_diff > 0) {
      buff = *value_2;
      if (mul10(value_2, 1) == 1) {
        *value_2 = buff;
        break;
      }
      exp_diff--;
    }
    if (exp_diff > 0) {
      set_exp(value_1, exp_diff);
      buff = *value_1;
      s21_bank_round(buff, value_1);
      max = max - exp_diff;
    }
  } else if ((exp2 || exp1) && exp2 > exp1) {
    max = exp2;
    exp_diff = exp2 - exp1;
    while (exp_diff > 0) {
      buff = *value_1;
      if (mul10(value_1, 1) == 1) {
        *value_1 = buff;
        break;
      }
      exp_diff--;
    }
    if (exp_diff > 0) {
      set_exp(value_2, exp_diff);
      buff = *value_2;
      s21_bank_round(buff, value_2);
      max = max - exp_diff;
    }
  }
  return max;
}

int s21_mod(s21_decimal value_1, s21_decimal value_2, s21_decimal *result) {
  if (value_2.bits[low] == 0 && value_2.bits[mid] == 0 &&
      value_2.bits[top] == 0)
    return DIV_BY_ZERO;
  initialize(result);
  s21_div(value_1, value_2, result);
  s21_mul(*result, value_2, result);
  s21_sub(value_1, *result, result);
  return OK;
}