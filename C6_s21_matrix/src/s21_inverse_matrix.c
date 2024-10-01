#include "s21_matrix.h"

int s21_inverse_matrix(matrix_t *A, matrix_t *result) {
  initialize(result);

  double D = 0;
  int check_flag = s21_determinant(A, &D);

  if (D == 0) {
    check_flag = ARIFMETIK_ERR;
  }

  if (check_flag == OK) {
    matrix_t tmp;
    s21_calc_complements(A, &tmp);

    matrix_t transposed;
    s21_transpose(&tmp, &transposed);

    double div = 1 / D;
    s21_mult_number(&transposed, div, result);

    s21_remove_matrix(&tmp);
    s21_remove_matrix(&transposed);
  }
  return check_flag;
}