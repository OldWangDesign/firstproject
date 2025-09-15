#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
配置文件管理模块
负责读取、验证和管理应用程序配置
"""

import json
import os
from typing import Dict, Any, Optional


class ConfigManager:
    """配置管理器"""
    
    def __init__(self, config_file: str = "config.json"):
        """
        初始化配置管理器
        
        Args:
            config_file: 配置文件路径
        """
        self.config_file = config_file
        self.config: Dict[str, Any] = {}
        
    def load_config(self) -> bool:
        """
        加载配置文件
        
        Returns:
            bool: 加载成功返回True，失败返回False
        """
        try:
            if not os.path.exists(self.config_file):
                print(f"❌ 配置文件 {self.config_file} 不存在")
                print(f"💡 请复制 {self.config_file}.example 为 {self.config_file} 并配置您的API密钥")
                return False
                
            with open(self.config_file, 'r', encoding='utf-8') as f:
                self.config = json.load(f)
                
            # 验证配置
            if not self._validate_config():
                return False
                
            print("✅ 配置文件加载成功")
            return True
            
        except json.JSONDecodeError as e:
            print(f"❌ 配置文件格式错误: {e}")
            return False
        except Exception as e:
            print(f"❌ 加载配置文件失败: {e}")
            return False
    
    def _validate_config(self) -> bool:
        """
        验证配置文件的完整性
        
        Returns:
            bool: 验证通过返回True，失败返回False
        """
        # 检查必需的配置项
        required_keys = {
            'deepseek': ['api_key', 'base_url', 'model'],
            'app': ['system_prompt_file']
        }
        
        for section, keys in required_keys.items():
            if section not in self.config:
                print(f"❌ 配置文件缺少 '{section}' 部分")
                return False
                
            for key in keys:
                if key not in self.config[section]:
                    print(f"❌ 配置文件缺少 '{section}.{key}' 配置项")
                    return False
        
        # 检查API密钥是否为示例值
        api_key = self.config['deepseek']['api_key']
        if api_key == "your-deepseek-api-key-here" or not api_key.strip():
            print("❌ 请在配置文件中设置有效的DeepSeek API密钥")
            return False
            
        # 检查系统提示词文件是否存在
        prompt_file = self.config['app']['system_prompt_file']
        if not os.path.exists(prompt_file):
            print(f"❌ 系统提示词文件 {prompt_file} 不存在")
            return False
            
        return True
    
    def get_deepseek_config(self) -> Dict[str, Any]:
        """
        获取DeepSeek API配置
        
        Returns:
            Dict: DeepSeek配置字典
        """
        return self.config.get('deepseek', {})
    
    def get_app_config(self) -> Dict[str, Any]:
        """
        获取应用程序配置
        
        Returns:
            Dict: 应用程序配置字典
        """
        return self.config.get('app', {})
    
    def get_api_key(self) -> str:
        """
        获取API密钥
        
        Returns:
            str: API密钥
        """
        return self.config.get('deepseek', {}).get('api_key', '')
    
    def get_base_url(self) -> str:
        """
        获取API基础URL
        
        Returns:
            str: API基础URL
        """
        return self.config.get('deepseek', {}).get('base_url', 'https://api.deepseek.com/v1')
    
    def get_model(self) -> str:
        """
        获取模型名称
        
        Returns:
            str: 模型名称
        """
        return self.config.get('deepseek', {}).get('model', 'deepseek-chat')
    
    def get_max_tokens(self) -> int:
        """
        获取最大token数
        
        Returns:
            int: 最大token数
        """
        return self.config.get('deepseek', {}).get('max_tokens', 2000)
    
    def get_temperature(self) -> float:
        """
        获取温度参数
        
        Returns:
            float: 温度参数
        """
        return self.config.get('deepseek', {}).get('temperature', 0.7)
    
    def get_system_prompt_file(self) -> str:
        """
        获取系统提示词文件路径
        
        Returns:
            str: 系统提示词文件路径
        """
        return self.config.get('app', {}).get('system_prompt_file', 'prompts/system.txt')
    
    def get_max_history(self) -> int:
        """
        获取最大历史记录数
        
        Returns:
            int: 最大历史记录数
        """
        return self.config.get('app', {}).get('max_history', 10)


def create_example_config() -> None:
    """
    创建示例配置文件
    """
    example_config = {
        "deepseek": {
            "api_key": "your-deepseek-api-key-here",
            "base_url": "https://api.deepseek.com/v1",
            "model": "deepseek-chat",
            "max_tokens": 2000,
            "temperature": 0.7
        },
        "app": {
            "system_prompt_file": "prompts/system.txt",
            "max_history": 10
        }
    }
    
    with open("config.json.example", 'w', encoding='utf-8') as f:
        json.dump(example_config, f, indent=2, ensure_ascii=False)
    
    print("✅ 示例配置文件 config.json.example 已创建")


if __name__ == "__main__":
    # 测试配置管理器
    config_manager = ConfigManager()
    if config_manager.load_config():
        print(f"API密钥: {config_manager.get_api_key()[:10]}...")
        print(f"模型: {config_manager.get_model()}")
        print(f"系统提示词文件: {config_manager.get_system_prompt_file()}")
    else:
        print("配置加载失败")