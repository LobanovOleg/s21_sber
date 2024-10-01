#include "s21_matrix.h"

int s21_mult_matrix(matrix_t *A, matrix_t *B, matrix_t *result) {
  initialize(result);

  int check_flag = ARIFMETIK_ERR;

  if (A->columns == B->rows) {
    check_flag = s21_create_matrix(A->rows, B->columns, result);
  }

  if (check_flag == OK) {
    for (int i = 0; i < A->rows; i++) {
      for (int j = 0; j < B->columns; j++) {
        result->matrix[i][j] = 0;
        for (int k = 0; k < A->columns; k++) {
          result->matrix[i][j] += A->matrix[i][k] * B->matrix[k][j];
        }
      }
    }
  }
  return check_flag;
}