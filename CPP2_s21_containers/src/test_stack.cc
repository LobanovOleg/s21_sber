#include <stack>

#include "main_test.h"

TEST(Stack, Constructor_Default) {
  s21::stack<int> our_stack;
  std::stack<int> std_stack;
  EXPECT_EQ(our_stack.empty(), std_stack.empty());
}

TEST(Stack, Constructor_List) {
  s21::stack<int> our = {1, 2, 3};
  std::stack<int> std;
  std.push(1);
  std.push(2);
  std.push(3);
  EXPECT_EQ(our.top(), std.top());
}

TEST(Stack, Constructor_Copy) {
  s21::stack<int> our = {1, 2, 3};
  std::stack<int> std;
  s21::stack<int> our_copy(our);
  std.push(1);
  std.push(2);
  std.push(3);
  std::stack<int> std_copy(std);
  EXPECT_EQ(our_copy.top(), std_copy.top());
}

TEST(Stack, Operator_Copy) {
  s21::stack<int> our_stack = {1, 2, 3};
  std::stack<int> std_stack;
  std_stack.push(1);
  std_stack.push(2);
  std_stack.push(3);
  s21::stack<int> new_our;
  std::stack<int> new_std;
  new_our = our_stack;
  new_std = std_stack;
  EXPECT_EQ(new_our.top(), new_std.top());
  EXPECT_EQ(our_stack.empty(), std_stack.empty());
}

TEST(Stack, Constructor_Move) {
  s21::stack<int> our = {1, 2, 3};
  std::stack<int> std;
  s21::stack<int> our_move(std::move(our));
  std.push(1);
  std.push(2);
  std.push(3);
  std::stack<int> std_move(std::move(std));
  EXPECT_EQ(our_move.top(), std_move.top());
  EXPECT_EQ(our.empty(), std.empty());
}

TEST(Stack, Operator_Move) {
  s21::stack<int> our = {1, 2, 3};
  std::stack<int> std;
  std.push(1);
  std.push(2);
  std.push(3);
  s21::stack<int> our_new;
  std::stack<int> std_new;
  our_new = std::move(our);
  std_new = std::move(std);
  EXPECT_EQ(our_new.top(), std_new.top());
  EXPECT_EQ(our.empty(), std.empty());
}

TEST(Stack, Top) {
  s21::stack<int> our = {1, 2, 3};
  std::stack<int> std;
  std.push(1);
  std.push(2);
  std.push(3);
  s21::stack<double> our_d = {1.1, 2.2, 3.3};
  std::stack<double> std_d;
  std_d.push(1.1);
  std_d.push(2.2);
  std_d.push(3.3);
  s21::stack<std::string> our_s = {"abc", "acb", "bca"};
  std::stack<std::string> std_s;
  std_s.push("abc");
  std_s.push("acb");
  std_s.push("bca");
  EXPECT_EQ(our.top(), std.top());
  EXPECT_EQ(our_d.top(), std_d.top());
  EXPECT_EQ(our_s.top(), std_s.top());
}

TEST(Stack, Empty) {
  s21::stack<int> our = {1, 2, 3};
  std::stack<int> std;
  std.push(1);
  std.push(2);
  std.push(3);
  EXPECT_EQ(our.empty(), std.empty());
  s21::stack<int> our_e;
  std::stack<int> std_e;
  EXPECT_EQ(our_e.empty(), std_e.empty());
}

TEST(Stack, Size) {
  s21::stack<int> our = {1, 2, 3};
  std::stack<int> std;
  std.push(1);
  std.push(2);
  std.push(3);
  EXPECT_EQ(our.size(), std.size());
}

TEST(Stack, Push) {
  s21::stack<int> our;
  our.push(1);
  our.push(2);
  our.push(3);
  std::stack<int> std;
  std.push(1);
  std.push(2);
  std.push(3);
  EXPECT_EQ(our.top(), std.top());
}

TEST(Stack, Pop) {
  s21::stack<int> our;
  our.push(1);
  our.push(2);
  our.push(3);
  our.pop();
  std::stack<int> std;
  std.push(1);
  std.push(2);
  std.push(3);
  std.pop();
  EXPECT_EQ(our.top(), std.top());
  our.pop();
  std.pop();
  our.pop();
  std.pop();
  EXPECT_EQ(our.empty(), std.empty());
}

TEST(Stack, Swap) {
  s21::stack<int> our = {1, 2, 3};
  std::stack<int> std;
  std.push(1);
  std.push(2);
  std.push(3);
  s21::stack<int> our_e;
  std::stack<int> std_e;
  our_e.swap(our);
  std_e.swap(std);
  EXPECT_EQ(our_e.top(), std_e.top());
}

TEST(Stack, Insert_Many_Front) {
  s21::stack<int> our;
  our.insert_many_front(1, 2, 3);
  EXPECT_EQ(our.top(), 3);
}
