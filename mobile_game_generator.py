import streamlit as st
import json
import os
import sys
import tempfile
import subprocess
from typing import Dict, Any, Optional

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config.settings import Config
from utils.logger import setup_logger
from games.math_game import MathGameGenerator
from games.chinese_game import ChineseGameGenerator
from games.english_game import EnglishGameGenerator
from games.scene_generator import GameSceneGenerator

logger = setup_logger("mobile_game_generator")

class MobileGameGenerator:
    """移动端游戏生成器"""
    
    def __init__(self):
        self.math_generator = MathGameGenerator()
        self.chinese_generator = ChineseGameGenerator()
        self.english_generator = EnglishGameGenerator()
        self.scene_generator = GameSceneGenerator()
        
    def generate_macos_game_code(self, game_data: Dict[str, Any], game_type: str) -> str:
        """生成macOS游戏代码"""
        game_json = json.dumps(game_data, ensure_ascii=False)
        
        if game_type == "math":
            return self._generate_macos_math_game(game_json)
        elif game_type == "chinese":
            return self._generate_macos_chinese_game(game_json)
        elif game_type == "english":
            return self._generate_macos_english_game(game_json)
        elif game_type == "scene":
            return self._generate_macos_scene_game(game_json)
        else:
            return ""
    
    def _generate_macos_math_game(self, game_json: str) -> str:
        """生成macOS数学游戏代码"""
        return f'''import tkinter as tk
from tkinter import ttk, messagebox
import json
import random

# macOS游戏数据
GAME_DATA = {game_json}

class MacOSMathGame:
    def __init__(self, root):
        self.root = root
        self.root.title("🎮 " + GAME_DATA['title'])
        self.root.geometry("800x600")
        self.root.configure(bg='#f0f0f0')
        
        # 游戏状态
        self.score = 0
        self.current_problem_index = 0
        self.lives = GAME_DATA['game_config']['lives']
        self.hints = GAME_DATA['game_config']['hints']
        self.game_over = False
        
        # 设置macOS风格
        self.setup_macos_style()
        self.setup_ui()
        
    def setup_macos_style(self):
        """设置macOS风格"""
        style = ttk.Style()
        style.theme_use('clam')  # macOS-like theme
        
        # 自定义样式
        style.configure('MacOS.TFrame', background='#f0f0f0')
        style.configure('MacOS.TLabel', background='#f0f0f0', font=('SF Pro Display', 14))
        style.configure('MacOS.TButton', font=('SF Pro Display', 12))
        style.configure('Title.TLabel', font=('SF Pro Display', 24, 'bold'))
        style.configure('Question.TLabel', font=('SF Pro Display', 18))
        
    def setup_ui(self):
        """设置用户界面"""
        # 主框架
        main_frame = ttk.Frame(self.root, style='MacOS.TFrame')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # 标题
        title_label = ttk.Label(main_frame, text="🎮 " + GAME_DATA['title'], 
                              style='Title.TLabel')
        title_label.pack(pady=(0, 20))
        
        # 状态框架
        status_frame = ttk.Frame(main_frame, style='MacOS.TFrame')
        status_frame.pack(fill=tk.X, pady=(0, 20))
        
        # 状态标签
        self.score_label = ttk.Label(status_frame, text=f"得分: {{self.score}}", 
                                    style='MacOS.TLabel')
        self.score_label.pack(side=tk.LEFT, padx=(0, 20))
        
        self.lives_label = ttk.Label(status_frame, text=f"生命: {{'❤️' * self.lives}}", 
                                    style='MacOS.TLabel')
        self.lives_label.pack(side=tk.LEFT, padx=(0, 20))
        
        self.hints_label = ttk.Label(status_frame, text=f"提示: {{self.hints}}", 
                                    style='MacOS.TLabel')
        self.hints_label.pack(side=tk.LEFT)
        
        # 进度条
        self.progress = ttk.Progressbar(main_frame, length=400, mode='determinate')
        self.progress.pack(pady=(0, 20))
        
        # 问题框架
        self.question_frame = ttk.Frame(main_frame, style='MacOS.TFrame')
        self.question_frame.pack(fill=tk.BOTH, expand=True)
        
        # 显示当前问题
        self.show_current_problem()
        
    def show_current_problem(self):
        """显示当前问题"""
        if self.current_problem_index >= len(GAME_DATA['problems']):
            self.show_game_over()
            return
            
        # 清空问题框架
        for widget in self.question_frame.winfo_children():
            widget.destroy()
            
        problem = GAME_DATA['problems'][self.current_problem_index]
        
        # 更新进度
        progress_value = (self.current_problem_index + 1) / len(GAME_DATA['problems']) * 100
        self.progress['value'] = progress_value
        
        # 问题标签
        question_label = ttk.Label(self.question_frame, 
                                  text=f"题目 {{self.current_problem_index + 1}}/{{len(GAME_DATA['problems'])}}: {{problem['question']}}",
                                  style='Question.TLabel')
        question_label.pack(pady=(0, 20))
        
        # 选项框架
        options_frame = ttk.Frame(self.question_frame, style='MacOS.TFrame')
        options_frame.pack(expand=True)
        
        # 选项按钮
        self.selected_answer = tk.StringVar()
        for i, option in enumerate(problem['options']):
            btn = ttk.Radiobutton(options_frame, text=str(option), 
                                 variable=self.selected_answer, 
                                 value=str(option),
                                 style='MacOS.TButton')
            btn.pack(pady=5)
        
        # 按钮框架
        button_frame = ttk.Frame(self.question_frame, style='MacOS.TFrame')
        button_frame.pack(pady=20)
        
        # 提示按钮
        if self.hints > 0:
            hint_btn = ttk.Button(button_frame, text="💡 使用提示", 
                                 command=self.use_hint,
                                 style='MacOS.TButton')
            hint_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # 提交按钮
        submit_btn = ttk.Button(button_frame, text="提交答案", 
                               command=self.submit_answer,
                               style='MacOS.TButton')
        submit_btn.pack(side=tk.LEFT)
        
    def use_hint(self):
        """使用提示"""
        if self.hints > 0:
            self.hints -= 1
            problem = GAME_DATA['problems'][self.current_problem_index]
            messagebox.showinfo("提示", f"正确答案是: {{problem['answer']}}")
            self.update_status()
            
    def submit_answer(self):
        """提交答案"""
        if not self.selected_answer.get():
            messagebox.showwarning("警告", "请选择一个答案")
            return
            
        problem = GAME_DATA['problems'][self.current_problem_index]
        selected = int(self.selected_answer.get())
        
        if selected == problem['answer']:
            self.score += 10
            messagebox.showinfo("正确", "✅ 答对了！")
        else:
            self.lives -= 1
            messagebox.showerror("错误", f"❌ 答错了！正确答案是: {{problem['answer']}}")
            
        if self.lives <= 0:
            self.game_over = True
            self.show_game_over()
        else:
            self.current_problem_index += 1
            self.show_current_problem()
            
        self.update_status()
        
    def update_status(self):
        """更新状态显示"""
        self.score_label.config(text=f"得分: {{self.score}}")
        self.lives_label.config(text=f"生命: {{'❤️' * self.lives}}")
        self.hints_label.config(text=f"提示: {{self.hints}}")
        
    def show_game_over(self):
        """显示游戏结束"""
        for widget in self.question_frame.winfo_children():
            widget.destroy()
            
        # 游戏结束标签
        game_over_label = ttk.Label(self.question_frame, text="🎉 游戏结束！", 
                                   style='Title.TLabel')
        game_over_label.pack(pady=20)
        
        # 最终得分
        score_label = ttk.Label(self.question_frame, 
                               text=f"最终得分: {{self.score}}",
                               style='Question.TLabel')
        score_label.pack(pady=10)
        
        # 完成情况
        completed_label = ttk.Label(self.question_frame, 
                                   text=f"完成题目: {{self.current_problem_index}}/{{len(GAME_DATA['problems'])}}",
                                   style='MacOS.TLabel')
        completed_label.pack(pady=10)
        
        # 结果
        if self.score >= GAME_DATA['game_config']['pass_score']:
            result_label = ttk.Label(self.question_frame, text="🎊 恭喜过关！", 
                                   style='Question.TLabel', foreground='green')
        else:
            result_label = ttk.Label(self.question_frame, text="😅 再接再厉！", 
                                   style='Question.TLabel', foreground='orange')
        result_label.pack(pady=10)
        
        # 重新开始按钮
        restart_btn = ttk.Button(self.question_frame, text="重新开始", 
                               command=self.restart_game,
                               style='MacOS.TButton')
        restart_btn.pack(pady=20)
        
    def restart_game(self):
        """重新开始游戏"""
        self.score = 0
        self.current_problem_index = 0
        self.lives = GAME_DATA['game_config']['lives']
        self.hints = GAME_DATA['game_config']['hints']
        self.game_over = False
        self.selected_answer.set("")
        self.update_status()
        self.show_current_problem()

# 主程序
if __name__ == "__main__":
    root = tk.Tk()
    game = MacOSMathGame(root)
    root.mainloop()
'''
    
    def _generate_macos_chinese_game(self, game_json: str) -> str:
        """生成macOS汉字游戏代码"""
        return f'''import tkinter as tk
from tkinter import ttk, messagebox
import json
import random

# macOS游戏数据
GAME_DATA = {game_json}

class MacOSChineseGame:
    def __init__(self, root):
        self.root = root
        self.root.title("🎮 " + GAME_DATA['title'])
        self.root.geometry("800x600")
        self.root.configure(bg='#f0f0f0')
        
        # 游戏状态
        self.score = 0
        self.current_question_index = 0
        self.lives = GAME_DATA['game_config']['lives']
        self.hints = GAME_DATA['game_config']['hints']
        self.game_over = False
        
        # 设置macOS风格
        self.setup_macos_style()
        self.setup_ui()
        
    def setup_macos_style(self):
        """设置macOS风格"""
        style = ttk.Style()
        style.theme_use('clam')
        
        style.configure('MacOS.TFrame', background='#f0f0f0')
        style.configure('MacOS.TLabel', background='#f0f0f0', font=('SF Pro Display', 14))
        style.configure('MacOS.TButton', font=('SF Pro Display', 12))
        style.configure('Title.TLabel', font=('SF Pro Display', 24, 'bold'))
        style.configure('Question.TLabel', font=('SF Pro Display', 18))
        style.configure('Chinese.TLabel', font=('PingFang SC', 16))
        
    def setup_ui(self):
        """设置用户界面"""
        # 主框架
        main_frame = ttk.Frame(self.root, style='MacOS.TFrame')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # 标题
        title_label = ttk.Label(main_frame, text="🎮 " + GAME_DATA['title'], 
                              style='Title.TLabel')
        title_label.pack(pady=(0, 20))
        
        # 状态框架
        status_frame = ttk.Frame(main_frame, style='MacOS.TFrame')
        status_frame.pack(fill=tk.X, pady=(0, 20))
        
        # 状态标签
        self.score_label = ttk.Label(status_frame, text=f"得分: {{self.score}}", 
                                    style='MacOS.TLabel')
        self.score_label.pack(side=tk.LEFT, padx=(0, 20))
        
        self.lives_label = ttk.Label(status_frame, text=f"生命: {{'❤️' * self.lives}}", 
                                    style='MacOS.TLabel')
        self.lives_label.pack(side=tk.LEFT, padx=(0, 20))
        
        self.hints_label = ttk.Label(status_frame, text=f"提示: {{self.hints}}", 
                                    style='MacOS.TLabel')
        self.hints_label.pack(side=tk.LEFT)
        
        # 进度条
        self.progress = ttk.Progressbar(main_frame, length=400, mode='determinate')
        self.progress.pack(pady=(0, 20))
        
        # 问题框架
        self.question_frame = ttk.Frame(main_frame, style='MacOS.TFrame')
        self.question_frame.pack(fill=tk.BOTH, expand=True)
        
        # 显示当前问题
        self.show_current_question()
        
    def show_current_question(self):
        """显示当前问题"""
        if self.current_question_index >= len(GAME_DATA['questions']):
            self.show_game_over()
            return
            
        # 清空问题框架
        for widget in self.question_frame.winfo_children():
            widget.destroy()
            
        question = GAME_DATA['questions'][self.current_question_index]
        
        # 更新进度
        progress_value = (self.current_question_index + 1) / len(GAME_DATA['questions']) * 100
        self.progress['value'] = progress_value
        
        # 问题标签
        question_label = ttk.Label(self.question_frame, 
                                  text=f"题目 {{self.current_question_index + 1}}/{{len(GAME_DATA['questions'])}}",
                                  style='MacOS.TLabel')
        question_label.pack(pady=(0, 10))
        
        # 汉字问题（大字体）
        char_label = ttk.Label(self.question_frame, 
                               text=question['question'],
                               style='Question.TLabel')
        char_label.pack(pady=(0, 20))
        
        # 选项框架
        options_frame = ttk.Frame(self.question_frame, style='MacOS.TFrame')
        options_frame.pack(expand=True)
        
        # 选项按钮
        self.selected_answer = tk.StringVar()
        for i, option in enumerate(question['options']):
            btn = ttk.Radiobutton(options_frame, text=option, 
                                 variable=self.selected_answer, 
                                 value=option,
                                 style='Chinese.TLabel')
            btn.pack(pady=5)
        
        # 按钮框架
        button_frame = ttk.Frame(self.question_frame, style='MacOS.TFrame')
        button_frame.pack(pady=20)
        
        # 提示按钮
        if self.hints > 0:
            hint_btn = ttk.Button(button_frame, text="💡 使用提示", 
                                 command=self.use_hint,
                                 style='MacOS.TButton')
            hint_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # 提交按钮
        submit_btn = ttk.Button(button_frame, text="提交答案", 
                               command=self.submit_answer,
                               style='MacOS.TButton')
        submit_btn.pack(side=tk.LEFT)
        
    def use_hint(self):
        """使用提示"""
        if self.hints > 0:
            self.hints -= 1
            question = GAME_DATA['questions'][self.current_question_index]
            hint_text = f"正确答案是: {{question['answer']}}"
            if 'meaning' in question:
                hint_text += f"\\n含义: {{question['meaning']}}"
            messagebox.showinfo("提示", hint_text)
            self.update_status()
            
    def submit_answer(self):
        """提交答案"""
        if not self.selected_answer.get():
            messagebox.showwarning("警告", "请选择一个答案")
            return
            
        question = GAME_DATA['questions'][self.current_question_index]
        selected = self.selected_answer.get()
        
        if selected == question['answer']:
            self.score += 10
            messagebox.showinfo("正确", "✅ 答对了！")
        else:
            self.lives -= 1
            messagebox.showerror("错误", f"❌ 答错了！正确答案是: {{question['answer']}}")
            
        if self.lives <= 0:
            self.game_over = True
            self.show_game_over()
        else:
            self.current_question_index += 1
            self.show_current_question()
            
        self.update_status()
        
    def update_status(self):
        """更新状态显示"""
        self.score_label.config(text=f"得分: {{self.score}}")
        self.lives_label.config(text=f"生命: {{'❤️' * self.lives}}")
        self.hints_label.config(text=f"提示: {{self.hints}}")
        
    def show_game_over(self):
        """显示游戏结束"""
        for widget in self.question_frame.winfo_children():
            widget.destroy()
            
        # 游戏结束标签
        game_over_label = ttk.Label(self.question_frame, text="🎉 游戏结束！", 
                                   style='Title.TLabel')
        game_over_label.pack(pady=20)
        
        # 最终得分
        score_label = ttk.Label(self.question_frame, 
                               text=f"最终得分: {{self.score}}",
                               style='Question.TLabel')
        score_label.pack(pady=10)
        
        # 完成情况
        completed_label = ttk.Label(self.question_frame, 
                                   text=f"完成题目: {{self.current_question_index}}/{{len(GAME_DATA['questions'])}}",
                                   style='MacOS.TLabel')
        completed_label.pack(pady=10)
        
        # 结果
        if self.score >= GAME_DATA['game_config']['pass_score']:
            result_label = ttk.Label(self.question_frame, text="🎊 恭喜过关！", 
                                   style='Question.TLabel', foreground='green')
        else:
            result_label = ttk.Label(self.question_frame, text="😅 再接再厉！", 
                                   style='Question.TLabel', foreground='orange')
        result_label.pack(pady=10)
        
        # 重新开始按钮
        restart_btn = ttk.Button(self.question_frame, text="重新开始", 
                               command=self.restart_game,
                               style='MacOS.TButton')
        restart_btn.pack(pady=20)
        
    def restart_game(self):
        """重新开始游戏"""
        self.score = 0
        self.current_question_index = 0
        self.lives = GAME_DATA['game_config']['lives']
        self.hints = GAME_DATA['game_config']['hints']
        self.game_over = False
        self.selected_answer.set("")
        self.update_status()
        self.show_current_question()

# 主程序
if __name__ == "__main__":
    root = tk.Tk()
    game = MacOSChineseGame(root)
    root.mainloop()
'''
    
    def _generate_macos_english_game(self, game_json: str) -> str:
        """生成macOS英语游戏代码"""
        return f'''import tkinter as tk
from tkinter import ttk, messagebox
import json
import random

# macOS游戏数据
GAME_DATA = {game_json}

class MacOSEnglishGame:
    def __init__(self, root):
        self.root = root
        self.root.title("🎮 " + GAME_DATA['title'])
        self.root.geometry("800x600")
        self.root.configure(bg='#f0f0f0')
        
        # 游戏状态
        self.score = 0
        self.current_question_index = 0
        self.lives = GAME_DATA['game_config']['lives']
        self.hints = GAME_DATA['game_config']['hints']
        self.game_over = False
        
        # 设置macOS风格
        self.setup_macos_style()
        self.setup_ui()
        
    def setup_macos_style(self):
        """设置macOS风格"""
        style = ttk.Style()
        style.theme_use('clam')
        
        style.configure('MacOS.TFrame', background='#f0f0f0')
        style.configure('MacOS.TLabel', background='#f0f0f0', font=('SF Pro Display', 14))
        style.configure('MacOS.TButton', font=('SF Pro Display', 12))
        style.configure('Title.TLabel', font=('SF Pro Display', 24, 'bold'))
        style.configure('Question.TLabel', font=('SF Pro Display', 18))
        
    def setup_ui(self):
        """设置用户界面"""
        # 主框架
        main_frame = ttk.Frame(self.root, style='MacOS.TFrame')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # 标题
        title_label = ttk.Label(main_frame, text="🎮 " + GAME_DATA['title'], 
                              style='Title.TLabel')
        title_label.pack(pady=(0, 20))
        
        # 状态框架
        status_frame = ttk.Frame(main_frame, style='MacOS.TFrame')
        status_frame.pack(fill=tk.X, pady=(0, 20))
        
        # 状态标签
        self.score_label = ttk.Label(status_frame, text=f"得分: {{self.score}}", 
                                    style='MacOS.TLabel')
        self.score_label.pack(side=tk.LEFT, padx=(0, 20))
        
        self.lives_label = ttk.Label(status_frame, text=f"生命: {{'❤️' * self.lives}}", 
                                    style='MacOS.TLabel')
        self.lives_label.pack(side=tk.LEFT, padx=(0, 20))
        
        self.hints_label = ttk.Label(status_frame, text=f"提示: {{self.hints}}", 
                                    style='MacOS.TLabel')
        self.hints_label.pack(side=tk.LEFT)
        
        # 进度条
        self.progress = ttk.Progressbar(main_frame, length=400, mode='determinate')
        self.progress.pack(pady=(0, 20))
        
        # 问题框架
        self.question_frame = ttk.Frame(main_frame, style='MacOS.TFrame')
        self.question_frame.pack(fill=tk.BOTH, expand=True)
        
        # 显示当前问题
        self.show_current_question()
        
    def show_current_question(self):
        """显示当前问题"""
        if self.current_question_index >= len(GAME_DATA['questions']):
            self.show_game_over()
            return
            
        # 清空问题框架
        for widget in self.question_frame.winfo_children():
            widget.destroy()
            
        question = GAME_DATA['questions'][self.current_question_index]
        
        # 更新进度
        progress_value = (self.current_question_index + 1) / len(GAME_DATA['questions']) * 100
        self.progress['value'] = progress_value
        
        # 问题标签
        question_label = ttk.Label(self.question_frame, 
                                  text=f"题目 {{self.current_question_index + 1}}/{{len(GAME_DATA['questions'])}}",
                                  style='MacOS.TLabel')
        question_label.pack(pady=(0, 10))
        
        # 英语问题
        english_label = ttk.Label(self.question_frame, 
                                 text=question['question'],
                                 style='Question.TLabel')
        english_label.pack(pady=(0, 20))
        
        # 选项框架
        options_frame = ttk.Frame(self.question_frame, style='MacOS.TFrame')
        options_frame.pack(expand=True)
        
        # 选项按钮
        self.selected_answer = tk.StringVar()
        for i, option in enumerate(question['options']):
            btn = ttk.Radiobutton(options_frame, text=option, 
                                 variable=self.selected_answer, 
                                 value=option,
                                 style='MacOS.TButton')
            btn.pack(pady=5)
        
        # 按钮框架
        button_frame = ttk.Frame(self.question_frame, style='MacOS.TFrame')
        button_frame.pack(pady=20)
        
        # 提示按钮
        if self.hints > 0:
            hint_btn = ttk.Button(button_frame, text="💡 使用提示", 
                                 command=self.use_hint,
                                 style='MacOS.TButton')
            hint_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # 提交按钮
        submit_btn = ttk.Button(button_frame, text="提交答案", 
                               command=self.submit_answer,
                               style='MacOS.TButton')
        submit_btn.pack(side=tk.LEFT)
        
    def use_hint(self):
        """使用提示"""
        if self.hints > 0:
            self.hints -= 1
            question = GAME_DATA['questions'][self.current_question_index]
            hint_text = f"正确答案是: {{question['answer']}}"
            if 'translation' in question:
                hint_text += f"\\n翻译: {{question['translation']}}"
            if 'explanation' in question:
                hint_text += f"\\n解释: {{question['explanation']}}"
            messagebox.showinfo("提示", hint_text)
            self.update_status()
            
    def submit_answer(self):
        """提交答案"""
        if not self.selected_answer.get():
            messagebox.showwarning("警告", "请选择一个答案")
            return
            
        question = GAME_DATA['questions'][self.current_question_index]
        selected = self.selected_answer.get()
        
        if selected == question['answer']:
            self.score += 10
            messagebox.showinfo("正确", "✅ 答对了！")
        else:
            self.lives -= 1
            messagebox.showerror("错误", f"❌ 答错了！正确答案是: {{question['answer']}}")
            
        if self.lives <= 0:
            self.game_over = True
            self.show_game_over()
        else:
            self.current_question_index += 1
            self.show_current_question()
            
        self.update_status()
        
    def update_status(self):
        """更新状态显示"""
        self.score_label.config(text=f"得分: {{self.score}}")
        self.lives_label.config(text=f"生命: {{'❤️' * self.lives}}")
        self.hints_label.config(text=f"提示: {{self.hints}}")
        
    def show_game_over(self):
        """显示游戏结束"""
        for widget in self.question_frame.winfo_children():
            widget.destroy()
            
        # 游戏结束标签
        game_over_label = ttk.Label(self.question_frame, text="🎉 游戏结束！", 
                                   style='Title.TLabel')
        game_over_label.pack(pady=20)
        
        # 最终得分
        score_label = ttk.Label(self.question_frame, 
                               text=f"最终得分: {{self.score}}",
                               style='Question.TLabel')
        score_label.pack(pady=10)
        
        # 完成情况
        completed_label = ttk.Label(self.question_frame, 
                                   text=f"完成题目: {{self.current_question_index}}/{{len(GAME_DATA['questions'])}}",
                                   style='MacOS.TLabel')
        completed_label.pack(pady=10)
        
        # 结果
        if self.score >= GAME_DATA['game_config']['pass_score']:
            result_label = ttk.Label(self.question_frame, text="🎊 恭喜过关！", 
                                   style='Question.TLabel', foreground='green')
        else:
            result_label = ttk.Label(self.question_frame, text="😅 再接再厉！", 
                                   style='Question.TLabel', foreground='orange')
        result_label.pack(pady=10)
        
        # 重新开始按钮
        restart_btn = ttk.Button(self.question_frame, text="重新开始", 
                               command=self.restart_game,
                               style='MacOS.TButton')
        restart_btn.pack(pady=20)
        
    def restart_game(self):
        """重新开始游戏"""
        self.score = 0
        self.current_question_index = 0
        self.lives = GAME_DATA['game_config']['lives']
        self.hints = GAME_DATA['game_config']['hints']
        self.game_over = False
        self.selected_answer.set("")
        self.update_status()
        self.show_current_question()

# 主程序
if __name__ == "__main__":
    root = tk.Tk()
    game = MacOSEnglishGame(root)
    root.mainloop()
'''
    
    def _generate_macos_scene_game(self, scene_json: str) -> str:
        """生成macOS场景游戏代码"""
        return f'''import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import json
import random

# macOS场景数据
SCENE_DATA = {scene_json}

class MacOSSceneGame:
    def __init__(self, root):
        self.root = root
        self.root.title("🎮 " + SCENE_DATA['title'])
        self.root.geometry("1000x700")
        self.root.configure(bg='#f0f0f0')
        
        # 游戏状态
        self.score = 0
        
        # 设置macOS风格
        self.setup_macos_style()
        self.setup_ui()
        
    def setup_macos_style(self):
        """设置macOS风格"""
        style = ttk.Style()
        style.theme_use('clam')
        
        style.configure('MacOS.TFrame', background='#f0f0f0')
        style.configure('MacOS.TLabel', background='#f0f0f0', font=('SF Pro Display', 14))
        style.configure('MacOS.TButton', font=('SF Pro Display', 12))
        style.configure('Title.TLabel', font=('SF Pro Display', 24, 'bold'))
        style.configure('Subtitle.TLabel', font=('SF Pro Display', 16, 'bold'))
        
    def setup_ui(self):
        """设置用户界面"""
        # 主框架
        main_frame = ttk.Frame(self.root, style='MacOS.TFrame')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # 标题
        title_label = ttk.Label(main_frame, text="🎮 " + SCENE_DATA['title'], 
                              style='Title.TLabel')
        title_label.pack(pady=(0, 10))
        
        # 场景描述
        desc_label = ttk.Label(main_frame, 
                               text=f"场景描述: {{SCENE_DATA['description']}}",
                               style='MacOS.TLabel')
        desc_label.pack(pady=(0, 10))
        
        # 动作逻辑
        logic_label = ttk.Label(main_frame, 
                               text=f"动作逻辑: {{SCENE_DATA['action_logic']}}",
                               style='MacOS.TLabel')
        logic_label.pack(pady=(0, 20))
        
        # 主要内容区域
        content_frame = ttk.Frame(main_frame, style='MacOS.TFrame')
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # 左侧：场景信息
        left_frame = ttk.Frame(content_frame, style='MacOS.TFrame')
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # 场景信息标题
        info_title = ttk.Label(left_frame, text="📋 场景信息", 
                              style='Subtitle.TLabel')
        info_title.pack(pady=(0, 10))
        
        # 场景信息文本
        info_text = scrolledtext.ScrolledText(left_frame, width=50, height=20, 
                                             font=('SF Pro Display', 11))
        info_text.pack(fill=tk.BOTH, expand=True)
        info_text.insert(tk.END, self.generate_scene_info())
        info_text.config(state=tk.DISABLED)
        
        # 右侧：互动区域
        right_frame = ttk.Frame(content_frame, style='MacOS.TFrame')
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # 互动区域标题
        interaction_title = ttk.Label(right_frame, text="🎯 互动区域", 
                                    style='Subtitle.TLabel')
        interaction_title.pack(pady=(0, 10))
        
        # 得分显示
        self.score_label = ttk.Label(right_frame, text=f"当前得分: {{self.score}}", 
                                    style='MacOS.TLabel')
        self.score_label.pack(pady=(0, 10))
        
        # 互动按钮区域
        self.interaction_frame = ttk.Frame(right_frame, style='MacOS.TFrame')
        self.interaction_frame.pack(fill=tk.BOTH, expand=True)
        
        # 生成互动按钮
        self.generate_interaction_buttons()
        
        # 重置按钮
        reset_btn = ttk.Button(right_frame, text="🔄 重置游戏", 
                              command=self.reset_game,
                              style='MacOS.TButton')
        reset_btn.pack(pady=10)
        
    def generate_scene_info(self):
        """生成场景信息文本"""
        info = "## 场景元素\\n\\n"
        
        # 角色信息
        if SCENE_DATA['scene_elements']['characters']:
            info += "### 角色\\n"
            for char in SCENE_DATA['scene_elements']['characters']:
                info += f"**{{char['name']}}**: {{char['description']}}\\n"
                info += f"能力: {{', '.join(char['abilities'])}}\\n\\n"
        
        # 环境信息
        env = SCENE_DATA['scene_elements']['environment']
        info += "### 环境\\n"
        info += f"**设置**: {{env['setting']}}\\n"
        info += f"**背景**: {{env['background']}}\\n"
        info += f"**氛围**: {{env['atmosphere']}}\\n\\n"
        
        # 物体信息
        if SCENE_DATA['scene_elements']['objects']:
            info += "### 物体\\n"
            for obj in SCENE_DATA['scene_elements']['objects']:
                info += f"**{{obj['name']}}**: {{obj['description']}}\\n"
                info += f"交互: {{obj['interaction']}}\\n\\n"
        
        return info
        
    def generate_interaction_buttons(self):
        """生成互动按钮"""
        # 清空现有按钮
        for widget in self.interaction_frame.winfo_children():
            widget.destroy()
        
        # 角色互动按钮
        if SCENE_DATA['scene_elements']['characters']:
            char_label = ttk.Label(self.interaction_frame, text="👥 角色互动", 
                                   style='Subtitle.TLabel')
            char_label.pack(pady=(10, 5))
            
            for char in SCENE_DATA['scene_elements']['characters']:
                btn = ttk.Button(self.interaction_frame, 
                               text=f"与 {{char['name']}} 互动",
                               command=lambda c=char: self.interact_with_character(c),
                               style='MacOS.TButton')
                btn.pack(pady=2, fill=tk.X)
        
        # 物体互动按钮
        if SCENE_DATA['scene_elements']['objects']:
            obj_label = ttk.Label(self.interaction_frame, text="🎪 物体互动", 
                                  style='Subtitle.TLabel')
            obj_label.pack(pady=(10, 5))
            
            for obj in SCENE_DATA['scene_elements']['objects']:
                btn = ttk.Button(self.interaction_frame, 
                               text=f"使用 {{obj['name']}}",
                               command=lambda o=obj: self.interact_with_object(o),
                               style='MacOS.TButton')
                btn.pack(pady=2, fill=tk.X)
    
    def interact_with_character(self, character):
        """与角色互动"""
        self.score += 5
        messagebox.showinfo("互动成功", 
                           f"你与 {{character['name']}} 互动了！\\n获得 5 分")
        self.update_score()
    
    def interact_with_object(self, obj):
        """与物体互动"""
        self.score += 3
        messagebox.showinfo("互动成功", 
                           f"你使用了 {{obj['name']}}！\\n获得 3 分")
        self.update_score()
    
    def update_score(self):
        """更新得分显示"""
        self.score_label.config(text=f"当前得分: {{self.score}}")
    
    def reset_game(self):
        """重置游戏"""
        self.score = 0
        self.update_score()
        messagebox.showinfo("游戏重置", "游戏已重置！")

# 主程序
if __name__ == "__main__":
    root = tk.Tk()
    game = MacOSSceneGame(root)
    root.mainloop()
'''
    
    def generate_ios_game_code(self, game_data: Dict[str, Any], game_type: str) -> str:
        """生成iOS游戏代码"""
        game_json = json.dumps(game_data, ensure_ascii=False)
        
        if game_type == "math":
            return self._generate_ios_math_game(game_json)
        elif game_type == "chinese":
            return self._generate_ios_chinese_game(game_json)
        elif game_type == "english":
            return self._generate_ios_english_game(game_json)
        elif game_type == "scene":
            return self._generate_ios_scene_game(game_json)
        else:
            return ""
    
    def _generate_ios_math_game(self, game_json: str) -> str:
        """生成iOS数学游戏代码"""
        return f'''import pygame
import sys
import json
import random
import math

# iOS游戏数据
GAME_DATA = {game_json}

class iOSMathGame:
    def __init__(self):
        pygame.init()
        
        # 设置iOS设备尺寸
        self.width = 375
        self.height = 667
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("🎮 " + GAME_DATA['title'])
        
        # 颜色定义
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.BLUE = (0, 122, 255)
        self.GREEN = (52, 199, 89)
        self.RED = (255, 59, 48)
        self.GRAY = (142, 142, 147)
        self.LIGHT_GRAY = (242, 242, 247)
        
        # 字体设置
        self.title_font = pygame.font.Font(None, 36)
        self.question_font = pygame.font.Font(None, 28)
        self.option_font = pygame.font.Font(None, 24)
        self.status_font = pygame.font.Font(None, 20)
        
        # 游戏状态
        self.score = 0
        self.current_problem_index = 0
        self.lives = GAME_DATA['game_config']['lives']
        self.hints = GAME_DATA['game_config']['hints']
        self.game_over = False
        self.selected_answer = None
        
        # 按钮位置
        self.option_buttons = []
        self.hint_button = None
        self.submit_button = None
        self.restart_button = None
        
        self.setup_ui()
        
    def setup_ui(self):
        """设置用户界面"""
        # 计算按钮位置
        button_width = 300
        button_height = 50
        button_spacing = 15
        start_y = 250
        
        # 选项按钮
        self.option_buttons = []
        for i in range(4):
            x = (self.width - button_width) // 2
            y = start_y + i * (button_height + button_spacing)
            rect = pygame.Rect(x, y, button_width, button_height)
            self.option_buttons.append(rect)
        
        # 提示按钮
        self.hint_button = pygame.Rect(20, self.height - 120, 120, 40)
        
        # 提交按钮
        self.submit_button = pygame.Rect(self.width - 140, self.height - 120, 120, 40)
        
        # 重新开始按钮
        self.restart_button = pygame.Rect((self.width - 200) // 2, self.height - 100, 200, 50)
        
    def draw_rounded_rect(self, surface, rect, color, radius=10):
        """绘制圆角矩形"""
        pygame.draw.rect(surface, color, rect, border_radius=radius)
        
    def draw_button(self, surface, rect, text, font, color, text_color):
        """绘制按钮"""
        self.draw_rounded_rect(surface, rect, color)
        text_surface = font.render(text, True, text_color)
        text_rect = text_surface.get_rect(center=rect.center)
        surface.blit(text_surface, text_rect)
        
    def draw(self):
        """绘制游戏画面"""
        # 背景
        self.screen.fill(self.LIGHT_GRAY)
        
        if self.game_over:
            self.draw_game_over()
        else:
            self.draw_game()
        
        pygame.display.flip()
        
    def draw_game(self):
        """绘制游戏画面"""
        if self.current_problem_index >= len(GAME_DATA['problems']):
            self.game_over = True
            return
            
        problem = GAME_DATA['problems'][self.current_problem_index]
        
        # 标题
        title_text = self.title_font.render("🎮 " + GAME_DATA['title'], True, self.BLACK)
        title_rect = title_text.get_rect(centerx=self.width // 2, y=30)
        self.screen.blit(title_text, title_rect)
        
        # 状态栏
        status_y = 80
        score_text = self.status_font.render(f"得分: {{self.score}}", True, self.BLACK)
        self.screen.blit(score_text, (20, status_y))
        
        lives_text = self.status_font.render(f"生命: {{'❤️' * self.lives}}", True, self.RED)
        lives_rect = lives_text.get_rect(centerx=self.width // 2, y=status_y)
        self.screen.blit(lives_text, lives_rect)
        
        hints_text = self.status_font.render(f"提示: {{self.hints}}", True, self.BLACK)
        hints_rect = hints_text.get_rect(right=self.width - 20, y=status_y)
        self.screen.blit(hints_text, hints_rect)
        
        # 进度条
        progress_y = 120
        progress_width = 300
        progress_height = 8
        progress_x = (self.width - progress_width) // 2
        
        # 进度条背景
        pygame.draw.rect(self.screen, self.GRAY, 
                        (progress_x, progress_y, progress_width, progress_height), 
                        border_radius=4)
        
        # 进度条前景
        progress_value = (self.current_problem_index + 1) / len(GAME_DATA['problems'])
        progress_fill_width = int(progress_width * progress_value)
        pygame.draw.rect(self.screen, self.BLUE, 
                        (progress_x, progress_y, progress_fill_width, progress_height), 
                        border_radius=4)
        
        # 题目
        question_text = self.question_font.render(
            f"题目 {{self.current_problem_index + 1}}: {{problem['question']}}", 
            True, self.BLACK)
        question_rect = question_text.get_rect(centerx=self.width // 2, y=160)
        self.screen.blit(question_text, question_rect)
        
        # 选项按钮
        for i, (rect, option) in enumerate(zip(self.option_buttons, problem['options'])):
            color = self.BLUE if self.selected_answer == i else self.WHITE
            self.draw_button(self.screen, rect, str(option), 
                           self.option_font, color, self.BLACK)
        
        # 提示按钮
        if self.hints > 0:
            self.draw_button(self.screen, self.hint_button, "💡 提示", 
                           self.status_font, self.GREEN, self.WHITE)
        
        # 提交按钮
        submit_color = self.BLUE if self.selected_answer is not None else self.GRAY
        self.draw_button(self.screen, self.submit_button, "提交", 
                       self.status_font, submit_color, self.WHITE)
        
    def draw_game_over(self):
        """绘制游戏结束画面"""
        # 游戏结束标题
        game_over_text = self.title_font.render("🎉 游戏结束！", True, self.BLACK)
        game_over_rect = game_over_text.get_rect(centerx=self.width // 2, y=100)
        self.screen.blit(game_over_text, game_over_rect)
        
        # 最终得分
        score_text = self.question_font.render(f"最终得分: {{self.score}}", True, self.BLACK)
        score_rect = score_text.get_rect(centerx=self.width // 2, y=200)
        self.screen.blit(score_text, score_rect)
        
        # 完成情况
        completed_text = self.status_font.render(
            f"完成题目: {{self.current_problem_index}}/{{len(GAME_DATA['problems'])}}", 
            True, self.BLACK)
        completed_rect = completed_text.get_rect(centerx=self.width // 2, y=250)
        self.screen.blit(completed_text, completed_rect)
        
        # 结果
        if self.score >= GAME_DATA['game_config']['pass_score']:
            result_text = self.question_font.render("🎊 恭喜过关！", True, self.GREEN)
        else:
            result_text = self.question_font.render("😅 再接再厉！", True, self.RED)
        result_rect = result_text.get_rect(centerx=self.width // 2, y=300)
        self.screen.blit(result_text, result_rect)
        
        # 重新开始按钮
        self.draw_button(self.screen, self.restart_button, "重新开始", 
                       self.option_font, self.BLUE, self.WHITE)
        
    def handle_click(self, pos):
        """处理点击事件"""
        if self.game_over:
            if self.restart_button.collidepoint(pos):
                self.restart_game()
        else:
            # 检查选项按钮点击
            for i, rect in enumerate(self.option_buttons):
                if rect.collidepoint(pos):
                    self.selected_answer = i
                    return
            
            # 检查提示按钮点击
            if self.hints > 0 and self.hint_button.collidepoint(pos):
                self.use_hint()
                return
            
            # 检查提交按钮点击
            if self.selected_answer is not None and self.submit_button.collidepoint(pos):
                self.submit_answer()
                
    def use_hint(self):
        """使用提示"""
        if self.hints > 0:
            self.hints -= 1
            problem = GAME_DATA['problems'][self.current_problem_index]
            print(f"提示: 正确答案是 {{problem['answer']}}")
            
    def submit_answer(self):
        """提交答案"""
        if self.selected_answer is None:
            return
            
        problem = GAME_DATA['problems'][self.current_problem_index]
        selected = problem['options'][self.selected_answer]
        
        if selected == problem['answer']:
            self.score += 10
            print("✅ 答对了！")
        else:
            self.lives -= 1
            print(f"❌ 答错了！正确答案是: {{problem['answer']}}")
            
        if self.lives <= 0:
            self.game_over = True
        else:
            self.current_problem_index += 1
            self.selected_answer = None
            
    def restart_game(self):
        """重新开始游戏"""
        self.score = 0
        self.current_problem_index = 0
        self.lives = GAME_DATA['game_config']['lives']
        self.hints = GAME_DATA['game_config']['hints']
        self.game_over = False
        self.selected_answer = None
        
    def run(self):
        """运行游戏"""
        clock = pygame.time.Clock()
        running = True
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_click(event.pos)
            
            self.draw()
            clock.tick(60)
        
        pygame.quit()
        sys.exit()

# 主程序
if __name__ == "__main__":
    game = iOSMathGame()
    game.run()
'''
    
    def _generate_ios_chinese_game(self, game_json: str) -> str:
        """生成iOS汉字游戏代码"""
        return f'''import pygame
import sys
import json
import random
import math

# iOS游戏数据
GAME_DATA = {game_json}

class iOSChineseGame:
    def __init__(self):
        pygame.init()
        
        # 设置iOS设备尺寸
        self.width = 375
        self.height = 667
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("🎮 " + GAME_DATA['title'])
        
        # 颜色定义
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.BLUE = (0, 122, 255)
        self.GREEN = (52, 199, 89)
        self.RED = (255, 59, 48)
        self.GRAY = (142, 142, 147)
        self.LIGHT_GRAY = (242, 242, 247)
        
        # 字体设置
        self.title_font = pygame.font.Font(None, 36)
        self.question_font = pygame.font.Font(None, 32)
        self.option_font = pygame.font.Font(None, 24)
        self.status_font = pygame.font.Font(None, 20)
        
        # 游戏状态
        self.score = 0
        self.current_question_index = 0
        self.lives = GAME_DATA['game_config']['lives']
        self.hints = GAME_DATA['game_config']['hints']
        self.game_over = False
        self.selected_answer = None
        
        # 按钮位置
        self.option_buttons = []
        self.hint_button = None
        self.submit_button = None
        self.restart_button = None
        
        self.setup_ui()
        
    def setup_ui(self):
        """设置用户界面"""
        # 计算按钮位置
        button_width = 300
        button_height = 50
        button_spacing = 15
        start_y = 280
        
        # 选项按钮
        self.option_buttons = []
        for i in range(4):
            x = (self.width - button_width) // 2
            y = start_y + i * (button_height + button_spacing)
            rect = pygame.Rect(x, y, button_width, button_height)
            self.option_buttons.append(rect)
        
        # 提示按钮
        self.hint_button = pygame.Rect(20, self.height - 120, 120, 40)
        
        # 提交按钮
        self.submit_button = pygame.Rect(self.width - 140, self.height - 120, 120, 40)
        
        # 重新开始按钮
        self.restart_button = pygame.Rect((self.width - 200) // 2, self.height - 100, 200, 50)
        
    def draw_rounded_rect(self, surface, rect, color, radius=10):
        """绘制圆角矩形"""
        pygame.draw.rect(surface, color, rect, border_radius=radius)
        
    def draw_button(self, surface, rect, text, font, color, text_color):
        """绘制按钮"""
        self.draw_rounded_rect(surface, rect, color)
        text_surface = font.render(text, True, text_color)
        text_rect = text_surface.get_rect(center=rect.center)
        surface.blit(text_surface, text_rect)
        
    def draw(self):
        """绘制游戏画面"""
        # 背景
        self.screen.fill(self.LIGHT_GRAY)
        
        if self.game_over:
            self.draw_game_over()
        else:
            self.draw_game()
        
        pygame.display.flip()
        
    def draw_game(self):
        """绘制游戏画面"""
        if self.current_question_index >= len(GAME_DATA['questions']):
            self.game_over = True
            return
            
        question = GAME_DATA['questions'][self.current_question_index]
        
        # 标题
        title_text = self.title_font.render("🎮 " + GAME_DATA['title'], True, self.BLACK)
        title_rect = title_text.get_rect(centerx=self.width // 2, y=30)
        self.screen.blit(title_text, title_rect)
        
        # 状态栏
        status_y = 80
        score_text = self.status_font.render(f"得分: {{self.score}}", True, self.BLACK)
        self.screen.blit(score_text, (20, status_y))
        
        lives_text = self.status_font.render(f"生命: {{'❤️' * self.lives}}", True, self.RED)
        lives_rect = lives_text.get_rect(centerx=self.width // 2, y=status_y)
        self.screen.blit(lives_text, lives_rect)
        
        hints_text = self.status_font.render(f"提示: {{self.hints}}", True, self.BLACK)
        hints_rect = hints_text.get_rect(right=self.width - 20, y=status_y)
        self.screen.blit(hints_text, hints_rect)
        
        # 进度条
        progress_y = 120
        progress_width = 300
        progress_height = 8
        progress_x = (self.width - progress_width) // 2
        
        pygame.draw.rect(self.screen, self.GRAY, 
                        (progress_x, progress_y, progress_width, progress_height), 
                        border_radius=4)
        
        progress_value = (self.current_question_index + 1) / len(GAME_DATA['questions'])
        progress_fill_width = int(progress_width * progress_value)
        pygame.draw.rect(self.screen, self.BLUE, 
                        (progress_x, progress_y, progress_fill_width, progress_height), 
                        border_radius=4)
        
        # 题目编号
        number_text = self.status_font.render(
            f"题目 {{self.current_question_index + 1}}/{{len(GAME_DATA['questions'])}}", 
            True, self.BLACK)
        number_rect = number_text.get_rect(centerx=self.width // 2, y=150)
        self.screen.blit(number_text, number_rect)
        
        # 汉字（大字体）
        char_text = self.question_font.render(question['question'], True, self.BLACK)
        char_rect = char_text.get_rect(centerx=self.width // 2, y=190)
        self.screen.blit(char_text, char_rect)
        
        # 选项按钮
        for i, (rect, option) in enumerate(zip(self.option_buttons, question['options'])):
            color = self.BLUE if self.selected_answer == i else self.WHITE
            self.draw_button(self.screen, rect, option, 
                           self.option_font, color, self.BLACK)
        
        # 提示按钮
        if self.hints > 0:
            self.draw_button(self.screen, self.hint_button, "💡 提示", 
                           self.status_font, self.GREEN, self.WHITE)
        
        # 提交按钮
        submit_color = self.BLUE if self.selected_answer is not None else self.GRAY
        self.draw_button(self.screen, self.submit_button, "提交", 
                       self.status_font, submit_color, self.WHITE)
        
    def draw_game_over(self):
        """绘制游戏结束画面"""
        # 游戏结束标题
        game_over_text = self.title_font.render("🎉 游戏结束！", True, self.BLACK)
        game_over_rect = game_over_text.get_rect(centerx=self.width // 2, y=100)
        self.screen.blit(game_over_text, game_over_rect)
        
        # 最终得分
        score_text = self.question_font.render(f"最终得分: {{self.score}}", True, self.BLACK)
        score_rect = score_text.get_rect(centerx=self.width // 2, y=200)
        self.screen.blit(score_text, score_rect)
        
        # 完成情况
        completed_text = self.status_font.render(
            f"完成题目: {{self.current_question_index}}/{{len(GAME_DATA['questions'])}}", 
            True, self.BLACK)
        completed_rect = completed_text.get_rect(centerx=self.width // 2, y=250)
        self.screen.blit(completed_text, completed_rect)
        
        # 结果
        if self.score >= GAME_DATA['game_config']['pass_score']:
            result_text = self.question_font.render("🎊 恭喜过关！", True, self.GREEN)
        else:
            result_text = self.question_font.render("😅 再接再厉！", True, self.RED)
        result_rect = result_text.get_rect(centerx=self.width // 2, y=300)
        self.screen.blit(result_text, result_rect)
        
        # 重新开始按钮
        self.draw_button(self.screen, self.restart_button, "重新开始", 
                       self.option_font, self.BLUE, self.WHITE)
        
    def handle_click(self, pos):
        """处理点击事件"""
        if self.game_over:
            if self.restart_button.collidepoint(pos):
                self.restart_game()
        else:
            # 检查选项按钮点击
            for i, rect in enumerate(self.option_buttons):
                if rect.collidepoint(pos):
                    self.selected_answer = i
                    return
            
            # 检查提示按钮点击
            if self.hints > 0 and self.hint_button.collidepoint(pos):
                self.use_hint()
                return
            
            # 检查提交按钮点击
            if self.selected_answer is not None and self.submit_button.collidepoint(pos):
                self.submit_answer()
                
    def use_hint(self):
        """使用提示"""
        if self.hints > 0:
            self.hints -= 1
            question = GAME_DATA['questions'][self.current_question_index]
            print(f"提示: 正确答案是 {{question['answer']}}")
            if 'meaning' in question:
                print(f"含义: {{question['meaning']}}")
            
    def submit_answer(self):
        """提交答案"""
        if self.selected_answer is None:
            return
            
        question = GAME_DATA['questions'][self.current_question_index]
        selected = question['options'][self.selected_answer]
        
        if selected == question['answer']:
            self.score += 10
            print("✅ 答对了！")
        else:
            self.lives -= 1
            print(f"❌ 答错了！正确答案是: {{question['answer']}}")
            
        if self.lives <= 0:
            self.game_over = True
        else:
            self.current_question_index += 1
            self.selected_answer = None
            
    def restart_game(self):
        """重新开始游戏"""
        self.score = 0
        self.current_question_index = 0
        self.lives = GAME_DATA['game_config']['lives']
        self.hints = GAME_DATA['game_config']['hints']
        self.game_over = False
        self.selected_answer = None
        
    def run(self):
        """运行游戏"""
        clock = pygame.time.Clock()
        running = True
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_click(event.pos)
            
            self.draw()
            clock.tick(60)
        
        pygame.quit()
        sys.exit()

# 主程序
if __name__ == "__main__":
    game = iOSChineseGame()
    game.run()
'''
    
    def _generate_ios_english_game(self, game_json: str) -> str:
        """生成iOS英语游戏代码"""
        return f'''import pygame
import sys
import json
import random
import math

# iOS游戏数据
GAME_DATA = {game_json}

class iOSEnglishGame:
    def __init__(self):
        pygame.init()
        
        # 设置iOS设备尺寸
        self.width = 375
        self.height = 667
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("🎮 " + GAME_DATA['title'])
        
        # 颜色定义
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.BLUE = (0, 122, 255)
        self.GREEN = (52, 199, 89)
        self.RED = (255, 59, 48)
        self.GRAY = (142, 142, 147)
        self.LIGHT_GRAY = (242, 242, 247)
        
        # 字体设置
        self.title_font = pygame.font.Font(None, 36)
        self.question_font = pygame.font.Font(None, 28)
        self.option_font = pygame.font.Font(None, 24)
        self.status_font = pygame.font.Font(None, 20)
        
        # 游戏状态
        self.score = 0
        self.current_question_index = 0
        self.lives = GAME_DATA['game_config']['lives']
        self.hints = GAME_DATA['game_config']['hints']
        self.game_over = False
        self.selected_answer = None
        
        # 按钮位置
        self.option_buttons = []
        self.hint_button = None
        self.submit_button = None
        self.restart_button = None
        
        self.setup_ui()
        
    def setup_ui(self):
        """设置用户界面"""
        # 计算按钮位置
        button_width = 300
        button_height = 50
        button_spacing = 15
        start_y = 250
        
        # 选项按钮
        self.option_buttons = []
        for i in range(4):
            x = (self.width - button_width) // 2
            y = start_y + i * (button_height + button_spacing)
            rect = pygame.Rect(x, y, button_width, button_height)
            self.option_buttons.append(rect)
        
        # 提示按钮
        self.hint_button = pygame.Rect(20, self.height - 120, 120, 40)
        
        # 提交按钮
        self.submit_button = pygame.Rect(self.width - 140, self.height - 120, 120, 40)
        
        # 重新开始按钮
        self.restart_button = pygame.Rect((self.width - 200) // 2, self.height - 100, 200, 50)
        
    def draw_rounded_rect(self, surface, rect, color, radius=10):
        """绘制圆角矩形"""
        pygame.draw.rect(surface, color, rect, border_radius=radius)
        
    def draw_button(self, surface, rect, text, font, color, text_color):
        """绘制按钮"""
        self.draw_rounded_rect(surface, rect, color)
        text_surface = font.render(text, True, text_color)
        text_rect = text_surface.get_rect(center=rect.center)
        surface.blit(text_surface, text_rect)
        
    def draw(self):
        """绘制游戏画面"""
        # 背景
        self.screen.fill(self.LIGHT_GRAY)
        
        if self.game_over:
            self.draw_game_over()
        else:
            self.draw_game()
        
        pygame.display.flip()
        
    def draw_game(self):
        """绘制游戏画面"""
        if self.current_question_index >= len(GAME_DATA['questions']):
            self.game_over = True
            return
            
        question = GAME_DATA['questions'][self.current_question_index]
        
        # 标题
        title_text = self.title_font.render("🎮 " + GAME_DATA['title'], True, self.BLACK)
        title_rect = title_text.get_rect(centerx=self.width // 2, y=30)
        self.screen.blit(title_text, title_rect)
        
        # 状态栏
        status_y = 80
        score_text = self.status_font.render(f"得分: {{self.score}}", True, self.BLACK)
        self.screen.blit(score_text, (20, status_y))
        
        lives_text = self.status_font.render(f"生命: {{'❤️' * self.lives}}", True, self.RED)
        lives_rect = lives_text.get_rect(centerx=self.width // 2, y=status_y)
        self.screen.blit(lives_text, lives_rect)
        
        hints_text = self.status_font.render(f"提示: {{self.hints}}", True, self.BLACK)
        hints_rect = hints_text.get_rect(right=self.width - 20, y=status_y)
        self.screen.blit(hints_text, hints_rect)
        
        # 进度条
        progress_y = 120
        progress_width = 300
        progress_height = 8
        progress_x = (self.width - progress_width) // 2
        
        pygame.draw.rect(self.screen, self.GRAY, 
                        (progress_x, progress_y, progress_width, progress_height), 
                        border_radius=4)
        
        progress_value = (self.current_question_index + 1) / len(GAME_DATA['questions'])
        progress_fill_width = int(progress_width * progress_value)
        pygame.draw.rect(self.screen, self.BLUE, 
                        (progress_x, progress_y, progress_fill_width, progress_height), 
                        border_radius=4)
        
        # 题目
        question_text = self.question_font.render(
            f"Q{{self.current_question_index + 1}}: {{question['question']}}", 
            True, self.BLACK)
        question_rect = question_text.get_rect(centerx=self.width // 2, y=160)
        self.screen.blit(question_text, question_rect)
        
        # 选项按钮
        for i, (rect, option) in enumerate(zip(self.option_buttons, question['options'])):
            color = self.BLUE if self.selected_answer == i else self.WHITE
            self.draw_button(self.screen, rect, option, 
                           self.option_font, color, self.BLACK)
        
        # 提示按钮
        if self.hints > 0:
            self.draw_button(self.screen, self.hint_button, "💡 提示", 
                           self.status_font, self.GREEN, self.WHITE)
        
        # 提交按钮
        submit_color = self.BLUE if self.selected_answer is not None else self.GRAY
        self.draw_button(self.screen, self.submit_button, "提交", 
                       self.status_font, submit_color, self.WHITE)
        
    def draw_game_over(self):
        """绘制游戏结束画面"""
        # 游戏结束标题
        game_over_text = self.title_font.render("🎉 Game Over!", True, self.BLACK)
        game_over_rect = game_over_text.get_rect(centerx=self.width // 2, y=100)
        self.screen.blit(game_over_text, game_over_rect)
        
        # 最终得分
        score_text = self.question_font.render(f"Final Score: {{self.score}}", True, self.BLACK)
        score_rect = score_text.get_rect(centerx=self.width // 2, y=200)
        self.screen.blit(score_text, score_rect)
        
        # 完成情况
        completed_text = self.status_font.render(
            f"Completed: {{self.current_question_index}}/{{len(GAME_DATA['questions'])}}", 
            True, self.BLACK)
        completed_rect = completed_text.get_rect(centerx=self.width // 2, y=250)
        self.screen.blit(completed_text, completed_rect)
        
        # 结果
        if self.score >= GAME_DATA['game_config']['pass_score']:
            result_text = self.question_font.render("🎊 Congratulations!", True, self.GREEN)
        else:
            result_text = self.question_font.render("😅 Try Again!", True, self.RED)
        result_rect = result_text.get_rect(centerx=self.width // 2, y=300)
        self.screen.blit(result_text, result_rect)
        
        # 重新开始按钮
        self.draw_button(self.screen, self.restart_button, "Restart", 
                       self.option_font, self.BLUE, self.WHITE)
        
    def handle_click(self, pos):
        """处理点击事件"""
        if self.game_over:
            if self.restart_button.collidepoint(pos):
                self.restart_game()
        else:
            # 检查选项按钮点击
            for i, rect in enumerate(self.option_buttons):
                if rect.collidepoint(pos):
                    self.selected_answer = i
                    return
            
            # 检查提示按钮点击
            if self.hints > 0 and self.hint_button.collidepoint(pos):
                self.use_hint()
                return
            
            # 检查提交按钮点击
            if self.selected_answer is not None and self.submit_button.collidepoint(pos):
                self.submit_answer()
                
    def use_hint(self):
        """使用提示"""
        if self.hints > 0:
            self.hints -= 1
            question = GAME_DATA['questions'][self.current_question_index]
            print(f"Hint: Correct answer is {{question['answer']}}")
            if 'translation' in question:
                print(f"Translation: {{question['translation']}}")
            if 'explanation' in question:
                print(f"Explanation: {{question['explanation']}}")
            
    def submit_answer(self):
        """提交答案"""
        if self.selected_answer is None:
            return
            
        question = GAME_DATA['questions'][self.current_question_index]
        selected = question['options'][self.selected_answer]
        
        if selected == question['answer']:
            self.score += 10
            print("✅ Correct!")
        else:
            self.lives -= 1
            print(f"❌ Wrong! Correct answer is: {{question['answer']}}")
            
        if self.lives <= 0:
            self.game_over = True
        else:
            self.current_question_index += 1
            self.selected_answer = None
            
    def restart_game(self):
        """重新开始游戏"""
        self.score = 0
        self.current_question_index = 0
        self.lives = GAME_DATA['game_config']['lives']
        self.hints = GAME_DATA['game_config']['hints']
        self.game_over = False
        self.selected_answer = None
        
    def run(self):
        """运行游戏"""
        clock = pygame.time.Clock()
        running = True
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_click(event.pos)
            
            self.draw()
            clock.tick(60)
        
        pygame.quit()
        sys.exit()

# 主程序
if __name__ == "__main__":
    game = iOSEnglishGame()
    game.run()
'''
    
    def _generate_ios_scene_game(self, scene_json: str) -> str:
        """生成iOS场景游戏代码"""
        return f'''import pygame
import sys
import json
import random
import math

# iOS场景数据
SCENE_DATA = {scene_json}

class iOSSceneGame:
    def __init__(self):
        pygame.init()
        
        # 设置iOS设备尺寸
        self.width = 375
        self.height = 667
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("🎮 " + SCENE_DATA['title'])
        
        # 颜色定义
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.BLUE = (0, 122, 255)
        self.GREEN = (52, 199, 89)
        self.RED = (255, 59, 48)
        self.GRAY = (142, 142, 147)
        self.LIGHT_GRAY = (242, 242, 247)
        
        # 字体设置
        self.title_font = pygame.font.Font(None, 36)
        self.subtitle_font = pygame.font.Font(None, 28)
        self.text_font = pygame.font.Font(None, 24)
        self.button_font = pygame.font.Font(None, 20)
        
        # 游戏状态
        self.score = 0
        
        # 滚动位置
        self.scroll_offset = 0
        self.max_scroll = 0
        
        # 按钮
        self.character_buttons = []
        self.object_buttons = []
        self.reset_button = None
        
        self.setup_ui()
        
    def setup_ui(self):
        """设置用户界面"""
        # 计算最大滚动高度
        self.calculate_max_scroll()
        
        # 重置按钮
        self.reset_button = pygame.Rect((self.width - 200) // 2, self.height - 60, 200, 40)
        
        # 生成互动按钮
        self.generate_interaction_buttons()
        
    def calculate_max_scroll(self):
        """计算最大滚动高度"""
        base_height = 200  # 标题和描述区域
        info_height = 0
        
        # 角色信息高度
        if SCENE_DATA['scene_elements']['characters']:
            info_height += 50  # 角色标题
            info_height += len(SCENE_DATA['scene_elements']['characters']) * 80  # 每个角色信息
        
        # 环境信息高度
        info_height += 50  # 环境标题
        info_height += 100  # 环境信息
        
        # 物体信息高度
        if SCENE_DATA['scene_elements']['objects']:
            info_height += 50  # 物体标题
            info_height += len(SCENE_DATA['scene_elements']['objects']) * 60  # 每个物体信息
        
        self.max_scroll = max(0, info_height - (self.height - 250))
        
    def generate_interaction_buttons(self):
        """生成互动按钮"""
        self.character_buttons = []
        self.object_buttons = []
        
        # 角色互动按钮
        if SCENE_DATA['scene_elements']['characters']:
            start_y = 200
            for i, char in enumerate(SCENE_DATA['scene_elements']['characters']):
                x = 20
                y = start_y + i * 60
                rect = pygame.Rect(x, y, self.width - 40, 50)
                self.character_buttons.append((rect, char))
        
        # 物体互动按钮
        if SCENE_DATA['scene_elements']['objects']:
            start_y = 200 + len(self.character_buttons) * 60
            for i, obj in enumerate(SCENE_DATA['scene_elements']['objects']):
                x = 20
                y = start_y + i * 60
                rect = pygame.Rect(x, y, self.width - 40, 50)
                self.object_buttons.append((rect, obj))
        
    def draw_rounded_rect(self, surface, rect, color, radius=10):
        """绘制圆角矩形"""
        pygame.draw.rect(surface, color, rect, border_radius=radius)
        
    def draw_button(self, surface, rect, text, font, color, text_color):
        """绘制按钮"""
        self.draw_rounded_rect(surface, rect, color)
        text_surface = font.render(text, True, text_color)
        text_rect = text_surface.get_rect(center=rect.center)
        surface.blit(text_surface, text_rect)
        
    def draw(self):
        """绘制游戏画面"""
        # 背景
        self.screen.fill(self.LIGHT_GRAY)
        
        # 标题
        title_text = self.title_font.render("🎮 " + SCENE_DATA['title'], True, self.BLACK)
        title_rect = title_text.get_rect(centerx=self.width // 2, y=20)
        self.screen.blit(title_text, title_rect)
        
        # 描述
        desc_text = self.text_font.render(SCENE_DATA['description'][:50] + "...", True, self.BLACK)
        desc_rect = desc_text.get_rect(centerx=self.width // 2, y=60)
        self.screen.blit(desc_text, desc_rect)
        
        # 动作逻辑
        logic_text = self.text_font.render(SCENE_DATA['action_logic'][:50] + "...", True, self.BLACK)
        logic_rect = logic_text.get_rect(centerx=self.width // 2, y=90)
        self.screen.blit(logic_text, logic_rect)
        
        # 得分
        score_text = self.subtitle_font.render(f"Score: {{self.score}}", True, self.BLUE)
        score_rect = score_text.get_rect(centerx=self.width // 2, y=130)
        self.screen.blit(score_text, score_rect)
        
        # 场景信息（可滚动）
        self.draw_scene_info()
        
        # 互动按钮
        self.draw_interaction_buttons()
        
        # 重置按钮
        self.draw_button(self.screen, self.reset_button, "🔄 Reset", 
                       self.button_font, self.BLUE, self.WHITE)
        
        pygame.display.flip()
        
    def draw_scene_info(self):
        """绘制场景信息"""
        y_offset = 200 - self.scroll_offset
        
        # 角色信息
        if SCENE_DATA['scene_elements']['characters']:
            # 角色标题
            char_title = self.subtitle_font.render("👥 Characters", True, self.BLACK)
            char_title_rect = char_title.get_rect(x=20, y=y_offset)
            if self.is_visible(char_title_rect):
                self.screen.blit(char_title, char_title_rect)
            y_offset += 40
            
            # 角色详情
            for char in SCENE_DATA['scene_elements']['characters']:
                char_text = self.text_font.render(f"• {{char['name']}}: {{char['description']}}", True, self.BLACK)
                char_rect = char_text.get_rect(x=40, y=y_offset)
                if self.is_visible(char_rect):
                    self.screen.blit(char_text, char_rect)
                y_offset += 30
                
                abilities_text = self.button_font.render(f"  Abilities: {{', '.join(char['abilities'])}}", True, self.GRAY)
                abilities_rect = abilities_text.get_rect(x=40, y=y_offset)
                if self.is_visible(abilities_rect):
                    self.screen.blit(abilities_text, abilities_rect)
                y_offset += 20
        
        # 环境信息
        env = SCENE_DATA['scene_elements']['environment']
        # 环境标题
        env_title = self.subtitle_font.render("🌍 Environment", True, self.BLACK)
        env_title_rect = env_title.get_rect(x=20, y=y_offset)
        if self.is_visible(env_title_rect):
            self.screen.blit(env_title, env_title_rect)
        y_offset += 40
        
        # 环境详情
        env_texts = [
            f"Setting: {{env['setting']}}",
            f"Background: {{env['background']}}",
            f"Atmosphere: {{env['atmosphere']}}"
        ]
        
        for env_text in env_texts:
            text_surface = self.text_font.render(env_text, True, self.BLACK)
            text_rect = text_surface.get_rect(x=40, y=y_offset)
            if self.is_visible(text_rect):
                self.screen.blit(text_surface, text_rect)
            y_offset += 25
        
        # 物体信息
        if SCENE_DATA['scene_elements']['objects']:
            # 物体标题
            obj_title = self.subtitle_font.render("🎪 Objects", True, self.BLACK)
            obj_title_rect = obj_title.get_rect(x=20, y=y_offset)
            if self.is_visible(obj_title_rect):
                self.screen.blit(obj_title, obj_title_rect)
            y_offset += 40
            
            # 物体详情
            for obj in SCENE_DATA['scene_elements']['objects']:
                obj_text = self.text_font.render(f"• {{obj['name']}}: {{obj['description']}}", True, self.BLACK)
                obj_rect = obj_text.get_rect(x=40, y=y_offset)
                if self.is_visible(obj_rect):
                    self.screen.blit(obj_text, obj_rect)
                y_offset += 30
                
                interaction_text = self.button_font.render(f"  Interaction: {{obj['interaction']}}", True, self.GRAY)
                interaction_rect = interaction_text.get_rect(x=40, y=y_offset)
                if self.is_visible(interaction_rect):
                    self.screen.blit(interaction_text, interaction_rect)
                y_offset += 20
        
        # 滚动指示器
        if self.max_scroll > 0:
            scroll_bar_height = max(20, (self.height - 250) * ((self.height - 250) / (self.height - 250 + self.max_scroll)))
            scroll_bar_y = 200 + (self.scroll_offset / self.max_scroll) * ((self.height - 250) - scroll_bar_height)
            pygame.draw.rect(self.screen, self.GRAY, 
                           (self.width - 10, scroll_bar_y, 5, scroll_bar_height), 
                           border_radius=2)
        
    def draw_interaction_buttons(self):
        """绘制互动按钮"""
        # 角色互动按钮
        for rect, char in self.character_buttons:
            adjusted_rect = pygame.Rect(rect.x, rect.y - self.scroll_offset, rect.width, rect.height)
            if self.is_visible(adjusted_rect):
                self.draw_button(self.screen, adjusted_rect, f"👤 Interact with {{char['name']}}", 
                               self.button_font, self.GREEN, self.WHITE)
        
        # 物体互动按钮
        for rect, obj in self.object_buttons:
            adjusted_rect = pygame.Rect(rect.x, rect.y - self.scroll_offset, rect.width, rect.height)
            if self.is_visible(adjusted_rect):
                self.draw_button(self.screen, adjusted_rect, f"🎪 Use {{obj['name']}}", 
                               self.button_font, self.BLUE, self.WHITE)
        
    def is_visible(self, rect):
        """检查元素是否可见"""
        return rect.bottom > 200 and rect.top < self.height - 100
        
    def handle_click(self, pos):
        """处理点击事件"""
        # 检查重置按钮
        if self.reset_button.collidepoint(pos):
            self.reset_game()
            return
        
        # 检查角色互动按钮
        for rect, char in self.character_buttons:
            adjusted_rect = pygame.Rect(rect.x, rect.y - self.scroll_offset, rect.width, rect.height)
            if adjusted_rect.collidepoint(pos):
                self.interact_with_character(char)
                return
        
        # 检查物体互动按钮
        for rect, obj in self.object_buttons:
            adjusted_rect = pygame.Rect(rect.x, rect.y - self.scroll_offset, rect.width, rect.height)
            if adjusted_rect.collidepoint(pos):
                self.interact_with_object(obj)
                return
    
    def interact_with_character(self, character):
        """与角色互动"""
        self.score += 5
        print(f"Interacted with {{character['name']}}! +5 points")
        
    def interact_with_object(self, obj):
        """与物体互动"""
        self.score += 3
        print(f"Used {{obj['name']}}! +3 points")
        
    def reset_game(self):
        """重置游戏"""
        self.score = 0
        self.scroll_offset = 0
        print("Game reset!")
        
    def handle_scroll(self, direction):
        """处理滚动"""
        if direction > 0:  # 向下滚动
            self.scroll_offset = min(self.scroll_offset + 30, self.max_scroll)
        else:  # 向上滚动
            self.scroll_offset = max(self.scroll_offset - 30, 0)
        
    def run(self):
        """运行游戏"""
        clock = pygame.time.Clock()
        running = True
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_click(event.pos)
                elif event.type == pygame.MOUSEWHEEL:
                    self.handle_scroll(event.y)
            
            self.draw()
            clock.tick(60)
        
        pygame.quit()
        sys.exit()

# 主程序
if __name__ == "__main__":
    game = iOSSceneGame()
    game.run()
'''
    
    def generate_mobile_game(self, game_data: Dict[str, Any], game_type: str, platform: str) -> Optional[str]:
        """生成移动端游戏"""
        try:
            if platform == "macos":
                game_code = self.generate_macos_game_code(game_data, game_type)
            elif platform == "ios":
                game_code = self.generate_ios_game_code(game_data, game_type)
            else:
                return None
            
            # 创建临时文件
            with tempfile.NamedTemporaryFile(mode='w', suffix=f'_{platform}_{game_type}_game.py', delete=False, encoding='utf-8') as f:
                f.write(game_code)
                temp_file = f.name
            
            logger.info(f"{{platform}}游戏文件已保存到: {{temp_file}}")
            return temp_file
            
        except Exception as e:
            logger.error(f"生成{{platform}}游戏时出错: {{str(e)}}")
            return None

# 全局实例
mobile_game_generator = MobileGameGenerator()

def generate_mobile_game(game_data: Dict[str, Any], game_type: str, platform: str) -> Optional[str]:
    """生成移动端游戏"""
    return mobile_game_generator.generate_mobile_game(game_data, game_type, platform)