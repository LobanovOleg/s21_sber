#ifndef SRC_SET_S21_SET_H_
#define SRC_SET_S21_SET_H_

#include "../avl_tree/AVLTree.h"
namespace s21 {
template <typename Key>
class set : public AVLTree<Key, Key> {
 public:
  using key_type = Key;
  using value_type = Key;
  using reference = value_type &;
  using const_reference = const Key &;
  using iterator = typename AVLTree<Key, Key>::Iterator;
  using const_iterator = typename AVLTree<Key, Key>::ConstIterator;
  using size_type = size_t;

  set() : AVLTree<Key, Key>(){};
  set(std::initializer_list<value_type> const &items);
  set(const set &other) : AVLTree<Key, Key>(other){};
  set(set &&other) noexcept : AVLTree<Key, Key>(std::move(other)){};
  set &operator=(set &&other) noexcept;
  set &operator=(const set &other);
  ~set() = default;

  iterator find(const Key &key) { return AVLTree<Key, Key>::Find(key); };
  template <class... Args>
  std::vector<std::pair<iterator, bool>> insert_many(Args &&...args);
};

}  // namespace s21

#include "s21_set.inc"
#endif  // SRC_SET_S21_SET_H_
