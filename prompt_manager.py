#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
系统提示词管理模块
负责加载、管理和提供系统提示词
"""

import os
from typing import Optional


class PromptManager:
    """提示词管理器"""
    
    def __init__(self, prompt_file: str = "prompts/system.txt"):
        """
        初始化提示词管理器
        
        Args:
            prompt_file: 系统提示词文件路径
        """
        self.prompt_file = prompt_file
        self.system_prompt: str = ""
        
    def load_system_prompt(self) -> bool:
        """
        加载系统提示词
        
        Returns:
            bool: 加载成功返回True，失败返回False
        """
        try:
            if not os.path.exists(self.prompt_file):
                print(f"❌ 系统提示词文件 {self.prompt_file} 不存在")
                # 创建默认的系统提示词文件
                self._create_default_prompt()
                return False
                
            with open(self.prompt_file, 'r', encoding='utf-8') as f:
                self.system_prompt = f.read().strip()
                
            if not self.system_prompt:
                print(f"⚠️ 系统提示词文件 {self.prompt_file} 为空，使用默认提示词")
                self.system_prompt = self._get_default_prompt()
                
            print(f"✅ 系统提示词加载成功 (长度: {len(self.system_prompt)} 字符)")
            return True
            
        except Exception as e:
            print(f"❌ 加载系统提示词失败: {e}")
            print("🔄 使用默认系统提示词")
            self.system_prompt = self._get_default_prompt()
            return False
    
    def get_system_prompt(self) -> str:
        """
        获取系统提示词
        
        Returns:
            str: 系统提示词内容
        """
        return self.system_prompt
    
    def reload_system_prompt(self) -> bool:
        """
        重新加载系统提示词
        
        Returns:
            bool: 重新加载成功返回True，失败返回False
        """
        print("🔄 重新加载系统提示词...")
        return self.load_system_prompt()
    
    def update_system_prompt(self, new_prompt: str) -> bool:
        """
        更新系统提示词并保存到文件
        
        Args:
            new_prompt: 新的系统提示词
            
        Returns:
            bool: 更新成功返回True，失败返回False
        """
        try:
            # 确保目录存在
            os.makedirs(os.path.dirname(self.prompt_file), exist_ok=True)
            
            with open(self.prompt_file, 'w', encoding='utf-8') as f:
                f.write(new_prompt.strip())
                
            self.system_prompt = new_prompt.strip()
            print(f"✅ 系统提示词已更新并保存到 {self.prompt_file}")
            return True
            
        except Exception as e:
            print(f"❌ 更新系统提示词失败: {e}")
            return False
    
    def _get_default_prompt(self) -> str:
        """
        获取默认系统提示词
        
        Returns:
            str: 默认系统提示词
        """
        return "你是一个有用的AI助手，请用简洁明了的方式回答用户的问题。保持回答准确、友好，并尽可能提供有价值的信息。"
    
    def _create_default_prompt(self) -> None:
        """
        创建默认的系统提示词文件
        """
        try:
            # 确保目录存在
            os.makedirs(os.path.dirname(self.prompt_file), exist_ok=True)
            
            default_prompt = self._get_default_prompt()
            with open(self.prompt_file, 'w', encoding='utf-8') as f:
                f.write(default_prompt)
                
            print(f"✅ 已创建默认系统提示词文件: {self.prompt_file}")
            self.system_prompt = default_prompt
            
        except Exception as e:
            print(f"❌ 创建默认系统提示词文件失败: {e}")
    
    def get_prompt_info(self) -> dict:
        """
        获取提示词信息
        
        Returns:
            dict: 包含提示词信息的字典
        """
        return {
            'file_path': self.prompt_file,
            'file_exists': os.path.exists(self.prompt_file),
            'prompt_length': len(self.system_prompt),
            'prompt_preview': self.system_prompt[:100] + '...' if len(self.system_prompt) > 100 else self.system_prompt
        }
    
    def validate_prompt_file(self) -> bool:
        """
        验证提示词文件的有效性
        
        Returns:
            bool: 文件有效返回True，无效返回False
        """
        if not os.path.exists(self.prompt_file):
            return False
            
        try:
            with open(self.prompt_file, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                return len(content) > 0
        except Exception:
            return False


def create_sample_prompts() -> None:
    """
    创建示例提示词文件
    """
    prompts = {
        "system.txt": "你是一个有用的AI助手，请用简洁明了的方式回答用户的问题。保持回答准确、友好，并尽可能提供有价值的信息。",
        "creative.txt": "你是一个富有创意的AI助手，擅长创意写作、头脑风暴和创新思维。请用富有想象力和创造性的方式回答用户的问题。",
        "technical.txt": "你是一个技术专家AI助手，专注于提供准确的技术信息、编程帮助和问题解决方案。请用专业、详细的方式回答技术相关问题。",
        "casual.txt": "你是一个友好随和的AI助手，用轻松、亲切的语调与用户交流。保持对话自然流畅，就像和朋友聊天一样。"
    }
    
    # 确保目录存在
    os.makedirs("prompts", exist_ok=True)
    
    for filename, content in prompts.items():
        filepath = os.path.join("prompts", filename)
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ 创建示例提示词文件: {filepath}")
        except Exception as e:
            print(f"❌ 创建文件 {filepath} 失败: {e}")


if __name__ == "__main__":
    # 测试提示词管理器
    prompt_manager = PromptManager()
    
    print("=== 提示词管理器测试 ===")
    
    # 加载系统提示词
    if prompt_manager.load_system_prompt():
        print(f"当前系统提示词: {prompt_manager.get_system_prompt()}")
    
    # 显示提示词信息
    info = prompt_manager.get_prompt_info()
    print(f"\n提示词信息:")
    for key, value in info.items():
        print(f"  {key}: {value}")
    
    # 创建示例提示词文件
    print("\n=== 创建示例提示词文件 ===")
    create_sample_prompts()