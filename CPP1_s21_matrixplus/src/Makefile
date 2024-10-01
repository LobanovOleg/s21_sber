CC = g++ -std=c++17
CGLAGS = -Wall -Wextra -Werror
TST = -lgtest -pthread

all: clean s21_matrix_oop.a

s21_matrix_oop.a: clean
	@echo "┏============================┓"
	@echo "     Making lybrary ...		"
	@echo "┗============================┛"

	@$(CC) $(CGLAGS) -c s21_matrix_oop.cpp -o s21_matrix_oop.o
	@ar rc s21_matrix_oop.a s21_matrix_oop.o
	@ranlib s21_matrix_oop.a

test: clean s21_matrix_oop.a
	@$(CC) test.cpp s21_matrix_oop.a $(TST) -o test
	@echo "┏====================┓"
	@echo "     Making test    "
	@echo "┗====================┛"

	@./test

check_style:
	@echo "┏========================┓"
	@echo "     Checking style     "
	@echo "┗========================┛"

	@clang-format -n s21_matrix_oop.cpp

change_style:
	@echo "┏=======================┓"
	@echo "     Changing style    "
	@echo "┗=======================┛"

	@clang-format -i s21_matrix_oop.cpp

clean:
	@rm -rf *.o
	@rm -rf *.a
	@rm -rf *.gc*
	@rm -rf *.gd*
	@rm -rf test
	@rm -rf test_html
