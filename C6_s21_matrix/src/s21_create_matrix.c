#include "s21_matrix.h"

int s21_create_matrix(int rows, int columns, matrix_t *result) {
  if (rows < 1 || columns < 1) {
    result->matrix = NULL;
    s21_remove_matrix(result);
    return MATRIX_ERR;
  }

  int not_allocate = 0;

  result->rows = rows;
  result->columns = columns;
  result->matrix = (double **)calloc(result->rows, sizeof(double));

  if (result->matrix) {
    for (int i = 0; i < result->rows; i++) {
      result->matrix[i] = (double *)calloc(result->columns, sizeof(double));
      if (!result->matrix[i]) {
        not_allocate = 1;
      }
    }
  } else {
    not_allocate = 1;
  }

  int check = OK;

  if (not_allocate) {
    s21_remove_matrix(result);
    check = MATRIX_ERR;
  }

  return check;
}