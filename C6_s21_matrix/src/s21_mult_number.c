#include "s21_matrix.h"

int s21_mult_number(matrix_t *A, double number, matrix_t *result) {
  int check_flag = s21_create_matrix(A->rows, A->columns, result);

  if (check_flag == OK) {
    for (int i = 0; i < A->rows; i++) {
      for (int j = 0; j < A->columns; j++) {
        result->matrix[i][j] = A->matrix[i][j] * number;
      }
    }
  }
  return check_flag == OK ? OK : ARIFMETIK_ERR;
}