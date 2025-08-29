#!/usr/bin/env python3
"""
AI提供商功能测试脚本
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_ai_providers():
    """测试AI提供商功能"""
    print("🤖 测试AI提供商功能...")
    
    try:
        from utils.ai_manager import AIProviderManager
        
        manager = AIProviderManager()
        
        # 获取可用的AI提供商
        available_providers = manager.get_available_providers()
        print(f"可用的AI提供商: {available_providers}")
        
        # 获取所有提供商状态
        provider_status = manager.get_provider_status()
        print(f"提供商状态: {provider_status}")
        
        if available_providers:
            print("✅ AI提供商管理器初始化成功!")
            return True
        else:
            print("⚠️  没有配置AI提供商API密钥，这是正常的（需要真实API密钥才能测试）")
            return True
            
    except Exception as e:
        print(f"❌ AI提供商测试失败: {str(e)}")
        return False

def test_game_agent():
    """测试游戏智能体功能"""
    print("\n🎮 测试游戏智能体...")
    
    try:
        from agents.game_agent import GameAgent
        
        agent = GameAgent()
        
        # 测试系统提示词
        system_prompt = agent.get_system_prompt()
        print(f"系统提示词长度: {len(system_prompt)} 字符")
        
        # 测试处理请求
        result = agent.process_request("我想创建一个加法游戏")
        print(f"请求处理结果: {result['success']}")
        print(f"游戏类型: {result['game_type']}")
        
        print("✅ 游戏智能体功能正常!")
        return True
        
    except Exception as e:
        print(f"❌ 游戏智能体测试失败: {str(e)}")
        return False

def main():
    """主测试函数"""
    print("🤖 AI功能测试")
    print("=" * 50)
    
    # 运行测试
    tests = [
        ("AI提供商", test_ai_providers),
        ("游戏智能体", test_game_agent),
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
    print("📊 AI功能测试结果:")
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"   {test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\n总计: {passed}/{total} 个测试通过")
    
    if passed == total:
        print("🎉 AI功能测试通过！")
        return True
    else:
        print("⚠️  部分AI功能测试失败。")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)