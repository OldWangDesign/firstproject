#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DeepSeek CLI Chat - 主程序
基于DeepSeek API的命令行对话工具
"""

import sys
import os
from typing import Optional

# 导入自定义模块
from config import ConfigManager
from prompt_manager import PromptManager
from api_client import DeepSeekClient


class DeepSeekCLI:
    """DeepSeek CLI主程序类"""
    
    def __init__(self):
        """
        初始化CLI程序
        """
        self.config_manager: Optional[ConfigManager] = None
        self.prompt_manager: Optional[PromptManager] = None
        self.api_client: Optional[DeepSeekClient] = None
        self.running = False
        
    def initialize(self) -> bool:
        """
        初始化所有组件
        
        Returns:
            bool: 初始化成功返回True，失败返回False
        """
        print("🚀 DeepSeek CLI Chat 启动中...")
        print("=" * 50)
        
        # 1. 初始化配置管理器
        print("📋 加载配置文件...")
        self.config_manager = ConfigManager()
        if not self.config_manager.load_config():
            print("\n💡 首次使用提示:")
            print("1. 复制 config.json.example 为 config.json")
            print("2. 在 config.json 中设置您的 DeepSeek API 密钥")
            print("3. 重新运行程序")
            return False
        
        # 2. 初始化提示词管理器
        print("\n📝 加载系统提示词...")
        prompt_file = self.config_manager.get_system_prompt_file()
        self.prompt_manager = PromptManager(prompt_file)
        if not self.prompt_manager.load_system_prompt():
            print("⚠️ 系统提示词加载失败，将使用默认提示词")
        
        # 3. 初始化API客户端
        print("\n🔗 初始化API客户端...")
        try:
            deepseek_config = self.config_manager.get_deepseek_config()
            self.api_client = DeepSeekClient(
                api_key=deepseek_config['api_key'],
                base_url=deepseek_config['base_url'],
                model=deepseek_config['model'],
                max_tokens=deepseek_config.get('max_tokens', 2000),
                temperature=deepseek_config.get('temperature', 0.7)
            )
            
            # 设置最大历史记录数
            app_config = self.config_manager.get_app_config()
            self.api_client.max_history = app_config.get('max_history', 10)
            
            # 设置系统提示词
            system_prompt = self.prompt_manager.get_system_prompt()
            self.api_client.set_system_prompt(system_prompt)
            
        except Exception as e:
            print(f"❌ API客户端初始化失败: {e}")
            return False
        
        # 4. 测试API连接
        print("\n🔍 测试API连接...")
        if not self.api_client.test_connection():
            print("❌ API连接测试失败，请检查网络和API密钥")
            return False
        
        print("\n✅ 所有组件初始化成功！")
        return True
    
    def show_welcome(self) -> None:
        """
        显示欢迎信息
        """
        print("\n" + "=" * 50)
        print("🎉 欢迎使用 DeepSeek CLI Chat!")
        print("=" * 50)
        print("💬 开始与AI对话吧！")
        print("\n📖 使用说明:")
        print("  • 直接输入问题开始对话")
        print("  • 输入 'quit', 'exit', 'q' 退出程序")
        print("  • 输入 'clear' 清空对话历史")
        print("  • 输入 'history' 查看对话统计")
        print("  • 输入 'reload' 重新加载系统提示词")
        print("  • 输入 'help' 显示帮助信息")
        print("\n" + "-" * 50)
        
        # 显示当前配置信息
        if self.config_manager and self.api_client:
            print(f"🤖 当前模型: {self.config_manager.get_model()}")
            print(f"🌡️ 温度参数: {self.config_manager.get_temperature()}")
            print(f"📏 最大Token: {self.config_manager.get_max_tokens()}")
            
            # 显示系统提示词预览
            if self.prompt_manager:
                prompt_preview = self.prompt_manager.get_system_prompt()[:100]
                if len(self.prompt_manager.get_system_prompt()) > 100:
                    prompt_preview += "..."
                print(f"📋 系统提示词: {prompt_preview}")
        
        print("-" * 50)
    
    def show_help(self) -> None:
        """
        显示帮助信息
        """
        print("\n📖 DeepSeek CLI Chat 帮助")
        print("=" * 30)
        print("🔧 命令列表:")
        print("  help     - 显示此帮助信息")
        print("  clear    - 清空对话历史")
        print("  history  - 显示对话统计信息")
        print("  reload   - 重新加载系统提示词")
        print("  quit     - 退出程序 (也可以用 exit, q)")
        print("\n💡 使用技巧:")
        print("  • 可以进行多轮对话，AI会记住上下文")
        print("  • 修改 prompts/system.txt 可以自定义AI行为")
        print("  • 修改 config.json 可以调整API参数")
        print("=" * 30)
    
    def handle_command(self, user_input: str) -> bool:
        """
        处理特殊命令
        
        Args:
            user_input: 用户输入
            
        Returns:
            bool: 如果是命令返回True，否则返回False
        """
        command = user_input.strip().lower()
        
        if command in ['quit', 'exit', 'q']:
            self.running = False
            print("\n👋 感谢使用 DeepSeek CLI Chat，再见！")
            return True
        
        elif command == 'clear':
            if self.api_client:
                self.api_client.clear_history()
                # 重新设置系统提示词
                if self.prompt_manager:
                    system_prompt = self.prompt_manager.get_system_prompt()
                    self.api_client.set_system_prompt(system_prompt)
            return True
        
        elif command == 'history':
            if self.api_client:
                summary = self.api_client.get_history_summary()
                print("\n📊 对话统计:")
                print(f"  总消息数: {summary['total_messages']}")
                print(f"  用户消息: {summary['user_messages']}")
                print(f"  AI回复: {summary['assistant_messages']}")
                print(f"  系统消息: {summary['system_messages']}")
                print(f"  最大历史: {summary['max_history']}")
            return True
        
        elif command == 'reload':
            if self.prompt_manager and self.api_client:
                if self.prompt_manager.reload_system_prompt():
                    system_prompt = self.prompt_manager.get_system_prompt()
                    self.api_client.set_system_prompt(system_prompt)
                    print("✅ 系统提示词已重新加载")
                else:
                    print("❌ 系统提示词重新加载失败")
            return True
        
        elif command == 'help':
            self.show_help()
            return True
        
        return False
    
    def run(self) -> None:
        """
        运行主程序循环
        """
        if not self.initialize():
            print("\n❌ 程序初始化失败，退出")
            sys.exit(1)
        
        self.show_welcome()
        self.running = True
        
        try:
            while self.running:
                # 获取用户输入
                try:
                    user_input = input("\n💭 您: ").strip()
                except (EOFError, KeyboardInterrupt):
                    print("\n\n👋 程序被中断，再见！")
                    break
                
                # 检查空输入
                if not user_input:
                    print("⚠️ 请输入一些内容")
                    continue
                
                # 处理特殊命令
                if self.handle_command(user_input):
                    continue
                
                # 发送消息给AI (使用流式输出)
                if self.api_client:
                    print()  # 换行
                    response = self.api_client.chat_stream(user_input)
                    
                    if not response:
                        print("抱歉，我现在无法回复。请稍后再试。")
                else:
                    print("❌ API客户端未初始化")
                    break
        
        except Exception as e:
            print(f"\n❌ 程序运行出错: {e}")
        
        finally:
            print("\n程序已退出")


def main():
    """
    主函数
    """
    # 检查Python版本
    if sys.version_info < (3, 6):
        print("❌ 此程序需要 Python 3.6 或更高版本")
        sys.exit(1)
    
    # 创建并运行CLI程序
    cli = DeepSeekCLI()
    cli.run()


if __name__ == "__main__":
    main()