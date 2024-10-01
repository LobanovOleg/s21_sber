#include "s21_matrix.h"

int s21_transpose(matrix_t *A, matrix_t *result) {
  initialize(result);

  int check_flag = ARIFMETIK_ERR;

  if (A->columns == A->rows) {
    check_flag = s21_create_matrix(A->rows, A->columns, result);
  }

  if (check_flag == OK) {
    for (int i = 0; i < A->rows; i++) {
      for (int j = 0; j < A->columns; j++) {
        result->matrix[i][j] = A->matrix[j][i];
      }
    }
  }
  return check_flag;
}