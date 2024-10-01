#include "main.h"

class ModelTest : public ::testing::Test {
protected:
    void SetUp() override {}
    s21::SmartCalculModel smart_calcul_;
};

TEST_F(ModelTest, ModelTestEmptyTest) {
    char input_string[] = "";
    EXPECT_ANY_THROW(smart_calcul_.GetStringFromCalculator(input_string));
}

TEST_F(ModelTest, ModelTestPlusTest) {
    char input_string[] = "1+2";
    char input_string_error[] = "1+";
    smart_calcul_.GetStringFromCalculator(input_string);
    ASSERT_EQ(smart_calcul_.get_container_numbers(), 3);
    ASSERT_ANY_THROW(smart_calcul_.GetStringFromCalculator(input_string_error));
}

TEST_F(ModelTest, ModelTestMinusTest) {
    char input_string[] = "1-2";
    char input_string_double[] = "5.3-2.3";
    smart_calcul_.GetStringFromCalculator(input_string);
    ASSERT_EQ(smart_calcul_.get_container_numbers(), -1);
    smart_calcul_.GetStringFromCalculator(input_string_double);
    ASSERT_EQ(smart_calcul_.get_container_numbers(), 3.0);
}

TEST_F(ModelTest, ModelTestMultTest) {
    char input_string[] = "0*(-0.3)";
    char input_string_error[] = "*0*";
    smart_calcul_.GetStringFromCalculator(input_string);
    ASSERT_EQ(smart_calcul_.get_container_numbers(), 0);
    ASSERT_ANY_THROW(smart_calcul_.GetStringFromCalculator(input_string_error));
}

TEST_F(ModelTest, ModelTestDivTest) {
    char input_string[] = "1/0";
    EXPECT_ANY_THROW(smart_calcul_.GetStringFromCalculator(input_string));
}

TEST_F(ModelTest, ModelTestModTest) {
    char input_string[] = "5mod3";
    smart_calcul_.GetStringFromCalculator(input_string);
    ASSERT_EQ(smart_calcul_.get_container_numbers(), 2);
}

TEST_F(ModelTest, ModelTestPowTest) {
    char input_string_zero[] = "0^(-0.3)";
    char input_string[] = "2^(-0.3)";
    ASSERT_ANY_THROW(smart_calcul_.GetStringFromCalculator(input_string_zero));
    smart_calcul_.GetStringFromCalculator(input_string);
    double tmp = pow(2,(-0.3));
    ASSERT_EQ(smart_calcul_.get_container_numbers(), tmp);
}

TEST_F(ModelTest, ModelTestUMinusTest) {
    char input_string[] = "-(8)-5";
    char input_string_middle[] = "8*(-2)";
    smart_calcul_.GetStringFromCalculator(input_string);
    ASSERT_EQ(smart_calcul_.get_container_numbers(), -13);
    smart_calcul_.GetStringFromCalculator(input_string_middle);
    ASSERT_EQ(smart_calcul_.get_container_numbers(), -16);
}

TEST_F(ModelTest, ModelTestCosTest) {
    char input_string[] = "cos(0.3)";
    smart_calcul_.GetStringFromCalculator(input_string);
    ASSERT_EQ(smart_calcul_.get_container_numbers(), std::cos(0.3));
}

TEST_F(ModelTest, ModelTestSinTest) {
    char input_string[] = "sin(1.3)";
    smart_calcul_.GetStringFromCalculator(input_string);
    ASSERT_EQ(smart_calcul_.get_container_numbers(), std::sin(1.3));
}

TEST_F(ModelTest, ModelTestTanTest) {
    char input_string[] = "tan(-1)";
    smart_calcul_.GetStringFromCalculator(input_string);
    ASSERT_EQ(smart_calcul_.get_container_numbers(), std::tan(-1));
}

TEST_F(ModelTest, ModelTestAcosTest) {
    char input_string[] = "acos(0)";
    smart_calcul_.GetStringFromCalculator(input_string);
    ASSERT_EQ(smart_calcul_.get_container_numbers(),std::acos(0));
}

TEST_F(ModelTest, ModelTestAsinTest) {
    char input_string[] = "asin(-1.1)";
    ASSERT_ANY_THROW(smart_calcul_.GetStringFromCalculator(input_string));
}

TEST_F(ModelTest, ModelTestAtanTest) {
    char input_string[] = "atan(0.1)";
    smart_calcul_.GetStringFromCalculator(input_string);
    double tmp = std::atan(0.1);
    ASSERT_EQ(smart_calcul_.get_container_numbers(),tmp);
}

TEST_F(ModelTest, ModelTestSqrtTest) {
    char input_string_error[] = "√(-2)";
    char input_string[] = "√(4)";
    ASSERT_ANY_THROW(smart_calcul_.GetStringFromCalculator(input_string_error));
    smart_calcul_.GetStringFromCalculator(input_string);
    ASSERT_EQ(smart_calcul_.get_container_numbers(), 2);
}

TEST_F(ModelTest, ModelTestLnTest) {
    char input_string[] = "ln(100)";
    char input_string_error[] = "ln(-2)";
    smart_calcul_.GetStringFromCalculator(input_string);
    ASSERT_EQ(smart_calcul_.get_container_numbers(), std::log(100));
    ASSERT_ANY_THROW(smart_calcul_.GetStringFromCalculator(input_string_error));
}

TEST_F(ModelTest, ModelTestLogTest) {
    char input_string[] = "log(1000)";
    char input_string_error[] = "log(0)";
    smart_calcul_.GetStringFromCalculator(input_string);
    ASSERT_EQ(smart_calcul_.get_container_numbers(), std::log10(1000));
    ASSERT_ANY_THROW(smart_calcul_.GetStringFromCalculator(input_string_error));
}

TEST_F(ModelTest, ModelTestLeftBracketTest) {
    char input_string[] = "-3*(((-2)))";
    char input_string_error[] = "(3+";
    smart_calcul_.GetStringFromCalculator(input_string);
    ASSERT_EQ(smart_calcul_.get_container_numbers(), 6);
    ASSERT_ANY_THROW(smart_calcul_.GetStringFromCalculator(input_string_error));
    ASSERT_ANY_THROW(smart_calcul_.GetStringFromCalculator("+3)"));
    ASSERT_ANY_THROW(smart_calcul_.GetStringFromCalculator("(-2)*(2/"));
}

TEST_F(ModelTest, ModelTestRightBracketTest) {
    char input_string[] = "(4*(3))";
    smart_calcul_.GetStringFromCalculator(input_string);
    ASSERT_EQ(smart_calcul_.get_container_numbers(), 12);
}

TEST_F(ModelTest, ModelTestPiETest) {
    char input_string[] = "π+e";
    smart_calcul_.GetStringFromCalculator(input_string);
    ASSERT_EQ(smart_calcul_.get_container_numbers(), M_PI + M_E);
}

TEST_F(ModelTest, ModelTestOnlyPointTest) {
    char input_string[] = ".+2";
    smart_calcul_.GetStringFromCalculator(input_string);
    ASSERT_EQ(smart_calcul_.get_container_numbers(), 2);
}

TEST_F(ModelTest, ModelTestExceptionTest) {
    char input_string_error[] = "sin(0.1)+cos";
    char input_string[] = "2+1";
    char input_string_error_1[] = "cos";
    ASSERT_ANY_THROW(smart_calcul_.GetStringFromCalculator(input_string_error));
    smart_calcul_.GetStringFromCalculator(input_string);
    smart_calcul_.get_container_numbers();
    ASSERT_ANY_THROW(smart_calcul_.get_container_numbers());
    ASSERT_ANY_THROW(smart_calcul_.GetStringFromCalculator(input_string_error_1));
}

TEST_F(ModelTest, ModelTestDoubleUminsTest) {
    char input_string[] = "-(8)-(8)";
    smart_calcul_.GetStringFromCalculator(input_string);
    ASSERT_EQ(smart_calcul_.get_container_numbers(), -16);
}