#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DeepSeek API客户端模块
负责与DeepSeek API进行通信
"""

import json
import requests
import time
from typing import Dict, List, Any, Optional, Generator
from dataclasses import dataclass


@dataclass
class ChatMessage:
    """聊天消息数据类"""
    role: str  # 'system', 'user', 'assistant'
    content: str
    
    def to_dict(self) -> Dict[str, str]:
        """转换为字典格式"""
        return {'role': self.role, 'content': self.content}


class DeepSeekClient:
    """DeepSeek API客户端"""
    
    def __init__(self, api_key: str, base_url: str = "https://api.deepseek.com/v1", 
                 model: str = "deepseek-chat", max_tokens: int = 2000, 
                 temperature: float = 0.7, timeout: int = 30):
        """
        初始化DeepSeek客户端
        
        Args:
            api_key: API密钥
            base_url: API基础URL
            model: 模型名称
            max_tokens: 最大token数
            temperature: 温度参数
            timeout: 请求超时时间(秒)
        """
        self.api_key = api_key
        self.base_url = base_url.rstrip('/')
        self.model = model
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.timeout = timeout
        
        # 设置请求头
        self.headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json',
            'User-Agent': 'DeepSeek-CLI-Chat/1.0'
        }
        
        # 会话管理
        self.conversation_history: List[ChatMessage] = []
        self.max_history = 10
    
    def set_system_prompt(self, system_prompt: str) -> None:
        """
        设置系统提示词
        
        Args:
            system_prompt: 系统提示词内容
        """
        # 移除旧的系统消息
        self.conversation_history = [msg for msg in self.conversation_history if msg.role != 'system']
        
        # 添加新的系统消息到开头
        if system_prompt.strip():
            system_message = ChatMessage(role='system', content=system_prompt.strip())
            self.conversation_history.insert(0, system_message)
    
    def add_user_message(self, content: str) -> None:
        """
        添加用户消息到对话历史
        
        Args:
            content: 用户消息内容
        """
        user_message = ChatMessage(role='user', content=content)
        self.conversation_history.append(user_message)
        self._trim_history()
    
    def add_assistant_message(self, content: str) -> None:
        """
        添加助手消息到对话历史
        
        Args:
            content: 助手消息内容
        """
        assistant_message = ChatMessage(role='assistant', content=content)
        self.conversation_history.append(assistant_message)
        self._trim_history()
    
    def _trim_history(self) -> None:
        """
        修剪对话历史，保持在最大长度内
        系统消息始终保留
        """
        # 分离系统消息和其他消息
        system_messages = [msg for msg in self.conversation_history if msg.role == 'system']
        other_messages = [msg for msg in self.conversation_history if msg.role != 'system']
        
        # 保留最近的消息
        if len(other_messages) > self.max_history:
            other_messages = other_messages[-self.max_history:]
        
        # 重新组合
        self.conversation_history = system_messages + other_messages
    
    def chat(self, user_input: str) -> Optional[str]:
        """
        发送聊天请求并获取回复
        
        Args:
            user_input: 用户输入
            
        Returns:
            Optional[str]: AI回复内容，失败时返回None
        """
        try:
            # 添加用户消息
            self.add_user_message(user_input)
            
            # 准备请求数据
            messages = [msg.to_dict() for msg in self.conversation_history]
            
            request_data = {
                'model': self.model,
                'messages': messages,
                'max_tokens': self.max_tokens,
                'temperature': self.temperature,
                'stream': False
            }
            
            # 发送请求
            print("🤖 正在思考...")
            start_time = time.time()
            
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=self.headers,
                json=request_data,
                timeout=self.timeout
            )
            
            end_time = time.time()
            response_time = end_time - start_time
            
            # 检查响应状态
            if response.status_code == 200:
                response_data = response.json()
                
                # 提取回复内容
                if 'choices' in response_data and len(response_data['choices']) > 0:
                    assistant_reply = response_data['choices'][0]['message']['content']
                    
                    # 添加助手回复到历史
                    self.add_assistant_message(assistant_reply)
                    
                    # 显示响应时间和token使用情况
                    usage = response_data.get('usage', {})
                    self._print_response_info(response_time, usage)
                    
                    return assistant_reply
                else:
                    print("❌ API响应格式异常")
                    return None
            else:
                self._handle_api_error(response)
                return None
                
        except requests.exceptions.Timeout:
            print(f"❌ 请求超时 (>{self.timeout}秒)，请检查网络连接")
            return None
        except requests.exceptions.ConnectionError:
            print("❌ 网络连接失败，请检查网络设置")
            return None
        except requests.exceptions.RequestException as e:
            print(f"❌ 请求失败: {e}")
            return None
        except json.JSONDecodeError:
            print("❌ API响应解析失败")
            return None
        except Exception as e:
            print(f"❌ 未知错误: {e}")
            return None
    
    def _handle_api_error(self, response: requests.Response) -> None:
        """
        处理API错误响应
        
        Args:
            response: HTTP响应对象
        """
        try:
            error_data = response.json()
            error_message = error_data.get('error', {}).get('message', '未知错误')
            error_type = error_data.get('error', {}).get('type', 'unknown')
            
            if response.status_code == 401:
                print("❌ API密钥无效，请检查配置文件中的API密钥")
            elif response.status_code == 429:
                print("❌ API调用频率超限，请稍后再试")
            elif response.status_code == 400:
                print(f"❌ 请求参数错误: {error_message}")
            elif response.status_code == 500:
                print("❌ 服务器内部错误，请稍后再试")
            else:
                print(f"❌ API错误 ({response.status_code}): {error_message}")
                
        except json.JSONDecodeError:
            print(f"❌ HTTP错误 {response.status_code}: {response.text[:200]}")
    
    def _print_response_info(self, response_time: float, usage: Dict[str, Any]) -> None:
        """
        打印响应信息
        
        Args:
            response_time: 响应时间
            usage: token使用情况
        """
        info_parts = [f"⏱️ {response_time:.2f}s"]
        
        if usage:
            if 'prompt_tokens' in usage:
                info_parts.append(f"📝 {usage['prompt_tokens']} tokens")
            if 'completion_tokens' in usage:
                info_parts.append(f"🤖 {usage['completion_tokens']} tokens")
            if 'total_tokens' in usage:
                info_parts.append(f"📊 总计 {usage['total_tokens']} tokens")
        
        print(f"ℹ️ {' | '.join(info_parts)}")
    
    def clear_history(self) -> None:
        """
        清空对话历史（保留系统消息）
        """
        system_messages = [msg for msg in self.conversation_history if msg.role == 'system']
        self.conversation_history = system_messages
        print("🗑️ 对话历史已清空")
    
    def get_history_summary(self) -> Dict[str, Any]:
        """
        获取对话历史摘要
        
        Returns:
            Dict: 历史摘要信息
        """
        total_messages = len(self.conversation_history)
        system_count = len([msg for msg in self.conversation_history if msg.role == 'system'])
        user_count = len([msg for msg in self.conversation_history if msg.role == 'user'])
        assistant_count = len([msg for msg in self.conversation_history if msg.role == 'assistant'])
        
        return {
            'total_messages': total_messages,
            'system_messages': system_count,
            'user_messages': user_count,
            'assistant_messages': assistant_count,
            'max_history': self.max_history
        }
    
    def test_connection(self) -> bool:
        """
        测试API连接
        
        Returns:
            bool: 连接成功返回True，失败返回False
        """
        try:
            print("🔍 测试API连接...")
            
            # 发送一个简单的测试请求
            test_messages = [
                {'role': 'user', 'content': 'Hello'}
            ]
            
            request_data = {
                'model': self.model,
                'messages': test_messages,
                'max_tokens': 10,
                'temperature': 0.1
            }
            
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=self.headers,
                json=request_data,
                timeout=10
            )
            
            if response.status_code == 200:
                print("✅ API连接测试成功")
                return True
            else:
                print(f"❌ API连接测试失败: HTTP {response.status_code}")
                self._handle_api_error(response)
                return False
                
        except Exception as e:
            print(f"❌ API连接测试失败: {e}")
            return False


if __name__ == "__main__":
    # 测试API客户端
    print("=== DeepSeek API客户端测试 ===")
    print("注意: 需要有效的API密钥才能进行测试")
    
    # 这里只是示例，实际使用时需要真实的API密钥
    test_api_key = "your-api-key-here"
    
    if test_api_key != "your-api-key-here":
        client = DeepSeekClient(api_key=test_api_key)
        
        # 测试连接
        if client.test_connection():
            # 设置系统提示词
            client.set_system_prompt("你是一个有用的AI助手。")
            
            # 测试对话
            response = client.chat("你好！")
            if response:
                print(f"AI回复: {response}")
                
            # 显示历史摘要
            summary = client.get_history_summary()
            print(f"对话历史: {summary}")
    else:
        print("⚠️ 请设置有效的API密钥进行测试")