import random
import json
from typing import Dict, Any, List, Tuple
from utils.logger import setup_logger

class MathGameGenerator:
    """数字游戏生成器"""
    
    def __init__(self):
        self.logger = setup_logger("math_game_generator")
    
    def generate_math_problems(self, operation: str, difficulty: str, count: int = 10) -> List[Dict[str, Any]]:
        """生成数学题目"""
        problems = []
        
        # 根据难度设置数字范围
        if difficulty == "简单":
            num_range = (1, 10)
        elif difficulty == "中等":
            num_range = (1, 50)
        else:  # 困难
            num_range = (1, 100)
        
        for i in range(count):
            if operation == "加法":
                problem = self._generate_addition_problem(num_range)
            elif operation == "减法":
                problem = self._generate_subtraction_problem(num_range)
            elif operation == "乘法":
                problem = self._generate_multiplication_problem(num_range)
            elif operation == "除法":
                problem = self._generate_division_problem(num_range)
            else:  # 混合运算
                problem = self._generate_mixed_problem(num_range)
            
            problems.append(problem)
        
        return problems
    
    def _generate_addition_problem(self, num_range: Tuple[int, int]) -> Dict[str, Any]:
        """生成加法题目"""
        a = random.randint(num_range[0], num_range[1])
        b = random.randint(num_range[0], num_range[1])
        answer = a + b
        
        return {
            'type': 'addition',
            'question': f"{a} + {b} = ?",
            'answer': answer,
            'options': self._generate_options(answer, num_range)
        }
    
    def _generate_subtraction_problem(self, num_range: Tuple[int, int]) -> Dict[str, Any]:
        """生成减法题目"""
        a = random.randint(num_range[0], num_range[1])
        b = random.randint(num_range[0], min(a, num_range[1]))
        answer = a - b
        
        return {
            'type': 'subtraction',
            'question': f"{a} - {b} = ?",
            'answer': answer,
            'options': self._generate_options(answer, num_range)
        }
    
    def _generate_multiplication_problem(self, num_range: Tuple[int, int]) -> Dict[str, Any]:
        """生成乘法题目"""
        # 乘法使用较小的数字范围
        mult_range = (1, min(num_range[1], 12))
        a = random.randint(mult_range[0], mult_range[1])
        b = random.randint(mult_range[0], mult_range[1])
        answer = a * b
        
        return {
            'type': 'multiplication',
            'question': f"{a} × {b} = ?",
            'answer': answer,
            'options': self._generate_options(answer, mult_range)
        }
    
    def _generate_division_problem(self, num_range: Tuple[int, int]) -> Dict[str, Any]:
        """生成除法题目"""
        # 除法使用较小的数字范围
        div_range = (1, min(num_range[1], 12))
        b = random.randint(div_range[0], div_range[1])
        answer = random.randint(div_range[0], div_range[1])
        a = b * answer
        
        return {
            'type': 'division',
            'question': f"{a} ÷ {b} = ?",
            'answer': answer,
            'options': self._generate_options(answer, div_range)
        }
    
    def _generate_mixed_problem(self, num_range: Tuple[int, int]) -> Dict[str, Any]:
        """生成混合运算题目"""
        operations = ['+', '-', '×']
        operation = random.choice(operations)
        
        if operation == '+':
            return self._generate_addition_problem(num_range)
        elif operation == '-':
            return self._generate_subtraction_problem(num_range)
        else:
            return self._generate_multiplication_problem(num_range)
    
    def _generate_options(self, correct_answer: int, num_range: Tuple[int, int]) -> List[int]:
        """生成选项"""
        options = [correct_answer]
        
        # 生成3个错误选项
        for _ in range(3):
            while True:
                # 生成接近正确答案的错误选项
                offset = random.randint(-10, 10)
                wrong_answer = correct_answer + offset
                
                # 确保错误选项在合理范围内且不重复
                if wrong_answer > 0 and wrong_answer not in options:
                    options.append(wrong_answer)
                    break
        
        # 打乱选项顺序
        random.shuffle(options)
        return options
    
    def create_math_game(self, title: str, operation: str, difficulty: str, age_group: str) -> Dict[str, Any]:
        """创建数字游戏"""
        game_data = {
            'title': title,
            'type': 'math',
            'operation': operation,
            'difficulty': difficulty,
            'age_group': age_group,
            'problems': self.generate_math_problems(operation, difficulty),
            'game_config': {
                'time_limit': 300,  # 5分钟
                'pass_score': 70,   # 70分及格
                'hints': 3,         # 3次提示机会
                'lives': 3          # 3条生命
            }
        }
        
        return game_data
    
    def generate_game_instructions(self, game_data: Dict[str, Any]) -> str:
        """生成游戏说明"""
        instructions = f"""
# {game_data['title']}

## 游戏说明
这是一个适合{game_data['age_group']}的{game_data['operation']}游戏。

## 游戏规则
1. 系统会显示{game_data['operation']}题目
2. 从四个选项中选择正确答案
3. 答对得10分，答错不得分
4. 游戏时间限制为{game_data['game_config']['time_limit']//60}分钟
5. 达到{game_data['game_config']['pass_score']}分即可过关

## 操作说明
- 点击选项选择答案
- 使用提示按钮可以获得帮助
- 生命值归零游戏结束

## 学习目标
通过游戏化的方式练习{game_data['operation']}，提高数学计算能力。
"""
        return instructions