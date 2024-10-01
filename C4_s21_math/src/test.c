#include <math.h>

#include <check.h>
#include "s21_math.h"

START_TEST(test_fmod_1) {
    ck_assert_double_nan(fmod(1, 0));
    ck_assert_double_nan(s21_fmod(1, 0));
    ck_assert_double_eq(fmod(0, -1), s21_fmod(0, -1));
    ck_assert_double_eq(fmod(0, 1), s21_fmod(0, 1));
    ck_assert_double_nan(fmod(S21_INFINITY, -1));
    ck_assert_double_nan(s21_fmod(S21_INFINITY, -1));
    ck_assert_double_eq(fmod(-1, S21_INFINITY), s21_fmod(-1, S21_INFINITY));
    ck_assert_double_eq(fmod(0, S21_INFINITY), s21_fmod(0, S21_INFINITY));
    ck_assert_double_nan(s21_fmod(0, S21_NAN));
    ck_assert_double_nan(fmod(0, NAN));
    ck_assert_double_nan(s21_fmod(S21_NAN, S21_NAN));
    ck_assert_double_nan(fmod(NAN, NAN));
    ck_assert_double_nan(s21_fmod(S21_NAN, S21_INFINITY));
    ck_assert_double_nan(s21_fmod(S21_INFINITY, S21_NAN));
    ck_assert_double_nan(s21_fmod(S21_NAN, -S21_INFINITY));
    ck_assert_double_nan(s21_fmod(-S21_INFINITY, S21_NAN));
    ck_assert_double_nan(fmod(NAN, INFINITY));
    ck_assert_double_nan(fmod(INFINITY, NAN));
    ck_assert_double_nan(fmod(NAN, -INFINITY));
    ck_assert_double_nan(fmod(-INFINITY, NAN));
}
END_TEST

START_TEST(test_fmod_2) {
    for (int i = -2300; i < 2000; i += 134) {
        for (int j = -12; j < 12; j += 1.38) {
            ck_assert_double_eq(fmod(j, i), s21_fmod(j, i));
        }
    }
}
END_TEST

Suite *s21_string_suite(void){
    Suite *suite;

    suite = suite_create("s21_math");
    TCase *tcase_core = tcase_create("Core");

    tcase_add_test(tcase_core, test_fmod_1);
    tcase_add_test(tcase_core, test_fmod_2);

    suite_add_tcase(suite, tcase_core);

    return suite;
}

int main() {
    Suite *suite = s21_string_suite();
    SRunner *suite_runner = srunner_create(suite);
    srunner_run_all(suite_runner, CK_VERBOSE);
    int failed_count = srunner_ntests_failed(suite_runner);
    srunner_free(suite_runner);
    return (failed_count == 0) ? EXIT_SUCCESS : EXIT_FAILURE;
}