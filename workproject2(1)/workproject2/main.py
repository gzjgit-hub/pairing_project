import math
import random
from fractions import Fraction

# 定义四则运算符
operation_symbols = ['+', '-', '×', '÷']

# 生成一个随机数，可能是自然数或真分数
def create_random_number(value_limit):
    if random.random() < 0.5:  # 50% 的概率生成真分数
        numer = random.randint(0, value_limit - 1)
        denom = random.randint(numer + 1, value_limit)
        return Fraction(numer, denom)
    else:  # 50% 的概率生成自然数
        return random.randint(0, value_limit - 1)

# 用集合来存储已生成的表达式，防止重复
expression_history = set()

# 确保除法结果为真分数
def ensure_proper_division(value_limit, dividend, divisor):
    while divisor == 0 or dividend % divisor != 0:
        dividend = create_random_number(value_limit)
        divisor = create_random_number(value_limit)
    return dividend, divisor

# 生成包含一个运算符的简单表达式
def create_single_operation_expression(value_limit):
    operand1 = create_random_number(value_limit)
    operand2 = create_random_number(value_limit)
    operator = random.choice(operation_symbols)
    
    # 如果是除法，确保结果为真分数
    if operator == '÷':
        operand1, operand2 = ensure_proper_division(value_limit, operand1, operand2)
    
    # 确保表达式不会出现0作为第一个操作数
    while operand1 == 0:
        operand1 = create_random_number(value_limit)
    
    # 防止交换律导致生成相同的表达式
    if operator in ('+', '×'):
        operand1, operand2 = min(operand1, operand2), max(operand1, operand2)
        if math.floor(operand2) == 0:
            operand2 = random.randint(1, value_limit)
        if min(operand1, operand2) == 0:
            operand1 = random.randint(1, math.floor(operand2))
    
    # 确保不会生成负数结果
    if operator == '-':
        operand1, operand2 = max(operand1, operand2), min(operand1, operand2)

    # 表达式的两种不同格式
    expr = f"{operand1} {operator} {operand2}"
    expr_with_paren = f"({operand1}) {operator} ({operand2})"

    return expr, expr_with_paren

# 生成包含两个运算符的表达式
def create_two_operation_expression(value_limit):
    operand3 = create_random_number(value_limit)
    operators_set = ['+', '-']
    second_operator = random.choice(operators_set)
    
    first_expr, first_expr_with_paren = create_single_operation_expression(value_limit)

    # 避免负数结果
    if second_operator == '-':
        while eval(first_expr_with_paren.replace('÷', '/').replace('×', '*')) < operand3:
            operand3 = create_random_number(value_limit)
    
    expr = f"{first_expr} {second_operator} {operand3}"
    expr_with_paren = f"{first_expr_with_paren} {second_operator} ({operand3})"
    return expr, expr_with_paren

# 生成包含三个运算符的复杂表达式
def create_three_operation_expression(value_limit):
    operators_set_3 = ['+', '×', '÷']
    third_operator = random.choice(operators_set_3)
    
    first_expr, first_expr_with_paren = create_single_operation_expression(value_limit)
    second_expr, second_expr_with_paren = create_single_operation_expression(value_limit)
    
    expr = first_expr + ' ' + third_operator + ' ' + second_expr
    expr_with_paren = first_expr_with_paren + third_operator + second_expr_with_paren

    # 确保没有负数结果
    while eval(expr_with_paren.replace('÷', '/').replace('×', '*')) < 0:
        first_expr, first_expr_with_paren = create_single_operation_expression(value_limit)
        second_expr, second_expr_with_paren = create_single_operation_expression(value_limit)
        expr = first_expr + ' ' + third_operator + ' ' + second_expr
        expr_with_paren = first_expr_with_paren + third_operator + second_expr_with_paren

    return expr, expr_with_paren

# 生成一个随机的表达式（包含1至3个运算符）
def create_arithmetic_expression(value_limit):
    if value_limit < 1:
        raise ValueError("数值范围必须大于等于1")

    while True:
        number_of_operators = random.randint(1, 3)

        if number_of_operators == 1:
            expr, expr_with_paren = create_single_operation_expression(value_limit)
        elif number_of_operators == 2:
            expr, expr_with_paren = create_two_operation_expression(value_limit)
        else:
            expr, expr_with_paren = create_three_operation_expression(value_limit)

        # 确保生成的表达式是唯一的
        if expr not in expression_history:
            expression_history.add(expr)
            return expr, expr_with_paren

# 将计算结果转换为最简分数
def convert_decimal_to_fraction(decimal_val):
    return Fraction(decimal_val).limit_denominator()

# 将假分数转换为带分数
def convert_improper_fraction(fraction_str):
    numer, denom = map(int, fraction_str.split('/'))
    if numer >= denom:
        integer_part = numer // denom
        remainder = numer % denom
        if remainder == 0:
            return str(integer_part)
        else:
            return f"{integer_part}‘{remainder}/{denom}"
    else:
        return fraction_str

# 生成题目和相应的答案
def generate_questions_and_solutions(question_count, value_limit):
    questions = []
    solutions = []
    for _ in range(question_count):
        expr, expr_with_paren = create_arithmetic_expression(value_limit)
        decimal_result = eval(expr_with_paren.replace('÷', '/').replace('×', '*'))
        fraction_result = convert_decimal_to_fraction(decimal_result)

        if isinstance(fraction_result, int) == False and fraction_result % 1 != 0:
            fraction_result = convert_improper_fraction(f"{Fraction(fraction_result).limit_denominator()}")
        
        questions.append(expr)
        solutions.append(fraction_result)
    return questions, solutions

# 将生成的题目和答案保存到文件中，文件名为 Exercises.txt 和 Answers.txt
def save_to_file(questions, solutions):
    with open("Exercises.txt", "w", encoding='utf-8') as exercise_file, open("Answers.txt", "w", encoding='utf-8') as answer_file:
        for i, (q, a) in enumerate(zip(questions, solutions), start=1):
            exercise_file.write(f"四则运算题目{i}：  {q}\n")
            answer_file.write(f"答案{i}：  {a}\n")

# 为所有数加上括号，确保正确的运算顺序
def wrap_with_parentheses(expr_str):
    tokens = []
    num_str = ''
    for char in expr_str:
        if char in '+-×÷':
            tokens.append(num_str)
            tokens.append(char)
            num_str = ''
        else:
            num_str += char
    tokens.append(num_str)
    
    result_expr = ''
    for i, token in enumerate(tokens):
        if token in '+-×÷':
            result_expr += token
        else:
            result_expr += '(' + token + ')'
    
    return result_expr

# 统计题目的正确与错误数量
def evaluate_answers(exercise_file, solution_file):
    correct_answers = []
    incorrect_answers = []

    try:
        with open(exercise_file, "r", encoding='utf-8') as q_file, open(solution_file, "r", encoding='utf-8') as s_file:
            for i, (q_line, s_line) in enumerate(zip(q_file, s_file), start=1):
                q_line = q_line.strip()
                s_line = s_line.strip()

                if q_line.startswith("四则运算题目"):
                    q_parts = q_line.split("：", 1)
                    if len(q_parts) == 2:
                        q_line = q_parts[1].strip()

                if s_line.startswith("答案"):
                    s_parts = s_line.split("：", 1)
                    if len(s_parts) == 2:
                        s_line = s_parts[1].strip()

                try:
                    user_solution = eval(s_line.replace('‘', '+'))
                    user_solution = Fraction(user_solution).limit_denominator()
                    correct_solution = eval(wrap_with_parentheses(q_line).replace('÷', '/').replace('×', '*'))
                    correct_solution = Fraction(correct_solution).limit_denominator()

                    if user_solution == correct_solution:
                        correct_answers.append(i)
                    else:
                        incorrect_answers.append(i)
                except Exception as err:
                    print(f"评估第 {i} 题时发生错误：{err}")

        return correct_answers, incorrect_answers
    except FileNotFoundError:
        print("未找到文件")
        return FileNotFoundError

# 将评分结果保存到文件，文件名为 Grade.txt，按照指定格式
def save_evaluation_results(correct_answers, incorrect_answers):
    with open("Grade.txt", "w") as results_file:
        results_file.write(f"Correct: {len(correct_answers)} ({', '.join(map(str, correct_answers))})\n")
        results_file.write(f"Wrong: {len(incorrect_answers)} ({', '.join(map(str, incorrect_answers))})\n")

if __name__ == "__main__":

    # 改进的功能菜单，增加独特性
    print("欢迎使用智能算术题生成与评估系统")
    print("请选择功能：\n1. 生成算术题\n2. 统计答题正确率\n")

    user_choice = int(input("请输入对应的数字进行选择："))

    if user_choice == 1:
        question_count = int(input("请输入需要生成的题目数量："))
        value_range = int(input("请输入数值范围："))
        questions, solutions = generate_questions_and_solutions(question_count, value_range)
        save_to_file(questions, solutions)
        print(f"已生成 {question_count} 道题目，并保存至 Exercises.txt 和 Answers.txt 文件中")

    elif user_choice == 2:
        exercise_filename = input("请输入题目文件名（例如 Exercises.txt）：")
        answer_filename = input("请输入答案文件名（例如 Answers.txt）：")
        correct_answers, incorrect_answers = evaluate_answers(exercise_filename, answer_filename)
        save_evaluation_results(correct_answers, incorrect_answers)
        print("答题统计已保存至 Grade.txt 文件中")












