#include <../../../../../../../../opt/homebrew/opt/googletest/include/gtest/gtest.h>
#include "s21_matrix_oop.h"

TEST(create_1, test_1) {
    S21Matrix matrix;
    SUCCEED();
}

TEST(create_2, test_2) {
    S21Matrix matrix(3, 3);
    SUCCEED();
    
}

TEST(create_3, test_3) {
    S21Matrix matrix(3, 3);
    matrix(1, 1) = 10;
    ASSERT_EQ(matrix(1, 1), 10);
}

TEST(equal_1, test_4) {
    S21Matrix matrix1(3, 3);
    matrix1(0, 0) = 1;
    matrix1(1, 0) = 2;
    matrix1(2, 0) = 3;
    matrix1(1, 2) = 10;
    matrix1(2, 1) = 5;
    matrix1(0, 1) = 2;
    matrix1(0, 2) = 3;
    matrix1(1, 1) = 4;
    matrix1(2, 2) = 8;

    S21Matrix matrix2(3, 3);
    matrix2(0, 0) = 1;
    matrix2(1, 0) = 2;
    matrix2(2, 0) = 3;
    matrix2(1, 2) = 10;
    matrix2(2, 1) = 5;
    matrix2(0, 1) = 2;
    matrix2(0, 2) = 3;
    matrix2(1, 1) = 4;
    matrix2(2, 2) = 8;

    ASSERT_EQ(matrix1.EqMatrix(matrix2), 1);
}

TEST(equal_2, test_5) {
    S21Matrix matrix1(3, 3);
    S21Matrix matrix2(3, 3);
    matrix2(0, 0) = 1;
    matrix2(1, 0) = 2;
    matrix2(2, 0) = 3;
    matrix2(0, 1) = 2;
    matrix2(0, 2) = 3;
    matrix2(1, 1) = 4;
    matrix2(2, 2) = 8;

    ASSERT_EQ(matrix1.EqMatrix(matrix2), 0);
}

TEST(equal_3, test_6) {
    S21Matrix matrix1(2, 2);
    S21Matrix matrix2(3, 3);

    ASSERT_EQ(matrix1.EqMatrix(matrix2), 0);
}

TEST(sum_1, test_7) {
    S21Matrix A(2, 2);
    S21Matrix B(2, 2);
    S21Matrix C(2, 2);

    A(0, 0) = 2;
    A(1, 0) = 3;
    A(0, 1) = 3;
    A(1, 1) = 2;

    B(0, 0) = 5;
    B(1, 0) = 6;
    B(0, 1) = 0;
    B(1, 1) = 10;

    C(0, 0) = 7;
    C(1, 0) = 9;
    C(0, 1) = 3;
    C(1, 1) = 12;

    A.SumMatrix(B);
    bool result = A.EqMatrix(C);

    ASSERT_EQ(result, 1);
}

 TEST(sum_2, test_8) {
    S21Matrix A(1, 1);
    S21Matrix B(1, 1);
    S21Matrix C(1, 1);

    A(0, 0) = 0;
    B(0, 0) = 0;
    C(0, 0) = 0;

    A.SumMatrix(B);
    bool result = A.EqMatrix(C);

    ASSERT_EQ(result, 1);
 }

 TEST(sub_1, test_9) {
    S21Matrix A(1, 1);
    S21Matrix B(1, 1);
    S21Matrix C(1, 1);

    A(0, 0) = 0;
    B(0, 0) = 0;
    C(0, 0) = 0;

    A.SubMatrix(B);
    bool result = A.EqMatrix(C);

    ASSERT_EQ(result, 1);
 }

 TEST(sub_2, test_10) {
    S21Matrix A(2, 2);
    S21Matrix B(2, 2);
    S21Matrix C(2, 2);

    A(0, 0) = 2;
    A(1, 0) = 3;
    A(0, 1) = 3;
    A(1, 1) = 2;

    B(0, 0) = 5;
    B(1, 0) = 6;
    B(0, 1) = 0;
    B(1, 1) = 10;

    C(0, 0) = -3;
    C(1, 0) = -3;
    C(0, 1) = 3;
    C(1, 1) = -8;

    A.SubMatrix(B);
    bool result = A.EqMatrix(C);
    ASSERT_EQ(result, 1);
 }

 TEST(mult_matrix_1, test_11) {
    S21Matrix A(2, 2);
    S21Matrix B(2, 2);
    S21Matrix C(2, 2);

    A(0, 0) = 2;
    A(1, 0) = 3;
    A(0, 1) = 3;
    A(1, 1) = 2;

    B(0, 0) = 5;
    B(1, 0) = 6;
    B(0, 1) = 6;
    B(1, 1) = 5;

    C(0, 0) = 28;
    C(1, 0) = 27;
    C(0, 1) = 27;
    C(1, 1) = 28;

    A.MulMatrix(B);
    bool result = A.EqMatrix(C);
    ASSERT_EQ(result, 1);
 }

 TEST(mult_matrix_2, test_12) {
    S21Matrix A(2, 1);
    S21Matrix B(1, 2);
    S21Matrix C(2, 2);

    A(0, 0) = 10;
    A(1, 0) = 10;
    
    B(0, 0) = 2;
    B(0, 1) = 4;

    C(0, 0) = 20;
    C(0, 1) = 40;
    C(1, 0) = 20;
    C(1, 1) = 40;

    A.MulMatrix(B);
    bool result = A.EqMatrix(C);
    ASSERT_EQ(result, 1);
 }

TEST(mult_number_1, test_13) {
    S21Matrix A(2, 2);
    S21Matrix B(2, 2);
    double n = 2.5;

    A(0, 0) = 10;
    A(1, 0) = 5;
    A(0, 1) = 0;
    A(1, 1) = 9;

    B(0, 0) = 25;
    B(1, 0) = 12.5;
    B(0, 1) = 0;
    B(1, 1) = 22.5;

    A.MulNumber(n);
    bool result = A.EqMatrix(B);
    ASSERT_EQ(result, 1);
}

TEST(transpose_1, test_14) {
    S21Matrix A(5, 4);
    S21Matrix B(4, 5);

    A(0, 0) = 2;
    A(0, 1) = 5;
    A(0, 2) = 7;
    A(0, 3) = -4;
    A(1, 0) = 6;
    A(1, 1) = 3;
    A(1, 2) = 4;
    A(1, 3) = 14;
    A(2, 0) = 5;
    A(2, 1) = -2;
    A(2, 2) = -3;
    A(2, 3) = -1;
    A(3, 0) = 10;
    A(3, 1) = 3;
    A(3, 2) = 9;
    A(3, 3) = -3;
    A(4, 0) = -3;
    A(4, 1) = 3;
    A(4, 2) = 1;
    A(4, 3) = 5;

    B(0, 0) = 2;
    B(0, 1) = 6;
    B(0, 2) = 5;
    B(0, 3) = 10;
    B(0, 4) = -3;
    B(1, 0) = 5;
    B(1, 1) = 3;
    B(1, 2) = -2;
    B(1, 3) = 3;
    B(1, 4) = 3;
    B(2, 0) = 7;
    B(2, 1) = 4;
    B(2, 2) = -3;
    B(2, 3) = 9;
    B(2, 4) = 1;
    B(3, 0) = -4;
    B(3, 1) = 14;
    B(3, 2) = -1;
    B(3, 3) = -3;
    B(3, 4) = 5;

    S21Matrix C = A.Transpose();
    bool result = C.EqMatrix(B);

    ASSERT_EQ(result, 1);
}

TEST(minor_matrix_1, test_15) {
    S21Matrix A(3, 3);
    S21Matrix B(2, 2);

    A(0, 0) = 1;
    A(0, 1) = 2;
    A(0, 2) = 3;
    A(1, 0) = 4;
    A(1, 1) = 5;
    A(1, 2) = 6;
    A(2, 0) = 7;
    A(2, 1) = 8;
    A(2, 2) = 9;

    B(0, 0) = 5;
    B(0, 1) = 6;
    B(1, 0) = 8;
    B(1, 1) = 9;

    S21Matrix C = A.find_minor(0, 0);
    bool result = C.EqMatrix(B);
    ASSERT_EQ(result, 1);

}

TEST(minor_matrix_2, test_16) {
    S21Matrix A(3, 3);
    S21Matrix B(2, 2);

    A(0, 0) = 1;
    A(0, 1) = 2;
    A(0, 2) = 3;
    A(1, 0) = 4;
    A(1, 1) = 5;
    A(1, 2) = 6;
    A(2, 0) = 7;
    A(2, 1) = 8;
    A(2, 2) = 9;

    B(0, 0) = 1;
    B(0, 1) = 3;
    B(1, 0) = 7;
    B(1, 1) = 9;

    S21Matrix C = A.find_minor(1, 1);
    bool result = C.EqMatrix(B);
    ASSERT_EQ(result, 1);
}

TEST(determinant_1, test_17) {
    S21Matrix A(2, 2);
    double n = 0;

    A(0, 0) = 1;
    A(0, 1) = 2;
    A(1, 0) = 3;
    A(1, 1) = 6;

    ASSERT_EQ(A.Determinant(), n);
}

TEST(determinant_2, test_18) {
    S21Matrix A(3, 3);
    A(0 ,0) = 0;
    A(0, 1) = 4;
    A(0, 2) = 3;
    A(1, 0) = 12;
    A(1, 1) = 2;
    A(1, 2) = -2;
    A(2, 0) = 10;
    A(2, 1) = 8;
    A(2, 2) = 7;

    double n = -188;
    double det = A.Determinant();

    ASSERT_EQ(det, n);
}

TEST(calc_complements_1, test_19) {
    S21Matrix A(2, 2);
    S21Matrix B(2, 2);

    A(0, 0) = 1;
    A(0, 1) = 2;
    A(1, 0) = 3;
    A(1, 1) = 4;

    B(0, 0) = 4;
    B(0, 1) = -3;
    B(1, 0) = -2;
    B(1, 1) = 1;

    S21Matrix C = A.CalcComplements();
    bool result = C.EqMatrix(B);
    ASSERT_EQ(result, 1);

}

TEST(calc_complements_2, test_20) {
    S21Matrix A(3, 3);
    S21Matrix B(3, 3);

    A(0, 0) = 1;
    A(0, 1) = 2;
    A(0, 2) = 3;
    A(1, 0) = 4;
    A(1, 1) = 5;
    A(1, 2) = 6;
    A(2, 0) = 7;
    A(2, 1) = 8;
    A(2, 2) = 9;

    B(0, 0) = -3;
    B(0, 1) = 6;
    B(0, 2) = -3;
    B(1, 0) = 6;
    B(1, 1) = -12;
    B(1, 2) = 6;
    B(2, 0) = -3;
    B(2, 1) = 6;
    B(2, 2) = -3;

    S21Matrix C = A.CalcComplements();
    bool result = C.EqMatrix(B);
    ASSERT_EQ(result, 1);
}

TEST(inverse_matrix_1, test_21) {
    S21Matrix A(3, 3);
    S21Matrix B(3, 3);

    A(0, 0) = 2;
    A(0, 1) = 3;
    A(0, 2) = 4;
    A(1, 0) = 3;
    A(1, 1) = 3;
    A(1, 2) = 4;
    A(2, 0) = 4;
    A(2, 1) = 4;
    A(2, 2) = 4;

    B(0, 0) = -1;
    B(0, 1) = 1;
    B(0, 2) = 0;
    B(1, 0) = 1;
    B(1, 1) = -2;
    B(1, 2) = 1;
    B(2, 0) = 0;
    B(2, 1) = 1;
    B(2, 2) = -0.75;

    S21Matrix C = A.InverseMatrix();
    bool result = C.EqMatrix(B);
    ASSERT_EQ(result, 1);

}

TEST(inverse_matrix_2, test_22) {
    S21Matrix A(1, 1);
    S21Matrix B(1, 1);

    A(0, 0) = 10;

    B(0, 0) = 1/10;

    S21Matrix C = A.InverseMatrix();
    bool result = C.EqMatrix(B);
    ASSERT_EQ(result, 1);
}

TEST(set_row_1, test_23) {
    S21Matrix A(2, 2);
    S21Matrix B(3, 2);

    A(0, 0) = 1;
    A(0, 1) = 1;
    A(1, 0) = 1;
    A(1, 1) = 1;

    B(0, 0) = 1;
    B(0, 1) = 1;
    B(1, 0) = 1;
    B(1, 1) = 1;
    B(2, 0) = 0;
    B(2, 1) = 0;

    A.SetRows(3);
    bool result = A.EqMatrix(B);
    ASSERT_EQ(result, 1);
}

TEST(set_row_2, test_24) {
    S21Matrix A(2, 2);
    S21Matrix B(1, 2);

    A(0, 0) = 1;
    A(0, 1) = 1;
    A(1, 0) = 1;
    A(1, 1) = 1;

    B(0, 0) = 1;
    B(0, 1) = 1;

    A.SetRows(1);
    bool result = A.EqMatrix(B);
    ASSERT_EQ(result, 1);   
}

TEST(set_col_1, test_25) {
    S21Matrix A(2, 2);
    S21Matrix B(2, 3);

    A(0, 0) = 1;
    A(0, 1) = 1;
    A(1, 0) = 1;
    A(1, 1) = 1;

    B(0, 0) = 1;
    B(0, 1) = 1;
    B(0, 2) = 0;
    B(1, 0) = 1;
    B(1, 1) = 1;
    B(1, 2) = 0;

    A.SetCols(3);
    bool result = A.EqMatrix(B);
    ASSERT_EQ(result, 1);
}

TEST(set_col_2, test_26) {
    S21Matrix A(2, 2);
    S21Matrix B(2, 1);

    A(0, 0) = 1;
    A(0, 1) = 1;
    A(1, 0) = 1;
    A(1, 1) = 1;

    B(0, 0) = 1;
    B(1, 0) = 1;

    A.SetCols(1);
    bool result = A.EqMatrix(B);
    ASSERT_EQ(result, 1);
}

int main(int argc, char *argv[]) {
    ::testing::InitGoogleTest(&argc, argv);
    return RUN_ALL_TESTS();
}