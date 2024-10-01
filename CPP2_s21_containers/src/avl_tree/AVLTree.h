#ifndef AVLTREE_H_
#define AVLTREE_H_

#include <iostream>

template <typename Key, typename Value>
class AVLTree {
 protected:
  struct Node;

 public:
  class Iterator;
  class ConstIterator;

  //
  //  Member type
  //

  using key_type = Key;
  using value_type = Value;
  using reference = value_type&;
  using const_reference = const value_type&;
  using iterator = Iterator;
  using const_iterator = ConstIterator;
  using size_type = size_t;

  class Iterator {
   public:
    Iterator();
    Iterator(Node* node, Node* past_node = nullptr);
    iterator& operator++();
    iterator operator++(int);
    iterator& operator--();
    iterator operator--(int);
    reference operator*();
    bool operator==(const iterator& it);
    friend class AVLTree<Key, Value>;
    bool operator!=(const iterator& it);

   protected:
    Node* iter_node;
    Node* iter_past_node;
    Node* moveForward(Node* node);
    Node* moveBack(Node* node);
  };
  class ConstIterator : public Iterator {
   public:
    ConstIterator() : Iterator(){};
    const_reference operator*() const { return Iterator::operator*(); };
  };

  AVLTree();
  AVLTree(const AVLTree& other);
  AVLTree(AVLTree&& other) noexcept;
  ~AVLTree();
  AVLTree& operator=(AVLTree&& other) noexcept;
  AVLTree& operator=(const AVLTree& other);
  iterator begin();
  iterator end();

  //
  //  Capacity
  //

  bool empty();
  size_type size();
  size_type max_size();

  //
  //  Modifiers
  //

  void clear();
  std::pair<iterator, bool> insert(const Key& key);
  void erase(iterator pos);
  void swap(AVLTree& other);
  void merge(AVLTree& other);
  bool contains(const Key& key);

 protected:
  struct Node {
    Key key;
    Value value;
    Node* left{};
    Node* right{};
    Node* parent{};
    int height{};
    Node(Key key, Value value) : key(key), value(value) {}
    Node(Key key, Value value, Node* parent)
        : key(key), value(value), parent(parent) {}
    friend class AVLTree<Key, Value>;
  };
  Node* root;

  int getBalance(Node* node);
  int getHeight(Node* node);
  void setHeight(Node* node);
  void swap(Node* a, Node* b);

  // void recursiveInsert(Node* node, const Key& key, const Value& value);
  bool recursiveInsert(Node* node, const Key& key, Value value);
  size_t recursiveSize(Node* node);
  Node* search(Node* node, const Key& key);
  iterator find(const Key& key);
  Node* del(Node* node, Key key);
  static Node* getMin(Node* node);
  static Node* getMax(Node* node);
  static Node* getRoot(Node* node);

  //  balance functins
  void balance(Node* node);

  void leftRotate(Node* node);
  void rightRotate(Node* node);

 public:
  //  support functions
  Node* copyTree(Node* node, Node* parent);
  void printTree(Node* node);
  void printTree(Node* node, int deep);
  void printTree() { printTree(root, 0); }
  void freeNode(Node* node);
};

#include "AVLTree.inc"

#endif  //  AVLTREE_H_
