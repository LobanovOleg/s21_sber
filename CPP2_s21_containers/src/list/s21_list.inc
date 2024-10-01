namespace s21 {

template <typename T>
void list<T>::listNode::free_memory() {
  pNext = nullptr;
  pPrev = nullptr;
}

template <typename T>
void list<T>::last_node() {
  node *p = head_;
  while (p->pNext != nullptr) {
    p = p->pNext;
  }
  back_ = p;
}

template <typename T>
list<T>::list() : size_(0), head_(nullptr), back_(nullptr) {}

template <typename T>
list<T>::list(size_t n) : size_(0) {
  for (size_t i = 0; i < n; i++) {
    push_back(value_type());
  }
}

template <typename T>
list<T>::list(size_t n, size_t value) : size_(0) {
  for (size_t i = 0; i < n; i++) {
    push_back(value);
  }
}

template <typename T>
list<T>::list(std::initializer_list<T> const &items) : size_(0) {
  for (const auto &data : items) {
    push_back(data);
  }
}

template <typename T>
list<T>::list(const list<T> &l) : size_(0) {
  list<T>::ListIterator ptr(l);
  while (ptr.itr) {
    push_back(*ptr);
    ++ptr;
  }
}

template <typename T>
list<T>::list(list<T> &&l) : size_(0) {
  if (&l != this) {
    head_ = l.head_;
    size_ = l.size_;
    l.head_ = nullptr;
    l.back_ = back_;
    l.size_ = 0;
  } else {
    head_ = new node;
    head_->pNext = nullptr;
    head_->pPrev = nullptr;
  }
}

template <typename T>
void list<T>::push_back(T data) {
  if (size_ == 0) {
    this->head_ = new node;
    head_->data = data;
    back_ = head_;
  } else {
    node *tmp = new node;
    tmp->pPrev = this->back_;
    tmp->pNext = nullptr;
    tmp->data = data;
    this->back_->pNext = tmp;
    back_ = tmp;
  }
  ++size_;
}

template <typename T>
bool list<T>::empty() {
  return size() == 0;
}

template <typename T>
size_t list<T>::size() {
  return size_;
}

template <typename T>
size_t list<T>::max_size() {
  return LLONG_MAX / sizeof(node) - 1;
}

template <typename T>
void list<T>::clear() {
  if (empty() == false) {
    node *p = head_;
    while (p->pNext != nullptr) {
      p = p->pNext;
    }
    while (p->pPrev != nullptr) {
      p = p->pPrev;
      delete p->pNext;
      --size_;
    }
    delete p;
    --size_;
  }
}

template <typename T>
void list<T>::pop_back() {
  list<T>::ListIterator ptr(*this);
  ptr.end->pPrev->pNext = nullptr;
  back_ = ptr.end->pPrev;
  delete ptr.end;
  size_--;
}

template <typename T>
void list<T>::push_front(T data) {
  if (size_ == 0) {
    head_ = new node;
    head_->pNext = nullptr;
    head_->pPrev = nullptr;
    head_->data = data;
    ++size_;
    back_ = head_;
  } else {
    node *first = new node;
    first->data = data;
    first->pPrev = nullptr;
    first->pNext = head_;
    head_->pPrev = first;
    head_ = first;
    ++size_;
  }
}

template <typename T>
void list<T>::pop_front() {
  if (size_ > 1) {
    head_ = head_->pNext;
    delete head_->pPrev;
    head_->pPrev = nullptr;
  } else if (size_ == 1) {
    delete head_;
  }
  size_--;
}

template <class T>
list<T> &list<T>::operator=(const list &l) {
  if (size_ != 0) {
    this->clear();
  }
  list<T>::ListIterator ptr(l);
  while (ptr.itr) {
    push_back(*ptr);
    ++ptr;
  }
  return *this;
}

template <class T>
list<T> &list<T>::operator=(list &&l) {
  *this = l;
  l.clear();
  return *this;
}

template <typename T>
T &list<T>::front() const {
  list<T>::ListIterator tmp(*this);
  return *tmp;
}

template <typename T>
T &list<T>::back() const {
  list<T>::ListIterator ptr(*this);
  ptr.itr = ptr.end;
  return *ptr;
}

template <typename T>
void list<T>::reverse() {
  list<T> ptr(*this);
  list<T>::ListIterator tmp = ptr.begin();
  this->clear();
  for (; this->size_ < ptr.size_;) {
    this->push_front(*tmp);
    ++tmp;
  }
}

template <typename T>
void list<T>::unique() {
  list<T>::ListIterator ptr = this->begin();
  auto c = *ptr;
  ++ptr;
  while (ptr.itr) {
    if (c == *ptr) {
      ptr.itr->pPrev->pNext = ptr.itr->pNext;
      if (ptr.itr->pNext != nullptr) {
        ptr.itr->pNext->pPrev = ptr.itr->pPrev;
      }
      node *tmp = ptr.itr;
      ++ptr;
      delete tmp;
      size_--;
    } else {
      c = *ptr;
      ++ptr;
    }
  }
}

template <typename T>
void list<T>::sort() {
  if (size_ < 2) {
    return;
  } else if (size_ == 2) {
    ListIterator ptr = begin();
    ListIterator ptr_e = end();
    if (*ptr > *ptr_e) {
      ptr.swap_elements(ptr_e);
    }
    return;
  } else {
    list<T> Left;
    list<T> Right;
    ListIterator ptr = begin();

    for (size_t i = 0; i < size_; i++) {
      if (i < size_ / 2) {
        Left.push_back(*ptr);
      } else {
        Right.push_back(*ptr);
      }
      ++ptr;
    }

    if (Left.size_ > 8192) {
      std::thread th(&list::sort, &Left);
      Right.sort();
      th.join();
    } else {
      Left.sort();
      Right.sort();
    }

    list<T> Result;

    list<T>::ListIterator ptr_left = Left.begin();
    list<T>::ListIterator ptr_right = Right.begin();

    bool flag = true;

    while (flag) {
      if (*ptr_left < *ptr_right) {
        Result.push_back(*ptr_left);
        if (ptr_left.itr->pNext != nullptr) {
          ++ptr_left;
        } else {
          while (ptr_right.itr != nullptr) {
            Result.push_back(*ptr_right);
            ++ptr_right;
          }
          flag = false;
        }
      } else {
        Result.push_back(*ptr_right);
        if (ptr_right.itr->pNext != nullptr) {
          ++ptr_right;
        } else {
          while (ptr_left.itr != nullptr) {
            Result.push_back(*ptr_left);
            ++ptr_left;
          }
          flag = false;
        }
      }
    }
    *this = std::move(Result);
  }
}

template <typename T>
void list<T>::iterator::swap_elements(typename list<T>::ListIterator l) {
  T tmp = l.itr->data;
  l.itr->data = itr->data;
  itr->data = tmp;
}

template <typename T>
void list<T>::merge(list &other) {  // NOLINT(*)
  list<T>::iterator first = this->end();
  list<T>::iterator second = other.begin();
  first.itr->pNext = second.itr;
  second.itr->pPrev = first.itr;
  size_ += other.size_;
  back_ = other.back_;
  other.head_ = nullptr;
  other.size_ = 0;
}

template <typename T>
void list<T>::swap(list &other) {
  node *tmp;
  tmp = other.head_;
  other.head_ = head_;
  head_ = tmp;
  int tmp_size = other.size_;
  other.size_ = size_;
  size_ = tmp_size;
  tmp = other.back_;
  other.back_ = back_;
  back_ = tmp;
}

template <typename T>
void list<T>::erase(typename list<T>::ListIterator pos) {
  if (pos.itr == pos.end) {
    pop_back();
  } else if (pos.itr == pos.first) {
    pop_front();
  } else {
    pos.itr->pPrev->pNext = pos.itr->pNext;
    pos.itr->pNext->pPrev = pos.itr->pPrev;
    delete pos.itr;
    size_--;
  }
}

template <typename T>
void list<T>::splice(const_iterator pos, list &l) {  // NOLINT(*)
  if (pos.A.itr == nullptr) {
    throw std::invalid_argument("attempt to dereference a null pointer");
  }
  if (l.size_ == 0) {
    return;
  }
  iterator tmp = l.end();
  if (pos.A.itr == pos.A.first) {
    pos.A.itr->pPrev = tmp.itr;
    head_ = tmp.first;
    tmp.end->pNext = pos.A.first;
    size_ += l.size_;
    l.size_ = 0;
    l.head_ = nullptr;
  } else if (pos.A.itr == pos.A.end) {
    pos.A.end->pNext = tmp.first;
    tmp.first->pPrev = pos.A.itr;
    size_ += l.size_;
    back_ = l.back_;
    l.size_ = 0;
    l.head_ = nullptr;
  } else {
    pos.A.itr->pPrev->pNext = tmp.first;
    tmp.first->pPrev = pos.A.itr->pPrev;
    tmp.itr->pNext = pos.A.itr;
    pos.A.itr->pPrev = tmp.itr;
    size_ += l.size_;
    l.size_ = 0;
    l.head_ = nullptr;
    last_node();
  }
}

// ITERATOR

template <typename T>
void list<T>::ListIterator::free_iterator() {
  first = nullptr;
  end = nullptr;
  itr = nullptr;
}

template <typename T>
T &list<T>::ListIterator::operator*() const {
  if (itr == nullptr) {
    throw std::invalid_argument("attempt to dereference a null pointer");
  }
  return itr->data;
}

template <typename T>
typename list<T>::ListIterator list<T>::ListIterator::operator++() {
  if (itr == nullptr) {
    throw std::invalid_argument("attempt to dereference a null pointer");
  }
  itr = itr->pNext;
  return *this;
}

template <typename T>
typename list<T>::ListIterator list<T>::ListIterator::operator++(int) {
  if (itr == nullptr) {
    throw std::invalid_argument("attempt to dereference a null pointer");
  }
  iterator ptr = *this;
  itr = itr->pNext;
  return ptr;
}

template <typename T>
typename list<T>::ListIterator list<T>::ListIterator::operator--() {
  if (itr == nullptr) {
    throw std::invalid_argument("attempt to dereference a null pointer");
  }
  itr = itr->pPrev;
  return *this;
}

template <typename T>
typename list<T>::ListIterator list<T>::ListIterator::operator--(int) {
  if (itr == nullptr) {
    throw std::invalid_argument("attempt to dereference a null pointer");
  }
  iterator ptr = *this;
  itr = itr->pPrev;
  return ptr;
}

template <typename T>
bool list<T>::ListIterator::operator==(const ListIterator &l) {
  return itr == l.itr;
}

template <typename T>
bool list<T>::ListIterator::operator!=(const ListIterator &l) {
  return itr != l.itr;
}

template <typename T>
typename list<T>::iterator list<T>::begin() {
  return ListIterator(*this);
}

template <typename T>
typename list<T>::iterator list<T>::end() {
  ListIterator tmp(*this);
  if (tmp.itr == nullptr) {
    return ListIterator(*this);
  }
  while (tmp.itr->pNext != nullptr) {
    ++tmp;
  }
  return tmp;
}

template <typename T>
typename list<T>::iterator list<T>::insert(ListIterator pos, const T &value) {
  if (pos.itr == pos.end) {
    push_back(value);
  } else if (pos.itr == pos.first) {
    push_front(value);
  } else {
    node *element = new node;
    element->data = pos.itr->data;
    pos.itr->data = value;
    element->pPrev = pos.itr;
    element->pNext = pos.itr->pNext;
    pos.itr->pNext->pPrev = element;
    pos.itr->pNext = element;
    size_++;
  }
  if (pos.itr != nullptr) {
    pos++;
  }
  return pos;
}

template <typename T>
typename list<T>::iterator list<T>::insert(ListConstIterator pos, node *node_) {
  iterator result = begin();
  for (; result.itr != pos.A.itr; ++result) {
  }

  if (result.first == result.end) {
    head_ = node_;
    back_ = node_;
    size_++;
  } else if (result.itr == result.first) {
    head_ = node_;
    node_->pNext = result.itr;
    result.itr->pPrev = node_;
    size_++;
  } else if (result.itr == result.end) {
    result.itr->pNext = node_;
    node_->pPrev = result.itr;
    size_++;
    back_ = node_;
  } else {
    node_->pPrev = result.itr->pPrev;
    node_->pNext = result.itr;
    result.itr->pPrev->pNext = node_;
    result.itr->pPrev = node_;
    size_++;
  }
  return result;
}

// BONUS

template <typename T>
template <typename... Args>
typename list<T>::iterator list<T>::insert_many(ListConstIterator pos,
                                                Args &&...args) {
  node *new_node = new node;
  std::allocator_traits<std::allocator<node>>::construct(
      _allocator, &new_node->data, std::forward<Args>(args)...);
  insert(pos, new_node);
  return pos;
}

template <typename T>
template <typename... Args>
void list<T>::insert_many_back(Args &&...args) {
  for (const auto &arg : {args...}) {
    push_back(arg);
  }
}

template <typename T>
template <typename... Args>
void list<T>::insert_many_front(Args &&...args) {
  for (const auto &arg : {args...}) {
    push_front(arg);
  }
}

}  // namespace s21
