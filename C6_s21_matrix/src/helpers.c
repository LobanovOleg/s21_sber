#include "s21_matrix.h"

int same(matrix_t *A, matrix_t *B) {
  return (A->rows == B->rows && A->columns == B->columns) ? 1 : 0;
}

double calc_minor(matrix_t *A, int i, int j) {
  int n = A->rows;
  double minor;
  matrix_t B;

  if (n == 1) {
    minor = A->matrix[0][0];
  } else {
    s21_create_matrix(n - 1, n - 1, &B);

    for (int k = 0; k < n; k++) {
      if (k < i) {
        for (int l = 0; l < j; l++) {
          B.matrix[k][l] = A->matrix[k][l];
        }
        for (int l = j + 1; l < n; l++) {
          B.matrix[k][l - 1] = A->matrix[k][l];
        }
      } else if (k > i) {
        for (int l = 0; l < j; l++) {
          B.matrix[k - 1][l] = A->matrix[k][l];
        }
        for (int l = j + 1; l < n; l++) {
          B.matrix[k - 1][l - 1] = A->matrix[k][l];
        }
      }
    }

    s21_determinant(&B, &minor);

    s21_remove_matrix(&B);
  }

  return minor;
}

int znak(int mult) {
  int check = 1;
  if (mult % 2 == 1) {
    check = -1;
  }
  return check;
}

double _abs(double n) {
  if (n < 0) {
    n *= (-1);
  }
  return n;
}

void initialize(matrix_t *A) {
  A->matrix = NULL;
  A->rows = 0;
  A->columns = 0;
}

int matrix_not_NULL(matrix_t *matrix) {
  int flag = 1;
  if (matrix != NULL && matrix->matrix != NULL && matrix->rows >= 1 &&
      matrix->columns >= 1) {
    flag = 1;
  } else {
    flag = 0;
  }
  return flag;
}