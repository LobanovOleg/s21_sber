#ifndef S21_STACK_H
#define S21_STACK_H

#include <iostream>

namespace s21 {
template <typename T>
class stack {
 public:
  using value_type = T;
  using reference = T &;
  using const_reference = const T &;
  using size_type = std::size_t;

  stack() noexcept;
  stack(std::initializer_list<value_type> const &items);
  stack(const stack &other);
  stack(stack &&other) noexcept;
  ~stack() noexcept;

  const_reference top() const noexcept;
  reference top() noexcept;
  bool empty() const noexcept;
  size_type size() const noexcept;

  void push(const_reference value);
  void pop();
  void swap(stack &other) noexcept;

  stack &operator=(const stack &other);
  stack &operator=(stack &&other) noexcept;

  template <typename... Args>
  void insert_many_front(Args &&...args);

 protected:
  struct Node {
    T data_;
    Node *prev_;
    Node *next_;
  };

  Node *back_;
  Node *root_;
  size_t size_;
};
}  // namespace s21

#include "s21_stack.inc"

#endif
