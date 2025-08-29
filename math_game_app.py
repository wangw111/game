#!/usr/bin/env python3
"""
数学游戏应用
使用游戏开发智能体生成的JSON数据创建互动数学游戏
"""

import json
import random
import time
import os
from typing import Dict, List, Any

class MathGameApp:
    """数学游戏应用类"""
    
    def __init__(self, game_data_file: str):
        """初始化游戏应用"""
        self.game_data = self.load_game_data(game_data_file)
        self.current_question_index = 0
        self.score = 0
        self.lives = self.game_data['game_config']['lives']
        self.hints = self.game_data['game_config']['hints']
        self.start_time = time.time()
        self.time_limit = self.game_data['game_config']['time_limit']
        
    def load_game_data(self, file_path: str) -> Dict[str, Any]:
        """加载游戏数据"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"❌ 错误: 找不到文件 {file_path}")
            return {}
        except json.JSONDecodeError:
            print(f"❌ 错误: 文件 {file_path} 格式错误")
            return {}
    
    def display_header(self):
        """显示游戏头部信息"""
        print("\n" + "="*60)
        print(f"🎮 {self.game_data['title']}")
        print(f"📚 游戏类型: {self.game_data['operation']}")
        print(f"👶 适合年龄: {self.game_data['age_group']}")
        print(f"📊 难度级别: {self.game_data['difficulty']}")
        print(f"❤️  生命值: {self.lives}")
        print(f"💡 提示次数: {self.hints}")
        print(f"⏰ 时间限制: {self.time_limit//60}分钟")
        print("="*60)
    
    def display_question(self, problem: Dict[str, Any]):
        """显示题目"""
        print(f"\n📝 题目 {self.current_question_index + 1}: {problem['question']}")
        print("🔢 选项:")
        
        # 显示选项
        for i, option in enumerate(problem['options'], 1):
            print(f"   {i}. {option}")
        
        print("\n💡 输入 'h' 获取提示")
        print("⏸️  输入 'q' 退出游戏")
    
    def get_user_answer(self, problem: Dict[str, Any]) -> int:
        """获取用户答案"""
        while True:
            try:
                user_input = input("🎯 请选择答案 (1-4): ").strip().lower()
                
                # 检查特殊命令
                if user_input == 'q':
                    return -1  # 退出游戏
                elif user_input == 'h':
                    self.use_hint(problem)
                    continue
                
                # 转换为数字
                answer_index = int(user_input) - 1
                if 0 <= answer_index < len(problem['options']):
                    return problem['options'][answer_index]
                else:
                    print("❌ 请输入1-4之间的数字")
                    
            except ValueError:
                print("❌ 请输入有效的数字")
    
    def use_hint(self, problem: Dict[str, Any]):
        """使用提示"""
        if self.hints > 0:
            self.hints -= 1
            correct_answer = problem['answer']
            
            # 提供不同类型的提示
            hint_types = [
                f"💡 提示: 答案在 {correct_answer-5} 到 {correct_answer+5} 之间",
                f"💡 提示: 正确答案是 {correct_answer} 位数",
                f"💡 提示: 答案是 {'奇数' if correct_answer % 2 == 1 else '偶数'}",
                f"💡 提示: 答案比 {correct_answer-3} 大，比 {correct_answer+3} 小"
            ]
            
            hint = random.choice(hint_types)
            print(f"\n{hint}")
            print(f"🎯 剩余提示次数: {self.hints}")
        else:
            print("\n❌ 提示次数已用完！")
    
    def check_answer(self, user_answer: int, correct_answer: int) -> bool:
        """检查答案"""
        if user_answer == correct_answer:
            print("🎉 ✅ 正确！")
            self.score += 10
            return True
        else:
            print(f"❌ 错误！正确答案是: {correct_answer}")
            self.lives -= 1
            print(f"❤️  剩余生命值: {self.lives}")
            return False
    
    def check_time_limit(self) -> bool:
        """检查时间限制"""
        elapsed_time = int(time.time() - self.start_time)
        remaining_time = max(0, self.time_limit - elapsed_time)
        
        if remaining_time <= 0:
            print("\n⏰ 时间到！游戏结束")
            return False
        
        minutes = remaining_time // 60
        seconds = remaining_time % 60
        print(f"⏱️  剩余时间: {minutes:02d}:{seconds:02d}")
        return True
    
    def display_game_over(self):
        """显示游戏结束信息"""
        print("\n" + "="*60)
        print("🎮 游戏结束！")
        print("="*60)
        
        total_questions = len(self.game_data['problems'])
        max_score = total_questions * 10
        pass_score = self.game_data['game_config']['pass_score']
        
        print(f"📊 最终得分: {self.score}/{max_score}")
        print(f"🎯 及格分数: {pass_score}")
        print(f"📝 答对题目: {self.score // 10}/{total_questions}")
        
        # 计算准确率
        if total_questions > 0:
            accuracy = (self.score // 10) / total_questions * 100
            print(f"🎯 准确率: {accuracy:.1f}%")
        
        # 游戏结果
        if self.score >= pass_score:
            print("\n🎉 🎊 🎉 恭喜通关！ 🎉 🎊 🎉")
            print("🏆 你真棒！继续保持！")
        else:
            print("\n💪 继续努力！下次一定能通关！")
        
        # 显示用时
        elapsed_time = int(time.time() - self.start_time)
        minutes = elapsed_time // 60
        seconds = elapsed_time % 60
        print(f"⏱️  用时: {minutes:02d}:{seconds:02d}")
        
        print("="*60)
    
    def run(self):
        """运行游戏"""
        if not self.game_data:
            print("❌ 无法加载游戏数据")
            return
        
        # 显示游戏信息
        self.display_header()
        
        # 开始游戏循环
        while (self.current_question_index < len(self.game_data['problems']) and 
               self.lives > 0):
            
            # 检查时间限制
            if not self.check_time_limit():
                break
            
            # 获取当前题目
            current_problem = self.game_data['problems'][self.current_question_index]
            
            # 显示题目
            self.display_question(current_problem)
            
            # 获取用户答案
            user_answer = self.get_user_answer(current_problem)
            
            # 检查是否退出
            if user_answer == -1:
                print("\n👋 感谢游玩！")
                break
            
            # 检查答案
            self.check_answer(user_answer, current_problem['answer'])
            
            # 进入下一题
            self.current_question_index += 1
            
            # 题目间暂停
            if self.current_question_index < len(self.game_data['problems']):
                print("\n" + "-"*40)
                input("按回车键继续...")
        
        # 显示游戏结束信息
        self.display_game_over()

def main():
    """主函数"""
    print("🎮 欢迎来到数学游戏世界！")
    print("="*60)
    
    # 检查游戏数据文件
    game_file = "sample_math_game.json"  # 您的游戏数据文件
    
    if not os.path.exists(game_file):
        print(f"❌ 找不到游戏数据文件: {game_file}")
        print("💡 请确保游戏数据文件存在")
        return
    
    # 创建并运行游戏
    game = MathGameApp(game_file)
    game.run()

if __name__ == "__main__":
    main()