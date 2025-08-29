import random
import json
from typing import Dict, Any, List
from utils.logger import setup_logger

class EnglishGameGenerator:
    """英语游戏生成器"""
    
    def __init__(self):
        self.logger = setup_logger("english_game_generator")
        self._init_english_database()
    
    def _init_english_database(self):
        """初始化英语数据库"""
        # 字母数据库
        self.alphabet = [
            {'letter': 'A', 'word': 'Apple', 'sound': '/eɪ/', 'example': 'A for Apple'},
            {'letter': 'B', 'word': 'Ball', 'sound': '/biː/', 'example': 'B for Ball'},
            {'letter': 'C', 'word': 'Cat', 'sound': '/siː/', 'example': 'C for Cat'},
            {'letter': 'D', 'word': 'Dog', 'sound': '/diː/', 'example': 'D for Dog'},
            {'letter': 'E', 'word': 'Elephant', 'sound': '/iː/', 'example': 'E for Elephant'},
            {'letter': 'F', 'word': 'Fish', 'sound': '/ef/', 'example': 'F for Fish'},
            {'letter': 'G', 'word': 'Giraffe', 'sound': '/dʒiː/', 'example': 'G for Giraffe'},
            {'letter': 'H', 'word': 'House', 'sound': '/eɪtʃ/', 'example': 'H for House'},
            {'letter': 'I', 'word': 'Ice', 'sound': '/aɪ/', 'example': 'I for Ice'},
            {'letter': 'J', 'word': 'Juice', 'sound': '/dʒeɪ/', 'example': 'J for Juice'},
            {'letter': 'K', 'word': 'Kite', 'sound': '/keɪ/', 'example': 'K for Kite'},
            {'letter': 'L', 'word': 'Lion', 'sound': '/el/', 'example': 'L for Lion'},
            {'letter': 'M', 'word': 'Moon', 'sound': '/em/', 'example': 'M for Moon'},
            {'letter': 'N', 'word': 'Nose', 'sound': '/en/', 'example': 'N for Nose'},
            {'letter': 'O', 'word': 'Orange', 'sound': '/əʊ/', 'example': 'O for Orange'},
            {'letter': 'P', 'word': 'Pen', 'sound': '/piː/', 'example': 'P for Pen'},
            {'letter': 'Q', 'word': 'Queen', 'sound': '/kjuː/', 'example': 'Q for Queen'},
            {'letter': 'R', 'word': 'Rabbit', 'sound': '/ɑːr/', 'example': 'R for Rabbit'},
            {'letter': 'S', 'word': 'Sun', 'sound': '/es/', 'example': 'S for Sun'},
            {'letter': 'T', 'word': 'Tree', 'sound': '/tiː/', 'example': 'T for Tree'},
            {'letter': 'U', 'word': 'Umbrella', 'sound': '/juː/', 'example': 'U for Umbrella'},
            {'letter': 'V', 'word': 'Violin', 'sound': '/viː/', 'example': 'V for Violin'},
            {'letter': 'W', 'word': 'Water', 'sound': '/dʌbəl.juː/', 'example': 'W for Water'},
            {'letter': 'X', 'word': 'X-ray', 'sound': '/eks/', 'example': 'X for X-ray'},
            {'letter': 'Y', 'word': 'Yellow', 'sound': '/waɪ/', 'example': 'Y for Yellow'},
            {'letter': 'Z', 'word': 'Zoo', 'sound': '/ziː/', 'example': 'Z for Zoo'},
        ]
        
        # 常用单词
        self.common_words = [
            {'word': 'hello', 'translation': '你好', 'category': 'greeting'},
            {'word': 'goodbye', 'translation': '再见', 'category': 'greeting'},
            {'word': 'thank you', 'translation': '谢谢', 'category': 'polite'},
            {'word': 'please', 'translation': '请', 'category': 'polite'},
            {'word': 'sorry', 'translation': '对不起', 'category': 'polite'},
            {'word': 'yes', 'translation': '是', 'category': 'basic'},
            {'word': 'no', 'translation': '不', 'category': 'basic'},
            {'word': 'book', 'translation': '书', 'category': 'object'},
            {'word': 'pen', 'translation': '笔', 'category': 'object'},
            {'word': 'table', 'translation': '桌子', 'category': 'object'},
            {'word': 'chair', 'translation': '椅子', 'category': 'object'},
            {'word': 'water', 'translation': '水', 'category': 'nature'},
            {'word': 'sun', 'translation': '太阳', 'category': 'nature'},
            {'word': 'moon', 'translation': '月亮', 'category': 'nature'},
            {'word': 'star', 'translation': '星星', 'category': 'nature'},
            {'word': 'red', 'translation': '红色', 'category': 'color'},
            {'word': 'blue', 'translation': '蓝色', 'category': 'color'},
            {'word': 'green', 'translation': '绿色', 'category': 'color'},
            {'word': 'yellow', 'translation': '黄色', 'category': 'color'},
            {'word': 'one', 'translation': '一', 'category': 'number'},
            {'word': 'two', 'translation': '二', 'category': 'number'},
            {'word': 'three', 'translation': '三', 'category': 'number'},
            {'word': 'four', 'translation': '四', 'category': 'number'},
            {'word': 'five', 'translation': '五', 'category': 'number'},
        ]
        
        # 简单对话
        self.simple_dialogues = [
            {
                'question': 'What is your name?',
                'answer': 'My name is...',
                'translation': '你叫什么名字？',
                'options': ['My name is...', 'I am fine.', 'Thank you.', 'Goodbye.']
            },
            {
                'question': 'How are you?',
                'answer': 'I am fine, thank you.',
                'translation': '你好吗？',
                'options': ['I am fine, thank you.', 'My name is...', 'Goodbye.', 'Hello.']
            },
            {
                'question': 'How old are you?',
                'answer': 'I am... years old.',
                'translation': '你多大了？',
                'options': ['I am... years old.', 'I am fine.', 'Thank you.', 'Hello.']
            },
            {
                'question': 'Where are you from?',
                'answer': 'I am from...',
                'translation': '你来自哪里？',
                'options': ['I am from...', 'I am fine.', 'Thank you.', 'Hello.']
            },
            {
                'question': 'What is this?',
                'answer': 'This is a...',
                'translation': '这是什么？',
                'options': ['This is a...', 'I am fine.', 'Thank you.', 'Hello.']
            }
        ]
        
        # 语法练习
        self.grammar_exercises = [
            {
                'question': 'I ___ a student.',
                'answer': 'am',
                'options': ['am', 'is', 'are', 'be'],
                'explanation': '主语是第一人称单数，用am'
            },
            {
                'question': 'She ___ to school every day.',
                'answer': 'goes',
                'options': ['go', 'goes', 'going', 'gone'],
                'explanation': '主语是第三人称单数，动词要加s'
            },
            {
                'question': 'They ___ playing football.',
                'answer': 'are',
                'options': ['am', 'is', 'are', 'be'],
                'explanation': '主语是第三人称复数，用are'
            },
            {
                'question': 'He ___ a book.',
                'answer': 'reads',
                'options': ['read', 'reads', 'reading', 'readed'],
                'explanation': '主语是第三人称单数，动词要加s'
            },
            {
                'question': 'We ___ happy.',
                'answer': 'are',
                'options': ['am', 'is', 'are', 'be'],
                'explanation': '主语是第一人称复数，用are'
            }
        ]
    
    def generate_english_questions(self, english_type: str, difficulty: str, count: int = 10) -> List[Dict[str, Any]]:
        """生成英语题目"""
        questions = []
        
        if english_type == "字母学习":
            data = self.alphabet
        elif english_type == "单词记忆":
            data = self.common_words
        elif english_type == "简单对话":
            data = self.simple_dialogues
        elif english_type == "语法练习":
            data = self.grammar_exercises
        else:
            data = self.common_words
        
        # 根据难度选择数量
        if difficulty == "简单":
            selected_data = data[:5]
        elif difficulty == "中等":
            selected_data = data[:10]
        else:  # 困难
            selected_data = data
        
        for i in range(min(count, len(selected_data))):
            item = selected_data[i]
            question = self._create_english_question(item, english_type)
            questions.append(question)
        
        return questions
    
    def _create_english_question(self, item: Dict[str, Any], english_type: str) -> Dict[str, Any]:
        """创建单个英语题目"""
        if english_type == "字母学习":
            return {
                'type': 'alphabet',
                'question': f"这个字母是什么？ {item['letter']}",
                'answer': item['letter'],
                'options': self._generate_letter_options(item['letter']),
                'word': item['word'],
                'sound': item['sound'],
                'example': item['example']
            }
        elif english_type == "单词记忆":
            return {
                'type': 'word',
                'question': f"'{item['word']}'的中文意思是什么？",
                'answer': item['translation'],
                'options': self._generate_translation_options(item['translation']),
                'category': item['category']
            }
        elif english_type == "简单对话":
            return {
                'type': 'dialogue',
                'question': f"如何回答: '{item['question']}'?",
                'answer': item['answer'],
                'options': item['options'],
                'translation': item['translation']
            }
        elif english_type == "语法练习":
            return {
                'type': 'grammar',
                'question': item['question'],
                'answer': item['answer'],
                'options': item['options'],
                'explanation': item.get('explanation', '')
            }
    
    def _generate_letter_options(self, correct_letter: str) -> List[str]:
        """生成字母选项"""
        options = [correct_letter]
        
        # 生成其他字母作为错误选项
        all_letters = [item['letter'] for item in self.alphabet]
        wrong_letters = [letter for letter in all_letters if letter != correct_letter]
        
        # 随机选择3个错误选项
        selected_wrong = random.sample(wrong_letters, min(3, len(wrong_letters)))
        options.extend(selected_wrong)
        
        # 打乱选项顺序
        random.shuffle(options)
        return options
    
    def _generate_translation_options(self, correct_translation: str) -> List[str]:
        """生成翻译选项"""
        options = [correct_translation]
        
        # 生成其他翻译作为错误选项
        all_translations = [item['translation'] for item in self.common_words]
        wrong_translations = [trans for trans in all_translations if trans != correct_translation]
        
        # 随机选择3个错误选项
        selected_wrong = random.sample(wrong_translations, min(3, len(wrong_translations)))
        options.extend(selected_wrong)
        
        # 打乱选项顺序
        random.shuffle(options)
        return options
    
    def create_english_game(self, title: str, english_type: str, difficulty: str, age_group: str) -> Dict[str, Any]:
        """创建英语游戏"""
        game_data = {
            'title': title,
            'type': 'english',
            'english_type': english_type,
            'difficulty': difficulty,
            'age_group': age_group,
            'questions': self.generate_english_questions(english_type, difficulty),
            'game_config': {
                'time_limit': 600,  # 10分钟
                'pass_score': 70,   # 70分及格
                'hints': 5,         # 5次提示机会
                'lives': 3          # 3条生命
            }
        }
        
        return game_data
    
    def generate_game_instructions(self, game_data: Dict[str, Any]) -> str:
        """生成游戏说明"""
        type_map = {
            '字母学习': '英文字母',
            '单词记忆': '英语单词',
            '简单对话': '英语对话',
            '语法练习': '英语语法'
        }
        
        instructions = f"""
# {game_data['title']}

## 游戏说明
这是一个适合{game_data['age_group']}的{type_map.get(game_data['english_type'], '英语')}学习游戏。

## 游戏规则
1. 系统会显示{type_map.get(game_data['english_type'], '英语')}相关题目
2. 从四个选项中选择正确答案
3. 答对得10分，答错不得分
4. 游戏时间限制为{game_data['game_config']['time_limit']//60}分钟
5. 达到{game_data['game_config']['pass_score']}分即可过关

## 学习内容
- 学习{type_map.get(game_data['english_type'], '英语')}的正确用法
- 提高英语听说读写能力
- 培养英语思维

## 操作说明
- 点击选项选择答案
- 使用提示按钮可以获得帮助
- 生命值归零游戏结束

## 学习目标
通过游戏化的方式学习{type_map.get(game_data['english_type'], '英语')}，提高英语水平。
"""
        return instructions