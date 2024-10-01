#ifndef S21_MATRIX_H
#define S21_MATRIX_H

#include <stdlib.h>
#include <stdio.h>

#define OK 0
#define MATRIX_ERR 1
#define ARIFMETIK_ERR 2

typedef struct matrix_struct {
    double** matrix;
    int rows;
    int columns;
} matrix_t;

////////////main////////////
int s21_create_matrix(int rows, int columns, matrix_t *result);
void s21_remove_matrix(matrix_t *A);
int s21_eq_matrix(matrix_t *A, matrix_t *B);
int s21_sum_matrix(matrix_t *A, matrix_t *B, matrix_t *result);
int s21_sub_matrix(matrix_t *A, matrix_t *B, matrix_t *result);
int s21_mult_number(matrix_t *A, double number, matrix_t *result);
int s21_mult_matrix(matrix_t *A, matrix_t *B, matrix_t *result);
int s21_transpose(matrix_t *A, matrix_t *result);
int s21_calc_complements(matrix_t *A, matrix_t *result);
int s21_determinant(matrix_t *A, double *result);
int s21_inverse_matrix(matrix_t *A, matrix_t *result);

///////////helpers/////////////
int same(matrix_t *A, matrix_t *B);
double calc_minor(matrix_t *A, int i, int j);
int znak(int mult);
double _abs(double n);
void initialize(matrix_t *A);
int matrix_not_NULL(matrix_t *matrix);


#endif
