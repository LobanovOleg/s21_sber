#ifndef S21_LIST_H
#define S21_LIST_H
#include <climits>
#include <iostream>
#include <thread>

namespace s21 {

template <typename T>
class list {
 public:
  using value_type = T;
  using reference = T &;
  using const_reference = const T &;
  using size_type = size_t;

  bool empty();
  size_t size();
  size_t max_size();
  void clear();
  void push_back(T data);
  void pop_back();
  void push_front(T data);
  void pop_front();
  void reverse();
  void swap(list &other);
  void unique();
  void merge(list &other);
  void sort();

  T &front() const;
  T &back() const;

  list();
  list(size_t n);
  list(size_t n, size_t value);
  list(std::initializer_list<T> const &items);
  list(list &&l);
  list(const list &l);

  list &operator=(const list &l);
  list &operator=(list &&l);

  ~list() { clear(); }

  class listNode {
   public:
    T data;
    listNode *pNext;
    listNode *pPrev;

    explicit listNode(T d_data = T(), listNode *d_pNext = nullptr,
                      listNode *d_pPrev = nullptr)
        : data(d_data), pNext(d_pNext), pPrev(d_pPrev) {}

    ~listNode() { free_memory(); }
    void free_memory();
  };
  using node = typename list<T>::listNode;

  class ListIterator {
   public:
    node *first;
    node *end;
    node *itr;

    ListIterator() {
      first = nullptr;
      end = nullptr;
      itr = nullptr;
    }
    explicit ListIterator(const list<T> &other) {
      first = other.head_;
      end = other.back_;
      itr = other.head_;
    }

    ~ListIterator() { free_iterator(); }
    void swap_elements(ListIterator pos);
    void free_iterator();
    T &operator*() const;
    ListIterator operator++();
    ListIterator operator++(int);
    ListIterator operator--();
    ListIterator operator--(int);
    bool operator==(const ListIterator &other);
    bool operator!=(const ListIterator &other);
  };
  using iterator = typename list<T>::ListIterator;

  iterator begin();
  iterator end();
  void erase(iterator pos);

  class ListConstIterator {
   public:
    list::iterator A;

    ListConstIterator() {}
    explicit ListConstIterator(const list<T> &other) : A(other) {}
    explicit ListConstIterator(const ListIterator &other) {
      A.first = other.first;
      A.itr = other.itr;
      A.end = other.end;
    }
    ~ListConstIterator() {}

    T operator*() const { return *A; }
    ListConstIterator operator++() { return (ListConstIterator)++A; }
    ListConstIterator operator++(int) { return (ListConstIterator)A++; }
    ListConstIterator operator--() { return (ListConstIterator)--A; }
    ListConstIterator operator--(int) { return (ListConstIterator)A--; }

    operator ListIterator() {
      iterator result;
      result.first = A.first;
      result.end = A.end;
      result.itr = A.itr;
      return result;
    }

    bool operator==(const ListConstIterator &other) {
      return this->A.itr == other.A.itr;
    }
    bool operator!=(const ListConstIterator &other) {
      return this->A.itr != other.A.itr;
    }
  };
  using const_iterator = typename list<T>::ListConstIterator;

  const_iterator cbegin() { return (ListConstIterator)begin(); }
  const_iterator cend() { return (ListConstIterator)end(); }

  void splice(const_iterator pos, list &other);  // NOLINT(*)
  iterator insert(iterator pos, const_reference value);
  iterator insert(const_iterator pos, list<T> &&other);
  iterator insert(const_iterator pos, node *node);

  template <typename... Args>
  iterator insert_many(const_iterator pos, Args &&...args);
  template <typename... Args>
  void insert_many_back(Args &&...args);
  template <typename... Args>
  void insert_many_front(Args &&...args);

 private:
  using Allocator = std::allocator<node>;
  Allocator _allocator;
  size_t size_;
  node *head_;
  node *back_;
  void last_node();
};
}  // namespace s21
#include "s21_list.inc"

#endif
