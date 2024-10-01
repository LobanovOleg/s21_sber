#include "s21_matrix.h"

#define SUCCESS 1
#define FAILURE 0
#define eps 1e-7

int s21_eq_matrix(matrix_t *A, matrix_t *B) {
  int check = SUCCESS;

  if ((A->rows != B->rows) || (A->columns != B->columns)) {
    check = FAILURE;
  }

  if (check == SUCCESS) {
    for (int i = 0; i < A->rows && check; i++) {
      for (int j = 0; j < A->columns && check; j++) {
        if (_abs(A->matrix[i][j] - B->matrix[i][j]) >= eps) {
          check = FAILURE;
        }
      }
    }
  }
  return check;
}
