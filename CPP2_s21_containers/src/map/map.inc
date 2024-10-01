#include "map.h"

namespace s21 {

#define __PAIR std::pair<typename map<Key, T>::iterator, bool>

template <typename Key, typename T>
map<Key, T>::map(const std::initializer_list<value_type> &items) {
  for (auto i = items.begin(); i != items.end(); ++i) {
    insert(*i);
  }
}

template <typename Key, typename T>
map<Key, T> &map<Key, T>::operator=(map &&other) noexcept {
  if (this != &other) {
    AVLTree<Key, T>::operator=(std::move(other));
  }
  return *this;
}

template <typename Key, typename T>
map<Key, T> &map<Key, T>::operator=(const map &other) {
  if (this != &other) {
    AVLTree<Key, T>::operator=(other);
  }
  return *this;
}

template <typename Key, typename T>
__PAIR map<Key, T>::insert(const value_type &value) {
  return insert(value.first, value.second);
}

template <typename Key, typename T>
__PAIR map<Key, T>::insert(const Key &key, const T &obj) {
  std::pair<iterator, bool> return_value;
  if (AVLTree<Key, T>::root == nullptr) {
    AVLTree<Key, T>::root = new typename AVLTree<Key, T>::Node(key, obj);
    return_value.first = iterator(AVLTree<Key, T>::root);
    return_value.second = true;
  } else {
    bool check_insert =
        AVLTree<Key, T>::recursiveInsert(AVLTree<Key, T>::root, key, obj);
    return_value.first = find(key);
    return_value.second = check_insert;
  }
  return return_value;
}

template <typename Key, typename T>
typename map<Key, T>::value_type &map<Key, T>::MapIterator::operator*() {
  if (AVLTree<Key, T>::Iterator::iter_node == nullptr) {
    static value_type fake_value{};
    return fake_value;
  }
  std::pair<const key_type, mapped_type> pr =
      std::make_pair(AVLTree<Key, T>::Iterator::iter_node->key,
                     AVLTree<Key, T>::Iterator::iter_node->value);
  std::pair<const key_type, mapped_type> &ref = pr;
  return ref;
}

template <typename Key, typename T>
T &map<Key, T>::MapIterator::return_value() {
  if (AVLTree<Key, T>::Iterator::iter_node == nullptr) {
    static T fake_value{};
    return fake_value;
  }
  return AVLTree<Key, T>::Iterator::iter_node->value;
}

template <typename Key, typename T>
typename map<Key, T>::iterator map<Key, T>::find(const Key &key) {
  typename AVLTree<Key, T>::Node *node =
      AVLTree<Key, T>::search(AVLTree<Key, T>::root, key);
  return iterator(node);
}

template <typename Key, typename T>
__PAIR map<Key, T>::insert_or_assign(const Key &key, const T &obj) {
  auto it = find(key);
  if (it != this->end()) {
    erase(it);
    auto pr = insert(key, obj);
    pr.second = false;
    return pr;
  }
  return insert(key, obj);
}

// template <typename Key, typename T>
// template <class... Args>
// std::vector<__PAIR> map<Key, T>::insert_many(Args &&...args) {
//   std::vector<__PAIR> vec;
//   for (const auto &arg : {args...}) {
//     vec.push_back(insert(arg));
//   }
//   return vec;
// }

template <typename Key, typename T>
T &map<Key, T>::at(const Key &key) {
  auto it = find(key);
  if (it == nullptr)
    throw std::out_of_range(
        "Container does not have an element with the specified key");
  return it.return_value();
}

template <typename Key, typename T>
T &map<Key, T>::operator[](const Key &key) {
  auto it = find(key);
  if (it == nullptr) {
    auto pr = insert(std::make_pair(key, T()));
    it = pr.first;
  }
  return it.return_value();
}

template <typename Key, typename T>
typename map<Key, T>::iterator map<Key, T>::begin() {
  return map<Key, T>::MapIterator(
      AVLTree<Key, T>::getMin(AVLTree<Key, T>::root));
}

template <typename Key, typename T>
typename map<Key, T>::iterator map<Key, T>::end() {
  if (AVLTree<Key, T>::root == nullptr) return begin();

  typename AVLTree<Key, T>::Node *last_node =
      AVLTree<Key, T>::getMax(AVLTree<Key, T>::root);
  MapIterator test(nullptr, last_node);
  return test;
}

template <typename Key, typename T>
typename map<Key, T>::const_iterator map<Key, T>::cbegin() const {
  return map<Key, T>::ConstMapIterator(
      AVLTree<Key, T>::getMin(AVLTree<Key, T>::root));
}

template <typename Key, typename T>
typename map<Key, T>::const_iterator map<Key, T>::cend() const {
  if (AVLTree<Key, T>::root == nullptr) return cbegin();

  typename AVLTree<Key, T>::Node *last_node =
      AVLTree<Key, T>::getMax(AVLTree<Key, T>::root);
  ConstMapIterator test(nullptr, last_node);
  return test;
}

template <typename Key, typename T>
void map<Key, T>::merge(map &other) {
  map const_tree(other);
  iterator const_it = const_tree.begin();
  for (; const_it != const_tree.end(); ++const_it) {
    auto key = (*const_it).first;
    auto obj = (*const_it).second;
    std::pair<iterator, bool> pr = insert(key, obj);
    if (pr.second) other.erase(pr.first);
  }
}

template <typename Key, typename T>
void map<Key, T>::erase(map::iterator pos) {
  if (AVLTree<Key, T>::root == nullptr || pos.iter_node == nullptr) return;
  AVLTree<Key, T>::root =
      AVLTree<Key, T>::del(AVLTree<Key, T>::root, (*pos).first);
}
}  // namespace s21
