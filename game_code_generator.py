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

logger = setup_logger("game_code_generator")

class GameCodeGenerator:
    """游戏代码生成器"""
    
    def __init__(self):
        self.math_generator = MathGameGenerator()
        self.chinese_generator = ChineseGameGenerator()
        self.english_generator = EnglishGameGenerator()
        self.scene_generator = GameSceneGenerator()
        
    def generate_math_game_code(self, game_data: Dict[str, Any]) -> str:
        """生成数学游戏代码"""
        game_json = json.dumps(game_data, ensure_ascii=False)
        
        code = f'''import streamlit as st
import random
import json

# 游戏数据
GAME_DATA = {game_json}

class MathGame:
    def __init__(self, game_data):
        self.game_data = game_data
        self.score = 0
        self.current_problem_index = 0
        self.lives = game_data['game_config']['lives']
        self.hints = game_data['game_config']['hints']
        self.game_over = False
        
    def start_game(self):
        st.title("🎮 " + self.game_data['title'])
        
        if self.game_over:
            self.show_game_over()
        else:
            self.show_current_problem()
            
    def show_current_problem(self):
        if self.current_problem_index >= len(self.game_data['problems']):
            self.show_game_over()
            return
            
        problem = self.game_data['problems'][self.current_problem_index]
        
        # 显示进度
        progress = (self.current_problem_index + 1) / len(self.game_data['problems'])
        st.progress(progress)
        st.write(f"题目 {{self.current_problem_index + 1}}/{{len(self.game_data['problems'])}}")
        
        # 显示游戏状态
        col1, col2, col3 = st.columns(3)
        with col1:
            st.write(f"得分: {{self.score}}")
        with col2:
            st.write(f"生命: {{'❤️' * self.lives}}")
        with col3:
            st.write(f"提示: {{self.hints}}")
        
        # 显示题目
        st.subheader(f"题目: {{problem['question']}}")
        
        # 显示选项
        options = problem['options']
        selected_answer = st.radio("选择答案:", options, key=f"problem_{{self.current_problem_index}}")
        
        # 提示按钮
        if self.hints > 0:
            if st.button("💡 使用提示"):
                self.hints -= 1
                st.info(f"提示: 正确答案是 {{problem['answer']}}")
                st.experimental_rerun()
        
        # 提交答案
        if st.button("提交答案"):
            self.check_answer(selected_answer, problem['answer'])
            
    def check_answer(self, selected_answer, correct_answer):
        if selected_answer == correct_answer:
            self.score += 10
            st.success("✅ 答对了！")
        else:
            self.lives -= 1
            st.error(f"❌ 答错了！正确答案是: {{correct_answer}}")
            
        if self.lives <= 0:
            self.game_over = True
        else:
            self.current_problem_index += 1
            
        st.experimental_rerun()
        
    def show_game_over(self):
        st.title("🎉 游戏结束！")
        st.write(f"最终得分: {{self.score}}")
        st.write(f"完成题目: {{self.current_problem_index}}/{{len(self.game_data['problems'])}}")
        
        if self.score >= self.game_data['game_config']['pass_score']:
            st.success("🎊 恭喜过关！")
        else:
            st.warning("😅 再接再厉！")
            
        if st.button("重新开始"):
            self.__init__(self.game_data)
            st.experimental_rerun()

# 运行游戏
if __name__ == "__main__":
    game = MathGame(GAME_DATA)
    game.start_game()
'''
        return code
    
    def generate_chinese_game_code(self, game_data: Dict[str, Any]) -> str:
        """生成汉字游戏代码"""
        game_json = json.dumps(game_data, ensure_ascii=False)
        
        code = f'''import streamlit as st
import random
import json

# 游戏数据
GAME_DATA = {game_json}

class ChineseGame:
    def __init__(self, game_data):
        self.game_data = game_data
        self.score = 0
        self.current_question_index = 0
        self.lives = game_data['game_config']['lives']
        self.hints = game_data['game_config']['hints']
        self.game_over = False
        
    def start_game(self):
        st.title("🎮 " + self.game_data['title'])
        
        if self.game_over:
            self.show_game_over()
        else:
            self.show_current_question()
            
    def show_current_question(self):
        if self.current_question_index >= len(self.game_data['questions']):
            self.show_game_over()
            return
            
        question = self.game_data['questions'][self.current_question_index]
        
        # 显示进度
        progress = (self.current_question_index + 1) / len(self.game_data['questions'])
        st.progress(progress)
        st.write(f"题目 {{self.current_question_index + 1}}/{{len(self.game_data['questions'])}}")
        
        # 显示游戏状态
        col1, col2, col3 = st.columns(3)
        with col1:
            st.write(f"得分: {{self.score}}")
        with col2:
            st.write(f"生命: {{'❤️' * self.lives}}")
        with col3:
            st.write(f"提示: {{self.hints}}")
        
        # 显示题目
        st.subheader(f"题目: {{question['question']}}")
        
        # 显示选项
        options = question['options']
        selected_answer = st.radio("选择答案:", options, key=f"question_{{self.current_question_index}}")
        
        # 提示按钮
        if self.hints > 0:
            if st.button("💡 使用提示"):
                self.hints -= 1
                st.info(f"提示: 正确答案是 {{question['answer']}}")
                if 'meaning' in question:
                    st.info(f"含义: {{question['meaning']}}")
                st.experimental_rerun()
        
        # 提交答案
        if st.button("提交答案"):
            self.check_answer(selected_answer, question['answer'])
            
    def check_answer(self, selected_answer, correct_answer):
        if selected_answer == correct_answer:
            self.score += 10
            st.success("✅ 答对了！")
        else:
            self.lives -= 1
            st.error(f"❌ 答错了！正确答案是: {{correct_answer}}")
            
        if self.lives <= 0:
            self.game_over = True
        else:
            self.current_question_index += 1
            
        st.experimental_rerun()
        
    def show_game_over(self):
        st.title("🎉 游戏结束！")
        st.write(f"最终得分: {{self.score}}")
        st.write(f"完成题目: {{self.current_question_index}}/{{len(self.game_data['questions'])}}")
        
        if self.score >= self.game_data['game_config']['pass_score']:
            st.success("🎊 恭喜过关！")
        else:
            st.warning("😅 再接再厉！")
            
        if st.button("重新开始"):
            self.__init__(self.game_data)
            st.experimental_rerun()

# 运行游戏
if __name__ == "__main__":
    game = ChineseGame(GAME_DATA)
    game.start_game()
'''
        return code
    
    def generate_english_game_code(self, game_data: Dict[str, Any]) -> str:
        """生成英语游戏代码"""
        game_json = json.dumps(game_data, ensure_ascii=False)
        
        code = f'''import streamlit as st
import random
import json

# 游戏数据
GAME_DATA = {game_json}

class EnglishGame:
    def __init__(self, game_data):
        self.game_data = game_data
        self.score = 0
        self.current_question_index = 0
        self.lives = game_data['game_config']['lives']
        self.hints = game_data['game_config']['hints']
        self.game_over = False
        
    def start_game(self):
        st.title("🎮 " + self.game_data['title'])
        
        if self.game_over:
            self.show_game_over()
        else:
            self.show_current_question()
            
    def show_current_question(self):
        if self.current_question_index >= len(self.game_data['questions']):
            self.show_game_over()
            return
            
        question = self.game_data['questions'][self.current_question_index]
        
        # 显示进度
        progress = (self.current_question_index + 1) / len(self.game_data['questions'])
        st.progress(progress)
        st.write(f"题目 {{self.current_question_index + 1}}/{{len(self.game_data['questions'])}}")
        
        # 显示游戏状态
        col1, col2, col3 = st.columns(3)
        with col1:
            st.write(f"得分: {{self.score}}")
        with col2:
            st.write(f"生命: {{'❤️' * self.lives}}")
        with col3:
            st.write(f"提示: {{self.hints}}")
        
        # 显示题目
        st.subheader(f"题目: {{question['question']}}")
        
        # 显示选项
        options = question['options']
        selected_answer = st.radio("选择答案:", options, key=f"question_{{self.current_question_index}}")
        
        # 提示按钮
        if self.hints > 0:
            if st.button("💡 使用提示"):
                self.hints -= 1
                st.info(f"提示: 正确答案是 {{question['answer']}}")
                if 'translation' in question:
                    st.info(f"翻译: {{question['translation']}}")
                if 'explanation' in question:
                    st.info(f"解释: {{question['explanation']}}")
                st.experimental_rerun()
        
        # 提交答案
        if st.button("提交答案"):
            self.check_answer(selected_answer, question['answer'])
            
    def check_answer(self, selected_answer, correct_answer):
        if selected_answer == correct_answer:
            self.score += 10
            st.success("✅ 答对了！")
        else:
            self.lives -= 1
            st.error(f"❌ 答错了！正确答案是: {{correct_answer}}")
            
        if self.lives <= 0:
            self.game_over = True
        else:
            self.current_question_index += 1
            
        st.experimental_rerun()
        
    def show_game_over(self):
        st.title("🎉 游戏结束！")
        st.write(f"最终得分: {{self.score}}")
        st.write(f"完成题目: {{self.current_question_index}}/{{len(self.game_data['questions'])}}")
        
        if self.score >= self.game_data['game_config']['pass_score']:
            st.success("🎊 恭喜过关！")
        else:
            st.warning("😅 再接再厉！")
            
        if st.button("重新开始"):
            self.__init__(self.game_data)
            st.experimental_rerun()

# 运行游戏
if __name__ == "__main__":
    game = EnglishGame(GAME_DATA)
    game.start_game()
'''
        return code
    
    def generate_scene_game_code(self, scene_data: Dict[str, Any]) -> str:
        """生成场景游戏代码"""
        scene_json = json.dumps(scene_data, ensure_ascii=False)
        
        code = f'''import streamlit as st
import json
import random

# 场景数据
SCENE_DATA = {scene_json}

class SceneGame:
    def __init__(self, scene_data):
        self.scene_data = scene_data
        self.score = 0
        self.game_state = "playing"
        
    def start_game(self):
        st.title("🎮 " + self.scene_data['title'])
        
        # 显示场景描述
        st.write(f"**场景描述:** {{self.scene_data['description']}}")
        st.write(f"**动作逻辑:** {{self.scene_data['action_logic']}}")
        
        # 显示场景元素
        with st.expander("场景详情"):
            st.markdown(self.generate_scene_info())
        
        # 简单的交互演示
        st.subheader("🎯 互动区域")
        
        # 根据场景元素创建简单的互动
        if self.scene_data['scene_elements']['characters']:
            st.write("角色互动:")
            for char in self.scene_data['scene_elements']['characters']:
                if st.button(f"与 {{char['name']}} 互动"):
                    st.success(f"你与 {{char['name']}} 互动了！")
                    self.score += 5
                    
        if self.scene_data['scene_elements']['objects']:
            st.write("物体互动:")
            for obj in self.scene_data['scene_elements']['objects']:
                if st.button(f"使用 {{obj['name']}}"):
                    st.success(f"你使用了 {{obj['name']}}！")
                    self.score += 3
        
        # 显示得分
        st.write(f"当前得分: {{self.score}}")
        
        # 重置按钮
        if st.button("重置游戏"):
            self.__init__(self.scene_data)
            st.experimental_rerun()
    
    def generate_scene_info(self):
        info = """
## 场景元素

### 角色
"""
        for char in self.scene_data['scene_elements']['characters']:
            info += f"- **{{char['name']}}**: {{char['description']}} (能力: {{', '.join(char['abilities'])}})\\n"
        
        info += f"""
### 环境
- **设置**: {{self.scene_data['scene_elements']['environment']['setting']}}
- **背景**: {{self.scene_data['scene_elements']['environment']['background']}}
- **氛围**: {{self.scene_data['scene_elements']['environment']['atmosphere']}}

### 物体
"""
        for obj in self.scene_data['scene_elements']['objects']:
            info += f"- **{{obj['name']}}**: {{obj['description']}} (交互: {{obj['interaction']}})\\n"
        
        return info

# 运行游戏
if __name__ == "__main__":
    game = SceneGame(SCENE_DATA)
    game.start_game()
'''
        return code
    
    def run_game(self, game_code: str, game_type: str) -> Optional[str]:
        """运行游戏并返回临时文件路径"""
        try:
            # 创建临时文件
            with tempfile.NamedTemporaryFile(mode='w', suffix=f'_{game_type}_game.py', delete=False, encoding='utf-8') as f:
                f.write(game_code)
                temp_file = f.name
            
            logger.info(f"游戏文件已保存到: {{temp_file}}")
            
            return temp_file
            
        except Exception as e:
            logger.error(f"运行游戏时出错: {{str(e)}}")
            return None

# 全局实例
game_code_generator = GameCodeGenerator()

def generate_and_run_game(game_data: Dict[str, Any], game_type: str) -> Optional[str]:
    """生成并运行游戏"""
    generator = GameCodeGenerator()
    
    if game_type == "math":
        game_code = generator.generate_math_game_code(game_data)
    elif game_type == "chinese":
        game_code = generator.generate_chinese_game_code(game_data)
    elif game_type == "english":
        game_code = generator.generate_english_game_code(game_data)
    elif game_type == "scene":
        game_code = generator.generate_scene_game_code(game_data)
    else:
        return None
    
    return generator.run_game(game_code, game_type)