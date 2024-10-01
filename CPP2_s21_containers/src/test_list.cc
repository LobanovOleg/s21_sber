#include <list>

#include "main_test.h"

TEST(List, Default_Constructor) {
  s21::list<int> our;
  std::list<int> std;
  ASSERT_EQ(our.empty(), std.empty());
}

TEST(List, Size_Constructor) {
  s21::list<int> our(5);
  ASSERT_EQ(our.size(), 5);
}

TEST(List, Init_Constructor) {
  s21::list<int> our{1, 2, 3};
  ASSERT_FALSE(our.empty());
  ASSERT_EQ(our.front(), 1);
  our.clear();
  ASSERT_TRUE(our.empty());
}

TEST(List, Init_String_Constructor) {
  s21::list<std::string> our{"hello", "world"};
  ASSERT_EQ(our.front(), "hello");
  ASSERT_EQ(our.back(), "world");
}

TEST(List, Copy_Constructor) {
  s21::list<int> our{3, 2, 1};
  s21::list<int> ourCopied(our);
  ASSERT_EQ(our.front(), ourCopied.front());
}

TEST(List, Move_Constructor) {
  s21::list<int> our{1, 2, 3};
  s21::list<int> ourMoved(std::move(our));
  ASSERT_TRUE(our.empty());
  ASSERT_FALSE(ourMoved.empty());
}

TEST(List, Move_Operator_Constructor) {
  s21::list<int> our{1, 2, 3};
  s21::list<int> ourMoved;
  ourMoved = std::move(our);
  ASSERT_TRUE(our.empty());
  ASSERT_FALSE(ourMoved.empty());
}

TEST(List, Size) {
  s21::list<int> our{1, 2, 3};
  std::list<int> std{1, 2, 3};
  EXPECT_EQ(our.size(), std.size());
}

TEST(List, Push_Int) {
  s21::list<int> our;
  our.push_front(99);
  our.push_back(123);
  std::list<int> std;
  std.push_front(99);
  std.push_back(123);
  ASSERT_EQ(our.front(), std.front());
  ASSERT_EQ(our.back(), std.back());
}

TEST(List, Pop_Int) {
  s21::list<int> our{566, 123};
  std::list<int> std;
  std.push_back(566);
  std.push_back(123);
  ASSERT_EQ(our.front(), std.front());
  ASSERT_EQ(our.back(), std.back());
  our.pop_back();
  std.pop_back();
  ASSERT_EQ(our.front(), std.front());
  ASSERT_EQ(our.back(), std.back());
  our.pop_front();
  std.pop_front();
  ASSERT_EQ(our.empty(), std.empty());
}

TEST(List, Pop_String) {
  s21::list<std::string> our{"hello", "world"};
  std::list<std::string> std;
  std.push_back("hello");
  std.push_back("world");
  ASSERT_EQ(our.front(), std.front());
  ASSERT_EQ(our.back(), std.back());
  our.pop_back();
  std.pop_back();
  ASSERT_EQ(our.front(), std.front());
  ASSERT_EQ(our.back(), std.back());
}

TEST(List, Size_Swap) {
  s21::list<int> our{566, 123, 3, 3, 2, 1};
  s21::list<int> our2{566, 123};
  ASSERT_EQ(our.size(), 6);
  ASSERT_EQ(our2.size(), 2);
  our.swap(our2);
  ASSERT_EQ(our.size(), 2);
  ASSERT_EQ(our2.size(), 6);
}

TEST(List, Erase_1) {
  s21::list<int> our{566, 123, 3, 3, 2, 1};
  our.erase(our.begin());
  our.erase(our.end());
  s21::list<int>::ListIterator s21it = our.begin();
  ASSERT_EQ(*s21it, 123);
  s21::list<int>::ListIterator s21it_ = our.end();
  ASSERT_EQ(*s21it_, 2);
}

TEST(List, Erase_2) {
  s21::list<int> our{566, 123, 3, 3, 2, 1};
  s21::list<int> check{566, 3, 3, 2, 1};

  s21::list<int>::ListIterator s21it = our.begin();
  s21it++;
  our.erase(s21it);

  s21::list<int>::ListIterator s21it_ = our.begin();
  s21::list<int>::ListIterator check_ = check.begin();

  while (s21it_.itr) {
    ASSERT_TRUE(*(s21it_++) <= *(check_++));
  }
}

TEST(List, Insert_Int_1) {
  s21::list<int> our{566, 123};
  std::list<int> std{44, 55};
  s21::list<int>::ListIterator s21it;
  s21it = our.begin();
  std::list<int>::iterator stdit = std.begin();
  our.insert(s21it, 77);
  std.insert(stdit, 77);
  ASSERT_EQ(our.front(), std.front());
  ++s21it;
  our.insert(s21it, 99);
  our.erase(s21it);
  ASSERT_EQ(our.size(), 3);
}

TEST(List, Insert_Int_2) {
  s21::list<int> our{566, 123, 18};
  s21::list<int> check{566, 77, 123, 18};
  s21::list<int>::ListIterator s21it;
  s21it = our.begin();
  s21it++;
  our.insert(s21it, 77);
  s21it = our.begin();
  s21::list<int>::ListIterator s21it_ = check.begin();
  while (s21it_.itr) {
    ASSERT_TRUE(*(s21it++) <= *(s21it_++));
  }
}

TEST(List, Sort) {
  s21::list<int> our{3, 5, 1, 4, 6, 2};
  std::list<int> std{3, 5, 1, 4, 6, 2};
  std::list<int> sortedlist{1, 2, 3, 4, 5, 6};
  our.sort();
  std.sort();
  s21::list<int>::ListIterator s21it = our.begin();
  std::list<int>::iterator stdit = std.begin();
  std::list<int>::iterator sortit = sortedlist.begin();
  while (s21it.itr) {
    ASSERT_EQ(*s21it, *stdit);
    ASSERT_EQ(*s21it, *sortit);
    ++s21it;
    ++stdit;
    ++sortit;
  }
}

TEST(List, Iterator_Begin) {
  s21::list<int> our{1, 2, 3};
  std::list<int> std{1, 2, 3};
  s21::list<int>::ListIterator our_it;
  our_it = our.begin();
  std::list<int>::iterator std_it;
  std_it = std.begin();
  EXPECT_EQ(*our_it, *std_it);
}

TEST(List, Iterator_End) {
  s21::list<int> our{3, 5, 1, 4, 6, 2};
  s21::list<int>::ListIterator s21it = our.end();
  int area[] = {2, 6, 4, 1, 5, 3};
  int i = 0;
  while (s21it.itr != s21it.first) {
    ASSERT_EQ(*(s21it--), area[i++]);
  }
}

TEST(List, Iterator_Eq) {
  s21::list<int> our{3, 5, 1, 4, 6, 2};
  s21::list<int>::ListIterator begin = our.begin();
  s21::list<int>::ListIterator begin1 = begin;
  s21::list<int>::ListConstIterator cbegin = our.cbegin();
  s21::list<int>::ListConstIterator cbegin1 = cbegin;
  ASSERT_TRUE(begin == begin1);
  ASSERT_FALSE(begin != begin1);
  ASSERT_TRUE(cbegin == cbegin1);
  ASSERT_FALSE(cbegin != cbegin1);
}

TEST(List, Reverse) {
  s21::list<int> our{6, 5, 4, 3, 2, 1};
  std::list<int> std{1, 2, 3, 4, 5, 6};
  our.reverse();
  s21::list<int>::ListConstIterator s21it;
  s21it = our.cbegin();
  std::list<int>::const_iterator stdit = std.cbegin();
  while (s21it.A.itr != s21it.A.end) {
    ASSERT_EQ(*s21it, *stdit);
    ++s21it;
    ++stdit;
  }
}

TEST(List, Unique) {
  s21::list<int> our{1, 1, 1, 1, 2, 2, 3, 3};
  std::list<int> std{1, 2, 3};
  our.unique();
  s21::list<int>::ListIterator s21it = our.begin();
  std::list<int>::iterator stdit = std.begin();
  while (s21it.itr) {
    ASSERT_EQ(*s21it, *stdit);
    ++s21it;
    ++stdit;
  }
}

TEST(List, Splice) {
  s21::list<int> our_1{1};
  s21::list<int> our_2{2, 3, 4, 5};
  std::list<int> std_1{1};
  std::list<int> std_2{2, 3, 4, 5};
  s21::list<int>::ListConstIterator our_it = our_1.cbegin();
  std::list<int>::iterator std_it = std_1.begin();
  our_1.splice(our_it, our_2);
  std_1.splice(std_it, std_2);
  EXPECT_EQ(our_1.front(), std_1.front());
  EXPECT_EQ(our_1.back(), std_1.back());
}

TEST(List, Merge) {
  s21::list<int> our_1{1};
  s21::list<int> our_2{2, 3, 4, 5};
  std::list<int> std_1{1};
  std::list<int> std_2{2, 3, 4, 5};
  our_1.merge(our_2);
  std_1.merge(std_2);
  EXPECT_EQ(our_1.front(), std_1.front());
  EXPECT_EQ(our_1.back(), std_1.back());
}

TEST(List, Insert_Many) {
  s21::list<int> our{1, 2, 3};
  s21::list<int> check{1, 33, 2, 3};
  s21::list<int>::ListConstIterator our_it = our.cbegin();
  ++our_it;
  our.insert_many(our_it, 33);
  s21::list<int>::ListIterator ch_1 = our.begin();
  s21::list<int>::ListIterator ch_2 = check.begin();
  while (ch_1.itr) {
    ASSERT_EQ(*ch_1, *ch_2);
    ++ch_1;
    ++ch_2;
  }
}

TEST(List, Insert_Many_Back) {
  s21::list<int> our{1, 2, 3};
  s21::list<int> check{1, 2, 3, 5};
  our.insert_many_back(5);
  s21::list<int>::ListIterator ch_1 = our.begin();
  s21::list<int>::ListIterator ch_2 = check.begin();
  while (ch_1.itr) {
    ASSERT_EQ(*ch_1, *ch_2);
    ++ch_1;
    ++ch_2;
  }
}

TEST(List, Insert_Many_Front) {
  s21::list<int> our{1, 2, 3};
  s21::list<int> check{10, 1, 2, 3};
  our.insert_many_front(10);
  s21::list<int>::ListIterator ch_1 = our.begin();
  s21::list<int>::ListIterator ch_2 = check.begin();
  while (ch_1.itr) {
    ASSERT_EQ(*ch_1, *ch_2);
    ++ch_1;
    ++ch_2;
  }
}
