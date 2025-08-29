import json
from typing import Dict, Any, List
from utils.logger import setup_logger

class GameSceneGenerator:
    """游戏场景生成器"""
    
    def __init__(self):
        self.logger = setup_logger("game_scene_generator")
    
    def generate_game_scene(self, title: str, description: str, action_logic: str, age_group: str) -> Dict[str, Any]:
        """生成游戏场景"""
        scene_data = {
            'title': title,
            'description': description,
            'action_logic': action_logic,
            'age_group': age_group,
            'scene_elements': self._analyze_scene_elements(description, action_logic),
            'game mechanics': self._design_game_mechanics(action_logic),
            'visual_design': self._create_visual_design(description, age_group),
            'audio_design': self._create_audio_design(description),
            'technical_requirements': self._define_technical_requirements()
        }
        
        return scene_data
    
    def _analyze_scene_elements(self, description: str, action_logic: str) -> Dict[str, Any]:
        """分析场景元素"""
        elements = {
            'characters': self._extract_characters(description, action_logic),
            'environment': self._extract_environment(description),
            'objects': self._extract_objects(description, action_logic),
            'interactions': self._extract_interactions(action_logic)
        }
        return elements
    
    def _extract_characters(self, description: str, action_logic: str) -> List[Dict[str, Any]]:
        """提取角色信息"""
        characters = []
        
        # 基于描述和动作逻辑生成角色
        if any(word in description.lower() for word in ['动物', 'animal', '宠物', 'pet']):
            characters.append({
                'type': 'animal',
                'name': '小动物',
                'description': '可爱的动物角色',
                'abilities': ['移动', '跳跃', '互动']
            })
        
        if any(word in description.lower() for word in ['人物', 'character', '玩家', 'player']):
            characters.append({
                'type': 'player',
                'name': '玩家角色',
                'description': '主要控制的角色',
                'abilities': ['移动', '操作', '选择']
            })
        
        if any(word in description.lower() for word in ['老师', 'teacher', '指导', 'guide']):
            characters.append({
                'type': 'guide',
                'name': '指导者',
                'description': '提供帮助和指导的角色',
                'abilities': ['说话', '示范', '提示']
            })
        
        return characters
    
    def _extract_environment(self, description: str) -> Dict[str, Any]:
        """提取环境信息"""
        environment = {
            'setting': '默认环境',
            'background': '简单背景',
            'atmosphere': '友好愉快',
            'lighting': '明亮自然'
        }
        
        if any(word in description.lower() for word in ['森林', 'forest', '自然', 'nature']):
            environment.update({
                'setting': '森林环境',
                'background': '树木和草地',
                'atmosphere': '自然清新',
                'lighting': '阳光透过树叶'
            })
        elif any(word in description.lower() for word in ['海洋', 'ocean', '水下', 'underwater']):
            environment.update({
                'setting': '海洋环境',
                'background': '海底世界',
                'atmosphere': '神秘宁静',
                'lighting': '水下光线'
            })
        elif any(word in description.lower() for word in ['太空', 'space', '宇宙', 'universe']):
            environment.update({
                'setting': '太空环境',
                'background': '星空和行星',
                'atmosphere': '神秘科幻',
                'lighting': '星光和霓虹'
            })
        elif any(word in description.lower() for word in ['教室', 'classroom', '学校', 'school']):
            environment.update({
                'setting': '教室环境',
                'background': '教室内部',
                'atmosphere': '学习氛围',
                'lighting': '教室照明'
            })
        
        return environment
    
    def _extract_objects(self, description: str, action_logic: str) -> List[Dict[str, Any]]:
        """提取物体信息"""
        objects = []
        
        # 基于描述和动作逻辑生成物体
        if any(word in description.lower() for word in ['数字', 'number', '数学', 'math']):
            objects.extend([
                {
                    'type': 'educational',
                    'name': '数字卡片',
                    'description': '显示数字的卡片',
                    'interaction': '点击选择'
                },
                {
                    'type': 'educational',
                    'name': '运算符号',
                    'description': '加减乘除符号',
                    'interaction': '拖拽使用'
                }
            ])
        
        if any(word in description.lower() for word in ['汉字', 'chinese', '文字', 'character']):
            objects.extend([
                {
                    'type': 'educational',
                    'name': '汉字卡片',
                    'description': '显示汉字的卡片',
                    'interaction': '点击学习'
                },
                {
                    'type': 'educational',
                    'name': '拼音提示',
                    'description': '显示拼音的提示',
                    'interaction': '悬停显示'
                }
            ])
        
        if any(word in description.lower() for word in ['英语', 'english', '单词', 'word']):
            objects.extend([
                {
                    'type': 'educational',
                    'name': '英语单词',
                    'description': '英语单词卡片',
                    'interaction': '点击发音'
                },
                {
                    'type': 'educational',
                    'name': '图片配对',
                    'description': '与单词对应的图片',
                    'interaction': '拖拽配对'
                }
            ])
        
        return objects
    
    def _extract_interactions(self, action_logic: str) -> List[Dict[str, Any]]:
        """提取交互信息"""
        interactions = []
        
        # 基于动作逻辑生成交互
        if any(word in action_logic.lower() for word in ['点击', 'click', '选择', 'select']):
            interactions.append({
                'type': 'click',
                'description': '点击选择答案或物体',
                'feedback': '视觉和音频反馈'
            })
        
        if any(word in action_logic.lower() for word in ['拖拽', 'drag', '移动', 'move']):
            interactions.append({
                'type': 'drag',
                'description': '拖拽物体到指定位置',
                'feedback': '拖拽效果和放置反馈'
            })
        
        if any(word in action_logic.lower() for word in ['输入', 'input', '填写', 'fill']):
            interactions.append({
                'type': 'input',
                'description': '输入文字或数字',
                'feedback': '输入验证和提示'
            })
        
        if any(word in action_logic.lower() for word in ['语音', 'voice', '发音', 'pronunciation']):
            interactions.append({
                'type': 'voice',
                'description': '语音识别和发音',
                'feedback': '语音反馈和评分'
            })
        
        return interactions
    
    def _design_game_mechanics(self, action_logic: str) -> Dict[str, Any]:
        """设计游戏机制"""
        mechanics = {
            'core_loop': '学习-练习-测试',
            'progression': '线性渐进',
            'feedback_system': '即时反馈',
            'reward_system': '积分和星级',
            'difficulty_adjustment': '自适应难度'
        }
        
        # 根据动作逻辑调整机制
        if '竞赛' in action_logic or 'competition' in action_logic.lower():
            mechanics['core_loop'] = '竞赛-排名-奖励'
            mechanics['progression'] = '竞技排名'
        
        if '探索' in action_logic or 'explore' in action_logic.lower():
            mechanics['core_loop'] = '探索-发现-学习'
            mechanics['progression'] = '地图解锁'
        
        if '创作' in action_logic or 'create' in action_logic.lower():
            mechanics['core_loop'] = '创作-展示-分享'
            mechanics['progression'] = '技能提升'
        
        return mechanics
    
    def _create_visual_design(self, description: str, age_group: str) -> Dict[str, Any]:
        """创建视觉设计"""
        visual_design = {
            'art_style': '卡通风格',
            'color_palette': '明亮多彩',
            'character_design': '可爱友好',
            'ui_design': '简洁直观'
        }
        
        # 根据年龄组调整设计
        if '3-6岁' in age_group:
            visual_design.update({
                'art_style': '简单卡通',
                'color_palette': '鲜艳对比',
                'character_design': '圆润可爱',
                'ui_design': '大按钮，简单图标'
            })
        elif '7-10岁' in age_group:
            visual_design.update({
                'art_style': '现代卡通',
                'color_palette': '协调多彩',
                'character_design': '个性鲜明',
                'ui_design': '清晰布局，互动元素'
            })
        elif '11-14岁' in age_group:
            visual_design.update({
                'art_style': '时尚卡通',
                'color_palette': '时尚配色',
                'character_design': '酷炫风格',
                'ui_design': '现代化界面，功能丰富'
            })
        
        return visual_design
    
    def _create_audio_design(self, description: str) -> Dict[str, Any]:
        """创建音频设计"""
        audio_design = {
            'background_music': '轻松愉快',
            'sound_effects': '清晰反馈',
            'voice_overs': '专业配音',
            'interactive_audio': '响应式音效'
        }
        
        # 根据描述调整音频设计
        if any(word in description.lower() for word in ['学习', 'learn', '教育', 'education']):
            audio_design['background_music'] = '轻柔专注'
        
        if any(word in description.lower() for word in ['冒险', 'adventure', '探索', 'explore']):
            audio_design['background_music'] = '激动人心'
        
        if any(word in description.lower() for word in ['竞赛', 'competition', '比赛', 'race']):
            audio_design['background_music'] = '紧张刺激'
        
        return audio_design
    
    def _define_technical_requirements(self) -> Dict[str, Any]:
        """定义技术要求"""
        return {
            'platform': 'Web应用',
            'framework': 'Streamlit',
            'programming_language': 'Python',
            'database': 'JSON文件存储',
            'media_support': '图片、音频、视频',
            'responsive_design': True,
            'accessibility': '基本无障碍支持'
        }
    
    def generate_scene_instructions(self, scene_data: Dict[str, Any]) -> str:
        """生成场景说明"""
        instructions = f"""
# {scene_data['title']}

## 场景描述
{scene_data['description']}

## 动作逻辑
{scene_data['action_logic']}

## 场景元素

### 角色
"""
        
        for character in scene_data['scene_elements']['characters']:
            instructions += f"- **{character['name']}**: {character['description']} (能力: {', '.join(character['abilities'])})\n"
        
        instructions += f"""
### 环境
- **设置**: {scene_data['scene_elements']['environment']['setting']}
- **背景**: {scene_data['scene_elements']['environment']['background']}
- **氛围**: {scene_data['scene_elements']['environment']['atmosphere']}
- **光照**: {scene_data['scene_elements']['environment']['lighting']}

### 物体
"""
        
        for obj in scene_data['scene_elements']['objects']:
            instructions += f"- **{obj['name']}**: {obj['description']} (交互: {obj['interaction']})\n"
        
        instructions += f"""
### 交互方式
"""
        
        for interaction in scene_data['scene_elements']['interactions']:
            instructions += f"- **{interaction['type']}**: {interaction['description']} - {interaction['feedback']}\n"
        
        instructions += f"""
## 游戏机制
- **核心循环**: {scene_data['game mechanics']['core_loop']}
- **进度系统**: {scene_data['game mechanics']['progression']}
- **反馈系统**: {scene_data['game mechanics']['feedback_system']}
- **奖励系统**: {scene_data['game mechanics']['reward_system']}
- **难度调整**: {scene_data['game mechanics']['difficulty_adjustment']}

## 视觉设计
- **艺术风格**: {scene_data['visual_design']['art_style']}
- **色彩方案**: {scene_data['visual_design']['color_palette']}
- **角色设计**: {scene_data['visual_design']['character_design']}
- **界面设计**: {scene_data['visual_design']['ui_design']}

## 音频设计
- **背景音乐**: {scene_data['audio_design']['background_music']}
- **音效**: {scene_data['audio_design']['sound_effects']}
- **配音**: {scene_data['audio_design']['voice_overs']}
- **交互音频**: {scene_data['audio_design']['interactive_audio']}

## 技术要求
- **平台**: {scene_data['technical_requirements']['platform']}
- **框架**: {scene_data['technical_requirements']['framework']}
- **编程语言**: {scene_data['technical_requirements']['programming_language']}
- **数据存储**: {scene_data['technical_requirements']['database']}
- **媒体支持**: {scene_data['technical_requirements']['media_support']}
- **响应式设计**: {scene_data['technical_requirements']['responsive_design']}
- **无障碍支持**: {scene_data['technical_requirements']['accessibility']}

## 适合年龄
{scene_data['age_group']}
"""
        return instructions