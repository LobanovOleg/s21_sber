#include "s21_matrix.h"

int s21_calc_complements(matrix_t *A, matrix_t *result) {
  initialize(result);

  int check_flag = ARIFMETIK_ERR;

  if (A->columns == A->rows) {
    check_flag = s21_create_matrix(A->rows, A->columns, result);
  }

  if (check_flag == OK) {
    for (int i = 0; i < A->rows; i++) {
      for (int j = 0; j < A->columns; j++) {
        double minor = calc_minor(A, i, j);
        result->matrix[i][j] = znak(i + j) * minor;
      }
    }
  }
  return check_flag == OK ? OK : ARIFMETIK_ERR;
}