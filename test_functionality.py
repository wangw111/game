#!/usr/bin/env python3
"""
游戏开发智能体功能测试脚本
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 激活虚拟环境
import subprocess
import json

def test_math_game():
    """测试数字游戏生成功能"""
    print("🧮 测试数字游戏生成...")
    
    try:
        from games.math_game import MathGameGenerator
        
        generator = MathGameGenerator()
        
        # 测试生成加法游戏
        game_data = generator.create_math_game(
            title="测试加法游戏",
            operation="加法",
            difficulty="简单",
            age_group="7-10岁"
        )
        
        print(f"✅ 数字游戏生成成功!")
        print(f"   标题: {game_data['title']}")
        print(f"   题目数量: {len(game_data['problems'])}")
        print(f"   示例题目: {game_data['problems'][0]['question']}")
        print(f"   正确答案: {game_data['problems'][0]['answer']}")
        
        return True
        
    except Exception as e:
        print(f"❌ 数字游戏测试失败: {str(e)}")
        return False

def test_chinese_game():
    """测试汉字游戏生成功能"""
    print("\n📝 测试汉字游戏生成...")
    
    try:
        from games.chinese_game import ChineseGameGenerator
        
        generator = ChineseGameGenerator()
        
        # 测试生成基础汉字游戏
        game_data = generator.create_chinese_game(
            title="测试汉字游戏",
            character_type="基础汉字",
            difficulty="简单",
            age_group="7-10岁"
        )
        
        print(f"✅ 汉字游戏生成成功!")
        print(f"   标题: {game_data['title']}")
        print(f"   题目数量: {len(game_data['questions'])}")
        print(f"   示例题目: {game_data['questions'][0]['question']}")
        print(f"   正确答案: {game_data['questions'][0]['answer']}")
        
        return True
        
    except Exception as e:
        print(f"❌ 汉字游戏测试失败: {str(e)}")
        return False

def test_english_game():
    """测试英语游戏生成功能"""
    print("\n🔤 测试英语游戏生成...")
    
    try:
        from games.english_game import EnglishGameGenerator
        
        generator = EnglishGameGenerator()
        
        # 测试生成字母学习游戏
        game_data = generator.create_english_game(
            title="测试英语游戏",
            english_type="字母学习",
            difficulty="简单",
            age_group="7-10岁"
        )
        
        print(f"✅ 英语游戏生成成功!")
        print(f"   标题: {game_data['title']}")
        print(f"   题目数量: {len(game_data['questions'])}")
        print(f"   示例题目: {game_data['questions'][0]['question']}")
        print(f"   正确答案: {game_data['questions'][0]['answer']}")
        
        return True
        
    except Exception as e:
        print(f"❌ 英语游戏测试失败: {str(e)}")
        return False

def test_scene_generator():
    """测试场景生成功能"""
    print("\n🎨 测试场景生成...")
    
    try:
        from games.scene_generator import GameSceneGenerator
        
        generator = GameSceneGenerator()
        
        # 测试生成场景
        scene_data = generator.generate_game_scene(
            title="测试场景",
            description="一个有趣的数学学习游戏",
            action_logic="玩家需要点击正确的答案来获得分数",
            age_group="7-10岁"
        )
        
        print(f"✅ 场景生成成功!")
        print(f"   标题: {scene_data['title']}")
        print(f"   角色数量: {len(scene_data['scene_elements']['characters'])}")
        print(f"   物体数量: {len(scene_data['scene_elements']['objects'])}")
        print(f"   交互方式: {len(scene_data['scene_elements']['interactions'])}")
        
        return True
        
    except Exception as e:
        print(f"❌ 场景生成测试失败: {str(e)}")
        return False

def test_config():
    """测试配置功能"""
    print("\n⚙️ 测试配置功能...")
    
    try:
        from config.settings import Config
        
        # 测试配置验证
        is_valid = Config.validate_config()
        print(f"配置验证结果: {is_valid}")
        
        # 测试配置属性
        print(f"应用名称: {Config.APP_NAME}")
        print(f"应用版本: {Config.APP_VERSION}")
        print(f"调试模式: {Config.DEBUG}")
        
        return True
        
    except Exception as e:
        print(f"❌ 配置测试失败: {str(e)}")
        return False

def main():
    """主测试函数"""
    print("🎮 游戏开发智能体功能测试")
    print("=" * 50)
    
    # 运行所有测试
    tests = [
        ("配置功能", test_config),
        ("数字游戏", test_math_game),
        ("汉字游戏", test_chinese_game),
        ("英语游戏", test_english_game),
        ("场景生成", test_scene_generator),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name}测试出现异常: {str(e)}")
            results.append((test_name, False))
    
    # 输出测试结果
    print("\n" + "=" * 50)
    print("📊 测试结果汇总:")
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"   {test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\n总计: {passed}/{total} 个测试通过")
    
    if passed == total:
        print("🎉 所有测试通过！应用功能正常。")
        return True
    else:
        print("⚠️  部分测试失败，请检查相关功能。")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)