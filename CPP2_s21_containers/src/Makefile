CC = g++
CFLAGS = -Wall -Werror -Wextra -lstdc++ -lm -fprofile-arcs -ftest-coverage -std=c++20
TEST_FLAGS = -lgtest -pthread
TEST_TARGET = test_elf
TEST_FILES := $(addprefix ./tests/,\
	main_test.cc\
	test_map.cc\
	test_set.cc\
	test_queue.cc\
	test_multiset.cc\
	test_array.cc\
	test_vector.cc\
	test_stack.cc\
	test_list.cc\
	)

all: test clean

build:
	$(CC) $(CFLAGS) $(TEST_FILES) $(TEST_FLAGS) -o $(TEST_TARGET)

test: build
	./$(TEST_TARGET)

gdb:
	$(CC) -g $(CFLAGS) $(TEST_FILES) $(TEST_FLAGS) -o $(TEST_TARGET)
	gdb ./$(TEST_TARGET)

clean:
	@echo "Deleting unnecessary files..."
	@rm -rf *.o *.a *.out *.log *.gcno *.gcda $(TEST_TARGET)

leaks: clean
	@$(CC) $(CFLAGS) tests/*.cc $(TEST_FLAGS) -o $(TEST_TARGET)
	leaks --atExit -- ./$(TEST_TARGET)

valgrind: clean build
	@CK_FORK=no valgrind --vgdb=no --leak-check=full \
	--show-leak-kinds=all --track-origins=yes --log-file="valgrind.log" -v --verbose -q --quiet -s ./$(TEST_TARGET)
	# valgrind --leak-check=full ./$(TEST_TARGET)

check_style:
	@echo "┏=========================================┓"
	@echo "┃  Checking your code for Google Style    ┃"
	@echo "┗=========================================┛"
	@find . \( -name '*.h' -o -name '*.cpp' -o -name '*.cc' -o -name '*.inc' \) -print0 | xargs -0 clang-format -n -style=Google

format_style:
	@echo "┏=========================================┓"
	@echo "┃  Formatting your code for Google Style  ┃"
	@echo "┗=========================================┛"
	@find . \( -name '*.h' -o -name '*.cpp' -o -name '*.cc' -o -name '*.inc' \) -print0 | xargs -0 clang-format -i -style=Google

style: check_style format_style
