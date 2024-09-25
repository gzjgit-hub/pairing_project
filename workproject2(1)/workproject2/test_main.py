import unittest
from main import *

class TestArithmeticGenerator(unittest.TestCase):
    
    # 测试生成随机数的功能（加入边界测试）
    def test_create_random_number(self):
        # 正常范围测试
        for _ in range(100):
            number = create_random_number(10)
            self.assertTrue(0 <= number < 10)
        
        # 边界测试：数值范围为0或1
        with self.assertRaises(ValueError):
            create_random_number(0)  # 处理范围为0的情况
        self.assertTrue(0 <= create_random_number(1) <= 1)  # 范围为1时只能生成0或1

    # 测试生成的表达式是否有重复
    def test_create_arithmetic_expression_uniqueness(self):
        value_limit = 10
        num_expressions = 1000
        generated_expressions = set()
        for _ in range(num_expressions):
            expression, _ = create_arithmetic_expression(value_limit)
            # 检查是否有重复表达式
            self.assertNotIn(expression, generated_expressions, f"发现重复表达式: {expression}")
            generated_expressions.add(expression)
    
    # 测试将小数转换为分数
    def test_convert_decimal_to_fraction(self):
        decimal_values = [0.25, 0.5, 0.75, 1.2, 2.5]
        expected_fractions = [Fraction(1, 4), Fraction(1, 2), Fraction(3, 4), Fraction(6, 5), Fraction(5, 2)]
        for decimal, expected in zip(decimal_values, expected_fractions):
            result = convert_decimal_to_fraction(decimal)
            self.assertEqual(result, expected)

    # 测试将假分数转换为带分数
    def test_convert_improper_fraction(self):
        test_cases = {
            '5/3': '1‘2/3',
            '34/11': '3‘1/11',
            '59/8': '7‘3/8',
            '2612/315': '8‘92/315',
            '383/40': '9‘23/40'
        }
        for improper, expected in test_cases.items():
            result = convert_improper_fraction(improper)
            self.assertEqual(result, expected)
    
    # 测试为表达式中的所有数加括号
    def test_wrap_with_parentheses(self):
        test_cases = {
            "1 - 0 ÷ 4/5 - 3/7": "(1 )-( 0 )÷( 4/5 )-( 3/7)",
            "7 + 2 - 4 ÷ 3/7": "(7 )+( 2 )-( 4 )÷( 3/7)",
            "1/4 ÷ 2 - 6/7": "(1/4 )÷( 2 )-( 6/7)",
            "4/5 × 6 + 1/3": "(4/5 )×( 6 )+( 1/3)",
            "2 × 5/8": "(2 )×( 5/8)"
        }
        for expression, expected in test_cases.items():
            result = wrap_with_parentheses(expression)
            self.assertEqual(result, expected)
    
    # 测试统计题目正确率的函数
    def test_evaluate_answers(self):
        correct_indices, wrong_indices = evaluate_answers("test_Exercises.txt", "test_Answers.txt")
        self.assertEqual(len(correct_indices), 100)
        self.assertEqual(len(wrong_indices), 0)
    
    # 测试文件路径不存在的情况
    def test_invalid_file_paths(self):
        self.assertEqual(evaluate_answers('不存在的文件.txt', '不存在的文件.txt'), FileNotFoundError)
    
    # 测试生成表达式是否合法（包括除以零的边界情况）
    def test_create_arithmetic_expression(self):
        for _ in range(100):
            expression, expression_with_paren = create_arithmetic_expression(10)
            try:
                result = eval(expression_with_paren.replace('÷', '/').replace('×', '*'))
                self.assertIsInstance(result, (int, float))
            except ZeroDivisionError:
                self.fail("生成了包含除以零的表达式")
    
    # 边界测试：极大数值范围
    def test_large_value_limit(self):
        value_limit = 10**6  # 设置极大范围
        for _ in range(10):
            expression, expression_with_paren = create_arithmetic_expression(value_limit)
            try:
                result = eval(expression_with_paren.replace('÷', '/').replace('×', '*'))
                self.assertIsInstance(result, (int, float))
            except ZeroDivisionError:
                self.fail("生成了包含除以零的表达式")
    
    # 边界测试：避免负数结果
    def test_no_negative_result(self):
        for _ in range(100):
            expression, expression_with_paren = create_arithmetic_expression(10)
            result = eval(expression_with_paren.replace('÷', '/').replace('×', '*'))
            self.assertGreaterEqual(result, 0, "生成了负数结果的表达式")

if __name__ == "__main__":
    unittest.main()

