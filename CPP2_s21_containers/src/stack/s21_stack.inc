namespace s21 {
template <typename T>
stack<T>::stack() noexcept : back_(nullptr), root_(nullptr), size_(0) {}

template <typename T>
stack<T>::stack(std::initializer_list<value_type> const &items)
    : back_(nullptr), root_(nullptr), size_(0) {
  for (auto i : items) {
    this->push(i);
  }
}

template <typename T>
stack<T>::stack(const stack &other) : back_(nullptr), root_(nullptr), size_(0) {
  Node *refresh = other.back_;
  while (refresh != nullptr) {
    push(refresh->data_);
    refresh = refresh->next_;
  }
}

template <typename T>
stack<T>::stack(stack &&other) noexcept
    : back_(other.back_), root_(other.root_), size_(other.size_) {
  other.back_ = nullptr;
  other.root_ = nullptr;
  other.size_ = 0;
}

template <typename T>
stack<T>::~stack() noexcept {
  while (back_ != nullptr) {
    this->pop();
  }
}

template <typename T>
stack<T> &stack<T>::operator=(stack &&other) noexcept {
  root_ = other.root_;
  back_ = other.back_;
  size_ = other.size_;

  other.root_ = nullptr;
  other.back_ = nullptr;
  other.size_ = 0;
  return *this;
}

template <typename T>
stack<T> &stack<T>::operator=(const stack &other) {
  if (this->root_ == other.root_) return *this;
  Node *buffer = other.back_;
  while (buffer != nullptr) {
    push(buffer->data_);
    buffer = buffer->next_;
  }
  return *this;
}

template <typename T>
typename stack<T>::reference stack<T>::top() noexcept {
  return root_->data_;
}

template <typename T>
typename stack<T>::const_reference stack<T>::top() const noexcept {
  return root_->data_;
}

template <typename T>
bool stack<T>::empty() const noexcept {
  return root_ == nullptr;
}

template <typename T>
typename stack<T>::size_type stack<T>::size() const noexcept {
  return size_;
}

template <typename T>
void stack<T>::push(const_reference value) {
  size_++;
  Node *refresh = new Node;
  refresh->data_ = value;
  refresh->next_ = nullptr;
  if (back_ != nullptr) {
    root_->next_ = refresh;
    refresh->prev_ = root_;
  } else {
    back_ = refresh;
    refresh->prev_ = nullptr;
  }
  root_ = refresh;
}

template <typename T>
void stack<T>::pop() {
  if (empty()) {
    throw std::length_error("Стек пуст");
  }
  size_--;
  Node *refresh = root_;
  root_ = root_->prev_;
  delete refresh;
  if (root_ == nullptr) {
    back_ = nullptr;
  } else {
    root_->next_ = nullptr;
  }
}

template <typename T>
void stack<T>::swap(stack &other) noexcept {
  stack buffer = other;
  other = *this;
  *this = buffer;
}

template <typename T>
template <typename... Args>
void stack<T>::insert_many_front(Args &&...args) {
  for (const auto &arg : {args...}) {
    push(arg);
  }
}
}  // namespace s21
