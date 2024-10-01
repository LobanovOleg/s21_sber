#ifndef S21_MATRIX_OOP_H
#define S21_MATRIX_OOP_H
#include <iostream>
#include <math.h>
#include <stdexcept>
#include <utility>

class S21Matrix {
    public:
        S21Matrix() noexcept;
        S21Matrix(int rows, int cols);
        S21Matrix(const S21Matrix& other);
        S21Matrix(S21Matrix&& other) noexcept;
        ~S21Matrix() noexcept;

        S21Matrix operator= (const S21Matrix &other);
        S21Matrix operator=(S21Matrix &&other) noexcept;
        S21Matrix operator+ (const S21Matrix other);
        S21Matrix operator- (const S21Matrix other);
        S21Matrix operator* (const S21Matrix other);
        S21Matrix operator* (double number);
        bool operator== (const S21Matrix other);
        S21Matrix operator+= (const S21Matrix other);
        S21Matrix operator-= (const S21Matrix other);
        S21Matrix operator*= (const S21Matrix other);
        S21Matrix operator*= (double number);
        double& operator() (int i, int j);
        double operator()(int i, int j) const;

        void SubMatrix(const S21Matrix& other);
        void SumMatrix(const S21Matrix& other);
        void MulMatrix(const S21Matrix& other);
        void MulNumber(const double number) noexcept;
        bool EqMatrix(const S21Matrix& other) const;
        S21Matrix Transpose();
        S21Matrix CalcComplements();
        double Determinant();
        S21Matrix InverseMatrix();
        S21Matrix find_minor(const int rows, const int cols);

        void SetRows(int row);
        void SetCols(int col);
        int GetRows() const noexcept;
        int GetCols() const noexcept;

    private:
        int rows_, cols_;
        double **matrix_;
        void create(int rows, int cols);
        const double eps = 1e-7;

};
#endif