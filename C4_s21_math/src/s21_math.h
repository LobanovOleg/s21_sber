#ifndef S21_MATH_H
#define S21_MATH_H


#include <limits.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#define S21_NAN 0.0 / 0.0
#define S21_INFINITY 1.0 / 0.0

long double s21_fmod(double x, double y);

#endif