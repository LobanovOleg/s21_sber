#include "test_suite.h"

using namespace s21;

TEST(Loader, LoadingFileErr) {
  Loader load;

  EXPECT_EQ(2, load.LoadingFile("obj_examples/nice_file.obj"));
}

TEST(Loader, LoadingFileSuccess) {
  Loader load;

  EXPECT_EQ(0, load.LoadingFile("obj_examples/cube.obj"));
}

TEST(Loader, Clearing) {
  Loader load;

  load.LoadingFile("obj_examples/nice_file.obj");

  EXPECT_EQ(0, load.GetCountVertices());
  EXPECT_EQ(0, load.GetCountPolygons());
}

TEST(Loader, LoadingFile) {
  Loader load;

  EXPECT_EQ(0, load.LoadingFile("obj_examples/cactus.obj"));
}