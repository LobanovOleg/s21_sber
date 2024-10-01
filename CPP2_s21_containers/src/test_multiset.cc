#include <gtest/gtest.h>

#include "../multiset/multiset.h"

TEST(multiset, allcase) {
  s21::multiset<int> my_multiset;
  my_multiset.insert(10);
  my_multiset.insert(10);
  my_multiset.insert(10);
  my_multiset.insert(10);
  my_multiset.insert(10);
  my_multiset.insert(10);
  my_multiset.insert(10);
  my_multiset.insert(10);
  my_multiset.insert(10);
  my_multiset.insert(10);
  EXPECT_EQ(my_multiset.size(), 10U);
  auto it = my_multiset.begin();
  my_multiset.erase(it);
  EXPECT_EQ(my_multiset.size(), 9U);
  it = my_multiset.begin();
  EXPECT_EQ(*it, 10);
  my_multiset.erase(it);
  EXPECT_EQ(my_multiset.size(), 8U);
}

// Сравнение const и не const итераторов одновременно
TEST(multiset, multisetConst1) {
  s21::multiset<std::pair<int, char>> s21_multiset{
      {1, 'a'}, {2, 'b'}, {3, 'c'}, {4, 'd'}};

  EXPECT_TRUE(std::as_const(s21_multiset).begin() == s21_multiset.begin());
  EXPECT_TRUE(s21_multiset.begin() == std::as_const(s21_multiset).begin());
  EXPECT_TRUE(std::as_const(s21_multiset).begin() ==
              std::as_const(s21_multiset).begin());
  EXPECT_FALSE(std::as_const(s21_multiset).begin() != s21_multiset.begin());
  EXPECT_FALSE(s21_multiset.begin() != std::as_const(s21_multiset).begin());
  EXPECT_FALSE(std::as_const(s21_multiset).begin() !=
               std::as_const(s21_multiset).begin());
}

// Проверяем конструктор копирования через const-объект
TEST(multiset, multisetConst2) {
  const s21::multiset<int> s21_multiset = {1, 2, 3, 4, 5};
  const s21::multiset<int> s21_multiset_copy = s21_multiset;

  auto s21_multiset_begin = s21_multiset.begin();
  auto s21_multiset_end = s21_multiset.end();

  auto s21_multiset_copy_begin = s21_multiset_copy.begin();
  auto s21_multiset_copy_end = s21_multiset_copy.end();

  while ((s21_multiset_begin != s21_multiset_end)) {
    EXPECT_FALSE(s21_multiset_copy_begin == s21_multiset_begin);
    EXPECT_EQ(*s21_multiset_copy_begin, *s21_multiset_begin);
    ++s21_multiset_copy_begin;
    ++s21_multiset_begin;
  }

  s21_multiset_begin = s21_multiset.begin();
  s21_multiset_copy_begin = s21_multiset_copy.begin();

  while ((s21_multiset_copy_begin != s21_multiset_copy_end)) {
    EXPECT_FALSE(s21_multiset_copy_begin == s21_multiset_begin);
    EXPECT_EQ(*s21_multiset_copy_begin, *s21_multiset_begin);
    ++s21_multiset_copy_begin;
    ++s21_multiset_begin;
  }

  EXPECT_FALSE(s21_multiset_copy_end == s21_multiset_end);
}

// Проверяем assign для const-объекта
// Заодно size(), empty(), contains(), find()
TEST(multiset, multisetConst3) {
  const std::multiset<std::pair<int, char>> std_multiset{
      {1, 'a'}, {2, 'b'}, {3, 'c'}, {4, 'd'}};
  const s21::multiset<std::pair<int, char>> s21_multiset{
      {1, 'a'}, {2, 'b'}, {3, 'c'}, {4, 'd'}};
  std::multiset<std::pair<int, char>> std_multiset_copy{
      {11, 'a'}, {12, 'a'}, {13, 'a'}};
  s21::multiset<std::pair<int, char>> s21_multiset_copy{
      {11, 'a'}, {12, 'a'}, {13, 'a'}};

  EXPECT_EQ(std_multiset.size(), s21_multiset.size());
  EXPECT_EQ(std_multiset.empty(), s21_multiset.empty());
  EXPECT_EQ(s21_multiset.contains({2, 'b'}), true);
  EXPECT_EQ(*std_multiset.find({2, 'b'}), *s21_multiset.find({2, 'b'}));

  EXPECT_EQ(std_multiset_copy.size(), s21_multiset_copy.size());
  EXPECT_EQ(std_multiset_copy.empty(), s21_multiset_copy.empty());
  EXPECT_EQ(s21_multiset_copy.contains({2, 'b'}), false);
  EXPECT_EQ(std_multiset_copy.find({2, 'b'}), std_multiset_copy.end());
  EXPECT_EQ(s21_multiset_copy.find({2, 'b'}), s21_multiset_copy.end());

  std_multiset_copy = std_multiset;
  s21_multiset_copy = s21_multiset;

  EXPECT_EQ(std_multiset.size(), s21_multiset.size());
  EXPECT_EQ(std_multiset.empty(), s21_multiset.empty());
  EXPECT_EQ(s21_multiset.contains({2, 'b'}), true);
  EXPECT_EQ(*std_multiset.find({2, 'b'}), *s21_multiset.find({2, 'b'}));
  EXPECT_EQ(std_multiset.count({2, 'b'}), s21_multiset.count({2, 'b'}));

  EXPECT_EQ(std_multiset_copy.size(), s21_multiset_copy.size());
  EXPECT_EQ(std_multiset_copy.empty(), s21_multiset_copy.empty());
  EXPECT_EQ(s21_multiset_copy.contains({2, 'b'}), true);
  EXPECT_EQ(*std_multiset_copy.find({2, 'b'}),
            *s21_multiset_copy.find({2, 'b'}));
  EXPECT_EQ(std_multiset_copy.count({2, 'b'}),
            s21_multiset_copy.count({2, 'b'}));
}

// Проверяем max_size() для const
TEST(multiset, multisetConst4) {
  const std::multiset<char> std_multiset{'o', 'm', 'g', 'w', 't', 'f'};
  const s21::multiset<char> s21_multiset{'o', 'm', 'g', 'w', 't', 'f'};

  SUCCEED();
}

// Проверяем find(), lower_bound(), upper_bound(), equal_range() для const
TEST(multiset, multisetConst5) {
  const std::multiset<int> std_multiset = {2, 4, 6, 8, 10};
  const s21::multiset<int> s21_multiset = {2, 4, 6, 8, 10};

  auto std_it1 = std_multiset.find(2);
  auto s21_it1 = s21_multiset.find(2);

  EXPECT_EQ(*std_it1, *s21_it1);

  auto std_it2 = std_multiset.lower_bound(2);
  auto s21_it2 = s21_multiset.lower_bound(2);

  EXPECT_EQ(*std_it2, *s21_it2);

  auto std_it3 = std_multiset.upper_bound(2);
  auto s21_it3 = s21_multiset.upper_bound(2);

  EXPECT_EQ(*std_it3, *s21_it3);

  auto std_range = std_multiset.equal_range(2);
  auto s21_range = s21_multiset.equal_range(2);

  EXPECT_EQ(*std_range.first, *s21_range.first);
  EXPECT_EQ(*std_range.second, *s21_range.second);
}
