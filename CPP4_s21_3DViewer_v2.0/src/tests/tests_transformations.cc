#include "test_suite.h"

using namespace s21;

TEST(Transformation, MoveX) {
  Transformation transform;
  std::vector<double> vector_v = {1.0, 1.0, 1.0};
  std::vector<double> check_v = {1.5, 1.0, 1.0};

  transform.move_x(&vector_v, 50.0);

  EXPECT_EQ(vector_v[0], check_v[0]);
  EXPECT_EQ(vector_v[1], check_v[1]);
  EXPECT_EQ(vector_v[2], check_v[2]);
}

TEST(Transformation, MoveY) {
  Transformation transform;
  std::vector<double> vector_v = {1.0, 1.0, 1.0};
  std::vector<double> check_v = {1.0, 1.1, 1.0};

  transform.move_y(&vector_v, 10.0);

  EXPECT_EQ(vector_v[0], check_v[0]);
  EXPECT_EQ(vector_v[1], check_v[1]);
  EXPECT_EQ(vector_v[2], check_v[2]);
}

TEST(Transformation, MoveZ) {
  Transformation transform;
  std::vector<double> vector_v = {1.0, 1.0, 1.0};
  std::vector<double> check_v = {1.0, 1.0, 0.5};

  transform.move_z(&vector_v, -50.0);

  EXPECT_EQ(vector_v[0], check_v[0]);
  EXPECT_EQ(vector_v[1], check_v[1]);
  EXPECT_EQ(vector_v[2], check_v[2]);
}

TEST(Transformation, RotateXYZ) {
  Transformation transform;
  std::vector<double> vector_v = {1.0, 2.0, 3.0};
  std::vector<double> check_v = {-3.0, -2.0, -1.0};

  transform.rotate_x(&vector_v, 90.0);
  transform.rotate_y(&vector_v, 90.0);
  transform.rotate_z(&vector_v, 90.0);

  EXPECT_NEAR(vector_v[0], check_v[0], 1e-7);
  EXPECT_NEAR(vector_v[1], check_v[1], 1e-7);
  EXPECT_NEAR(vector_v[2], check_v[2], 1e-7);
}

TEST(Transformation, Scale1) {
  Transformation transform;
  std::vector<double> vector_v = {1.0, 1.0, 1.0};
  std::vector<double> check_v = {3.0, 3.0, 3.0};

  transform.scale(&vector_v, 3.0);

  EXPECT_EQ(vector_v[0], check_v[0]);
  EXPECT_EQ(vector_v[1], check_v[1]);
  EXPECT_EQ(vector_v[2], check_v[2]);
}

TEST(Transformation, Scale2) {
  Transformation transform;
  std::vector<double> vector_v = {10.0, 10.0, 10.0};
  std::vector<double> check_v = {2.0, 2.0, 2.0};

  transform.scale(&vector_v, -5.0);

  EXPECT_EQ(vector_v[0], check_v[0]);
  EXPECT_EQ(vector_v[1], check_v[1]);
  EXPECT_EQ(vector_v[2], check_v[2]);
}

TEST(Transformation, Scale3) {
  Transformation transform;
  std::vector<double> vector_v = {1.0, 1.0, 1.0, 1.0, 1.0,
                                  1.0, 1.0, 1.0, 1.0, 1.0};
  std::vector<double> check_v = {10.0, 10.0, 10.0, 10.0, 10.0,
                                 10.0, 10.0, 10.0, 10.0, 10.0};

  transform.scale(&vector_v, 10.0);

  EXPECT_EQ(vector_v[0], check_v[0]);
  EXPECT_EQ(vector_v[1], check_v[1]);
  EXPECT_EQ(vector_v[2], check_v[2]);
  EXPECT_EQ(vector_v[3], check_v[3]);
  EXPECT_EQ(vector_v[4], check_v[4]);
  EXPECT_EQ(vector_v[5], check_v[5]);
  EXPECT_EQ(vector_v[6], check_v[6]);
  EXPECT_EQ(vector_v[7], check_v[7]);
  EXPECT_EQ(vector_v[8], check_v[8]);
  EXPECT_EQ(vector_v[9], check_v[9]);
}