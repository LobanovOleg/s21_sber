#include <limits>

#include "AVLTree.h"

#define __Node typename AVLTree<Key, Value>::Node
#define __Iter typename AVLTree<Key, Value>::Iterator

template <typename Key, typename Value>
inline AVLTree<Key, Value>::AVLTree() : root(nullptr) {}

template <typename Key, typename Value>
AVLTree<Key, Value>::AVLTree(const AVLTree &other) {
  root = copyTree(other.root, nullptr);
}

template <typename Key, typename Value>
AVLTree<Key, Value>::AVLTree(AVLTree &&other) noexcept {
  root = other.root;
  other.root = nullptr;
}

template <typename Key, typename Value>
inline AVLTree<Key, Value>::~AVLTree() {
  clear();
}
template <typename Key, typename Value>
AVLTree<Key, Value> &AVLTree<Key, Value>::operator=(AVLTree &&other) noexcept {
  if (this != &other) {
    root = other.root;
    other.root = nullptr;
  }
  return *this;
}

template <typename Key, typename Value>
AVLTree<Key, Value> &AVLTree<Key, Value>::operator=(const AVLTree &other) {
  if (this != &other) {
    AVLTree temp(other);
    FreeNode(root);
    *this = std::move(temp);
  }
  return *this;
}

template <typename Key, typename Value>
typename AVLTree<Key, Value>::Iterator AVLTree<Key, Value>::begin() {
  return AVLTree::Iterator(getMin(root));
}

template <typename Key, typename Value>
typename AVLTree<Key, Value>::Iterator AVLTree<Key, Value>::end() {
  if (root == nullptr) return begin();
  Node *last_node = getMax(root);
  Iterator test(nullptr, last_node);
  return test;
}

//
//  Capacity
//

template <typename Key, typename Value>
bool AVLTree<Key, Value>::empty() {
  return (root == nullptr) ? true : false;
}

template <typename Key, typename Value>
size_t AVLTree<Key, Value>::size() {
  return recursiveSize(root);
}

template <typename Key, typename Value>
size_t AVLTree<Key, Value>::max_size() {
  return std::numeric_limits<size_type>::max() /
         sizeof(typename AVLTree<Key, Value>::Node);
}

//
//  Modifiers
//

template <typename Key, typename Value>
void AVLTree<Key, Value>::clear() {
  if (root != nullptr) freeNode(root);
  root = nullptr;
}

template <typename Key, typename Value>
std::pair<typename AVLTree<Key, Value>::Iterator, bool>
AVLTree<Key, Value>::insert(
    const Key &key) {  // Обычный инсерт обертка для основной вставки с
                       // алгоритмом, и возвращаемые значения по таску
  std::pair<Iterator, bool> return_value;
  if (root == nullptr) {
    root = new Node(key, key);
    return_value.first = Iterator(root);
    return_value.second = true;
  } else {
    bool check_insert = recursiveInsert(root, key, key);
    return_value.first = find(key);  // НАДО НАПИСАТЬ ФУНКЦИЮ FIND
    return_value.second = check_insert;
  }
  return return_value;
}

template <typename Key, typename Value>
void AVLTree<Key, Value>::erase(iterator pos) {
  if (root == nullptr || pos.iter_node == nullptr) return;
  root = del(root, *pos);
}

template <typename Key, typename Value>
void AVLTree<Key, Value>::swap(AVLTree &other) {
  std::swap(root, other.root);
}

template <typename Key, typename Value>
void AVLTree<Key, Value>::merge(AVLTree &other) {
  AVLTree const_tree(other);
  Iterator const_it = const_tree.begin();
  //    Iterator it = other.begin();
  for (; const_it != const_tree.end(); ++const_it) {
    std::pair<Iterator, bool> pr = recursiveInsert(*const_it);
    if (pr.second) other.erase(pr.first);
  }
}

template <typename Key, typename Value>
bool AVLTree<Key, Value>::contains(const Key &key) {
  Node *found = search(root, key);
  return (found == nullptr) ? false : true;
}

template <typename Key, typename Value>
size_t AVLTree<Key, Value>::recursiveSize(AVLTree::Node *node) {
  if (node == nullptr) return 0;
  size_t left_size = recursiveSize(node->left);
  size_t right_size = recursiveSize(node->right);
  return 1 + left_size + right_size;
}

// template <typename Key, typename Value>
// void AVLTree<Key, Value>::recursiveInsert(Node *node,
//                                           const Key &key,
//                                           const Value &value) {
//   if (key < node->key) {
//     if (node->left == nullptr)
//       node->left = new Node(key, value);
//     else
//       recursiveInsert(node->left, key, value);
//   } else {
//     if (node->right == nullptr)
//       node->right = new Node(key, value);
//     else
//       recursiveInsert(node->right, key, value);
//   }
//   setHeight(node);
//   balance(node);
// }

template <typename Key, typename Value>
bool AVLTree<Key, Value>::recursiveInsert(AVLTree::Node *node, const Key &key,
                                          Value value) {
  bool check_insert = false;
  if (key < node->key) {
    if (node->left == nullptr) {
      node->left = new Node(key, value, node);
      check_insert = true;
    } else {
      check_insert = recursiveInsert(node->left, key, value);
    }
  } else if (key > node->key) {
    if (node->right == nullptr) {
      node->right = new Node(key, value, node);
      check_insert = true;
    } else {
      check_insert = recursiveInsert(node->right, key, value);
    }
  } else if (key == node->key) {
    return check_insert;  // инсерт не произошел потому что такой ключ был в
                          // дереве
  }
  setHeight(node);
  balance(node);
  return check_insert;
}

template <typename Key, typename Value>
inline int AVLTree<Key, Value>::getBalance(Node *node) {
  return (node == nullptr) ? 0 : getHeight(node->right) - getHeight(node->left);
}

template <typename Key, typename Value>
inline int AVLTree<Key, Value>::getHeight(Node *node) {
  return (node == nullptr) ? -1 : node->height;
}

template <typename Key, typename Value>
void AVLTree<Key, Value>::setHeight(Node *node) {
  node->height = std::max(getHeight(node->left), getHeight(node->right)) + 1;
}

template <typename Key, typename Value>
__Node *AVLTree<Key, Value>::search(Node *node, const Key &key) {
  if (node == nullptr) return nullptr;
  if (node->key == key) return node;
  return (key < node->key) ? search(node->left, key) : search(node->right, key);
}

template <typename Key, typename Value>
__Iter AVLTree<Key, Value>::find(const Key &key) {
  Node *exact_node = search(root, key);
  return Iterator(exact_node);
}

template <typename Key, typename Value>
__Node *AVLTree<Key, Value>::del(AVLTree<Key, Value>::Node *node, Key key) {
  if (node == nullptr)
    return nullptr;
  else if (key < node->key)
    node->left = del(node->left, key);
  else if (key > node->key)
    node->right = del(node->right, key);
  else {
    if (node->left == nullptr || node->right == nullptr) {
      Node *node_right = node->right;
      Node *node_left = node->left;
      Node *node_parent = node->parent;
      delete node;
      if (node_left == nullptr) {
        node = node_right;
      } else {
        node = node_left;
      }
      if (node != nullptr) node->parent = node_parent;
    } else {
      Node *maxInLeft = getMax(node->left);
      node->key = maxInLeft->key;
      node->value = maxInLeft->value;
      node->left = del(node->left, maxInLeft->key);
    }
  }
  if (node != nullptr) {
    setHeight(node);
    balance(node);
  }
  return node;
}

template <typename Key, typename Value>
__Node *AVLTree<Key, Value>::getMin(AVLTree::Node *node) {
  if (node == nullptr) return nullptr;
  if (node->left == nullptr) return node;
  return getMin(node->left);
}

template <typename Key, typename Value>
void AVLTree<Key, Value>::swap(AVLTree::Node *a, AVLTree::Node *b) {
  Key key = a->key;
  a->key = b->key;
  b->key = key;
  Value val = a->value;
  a->value = b->value;
  b->value = val;
}

template <typename Key, typename Value>
__Node *AVLTree<Key, Value>::getMax(AVLTree::Node *node) {
  if (node == nullptr) return nullptr;
  if (node->right == nullptr) return node;
  return getMax(node->right);
}

template <typename Key, typename Value>
__Node *AVLTree<Key, Value>::getRoot(AVLTree::Node *node) {
  if (node == nullptr) return nullptr;
  if (node->parent == nullptr) return node;
  return getRoot(node->parent);
}

//
//  balance functins
//

template <typename Key, typename Value>
void AVLTree<Key, Value>::balance(Node *node) {
  int balance = getBalance(node);
  if (balance == -2) {
    if (getBalance(node->left) == 1) leftRotate(node->left);
    rightRotate(node);
  } else if (balance == 2) {
    if (getBalance(node->right) == -1) rightRotate(node->right);
    leftRotate(node);
  }
}

template <typename Key, typename Value>
void AVLTree<Key, Value>::leftRotate(Node *node) {
  swap(node, node->right);
  Node *nodeLeft = node->left;
  node->left = node->right;
  node->right = node->left->right;
  node->left->right = node->left->left;
  node->left->left = nodeLeft;
  if (node->left) {
    node->left->parent = node;
    if (node->left->right) node->left->right->parent = node->left;
    if (node->left->left) node->left->left->parent = node->left;
  }
  if (node->right) {
    node->right->parent = node;
    if (node->right->right) node->right->right->parent = node->right;
    if (node->right->left) node->right->left->parent = node->right;
  }
  setHeight(node->left);
  setHeight(node);
}

template <typename Key, typename Value>
void AVLTree<Key, Value>::rightRotate(Node *node) {
  swap(node, node->left);
  Node *nodeRight = node->right;
  node->right = node->left;
  node->left = node->right->left;
  node->right->left = node->right->right;
  node->right->right = nodeRight;
  if (node->left) {
    node->left->parent = node;
    if (node->left->right) node->left->right->parent = node->left;
    if (node->left->left) node->left->left->parent = node->left;
  }
  if (node->right) {
    node->right->parent = node;
    if (node->right->right) node->right->right->parent = node->right;
    if (node->right->left) node->right->left->parent = node->right;
  }
  setHeight(node->right);
  setHeight(node);
}

//
//  support functions
//

template <typename Key, typename Value>
__Node *AVLTree<Key, Value>::copyTree(Node *node, Node *parent) {
  if (node == nullptr) return nullptr;
  Node *new_copy = new Node(node->key, node->value, parent);
  new_copy->left = copyTree(node->left, new_copy);
  new_copy->right = copyTree(node->right, new_copy);
  return new_copy;
}

template <typename Key, typename Value>
void AVLTree<Key, Value>::printTree(Node *node) {
  if (node == nullptr) return;
  printTree(node->left);
  std::cout << std::endl << "key=" << node->key << " value=" << node->value;
  printTree(node->right);
}

template <typename Key, typename Value>
void AVLTree<Key, Value>::printTree(Node *node, int deep) {
  if (node == nullptr) return;
  for (int i = 0; i < deep * 2; ++i) std::cout << "\t";
  std::cout << "key=" << node->key << " value=" << node->value;
  if (node->parent != nullptr)
    std::cout << "{ key=" << node->parent->key
              << " value=" << node->parent->value << " }";
  std::cout << std::endl;
  printTree(node->left, deep + 1);
  printTree(node->right, deep + 1);
}

template <typename Key, typename Value>
void AVLTree<Key, Value>::freeNode(Node *node) {
  if (node == nullptr) return;
  freeNode(node->left);
  freeNode(node->right);
  delete node;
}

//
//  Iterator
//

template <typename Key, typename Value>
inline AVLTree<Key, Value>::Iterator::Iterator()
    : iter_node(nullptr), iter_past_node(nullptr) {}

template <typename Key, typename Value>
inline AVLTree<Key, Value>::Iterator::Iterator(AVLTree::Node *node,
                                               AVLTree::Node *past_node)
    : iter_node(node), iter_past_node(past_node) {}

template <typename Key, typename Value>
__Iter &AVLTree<Key, Value>::Iterator::operator++() {
  Node *tmp;
  if (iter_node != nullptr) {
    tmp = getMax(iter_node);
  }
  iter_node = moveForward(iter_node);
  if (iter_node == nullptr) {
    iter_past_node = tmp;
  }
  return *this;
}

template <typename Key, typename Value>
__Iter AVLTree<Key, Value>::Iterator::operator++(int) {
  Iterator temp = *this;
  operator++();
  return temp;
}

template <typename Key, typename Value>
__Iter &AVLTree<Key, Value>::Iterator::operator--() {
  if (iter_node == nullptr && iter_past_node != nullptr) {
    *this = iter_past_node;
    return *this;
  }
  iter_node = moveBack(iter_node);
  return *this;
}

template <typename Key, typename Value>
__Iter AVLTree<Key, Value>::Iterator::operator--(int) {
  Iterator temp = *this;
  operator--();
  return temp;
}

template <typename Key, typename Value>
Value &AVLTree<Key, Value>::Iterator::operator*() {
  if (iter_node == nullptr) {
    static Value fake_value{};
    return fake_value;
  }
  return iter_node->value;  // тут было value - изменил из-за мапы (key)
}

template <typename Key, typename Value>
bool AVLTree<Key, Value>::Iterator::operator==(const AVLTree::Iterator &it) {
  return iter_node == it.iter_node;
}

template <typename Key, typename Value>
bool AVLTree<Key, Value>::Iterator::operator!=(const AVLTree::Iterator &it) {
  return iter_node != it.iter_node;
}

template <typename Key, typename Value>
__Node *AVLTree<Key, Value>::Iterator::moveForward(AVLTree::Node *node) {
  if (node == getMax(getRoot(node))) {
    return nullptr;
  }
  if (node->right != nullptr) {
    return getMin(node->right);
  }
  AVLTree<Key, Value>::Node *parent = node->parent;
  while (parent != nullptr && node == parent->right) {
    node = parent;
    parent = parent->parent;
  }
  return parent;
}

template <typename Key, typename Value>
__Node *AVLTree<Key, Value>::Iterator::moveBack(AVLTree::Node *node) {
  if (node->left != nullptr) {
    return getMax(node->left);
  }
  Node *parent = node->parent;
  while (parent != nullptr && node == parent->left) {
    node = parent;
    parent = node->parent;
  }
  return parent;
}
