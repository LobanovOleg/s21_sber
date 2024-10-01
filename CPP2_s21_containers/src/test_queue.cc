
#include <queue>

#include "main_test.h"

TEST(queue, default_constructor) {
  s21::queue<int> s21Queue;
  std::queue<int> stdQueue;
  ASSERT_EQ(s21Queue.empty(), stdQueue.empty());
}

TEST(queue, init_constructor) {
  s21::queue<int> s21Queue{1, 2, 3};
  ASSERT_FALSE(s21Queue.empty());
}

TEST(queue, init_string_constructor) {
  s21::queue<std::string> s21Queue{"hello", "world"};
  ASSERT_EQ(s21Queue.back(), "world");
  ASSERT_EQ(s21Queue.front(), "hello");
}

TEST(queue, copy_constructor) {
  s21::queue<int> s21Queue{1};
  s21::queue<int> s21QueueCopied(s21Queue);
  ASSERT_EQ(s21Queue.front(), s21QueueCopied.front());
}

TEST(queue, move_constructor) {
  s21::queue<int> s21Queue{1, 2, 3};
  s21::queue<int> s21QueueMoved(std::move(s21Queue));
  ASSERT_TRUE(s21Queue.empty());
  ASSERT_FALSE(s21QueueMoved.empty());
}

TEST(queue, move_operator_constructor) {
  s21::queue<int> s21Queue{1, 2, 3};
  s21::queue<int> s21QueueMoved(std::move(s21Queue));
  ASSERT_TRUE(s21Queue.empty());
  ASSERT_FALSE(s21QueueMoved.empty());
}

TEST(queue, push_int) {
  s21::queue<int> s21Queue;
  s21Queue.push(566);
  std::queue<int> stdQueue;
  stdQueue.push(566);
  ASSERT_EQ(s21Queue.front(), stdQueue.front());
  ASSERT_EQ(s21Queue.back(), stdQueue.back());
}

TEST(queue, pop_int) {
  s21::queue<int> s21Queue{566, 123};
  std::queue<int> stdQueue;
  stdQueue.push(566);
  stdQueue.push(123);
  ASSERT_EQ(s21Queue.front(), stdQueue.front());
  ASSERT_EQ(s21Queue.back(), stdQueue.back());
  s21Queue.pop();
  stdQueue.pop();
  ASSERT_EQ(s21Queue.front(), stdQueue.front());
  ASSERT_EQ(s21Queue.back(), stdQueue.back());
}

TEST(queue, pop_string) {
  s21::queue<std::string> s21Queue{"hello", "world"};
  std::queue<std::string> stdQueue;
  stdQueue.push("hello");
  stdQueue.push("world");
  ASSERT_EQ(s21Queue.front(), stdQueue.front());
  ASSERT_EQ(s21Queue.back(), stdQueue.back());
  s21Queue.pop();
  stdQueue.pop();
  ASSERT_EQ(s21Queue.front(), stdQueue.front());
  ASSERT_EQ(s21Queue.back(), stdQueue.back());
}

TEST(queue, size) {
  s21::queue<int> s21Queue{566, 123, 3, 3, 2, 1};
  s21::queue<int> s21Queue2{566, 123};
  ASSERT_EQ(s21Queue.size(), 6);
  ASSERT_EQ(s21Queue2.size(), 2);
}

TEST(queue, swap) {
  s21::queue<int> s21Queue{566, 123, 3, 3, 2, 1};
  s21::queue<int> s21Queue2{566, 123};
  s21Queue.swap(s21Queue2);
  ASSERT_EQ(s21Queue.size(), 2);
  ASSERT_EQ(s21Queue2.size(), 6);
}
