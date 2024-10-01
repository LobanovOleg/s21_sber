#include "s21_matrix_oop.h"
using namespace std;

S21Matrix::S21Matrix() noexcept : rows_(0), cols_(0), matrix_(NULL) {}

S21Matrix::~S21Matrix() noexcept {
  for (int i = 0; i < rows_; i++) {
    delete[] matrix_[i];
  }
  delete[] matrix_;
  matrix_ = NULL;
}

S21Matrix::S21Matrix(int rows, int cols) : rows_(rows), cols_(cols) {
  if (rows_ < 0 || cols_ < 0) {
    throw length_error("Ряд или столбец не может быть меньше 0.");
  }
  matrix_ = new double *[rows_];
  for (int i = 0; i < rows_; i++) {
    matrix_[i] = new double[cols_];
  }
}

S21Matrix::S21Matrix(const S21Matrix &other)
    : rows_(other.rows_), cols_(other.cols_) {
  matrix_ = new double *[rows_];
  for (int i = 0; i < rows_; i++) {
    matrix_[i] = new double[cols_];
  }

  for (int a = 0; a < rows_; a++) {
    for (int b = 0; b < cols_; b++) {
      matrix_[a][b] = other.matrix_[a][b];
    }
  }
}

S21Matrix::S21Matrix(S21Matrix &&other) noexcept
    : rows_(other.rows_), cols_(other.cols_), matrix_(other.matrix_) {
  other.matrix_ = NULL;
  other.cols_ = 0;
  other.rows_ = 0;
}

S21Matrix S21Matrix::operator=(const S21Matrix &other) {
  S21Matrix copy(other);
  *this = std::move(copy);
  return *this;
}

S21Matrix S21Matrix::operator=(S21Matrix &&other) noexcept {
  if (this != &other) {
    swap(rows_, other.rows_);
    swap(cols_, other.cols_);
    swap(matrix_, other.matrix_);
  }
  return *this;
}

S21Matrix S21Matrix::operator+(const S21Matrix other) {
  S21Matrix check(*this);
  check.SumMatrix(other);
  return check;
}

S21Matrix S21Matrix::operator-(const S21Matrix other) {
  S21Matrix check(*this);
  check.SubMatrix(other);
  return check;
}

S21Matrix S21Matrix::operator*(const S21Matrix other) {
  S21Matrix check(*this);
  check.MulMatrix(other);
  return check;
}

S21Matrix S21Matrix::operator*(double number) {
  S21Matrix check(*this);
  check.MulNumber(number);
  return check;
}

bool S21Matrix::operator==(const S21Matrix other) {
  return this->EqMatrix(other);
}

S21Matrix S21Matrix::operator+=(const S21Matrix other) {
  SumMatrix(other);
  return *this;
}

S21Matrix S21Matrix::operator-=(const S21Matrix other) {
  SubMatrix(other);
  return *this;
}

S21Matrix S21Matrix::operator*=(const S21Matrix other) {
  this->MulMatrix(other);
  return *this;
}

S21Matrix S21Matrix::operator*=(double number) {
  this->MulNumber(number);
  return *this;
}

double &S21Matrix::operator()(int i, int j) {
  if (i < 0 || j < 0 || i > rows_ || j > cols_) {
    throw length_error("Неверный ввод данных");
  }
  return matrix_[i][j];
}

double S21Matrix::operator()(int i, int j) const {
  if (i < 0 || j < 0 || i > rows_ || j > cols_) {
    throw length_error("Неверный ввод данных");
  }
  return matrix_[i][j];
}

void S21Matrix::SubMatrix(const S21Matrix &other) {
  if (rows_ != other.rows_ || cols_ != other.cols_) {
    throw logic_error("Невырные размеры мариц");
  }

  for (int i = 0; i < rows_; i++) {
    for (int j = 0; j < cols_; j++) {
      matrix_[i][j] -= other.matrix_[i][j];
    }
  }
}

void S21Matrix::SumMatrix(const S21Matrix &other) {
  if (rows_ != other.rows_ || cols_ != other.cols_) {
    throw logic_error("Неверные размеры матриц");
  }

  for (int i = 0; i < rows_; i++) {
    for (int j = 0; j < cols_; j++) {
      matrix_[i][j] += other.matrix_[i][j];
    }
  }
}

void S21Matrix::MulMatrix(const S21Matrix &other) {
  if (cols_ != other.GetRows()) {
    throw logic_error("Невозможно перемножение матриц");
  }

  S21Matrix result(rows_, other.GetCols());

  for (int i = 0; i < result.GetRows(); i++) {
    for (int j = 0; j < result.GetCols(); j++) {
      for (int k = 0; k < cols_; k++) {
        result(i, j) += (*this)(i, k) * other(k, j);
      }
    }
  }
  *this = std::move(result);
}

void S21Matrix::MulNumber(const double number) noexcept {
  for (int i = 0; i < rows_; i++) {
    for (int j = 0; j < cols_; j++) {
      matrix_[i][j] *= number;
    }
  }
}

bool S21Matrix::EqMatrix(const S21Matrix &other) const {
  if (!(rows_ == other.rows_ && cols_ == other.cols_)) {
    return false;
  }
  for (int i = 0; i < rows_; i++) {
    for (int j = 0; j < cols_; j++) {
      if (abs(other(i, j) - (*this)(i, j)) > eps) {
        return false;
      }
    }
  }
  return true;
}

void S21Matrix::create(int rows, int cols) {
  rows_ = rows;
  cols_ = cols;
  matrix_ = new double *[rows_];
  for (int i = 0; i < rows_; i++) {
    matrix_[i] = new double[cols_];
  }
}

S21Matrix S21Matrix::Transpose() {
  S21Matrix check(cols_, rows_);
  for (int i = 0; i < check.rows_; i++) {
    for (int j = 0; j < check.cols_; j++) {
      check.matrix_[i][j] = matrix_[j][i];
    }
  }
  return check;
}

S21Matrix S21Matrix::CalcComplements() {
  S21Matrix check(rows_, cols_);

  if (rows_ == cols_) {
    for (int i = 0; i < rows_; i++) {
      for (int j = 0; j < cols_; j++) {
        S21Matrix minor = this->find_minor(i, j);
        check.matrix_[i][j] = minor.Determinant() * pow(-1, i + j);
      }
    }
  } else {
    throw length_error("Матрица должна быть квадратной");
  }
  return check;
}

double S21Matrix::Determinant() {
  double result = 0.0;
  if (rows_ == cols_) {
    if (rows_ == 1) {
      result = matrix_[0][0];
    } else if (rows_ == 2) {
      result = matrix_[0][0] * matrix_[1][1] - matrix_[1][0] * matrix_[0][1];
    } else {
      for (int i = 0; i < cols_; i++) {
        S21Matrix minor = find_minor(0, i);
        result += matrix_[0][i] * minor.Determinant() * pow(-1, i);
      }
    }
  } else {
    throw length_error("Матрица должна быть квадратной");
  }
  return result;
}

S21Matrix S21Matrix::find_minor(const int rows, const int cols) {
  S21Matrix check(rows_ - 1, cols_ - 1);

  int skipI = 0;
  for (int i = 0; i < check.GetRows(); i++) {
    if (i == rows)
      skipI = 1;
    int skipJ = 0;
    for (int j = 0; j < check.GetCols(); j++) {
      if (j == cols)
        skipJ = 1;
      check(i, j) = (*this)(i + skipI, j + skipJ);
    }
  }
  return check;
}

S21Matrix S21Matrix::InverseMatrix() {
  if (Determinant() == 0) {
    throw length_error(
        "Обратной матрицы не существует т.к. определитель равен 0");
  }

  S21Matrix check = CalcComplements();
  S21Matrix result = check.Transpose();
  result.MulNumber(1 / Determinant());
  return result;
}

void S21Matrix::SetRows(int row) {
  if (row < 0) {
    throw length_error("Количество строк не может быть меньше 0.");
  }

  if (row > rows_) {
    double **new_matrix = new double *[row]();
    for (int i = 0; i < row; i++) {
      new_matrix[i] = new double[cols_]();
      for (int j = 0; j < cols_; j++) {
        if (i < rows_) {
          new_matrix[i][j] = matrix_[i][j];
        } else {
          new_matrix[i][j] = 0.0;
        }
      }
    }
    matrix_ = new_matrix;
    rows_ = row;
  } else if (row <= rows_) {
    double **new_matrix = new double *[row];
    for (int i = 0; i < row; i++) {
      new_matrix[i] = new double[cols_];
      for (int j = 0; j < cols_; j++) {
        new_matrix[i][j] = matrix_[i][j];
      }
    }
    matrix_ = new_matrix;
    rows_ = row;
  }
}

void S21Matrix::SetCols(int col) {
  if (col < 0) {
    throw length_error("Количество столбцов не может быть меньше 0.");
  }

  if (col > cols_) {
    double **new_matrix = new double *[rows_];
    for (int i = 0; i < rows_; i++) {
      new_matrix[i] = new double[col];
      for (int j = 0; j < col; j++) {
        if (j < cols_) {
          new_matrix[i][j] = matrix_[i][j];
        } else {
          new_matrix[i][j] = 0.0;
        }
      }
    }
    matrix_ = new_matrix;
    cols_ = col;
  } else if (col <= cols_) {
    double **new_matrix = new double *[rows_];
    for (int i = 0; i < rows_; i++) {
      new_matrix[i] = new double[col];
      for (int j = 0; j < col; j++) {
        new_matrix[i][j] = matrix_[i][j];
      }
    }
    matrix_ = new_matrix;
    cols_ = col;
  }
}

int S21Matrix::GetCols() const noexcept { return cols_; }

int S21Matrix::GetRows() const noexcept { return rows_; }
