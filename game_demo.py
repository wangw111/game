#!/usr/bin/env python3
"""
数学游戏演示脚本
展示如何使用游戏数据创建互动游戏
"""

import json
import random
import time

def demo_game():
    """演示游戏功能"""
    
    # 加载游戏数据
    with open('sample_math_game.json', 'r', encoding='utf-8') as f:
        game_data = json.load(f)
    
    print("🎮 数学游戏演示")
    print("="*50)
    print(f"📚 游戏标题: {game_data['title']}")
    print(f"🔢 运算类型: {game_data['operation']}")
    print(f"👶 适合年龄: {game_data['age_group']}")
    print(f"📊 难度级别: {game_data['difficulty']}")
    print(f"⏰ 时间限制: {game_data['game_config']['time_limit']//60}分钟")
    print(f"🎯 及格分数: {game_data['game_config']['pass_score']}")
    print(f"❤️  生命值: {game_data['game_config']['lives']}")
    print(f"💡 提示次数: {game_data['game_config']['hints']}")
    print("="*50)
    
    # 模拟游戏过程
    score = 0
    lives = game_data['game_config']['lives']
    hints = game_data['game_config']['hints']
    
    for i, problem in enumerate(game_data['problems'][:5]):  # 只演示前5题
        print(f"\n📝 题目 {i+1}: {problem['question']}")
        print("🔢 选项:")
        for j, option in enumerate(problem['options'], 1):
            print(f"   {j}. {option}")
        
        # 模拟用户选择
        if i == 0:
            user_choice = 3  # 选择正确答案
            print(f"\n🎯 模拟选择选项 {user_choice}")
        elif i == 1:
            user_choice = 2  # 选择正确答案
            print(f"\n🎯 模拟选择选项 {user_choice}")
        elif i == 2:
            user_choice = 1  # 选择正确答案
            print(f"\n🎯 模拟选择选项 {user_choice}")
        else:
            user_choice = random.randint(1, 4)  # 随机选择
            print(f"\n🎯 模拟随机选择选项 {user_choice}")
        
        selected_answer = problem['options'][user_choice - 1]
        
        if selected_answer == problem['answer']:
            print("🎉 ✅ 正确！")
            score += 10
        else:
            print(f"❌ 错误！正确答案是: {problem['answer']}")
            lives -= 1
            print(f"❤️  剩余生命值: {lives}")
        
        print(f"🏆 当前得分: {score}")
        
        if lives <= 0:
            print("\n💀 生命值耗尽，游戏结束！")
            break
        
        time.sleep(1)
    
    # 显示最终结果
    print("\n" + "="*50)
    print("🎮 游戏结束！")
    print("="*50)
    
    total_questions = len(game_data['problems'])
    max_score = total_questions * 10
    pass_score = game_data['game_config']['pass_score']
    
    print(f"📊 最终得分: {score}/{max_score}")
    print(f"🎯 及格分数: {pass_score}")
    print(f"📝 答对题目: {score // 10}/{total_questions}")
    
    if total_questions > 0:
        accuracy = (score // 10) / total_questions * 100
        print(f"🎯 准确率: {accuracy:.1f}%")
    
    if score >= pass_score:
        print("\n🎉 🎊 🎉 恭喜通关！ 🎉 🎊 🎉")
        print("🏆 你真棒！继续保持！")
    else:
        print("\n💪 继续努力！下次一定能通关！")
    
    print("="*50)

def show_usage_examples():
    """显示使用示例"""
    print("\n📚 使用示例:")
    print("="*50)
    
    print("1. Python 版本游戏:")
    print("   python3 math_game_app.py")
    print()
    
    print("2. Web 版本游戏:")
    print("   在浏览器中打开 math_game_web.html")
    print()
    
    print("3. 在其他应用中使用游戏数据:")
    print("""
   # 加载游戏数据
   with open('sample_math_game.json', 'r', encoding='utf-8') as f:
       game_data = json.load(f)
   
   # 使用题目
   for problem in game_data['problems']:
       print(f"题目: {problem['question']}")
       print(f"答案: {problem['answer']}")
       print(f"选项: {problem['options']}")
   """)

if __name__ == "__main__":
    demo_game()
    show_usage_examples()