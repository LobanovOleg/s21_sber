#ifndef SMART_CALC_H
#define SMART_CALC_H

#include <iso646.h>
#include <limits.h>
#include <math.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_LEN 255

#include "mechanic/calculate.h"
#include "mechanic/deposit_calc.h"
#include "mechanic/input_validation.h"
#include "mechanic/loan_calc.h"
#include "mechanic/shunting_yard.h"
#include "mechanic/stack.h"
#include "mechanic/tokens_devider.h"

int api_calculate_str(const char *str, long double *res);
int api_infix_to_postfix_notation(const char *str, char *res_str);
int api_calculate_str_with_x(const char *str, long double x, long double *res);

#endif