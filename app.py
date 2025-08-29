import streamlit as st
import os
import sys
import json
from dotenv import load_dotenv

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config.settings import Config
from utils.logger import setup_logger
from agents.game_agent import GameAgent
from utils.ai_manager import AIProviderManager
from games.math_game import MathGameGenerator
from games.chinese_game import ChineseGameGenerator
from games.english_game import EnglishGameGenerator
from games.scene_generator import GameSceneGenerator

# 加载环境变量
load_dotenv()

# 设置日志
logger = setup_logger()

# 初始化游戏智能体和AI管理器
game_agent = GameAgent()
ai_manager = AIProviderManager()
math_game_generator = MathGameGenerator()
chinese_game_generator = ChineseGameGenerator()
english_game_generator = EnglishGameGenerator()
scene_generator = GameSceneGenerator()

def main():
    """主应用函数"""
    st.set_page_config(
        page_title=Config.APP_NAME,
        page_icon="🎮",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # 验证配置
    if not Config.validate_config():
        st.error("请配置至少一个AI提供商的API密钥")
        st.info("请复制 .env.example 为 .env 并填入相应的API密钥")
        return
    
    # 应用标题
    st.title("🎮 游戏开发智能体")
    st.markdown("---")
    
    # 侧边栏
    with st.sidebar:
        st.header("游戏类型选择")
        game_type = st.selectbox(
            "选择游戏类型",
            ["数字游戏", "汉字游戏", "英语游戏", "自定义游戏场景"]
        )
        
        st.header("游戏设置")
        difficulty = st.selectbox(
            "难度级别",
            ["简单", "中等", "困难"]
        )
        
        age_group = st.selectbox(
            "适合年龄",
            ["3-6岁", "7-10岁", "11-14岁"]
        )
    
    # 主内容区域
    if game_type == "数字游戏":
        st.subheader("🔢 数字游戏开发")
        st.write("帮助开发数字加减乘除学习游戏")
        
        with st.form("math_game_form"):
            game_title = st.text_input("游戏标题")
            math_operation = st.selectbox(
                "数学运算类型",
                ["加法", "减法", "乘法", "除法", "混合运算"]
            )
            number_range = st.slider("数字范围", 1, 100, (1, 20))
            
            if st.form_submit_button("生成数字游戏"):
                if game_title:
                    with st.spinner("正在生成数字游戏..."):
                        # 生成游戏数据
                        game_data = math_game_generator.create_math_game(
                            title=game_title,
                            operation=math_operation,
                            difficulty=difficulty,
                            age_group=age_group
                        )
                        
                        # 显示游戏说明
                        st.success(f"✅ 数字游戏 '{game_title}' 生成成功！")
                        
                        # 显示游戏预览
                        with st.expander("游戏预览"):
                            st.markdown(math_game_generator.generate_game_instructions(game_data))
                            
                            # 显示示例题目
                            st.subheader("示例题目")
                            if game_data['problems']:
                                sample_problem = game_data['problems'][0]
                                st.write(f"题目: {sample_problem['question']}")
                                st.write(f"选项: {', '.join(map(str, sample_problem['options']))}")
                                st.write(f"正确答案: {sample_problem['answer']}")
                        
                        # 存储游戏数据供下载
                        st.session_state.current_math_game = game_data
                        st.session_state.current_math_game_title = game_title
                else:
                    st.warning("请输入游戏标题")
        
        # 在表单外显示下载按钮
        if 'current_math_game' in st.session_state and st.session_state.current_math_game:
            game_json = json.dumps(st.session_state.current_math_game, ensure_ascii=False, indent=2)
            st.download_button(
                label="下载游戏数据",
                data=game_json,
                file_name=f"{st.session_state.current_math_game_title}.json",
                mime="application/json"
            )
    
    elif game_type == "汉字游戏":
        st.subheader("📝 汉字游戏开发")
        st.write("帮助开发汉字学习游戏")
        
        with st.form("chinese_game_form"):
            game_title = st.text_input("游戏标题")
            character_type = st.selectbox(
                "汉字类型",
                ["基础汉字", "常用词语", "成语", "古诗词"]
            )
            
            if st.form_submit_button("生成汉字游戏"):
                if game_title:
                    with st.spinner("正在生成汉字游戏..."):
                        # 生成游戏数据
                        game_data = chinese_game_generator.create_chinese_game(
                            title=game_title,
                            character_type=character_type,
                            difficulty=difficulty,
                            age_group=age_group
                        )
                        
                        # 显示游戏说明
                        st.success(f"✅ 汉字游戏 '{game_title}' 生成成功！")
                        
                        # 显示游戏预览
                        with st.expander("游戏预览"):
                            st.markdown(chinese_game_generator.generate_game_instructions(game_data))
                            
                            # 显示示例题目
                            st.subheader("示例题目")
                            if game_data['questions']:
                                sample_question = game_data['questions'][0]
                                st.write(f"题目: {sample_question['question']}")
                                st.write(f"选项: {', '.join(sample_question['options'])}")
                                st.write(f"正确答案: {sample_question['answer']}")
                                if 'meaning' in sample_question:
                                    st.write(f"含义: {sample_question['meaning']}")
                        
                        # 存储游戏数据供下载
                        st.session_state.current_chinese_game = game_data
                        st.session_state.current_chinese_game_title = game_title
                else:
                    st.warning("请输入游戏标题")
            
            # 在表单外显示下载按钮
        if 'current_chinese_game' in st.session_state and st.session_state.current_chinese_game:
            game_json = json.dumps(st.session_state.current_chinese_game, ensure_ascii=False, indent=2)
            st.download_button(
                label="下载游戏数据",
                data=game_json,
                file_name=f"{st.session_state.current_chinese_game_title}.json",
                mime="application/json"
            )
    
    elif game_type == "英语游戏":
        st.subheader("🔤 英语游戏开发")
        st.write("帮助开发英语学习游戏")
        
        with st.form("english_game_form"):
            game_title = st.text_input("游戏标题")
            english_type = st.selectbox(
                "英语学习类型",
                ["字母学习", "单词记忆", "简单对话", "语法练习"]
            )
            
            if st.form_submit_button("生成英语游戏"):
                if game_title:
                    with st.spinner("正在生成英语游戏..."):
                        # 生成游戏数据
                        game_data = english_game_generator.create_english_game(
                            title=game_title,
                            english_type=english_type,
                            difficulty=difficulty,
                            age_group=age_group
                        )
                        
                        # 显示游戏说明
                        st.success(f"✅ 英语游戏 '{game_title}' 生成成功！")
                        
                        # 显示游戏预览
                        with st.expander("游戏预览"):
                            st.markdown(english_game_generator.generate_game_instructions(game_data))
                            
                            # 显示示例题目
                            st.subheader("示例题目")
                            if game_data['questions']:
                                sample_question = game_data['questions'][0]
                                st.write(f"题目: {sample_question['question']}")
                                st.write(f"选项: {', '.join(sample_question['options'])}")
                                st.write(f"正确答案: {sample_question['answer']}")
                                if 'translation' in sample_question:
                                    st.write(f"翻译: {sample_question['translation']}")
                                if 'explanation' in sample_question:
                                    st.write(f"解释: {sample_question['explanation']}")
                        
                        # 存储游戏数据供下载
                        st.session_state.current_english_game = game_data
                        st.session_state.current_english_game_title = game_title
                else:
                    st.warning("请输入游戏标题")
            
            # 在表单外显示下载按钮
        if 'current_english_game' in st.session_state and st.session_state.current_english_game:
            game_json = json.dumps(st.session_state.current_english_game, ensure_ascii=False, indent=2)
            st.download_button(
                label="下载游戏数据",
                data=game_json,
                file_name=f"{st.session_state.current_english_game_title}.json",
                mime="application/json"
            )
    
    elif game_type == "自定义游戏场景":
        st.subheader("🎨 自定义游戏场景")
        st.write("根据指定的动作逻辑生成游戏场景")
        
        with st.form("custom_game_form"):
            game_title = st.text_input("游戏标题")
            game_description = st.text_area("游戏描述")
            action_logic = st.text_area("动作逻辑描述")
            
            if st.form_submit_button("生成自定义游戏"):
                if game_title and game_description:
                    with st.spinner("正在生成自定义游戏场景..."):
                        # 生成场景数据
                        scene_data = scene_generator.generate_game_scene(
                            title=game_title,
                            description=game_description,
                            action_logic=action_logic,
                            age_group=age_group
                        )
                        
                        # 显示场景说明
                        st.success(f"✅ 自定义游戏场景 '{game_title}' 生成成功！")
                        
                        # 显示场景详情
                        with st.expander("场景详情"):
                            st.markdown(scene_generator.generate_scene_instructions(scene_data))
                        
                        # 存储场景数据供下载
                        st.session_state.current_scene = scene_data
                        st.session_state.current_scene_title = game_title
                else:
                    st.warning("请填写游戏标题和描述")
            
            # 在表单外显示下载按钮
        if 'current_scene' in st.session_state and st.session_state.current_scene:
            scene_json = json.dumps(st.session_state.current_scene, ensure_ascii=False, indent=2)
            st.download_button(
                label="下载场景数据",
                data=scene_json,
                file_name=f"{st.session_state.current_scene_title}_scene.json",
                mime="application/json"
            )

if __name__ == "__main__":
    main()