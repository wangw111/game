import random
import json
from typing import Dict, Any, List
from utils.logger import setup_logger

class ChineseGameGenerator:
    """汉字游戏生成器"""
    
    def __init__(self):
        self.logger = setup_logger("chinese_game_generator")
        self._init_character_database()
    
    def _init_character_database(self):
        """初始化汉字数据库"""
        # 基础汉字数据库
        self.basic_characters = [
            {'char': '人', 'pinyin': 'rén', 'meaning': '人', 'stroke_count': 2},
            {'char': '大', 'pinyin': 'dà', 'meaning': '大', 'stroke_count': 3},
            {'char': '小', 'pinyin': 'xiǎo', 'meaning': '小', 'stroke_count': 3},
            {'char': '山', 'pinyin': 'shān', 'meaning': '山', 'stroke_count': 3},
            {'char': '水', 'pinyin': 'shuǐ', 'meaning': '水', 'stroke_count': 4},
            {'char': '火', 'pinyin': 'huǒ', 'meaning': '火', 'stroke_count': 4},
            {'char': '木', 'pinyin': 'mù', 'meaning': '木', 'stroke_count': 4},
            {'char': '土', 'pinyin': 'tǔ', 'meaning': '土', 'stroke_count': 3},
            {'char': '日', 'pinyin': 'rì', 'meaning': '太阳', 'stroke_count': 4},
            {'char': '月', 'pinyin': 'yuè', 'meaning': '月亮', 'stroke_count': 4},
            {'char': '天', 'pinyin': 'tiān', 'meaning': '天空', 'stroke_count': 4},
            {'char': '地', 'pinyin': 'dì', 'meaning': '土地', 'stroke_count': 6},
            {'char': '父', 'pinyin': 'fù', 'meaning': '父亲', 'stroke_count': 4},
            {'char': '母', 'pinyin': 'mǔ', 'meaning': '母亲', 'stroke_count': 5},
            {'char': '子', 'pinyin': 'zǐ', 'meaning': '孩子', 'stroke_count': 3},
            {'char': '女', 'pinyin': 'nǚ', 'meaning': '女性', 'stroke_count': 3},
            {'char': '男', 'pinyin': 'nán', 'meaning': '男性', 'stroke_count': 7},
            {'char': '上', 'pinyin': 'shàng', 'meaning': '上面', 'stroke_count': 3},
            {'char': '下', 'pinyin': 'xià', 'meaning': '下面', 'stroke_count': 3},
            {'char': '左', 'pinyin': 'zuǒ', 'meaning': '左边', 'stroke_count': 5},
            {'char': '右', 'pinyin': 'yòu', 'meaning': '右边', 'stroke_count': 5},
            {'char': '中', 'pinyin': 'zhōng', 'meaning': '中间', 'stroke_count': 4},
            {'char': '东', 'pinyin': 'dōng', 'meaning': '东方', 'stroke_count': 5},
            {'char': '西', 'pinyin': 'xī', 'meaning': '西方', 'stroke_count': 6},
            {'char': '南', 'pinyin': 'nán', 'meaning': '南方', 'stroke_count': 9},
            {'char': '北', 'pinyin': 'běi', 'meaning': '北方', 'stroke_count': 5},
        ]
        
        # 常用词语
        self.common_words = [
            {'word': '你好', 'pinyin': 'nǐ hǎo', 'meaning': '问候'},
            {'word': '谢谢', 'pinyin': 'xiè xiè', 'meaning': '感谢'},
            {'word': '再见', 'pinyin': 'zài jiàn', 'meaning': '告别'},
            {'word': '朋友', 'pinyin': 'péng yǒu', 'meaning': '朋友'},
            {'word': '老师', 'pinyin': 'lǎo shī', 'meaning': '老师'},
            {'word': '学生', 'pinyin': 'xué shēng', 'meaning': '学生'},
            {'word': '学校', 'pinyin': 'xué xiào', 'meaning': '学校'},
            {'word': '家庭', 'pinyin': 'jiā tíng', 'meaning': '家庭'},
            {'word': '快乐', 'pinyin': 'kuài lè', 'meaning': '快乐'},
            {'word': '学习', 'pinyin': 'xué xí', 'meaning': '学习'},
        ]
        
        # 成语
        self.idioms = [
            {'idiom': '一心一意', 'pinyin': 'yī xīn yī yì', 'meaning': '专心致志'},
            {'idiom': '四面八方', 'pinyin': 'sì miàn bā fāng', 'meaning': '各个方向'},
            {'idiom': '五颜六色', 'pinyin': 'wǔ yán liù sè', 'meaning': '色彩丰富'},
            {'idiom': '七上八下', 'pinyin': 'qī shàng bā xià', 'meaning': '心神不定'},
            {'idiom': '十全十美', 'pinyin': 'shí quán shí měi', 'meaning': '完美无缺'},
        ]
    
    def generate_character_questions(self, character_type: str, difficulty: str, count: int = 10) -> List[Dict[str, Any]]:
        """生成汉字题目"""
        questions = []
        
        if character_type == "基础汉字":
            characters = self.basic_characters
        elif character_type == "常用词语":
            characters = self.common_words
        elif character_type == "成语":
            characters = self.idioms
        else:
            characters = self.basic_characters
        
        # 根据难度选择数量
        if difficulty == "简单":
            selected_chars = characters[:5]
        elif difficulty == "中等":
            selected_chars = characters[:10]
        else:  # 困难
            selected_chars = characters
        
        for i in range(min(count, len(selected_chars))):
            char_data = selected_chars[i]
            question = self._create_character_question(char_data, character_type)
            questions.append(question)
        
        return questions
    
    def _create_character_question(self, char_data: Dict[str, Any], character_type: str) -> Dict[str, Any]:
        """创建单个汉字题目"""
        if character_type == "基础汉字":
            return {
                'type': 'character',
                'question': f"这个字读什么？ {char_data['char']}",
                'answer': char_data['pinyin'],
                'options': self._generate_pinyin_options(char_data['pinyin']),
                'meaning': char_data['meaning'],
                'stroke_count': char_data['stroke_count']
            }
        elif character_type == "常用词语":
            return {
                'type': 'word',
                'question': f"这个词读什么？ {char_data['word']}",
                'answer': char_data['pinyin'],
                'options': self._generate_pinyin_options(char_data['pinyin']),
                'meaning': char_data['meaning']
            }
        elif character_type == "成语":
            return {
                'type': 'idiom',
                'question': f"这个成语读什么？ {char_data['idiom']}",
                'answer': char_data['pinyin'],
                'options': self._generate_pinyin_options(char_data['pinyin']),
                'meaning': char_data['meaning']
            }
    
    def _generate_pinyin_options(self, correct_pinyin: str) -> List[str]:
        """生成拼音选项"""
        options = [correct_pinyin]
        
        # 生成相似的拼音作为错误选项
        similar_sounds = {
            'rén': ['rèn', 'rēn', 'rén'],
            'dà': ['dā', 'dá', 'dǎ'],
            'xiǎo': ['xiāo', 'xiáo', 'xiào'],
            'shān': ['shān', 'shǎn', 'shàn'],
            'shuǐ': ['shuī', 'shuí', 'shuì'],
            'nǐ hǎo': ['nǐ hào', 'ní hǎo', 'nǐ hǎi'],
            'xiè xiè': ['xiě xiè', 'xiè xiě', 'xie xie'],
            'yī xīn yī yì': ['yī xīn yī yí', 'yī xīn yī yì', 'yī xīn yī yì']
        }
        
        # 如果有预设的相似音，使用它们
        if correct_pinyin in similar_sounds:
            for wrong_pinyin in similar_sounds[correct_pinyin]:
                if wrong_pinyin != correct_pinyin and wrong_pinyin not in options:
                    options.append(wrong_pinyin)
        
        # 补充随机选项
        while len(options) < 4:
            random_pinyin = random.choice(['a', 'e', 'i', 'o', 'u', 'ai', 'ei', 'ui', 'ao', 'ou'])
            if random_pinyin not in options:
                options.append(random_pinyin)
        
        # 打乱选项顺序
        random.shuffle(options)
        return options
    
    def create_chinese_game(self, title: str, character_type: str, difficulty: str, age_group: str) -> Dict[str, Any]:
        """创建汉字游戏"""
        game_data = {
            'title': title,
            'type': 'chinese',
            'character_type': character_type,
            'difficulty': difficulty,
            'age_group': age_group,
            'questions': self.generate_character_questions(character_type, difficulty),
            'game_config': {
                'time_limit': 600,  # 10分钟
                'pass_score': 80,   # 80分及格
                'hints': 5,         # 5次提示机会
                'lives': 3          # 3条生命
            }
        }
        
        return game_data
    
    def generate_game_instructions(self, game_data: Dict[str, Any]) -> str:
        """生成游戏说明"""
        type_map = {
            '基础汉字': '单个汉字',
            '常用词语': '常用词语',
            '成语': '成语'
        }
        
        instructions = f"""
# {game_data['title']}

## 游戏说明
这是一个适合{game_data['age_group']}的{type_map.get(game_data['character_type'], '汉字')}学习游戏。

## 游戏规则
1. 系统会显示{type_map.get(game_data['character_type'], '汉字')}
2. 从四个选项中选择正确的拼音
3. 答对得10分，答错不得分
4. 游戏时间限制为{game_data['game_config']['time_limit']//60}分钟
5. 达到{game_data['game_config']['pass_score']}分即可过关

## 学习内容
- 学习{type_map.get(game_data['character_type'], '汉字')}的正确读音
- 理解{type_map.get(game_data['character_type'], '汉字')}的含义
- 掌握{type_map.get(game_data['character_type'], '汉字')}的用法

## 操作说明
- 点击选项选择答案
- 使用提示按钮可以获得帮助
- 生命值归零游戏结束

## 学习目标
通过游戏化的方式学习{type_map.get(game_data['character_type'], '汉字')}，提高中文水平。
"""
        return instructions