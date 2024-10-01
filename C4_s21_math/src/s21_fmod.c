#include "s21_math.h"

long double s21_fmod(double x, double y) {
    long double result = 0;
    long long int check = x / y;
    if (y == 0.0 || x == S21_INFINITY || x == - S21_INFINITY) {
        result = S21_NAN;
    } else if (y == S21_INFINITY || y == - S21_INFINITY) {
        result = x;
    } else {
        result = x - (check * y);
    }
    return result;
}