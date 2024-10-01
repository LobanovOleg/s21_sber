#ifndef SRC_QUEUE_QUEUE_H_
#define SRC_QUEUE_QUEUE_H_
//  #include "../list/list.h"
#include <list>

namespace s21 {

template <typename T, class s21_queue = std::list<T>>
class queue {
 private:
  s21_queue A;

 public:
  using value_type = typename s21_queue::value_type;
  using reference = typename s21_queue::reference;
  using const_reference = typename s21_queue::const_reference;
  using size_type = typename s21_queue::size_type;

  queue() : A(){};
  queue(std::initializer_list<T> const& items) : A(items){};
  queue(const queue& q) : A(q.A){};
  queue(queue&& q) : A(std::move(q.A)){};
  ~queue() {}

  queue<T>& operator=(queue&& q) {
    this->A = q.A;
    return *this;
  }

  void push(const_reference value) { A.push_back(value); }
  void pop() { A.pop_front(); }
  void swap(queue& other) { A.swap(other.A); }

  const_reference front() { return A.front(); }
  const_reference back() { return A.back(); }
  bool empty() { return A.empty(); }
  size_type size() { return A.size(); }
};

}  // namespace s21

#endif  // SRC_QUEUE_QUEUE_H_
