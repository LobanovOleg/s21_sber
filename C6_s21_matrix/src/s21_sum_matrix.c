#include "s21_matrix.h"

int s21_sum_matrix(matrix_t *A, matrix_t *B, matrix_t *result) {
  initialize(result);

  int check_flag = MATRIX_ERR;

  if (same(A, B)) {
    check_flag = s21_create_matrix(A->rows, A->columns, result);
  }

  if (check_flag == OK) {
    for (int i = 0; i < A->rows; i++) {
      for (int j = 0; j < A->columns; j++) {
        result->matrix[i][j] = A->matrix[i][j] + B->matrix[i][j];
      }
    }
  }
  return check_flag == OK ? OK : ARIFMETIK_ERR;
}