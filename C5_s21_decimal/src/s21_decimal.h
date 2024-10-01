#ifndef S21_DECIMAL_H
#define S21_DECIMAL_H

#include <math.h>
#include <stdint.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <limits.h>

#define s21_MAXDEC 2e96 - 1
#define CONVERT_ERROR 1
#define COMPAR_TRUE 1
#define COMPAR_FALSE 0
#define TOO_LARGE_OR_INF 1
#define TOO_SMALL_OR_NEG_INF 2
#define DIV_BY_ZERO 3
#define OK 0
#define s21_NAN (__builtin_nanf(""))
#define s21_INF (__builtin_inff())
#define is_nan(x) __builtin_isnan(x)
#define is_inf(x) __builtin_isinf(x)

typedef struct {
    unsigned int bits[4];
} s21_decimal;

typedef struct {
    int exponent;
    int sign;
} info;

typedef struct {
    int exponent;
    int sign;
    int mantissa;
} float_info;

enum {low, mid, top, scale};

//math
int s21_add(s21_decimal value_1, s21_decimal value_2, s21_decimal *result);
int s21_div(s21_decimal value_1, s21_decimal value_2, s21_decimal *result);
int s21_mul(s21_decimal value_1, s21_decimal value_2, s21_decimal *result);
int s21_sub(s21_decimal value_1, s21_decimal value_2, s21_decimal *result);

//compare
int s21_is_equal(s21_decimal num1, s21_decimal num2);
int s21_is_not_equal(s21_decimal num1, s21_decimal num2);
int s21_is_less(s21_decimal num1, s21_decimal num2);
int s21_is_less_or_equal(s21_decimal num1, s21_decimal num2);
int s21_is_greater(s21_decimal num1, s21_decimal num2);
int s21_is_greater_or_equal(s21_decimal num1, s21_decimal num2);

//convert
int s21_from_decimal_to_float(s21_decimal src, float *dst);
int s21_from_decimal_to_int(s21_decimal src, int *dst);
int s21_from_float_to_decimal(float src, s21_decimal *dst);
int s21_from_int_to_decimal(int src, s21_decimal *dst);

//others
int s21_floor(s21_decimal value, s21_decimal *result);
int s21_round(s21_decimal value, s21_decimal *result);
int s21_truncate(s21_decimal value, s21_decimal *result);
int s21_negate(s21_decimal value, s21_decimal *result);

//helpers

int checkPow(s21_decimal check);
void Min(s21_decimal *check);
int checkBit(s21_decimal *check, int num);
void Plus(s21_decimal *check);
int not_zero(s21_decimal check);
int s21_clear_decimal(s21_decimal *value);
int s21_get_sign(s21_decimal value);
int s21_get_exp(s21_decimal value);
int s21_set_sign(s21_decimal *value);
int lessnes(s21_decimal value_1, s21_decimal value_2);
int both_zeroes(s21_decimal value_1, s21_decimal value_2);
void set_exp(s21_decimal *result, int exp);
void set_info(s21_decimal *result, int sign, int exp);
int mul10(s21_decimal* value_1, int exp);
int pre_sub(s21_decimal value_1, s21_decimal value_2, s21_decimal *result);
int pre_add(s21_decimal value_1, s21_decimal value_2, s21_decimal *result);
void initialize(s21_decimal *result);
void shift_right(s21_decimal *val);
void shift_left(s21_decimal *val);
void swap(s21_decimal* val_1, s21_decimal* val_2);
bool bits_eq(const unsigned bits_a[4], const unsigned bits_b[4]);
void set_bit_nums(unsigned int *val, int bit, int pos);
int get_bit_nums(unsigned int num, int pos);
void set_bit(s21_decimal *val, int bit, int pos);
int get_bit(s21_decimal num, int pos);
bool get_sign(s21_decimal decimal);
void set_sign(s21_decimal *result, int flag);
void get_exp(info *bits, s21_decimal *src);
void s21_bank_round(s21_decimal value, s21_decimal *result);
int equal_exp(unsigned exp1, unsigned exp2, s21_decimal *value_1, s21_decimal *value_2);
int s21_mod(s21_decimal value_1, s21_decimal value_2, s21_decimal *result);

#endif