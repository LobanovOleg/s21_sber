#include "s21_matrix.h"

int s21_sub_matrix(matrix_t *A, matrix_t *B, matrix_t *result) {
  initialize(result);

  matrix_t C;
  int sum_check = ARIFMETIK_ERR;
  int mult_check = s21_mult_number(B, -1.0, &C);

  if (mult_check == OK) {
    sum_check = s21_sum_matrix(A, &C, result);
  }
  s21_remove_matrix(&C);
  return sum_check;
}