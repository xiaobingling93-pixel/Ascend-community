#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gitcode门禁检查脚本，包含如下规则：
1. 检查yaml格式
2. 检查每个项目目录下的sigs目录中的子目录（除去ascend）是否存在于该项目目录下的org-info.yaml的sig_name字段中
3. 检查org-info.yaml、sig-info.yaml中的gitcode_id是否存在
4. 检查repo-info.yaml文件位置是否正确
5. 检查org-info.yaml中每个sig maintainer至少需要两位
6. 检查整个仓库中的sig名是否唯一
7. 检查sig目录名和sig-info.yaml中的name字段是否一致
8. 检查sig-info.yaml中仓库是否存在
9. 检查仓库类型是否为public
"""

import os
import sys
import yaml
import time
import shutil
import subprocess
from pathlib import Path
from typing import Dict, List, Any, Optional, Set
import requests
import argparse
from collections import defaultdict

GITCODE_BASE_URL = "https://api.gitcode.com/api/v5/"

class GitCodeAdapter:
    def __init__(self, base_url: str, token: str):
        self.base_url = base_url.rstrip('/') + '/'
        self.token = token
        self.session = requests.Session()
        if token:
            self.session.params = {"access_token": token}
    
    def get_user(self, username: str) -> bool:
        """获取用户信息"""
        endpoint = f"{self.base_url}users/{username}"
        headers = {'Accept': 'application/json'}
        response = self.session.get(endpoint, headers=headers, timeout=15)
        return response.status_code == 200
            
    def get_repo(self, owner: str, repo: str) -> bool:
        url = f"{self.base_url}repos/{owner}/{repo}/repo_settings"
        headers = {'Accept': 'application/json'}
        response = self.session.get(url, headers=headers, timeout=15)
        return response.status_code == 200


class GitcodeGateCheck:
    def __init__(self, 
                 repo_root: str = ".",
                 gitcode_token: str = "",
                 gitcode_namespace: Optional[str] = None,
                 gitcode_project: Optional[str] = None,
                 clone_url: Optional[str] = None,
                 cache_ttl: int = 300,
                 ):
        """
        初始化检查器
        """
        self.repo_root = Path(repo_root)
        self.gitcode_api_base = GITCODE_BASE_URL.rstrip('/') + '/'
        self.gitcode_token = gitcode_token or os.environ.get("GITCODE_TOKEN")
        self.gitcode_namespace = gitcode_namespace or os.environ.get("GITCODE_NAMESPACE")
        self.gitcode_project = gitcode_project or os.environ.get("GITCODE_PROJECT")
        self.clone_url = clone_url
        self.cache_ttl = cache_ttl
        
        # 克隆相关属性
        self.temp_dir = None
        self.cloned_repo_path = None
        
        # 初始化缓存和会话
        self.gitcode_id_cache = {}
        self.repo_exists_cache = {}
        
        # 创建GitCode适配器，参考第一个代码
        self.gitcode_adapter = GitCodeAdapter(
            base_url=self.gitcode_api_base,
            token=self.gitcode_token
        )
        
        # 错误列表（按类别组织）
        self.errors_by_category = defaultdict(list)  # 按错误类别组织的错误列表
        self.errors = []  # 保持向后兼容
        
        # 新增：收集所有sig名的集合
        self.all_sig_names = set()  # 所有收集到的sig名
        self.sig_directories_info = defaultdict(list)  # 按项目目录存储(sig目录名, sig目录路径)列表
    
    def add_error(self, message: str, file_path: Optional[str] = None, category: Optional[str] = None):
        """添加错误信息，可指定错误类别"""
        error_msg = f"{file_path}: {message}" if file_path else message
        
        # 添加到向后兼容的错误列表
        self.errors.append(error_msg)
        
        # 按类别分组
        if category:
            self.errors_by_category[category].append(error_msg)
        else:
            # 如果没有指定类别，尝试根据消息内容自动分类
            category = self._detect_error_category(message)
            self.errors_by_category[category].append(error_msg)
    
    def _detect_error_category(self, message: str) -> str:
        """根据错误消息内容自动检测错误类别"""
        # org-info.yaml 相关错误
        if "缺少必须字段" in message:
            return "缺少必须字段"
        elif "gitcode_id不存在" in message:
            return "gitcode_id不存在"
        elif "仓库不存在" in message:
            return "仓库不存在"
        elif "文件位置错误" in message or "必须在ascend目录下" in message:
            return "文件位置错误"
        elif "不一致" in message:
            return "字段不一致"
        elif "至少需要" in message:
            return "数量检查错误"
        elif "必须是列表类型" in message or "格式错误" in message:
            return "格式错误"
        elif "仓库类型必须是" in message:
            return "仓库类型错误"
        elif "仓库名不能包含空格" in message:
            return "命名规范错误"
        elif "sig名必须是唯一的" in message or "重复的sig名" in message:
            return "sig名重复"
        elif "sig目录" in message and "不在org-info.yaml的sig_name列表中" in message:
            return "sig目录未注册"
        else:
            return "其他错误"
    
    def collect_gitcode_ids(self, data: Dict[str, Any]) -> Set[str]:
        """
        递归收集data中所有的gitcode_id
        """
        gitcode_ids = set()
        
        def _collect(obj, path=""):
            if isinstance(obj, dict):
                for key, value in obj.items():
                    if key == 'gitcode_id' and isinstance(value, str) and value.strip():
                        gitcode_id = value.strip()
                        gitcode_ids.add(gitcode_id)
                    elif isinstance(value, (dict, list)):
                        _collect(value, f"{path}.{key}" if path else key)
            elif isinstance(obj, list):
                for i, item in enumerate(obj):
                    if isinstance(item, (dict, list)):
                        _collect(item, f"{path}[{i}]")
        
        _collect(data)
        return gitcode_ids
    
    def clone_repository(self) -> bool:
        """
        克隆远程仓库到当前工作目录下的临时目录
        """
        # 确定克隆URL
        url_to_clone = self.clone_url
        if not url_to_clone and self.gitcode_namespace and self.gitcode_project:
            # 构建标准GitCode HTTPS URL
            url_to_clone = f"https://gitcode.com/{self.gitcode_namespace}/{self.gitcode_project}.git"
        
        if not url_to_clone:
            # 如果没有克隆URL，直接返回失败
            self.add_error("未提供克隆URL或namespace/project信息", category="系统错误")
            return False
        
        print(f"正在克隆仓库: {url_to_clone}")
        
        try:
            # 获取当前工作目录
            current_dir = Path.cwd()
            
            # 在当前工作目录下创建临时目录
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            clone_dir_name = f"gitcode_check_{self.gitcode_project or 'repo'}_{timestamp}"
            self.temp_dir = current_dir / clone_dir_name
            
            # 如果目录已存在，先删除
            if self.temp_dir.exists():
                shutil.rmtree(self.temp_dir)
            
            # 创建目录
            self.temp_dir.mkdir(parents=True, exist_ok=True)
            
            print(f"创建克隆目录: {self.temp_dir}")
            
            # 执行git clone
            clone_cmd = ["git", "clone", "--depth=1", url_to_clone, str(self.temp_dir)]
            
            result = subprocess.run(
                clone_cmd,
                capture_output=True,
                text=True,
                timeout=300
            )
            
            if result.returncode != 0:
                self.add_error(f"克隆仓库失败: {result.stderr}", category="系统错误")
                if self.temp_dir.exists():
                    shutil.rmtree(self.temp_dir, ignore_errors=True)
                return False
            
            print(f"✓ 仓库已克隆到: {self.temp_dir}")
            
            # 更新repo_root为克隆的仓库路径
            self.cloned_repo_path = self.temp_dir
            
            # 检查克隆后是否存在可能的子目录
            dir_contents = list(self.temp_dir.iterdir())
            if len(dir_contents) == 1 and dir_contents[0].is_dir():
                # 如果只有一个子目录，很可能仓库内容在其中
                self.repo_root = dir_contents[0]
                print(f"✓ 仓库内容在子目录: {self.repo_root}")
            else:
                self.repo_root = self.temp_dir
                print(f"✓ 仓库内容在根目录: {self.repo_root}")
            
            return True
            
        except subprocess.TimeoutExpired:
            self.add_error("克隆操作超时（300秒）", category="系统错误")
            if hasattr(self, 'temp_dir') and self.temp_dir and self.temp_dir.exists():
                shutil.rmtree(self.temp_dir, ignore_errors=True)
            return False
        except Exception as e:
            self.add_error(f"克隆过程中发生错误: {str(e)}", category="系统错误")
            if hasattr(self, 'temp_dir') and self.temp_dir and self.temp_dir.exists():
                shutil.rmtree(self.temp_dir, ignore_errors=True)
            return False
    
    def cleanup(self):
        """清理临时目录（如果存在）"""
        if self.temp_dir and Path(self.temp_dir).exists():
            try:
                shutil.rmtree(self.temp_dir)
                print(f"已清理临时目录: {self.temp_dir}")
            except Exception as e:
                # 清理失败不视为错误
                pass
    
    def load_yaml_file(self, file_path: Path) -> Optional[Dict[str, Any]]:
        """加载YAML文件并进行基本格式校验"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = yaml.safe_load(f)
                
            if content is None:
                self.add_error("YAML文件为空", str(file_path), "格式错误")
                return None
                
            return content
            
        except yaml.YAMLError as e:
            self.add_error(f"YAML格式错误: {str(e)}", str(file_path), "格式错误")
            return None
        except Exception as e:
            self.add_error(f"读取文件失败: {str(e)}", str(file_path), "系统错误")
            return None
    
    # ========== 规则检查方法 ==========
    
    def check_org_info_required_fields(self, data: Dict[str, Any], file_path: str):
        """检查org-info.yaml的必须字段"""
        required_fields = ['sigs', 'name', 'tc_members']
        
        for field in required_fields:
            if field not in data:
                self.add_error(f"缺少必须字段: {field}", file_path, "缺少必须字段")
        
        # 检查sigs字段，确保它是列表类型
        if 'sigs' in data:
            sigs = data['sigs']
            if not isinstance(sigs, list):
                self.add_error("sigs字段必须是列表类型", file_path, "格式错误")
                return
            
            # 检查每个sig
            for i, sig in enumerate(sigs):
                if not isinstance(sig, dict):
                    self.add_error(f"sigs[{i}]必须是字典类型", file_path, "格式错误")
                    continue
                
                # 检查sig_name字段
                if 'sig_name' not in sig:
                    self.add_error(f"sigs[{i}]缺少sig_name字段", file_path, "缺少必须字段")
                elif not isinstance(sig['sig_name'], str) or not sig['sig_name'].strip():
                    self.add_error(f"sigs[{i}]的sig_name字段必须是有效的字符串", file_path, "格式错误")
                
                # 规则5: 每个sig的maintainer至少需要两位
                if 'maintainers' in sig:
                    maintainers = sig['maintainers']
                    if isinstance(maintainers, list):
                        if len(maintainers) < 2:
                            sig_name = sig.get('sig_name', f'sig_{i}')
                            self.add_error(f"sig '{sig_name}' 的maintainer至少需要两位，当前只有 {len(maintainers)} 位", 
                                         file_path, "数量检查错误")
                        
                        # 检查每个maintainer
                        for j, maintainer in enumerate(maintainers):
                            if isinstance(maintainer, dict):
                                if 'gitcode_id' in maintainer:
                                    gitcode_id = maintainer['gitcode_id']
                                    if isinstance(gitcode_id, str) and gitcode_id.strip():
                                        # 直接验证gitcode_id
                                        # self.verify_gitcode_id(gitcode_id, file_path)
                                        pass
                                    else:
                                        sig_name = sig.get('sig_name', f'sig_{i}')
                                        self.add_error(f"sig '{sig_name}' 的第 {j+1} 个maintainer的gitcode_id无效", 
                                                     file_path, "格式错误")
                                else:
                                    sig_name = sig.get('sig_name', f'sig_{i}')
                                    self.add_error(f"sig '{sig_name}' 的第 {j+1} 个maintainer缺少gitcode_id字段", 
                                                 file_path, "缺少必须字段")
                            else:
                                sig_name = sig.get('sig_name', f'sig_{i}')
                                self.add_error(f"sig '{sig_name}' 的第 {j+1} 个maintainer格式错误，应为字典类型", 
                                             file_path, "格式错误")
                    else:
                        sig_name = sig.get('sig_name', f'sig_{i}')
                        self.add_error(f"sig '{sig_name}' 的maintainers字段必须是列表类型", file_path, "格式错误")
                else:
                    sig_name = sig.get('sig_name', f'sig_{i}')
                    self.add_error(f"sig '{sig_name}' 缺少maintainers字段", file_path, "缺少必须字段")
        
        # 额外收集并验证所有gitcode_id
        self.collect_and_verify_gitcode_ids(data, file_path)
    
    def check_sig_info_required_fields(self, data: Dict[str, Any], file_path: str):
        """检查sig-info.yaml的必须字段"""
        required_fields = [
            'name',
            'description',
            'mailing_list',
            'meeting_url',
        ]
        
        for field in required_fields:
            if field not in data:
                self.add_error(f"缺少必须字段: {field}", file_path, "缺少必须字段")
        
        # 检查committers和reviewers字段
        for field_name in ['committers', 'reviewers']:
            if field_name in data:
                members = data[field_name]
                if isinstance(members, list):
                    for i, member in enumerate(members):
                        if isinstance(member, dict):
                            if 'gitcode_id' not in member:
                                self.add_error(f"{field_name} 中第 {i+1} 个成员缺少gitcode_id字段", file_path, "缺少必须字段")
                        else:
                            self.add_error(f"{field_name} 中第 {i+1} 个成员不是字典类型", file_path, "格式错误")
                else:
                    self.add_error(f"{field_name}字段必须是列表类型", file_path, "格式错误")
        
        # 检查mentors字段（如果存在）
        if 'mentors' in data:
            mentors = data['mentors']
            if isinstance(mentors, list):
                for i, mentor in enumerate(mentors):
                    if isinstance(mentor, dict) and 'gitcode_id' in mentor:
                        gitcode_id = mentor['gitcode_id']
                        if isinstance(gitcode_id, str) and gitcode_id.strip():
                            # 直接验证gitcode_id
                            self.verify_gitcode_id(gitcode_id, file_path)
        
        # 额外收集并验证所有gitcode_id
        self.collect_and_verify_gitcode_ids(data, file_path)
    
    def check_repo_info_required_fields(self, data: Dict[str, Any], file_path: str):
        """检查repo-info.yaml的必须字段"""
        required_fields = ['name', 'description', 'type', 'branches']
        
        for field in required_fields:
            if field not in data:
                self.add_error(f"缺少必须字段: {field}", file_path, "缺少必须字段")
        
        # 规则4: repo-info.yaml只能放公仓信息，不能放私仓信息
        if 'type' in data:
            if data['type'] != 'public':
                self.add_error(f"仓库类型必须是'public'，当前为'{data['type']}'", file_path, "仓库类型错误")
        
        # 检查branches字段
        if 'branches' in data:
            branches = data['branches']
            if isinstance(branches, list):
                for i, branch in enumerate(branches):
                    if isinstance(branch, dict):
                        if 'name' not in branch:
                            self.add_error(f"branches[{i}]缺少name字段", file_path, "缺少必须字段")
                        
                        # 检查type字段的值
                        if 'type' in branch and branch['type'] not in [None, 'protected']:
                            self.add_error(f"branches[{i}].type字段只能是'protected'或为空", file_path, "格式错误")
                    else:
                        self.add_error(f"branches[{i}]不是字典类型", file_path, "格式错误")
            else:
                self.add_error("branches字段必须是列表类型", file_path, "格式错误")
        
        # 检查仓库名是否包含空格
        if 'name' in data and isinstance(data['name'], str):
            if ' ' in data['name']:
                self.add_error("仓库名不能包含空格", file_path, "命名规范错误")
        
        # 收集并验证所有gitcode_id
        self.collect_and_verify_gitcode_ids(data, file_path)
    
    def collect_and_verify_gitcode_ids(self, data: Dict[str, Any], file_path: str):
        """收集并验证数据中的所有gitcode_id"""
        gitcode_ids = self.collect_gitcode_ids(data)
        for gitcode_id in gitcode_ids:
            self.verify_gitcode_id(gitcode_id, file_path)
    
    def verify_gitcode_id(self, gitcode_id: str, file_path: str):
        """验证单个gitcode_id是否存在"""
        result = self.verify_gitcode_id_via_api(gitcode_id)
        
        if result is None:
            # API错误或网络问题视为错误
            self.add_error(f"无法验证gitcode_id: {gitcode_id} (API错误或网络问题)", file_path, "gitcode_id不存在")
        elif result is False:
            format_file_path = "/".join(file_path.split("/")[2:])
            self.add_error(f"gitcode_id不存在: {format_file_path}: {gitcode_id}", file_path, "gitcode_id不存在")
    
    def verify_gitcode_id_via_api(self, gitcode_id: str) -> Optional[bool]:
        try:
            # 使用适配器获取用户信息，参考第一个代码
            exists = self.gitcode_adapter.get_user(gitcode_id)
            return exists
            
        except Exception as e:
            # API调用异常，返回None
            return None
    
    def check_sig_consistency(self, file_path: Path, data: Dict[str, Any]):
        """校验sig目录名和org-info.yaml中的sig_name字段和sig-info.yaml中的name字段，三处是否一致"""
        sig_dir = file_path.parent.name
        
        if file_path.name == 'org-info.yaml':
            if 'sig_name' in data and isinstance(data['sig_name'], str):
                org_sig_name = data['sig_name']
                
                # 新增：收集sig名用于唯一性检查
                self.collect_sig_name(org_sig_name, str(file_path))
                
                if org_sig_name != sig_dir:
                    self.add_error(f"org-info.yaml中的sig_name字段('{org_sig_name}')与目录名('{sig_dir}')不一致", str(file_path), "字段不一致")
                
                sig_info_path = file_path.parent / 'sig-info.yaml'
                if sig_info_path.exists():
                    sig_info_data = self.load_yaml_file(sig_info_path)
                    if sig_info_data and 'name' in sig_info_data:
                        sig_info_name = sig_info_data['name']
                        if sig_info_name != org_sig_name:
                            self.add_error(f"org-info.yaml中的sig_name字段('{org_sig_name}')与sig-info.yaml中的name字段('{sig_info_name}')不一致", str(file_path), "字段不一致")
                        if sig_info_name != sig_dir:
                            self.add_error(f"sig-info.yaml中的name字段('{sig_info_name}')与目录名('{sig_dir}')不一致", str(sig_info_path), "字段不一致")
        
        elif file_path.name == 'sig-info.yaml':
            if 'name' in data and isinstance(data['name'], str):
                sig_info_name = data['name']
                
                # 新增：收集sig名用于唯一性检查
                self.collect_sig_name(sig_info_name, str(file_path))
                
                if sig_info_name != sig_dir:
                    self.add_error(f"sig-info.yaml中的name字段('{sig_info_name}')与目录名('{sig_dir}')不一致", str(file_path), "字段不一致")
                
                org_info_path = file_path.parent / 'org-info.yaml'
                if org_info_path.exists():
                    org_info_data = self.load_yaml_file(org_info_path)
                    if org_info_data and 'sig_name' in org_info_data:
                        org_sig_name = org_info_data['sig_name']
                        if org_sig_name != sig_info_name:
                            self.add_error(f"sig-info.yaml中的name字段('{sig_info_name}')与org-info.yaml中的sig_name字段('{org_sig_name}')不一致", str(file_path), "字段不一致")
                        if org_sig_name != sig_dir:
                            self.add_error(f"org-info.yaml中的sig_name字段('{org_sig_name}')与目录名('{sig_dir}')不一致", str(org_info_path), "字段不一致")
    
    def collect_sig_name(self, sig_name: str, file_path: str):
        """收集sig名用于唯一性检查"""
        if sig_name in self.all_sig_names:
            self.add_error(f"重复的sig名: '{sig_name}'，整个仓库中的sig名必须是唯一的", file_path, "sig名重复")
        self.all_sig_names.add(sig_name)
    
    def verify_repo_exists_via_api(self, repo_path: str) -> Optional[bool]:
        """
        通过Gitcode API验证仓库是否存在
        使用参考代码中的适配器模式
        """
        
        current_time = time.time()
        if repo_path in self.repo_exists_cache:
            exists, timestamp = self.repo_exists_cache[repo_path]
            if current_time - timestamp < self.cache_ttl:
                return exists
        
        if not self.gitcode_token:
            # 没有token无法验证，返回None
            return None
        
        try:
            # 解析repo_path格式：owner/repo 或 namespace/repo
            parts = repo_path.split('/')
            if len(parts) != 2:
                # 路径格式错误
                return None
            
            owner, repo = parts
            
            # 使用适配器获取仓库信息
            exists = self.gitcode_adapter.get_repo(owner, repo)
            
            self.repo_exists_cache[repo_path] = (exists, current_time)
            return exists
            
        except Exception as e:
            # API调用异常，返回None
            return None
    
    def check_sig_info_repos_exist(self, data: Dict[str, Any], file_path: str):
        """校验sig-info里的repo是否存在"""
        if not self.gitcode_token:
            # 没有token，跳过验证
            return
        
        if 'repositories' in data and isinstance(data['repositories'], list):
            for i, repo_info in enumerate(data['repositories']):
                if isinstance(repo_info, dict) and 'repo' in repo_info:
                    repos = repo_info['repo']
                    if isinstance(repos, list):
                        for repo in repos:
                            if isinstance(repo, str):
                                exists = self.verify_repo_exists_via_api(repo)
                                if exists is None:
                                    # API错误或格式错误，不记录错误
                                    pass
                                elif exists is False:
                                    self.add_error(f"仓库不存在: {repo}", file_path, "仓库不存在")
    
    def check_repo_info_file_location(self, file_path: Path, data: Dict[str, Any]):
        """检查repo-info.yaml文件位置是否正确"""
        if 'ascend' not in file_path.parts:
            self.add_error("repo-info.yaml文件必须在ascend目录下", str(file_path), "文件位置错误")
            return
        
        parts = file_path.relative_to(self.repo_root).parts
        
        if len(parts) < 4:
            self.add_error(f"repo-info.yaml文件路径不符合规范: {file_path}", str(file_path), "文件位置错误")
            return
        
        # 检查路径结构：项目/sigs/SIG目录/ascend/repo-info.yaml
        if parts[1] == 'sigs':
            # 这是正确的结构：项目/sigs/SIG目录/ascend/repo-info.yaml
            pass
        else:
            self.add_error(f"repo-info.yaml文件必须在sigs目录下的ascend目录中", str(file_path), "文件位置错误")
            return
        
        # 检查文件名
        if 'name' in data:
            repo_name = data['name']
            expected_filename = f"{repo_name}.yaml"
            if file_path.name != expected_filename:
                self.add_error(f"文件名应为'{expected_filename}'，实际为'{file_path.name}'", str(file_path), "文件位置错误")
    
    # ========== 新增的校验规则方法 ==========
    
    def check_unique_sig_names(self):
        """
        规则1: 检查整个仓库中的sig名是否唯一
        这个方法在检查完所有文件后调用
        """
        if len(self.all_sig_names) > 0:
            print(f"检查到 {len(self.all_sig_names)} 个不同的sig名")
            
            # 如果有重复，错误已经在collect_sig_name中添加了
            duplicate_count = len([e for e in self.errors if "重复的sig名" in e])
            if duplicate_count > 0:
                print(f"发现 {duplicate_count} 个重复的sig名")
        else:
            print("未检查到任何sig名，跳过sig名唯一性检查")
    
    def collect_project_sig_directories(self):
        """
        收集每个项目下的sigs目录信息
        根据目录结构：项目目录/sigs/SIG目录
        """
        print("收集项目目录和sigs目录信息...")
        
        # 查找所有项目目录（包含org-info.yaml的目录）
        project_dirs = []
        for org_info_file in self.repo_root.rglob("org-info.yaml"):
            project_dir = org_info_file.parent
            if project_dir not in project_dirs:
                project_dirs.append(project_dir)
                print(f"发现项目目录: {project_dir.relative_to(self.repo_root)}")
        
        if not project_dirs:
            print("未找到任何项目目录（包含org-info.yaml的目录）")
            return
        
        # 对每个项目目录，收集其sigs目录下的SIG子目录
        for project_dir in project_dirs:
            project_name = project_dir.name
            sigs_dir = project_dir / "sigs"
            
            if not sigs_dir.exists() or not sigs_dir.is_dir():
                print(f"项目 '{project_name}' 中没有sigs目录")
                continue
            
            print(f"检查项目 '{project_name}' 的sigs目录: {sigs_dir.relative_to(self.repo_root)}")
            
            # 收集sigs目录下的所有SIG子目录（除去ascend）
            sig_dirs = []
            for item in sigs_dir.iterdir():
                if item.is_dir() and item.name != 'ascend':
                    # 检查SIG目录中是否有sig-info.yaml文件
                    sig_info_path = item / "sig-info.yaml"
                    if sig_info_path.exists():
                        sig_dirs.append((item.name, str(item.relative_to(self.repo_root))))
                        print(f"  发现SIG目录: {item.name}")
                    else:
                        # SIG目录中没有sig-info.yaml视为错误
                        self.add_error(f"SIG目录 '{item.name}' 中没有sig-info.yaml文件", str(item), "缺少必须字段")
            
            if sig_dirs:
                self.sig_directories_info[str(project_dir)] = sig_dirs
    
    def check_sig_directories_in_project_org_info(self):
        """
        规则2: 检查每个项目目录下的sigs目录中的子目录（除去ascend）
              是否存在于该项目目录下的org-info.yaml的sig_name字段中
        """
        if not self.sig_directories_info:
            print("未收集到任何项目下的sig目录信息，跳过sig目录校验")
            return
        
        print(f"\n开始检查规则2: 项目sigs目录下的SIG子目录是否在项目org-info.yaml中注册")
        
        total_projects = len(self.sig_directories_info)
        total_sig_dirs = sum(len(dirs) for dirs in self.sig_directories_info.values())
        print(f"共检查 {total_projects} 个项目，{total_sig_dirs} 个SIG目录")
        
        for project_dir_path, sig_dirs in self.sig_directories_info.items():
            project_dir = Path(project_dir_path)
            project_name = project_dir.name
            
            # 找到项目目录下的org-info.yaml
            org_info_path = project_dir / "org-info.yaml"
            
            if not org_info_path.exists():
                # 如果没有找到org-info.yaml，报告错误
                self.add_error(f"项目目录 '{project_name}' 中缺少org-info.yaml文件", str(project_dir), "sig目录未注册")
                continue
            
            relative_org_path = org_info_path.relative_to(self.repo_root)
            print(f"\n检查项目: {project_name}")
            print(f"对应org-info.yaml: {relative_org_path}")
            
            # 加载org-info.yaml
            org_info_data = self.load_yaml_file(org_info_path)
            if not org_info_data:
                self.add_error(f"无法加载org-info.yaml文件: {relative_org_path}", str(org_info_path), "格式错误")
                continue
            
            # 获取org-info.yaml中的sig_name列表
            org_sig_names = set()
            if 'sigs' in org_info_data and isinstance(org_info_data['sigs'], list):
                for sig in org_info_data['sigs']:
                    if isinstance(sig, dict) and 'sig_name' in sig and isinstance(sig['sig_name'], str):
                        org_sig_names.add(sig['sig_name'].strip())
            
            if not org_sig_names:
                self.add_error(f"org-info.yaml中没有找到有效的sig_name列表", str(org_info_path), "缺少必须字段")
                continue
            
            print(f"org-info.yaml中包含 {len(org_sig_names)} 个sig_name: {sorted(org_sig_names)}")
            
            # 检查该项目目录下的所有SIG目录是否在org-info.yaml的sig_name列表中
            sig_dirs_checked = 0
            sig_dirs_valid = 0
            
            for sig_dir_name, sig_dir_path in sig_dirs:
                if sig_dir_name in org_sig_names:
                    print(f"  ✓ SIG目录 '{sig_dir_name}' 在项目org-info.yaml中已注册")
                    sig_dirs_valid += 1
                else:
                    self.add_error(f"SIG目录 '{sig_dir_name}' 不在项目org-info.yaml的sig_name列表中", 
                                 str(org_info_path), "sig目录未注册")
                    print(f"  ✗ SIG目录 '{sig_dir_name}' 未在项目org-info.yaml中注册")
                sig_dirs_checked += 1
            
            print(f"  完成检查: {sig_dirs_valid}/{sig_dirs_checked} 个SIG目录已注册")
    
    # ========== 主检查流程 ==========
    
    def check_all_files(self, file_patterns: Optional[List[str]] = None) -> bool:
        """检查所有相关文件"""
        # 查找所有相关文件
        if file_patterns:
            files_to_check = []
            for pattern in file_patterns:
                pattern_path = self.repo_root / pattern
                if pattern_path.exists():
                    if pattern_path.is_file():
                        files_to_check.append(pattern_path)
                    else:
                        files_to_check.extend(list(pattern_path.rglob("*.yaml")))
                        files_to_check.extend(list(pattern_path.rglob("*.yml")))
        else:
            files_to_check = []
            files_to_check.extend(list(self.repo_root.rglob("org-info.yaml")))
            files_to_check.extend(list(self.repo_root.rglob("sig-info.yaml")))
            
            # 查找所有ascend目录下的repo-info.yaml文件
            for ascend_dir in self.repo_root.rglob("ascend"):
                if ascend_dir.is_dir():
                    files_to_check.extend(list(ascend_dir.glob("*.yaml")))
                    files_to_check.extend(list(ascend_dir.glob("*.yml")))
        
        files_to_check = list(set(files_to_check))
        
        # 显示检查上下文
        print(f"\n{'='*60}")
        print("检查上下文信息")
        print(f"{'='*60}")
        print(f"检查根目录: {self.repo_root}")
        if self.cloned_repo_path:
            print(f"克隆来源: {self.clone_url or f'{self.gitcode_namespace}/{self.gitcode_project}'}")
        print(f"GitCode命名空间: {self.gitcode_namespace or '未设置'}")
        print(f"GitCode项目: {self.gitcode_project or '未设置'}")
        print(f"API地址: {self.gitcode_api_base}")
        print(f"待检查文件数: {len(files_to_check)}")
        print(f"{'='*60}\n")
        
        # 检查每个文件
        all_passed = True
        for file_path in sorted(files_to_check):
            relative_path = file_path.relative_to(self.repo_root)
            print(f"检查文件: {relative_path}")
            if not self.check_file(file_path):
                all_passed = False
        
        # 新增：在检查完所有文件后，执行全局校验规则
        print(f"\n{'='*60}")
        print("执行全局校验规则")
        print(f"{'='*60}")
        
        # 先收集项目目录和sigs目录信息
        print("收集项目目录和sigs目录信息...")
        self.collect_project_sig_directories()
        
        # 规则1: 检查整个仓库中的sig名是否唯一
        self.check_unique_sig_names()
        
        # 规则2: 检查每个项目目录下的sigs目录中的SIG子目录是否在项目org-info.yaml中注册
        self.check_sig_directories_in_project_org_info()
        
        return all_passed
    
    def check_file(self, file_path: Path) -> bool:
        """检查单个文件"""
        if file_path.suffix.lower() not in ['.yaml', '.yml']:
            return True
        
        data = self.load_yaml_file(file_path)
        if data is None:
            return False
        
        file_path_str = str(file_path)
        
        # 根据文件名进行不同的检查
        if file_path.name == 'org-info.yaml':
            self.check_org_info_required_fields(data, file_path_str)
            self.check_sig_consistency(file_path, data)
            
        elif file_path.name == 'sig-info.yaml':
            self.check_sig_info_required_fields(data, file_path_str)
            self.check_sig_consistency(file_path, data)
            self.check_sig_info_repos_exist(data, file_path_str)
            
        elif file_path.name.endswith('.yaml') and 'ascend' in file_path.parts:
            # 检查是否是项目/sigs/SIG目录/ascend/下的文件
            self.check_repo_info_required_fields(data, file_path_str)
            self.check_repo_info_file_location(file_path, data)
        
        return len([e for e in self.errors if file_path_str in e]) == 0
    
    def get_error_summary_for_category(self, errors: List[str]) -> str:
        """为错误类别生成简明的摘要"""
        if not errors:
            return ""
        
        # 如果错误数量较少，直接显示所有错误
        if len(errors) <= 10:
            error_list = [
                (error.split(": ", 1)[1] if ": " in error else error)[:300]
                for error in errors
            ]
            return "; ".join(error_list)
        
        # 错误数量较多时，显示统计信息
        # 按文件分组错误
        file_errors = defaultdict(list)
        for error in errors:
            if ": " in error:
                file_path, msg = error.split(": ", 1)
                file_errors[file_path].append(msg)
            else:
                file_errors["其他"].append(error)
        
        summary_parts = []
        for file_path, msgs in list(file_errors.items())[:3]:
            if file_path == "其他":
                summary_parts.append(f"{len(msgs)}个其他错误")
            else:
                summary_parts.append(f"{Path(file_path).name}: {len(msgs)}个错误")
        
        if len(file_errors) > 3:
            summary_parts.append(f"等共{len(errors)}个错误")
        
        return "; ".join(summary_parts)
    
    def print_results(self):
        """打印检查结果并写入result.md文件，输出格式为markdown表格"""
        total_errors = sum(len(errors) for errors in self.errors_by_category.values())
        
        results = []
        
        # 标题行
        if total_errors == 0:
            results.append("✅ 规则检查门禁通过！\n")
        else:
            results.append(f"❌ 规则检查门禁未通过\n")
        
        results.append("检查项 | 检查结果 | 错误详情")
        results.append("--- | --- | ---")
        
        # 定义检查项及其对应的错误类别
        check_items = [
            ("YAML格式检查", ["格式错误"]),
            ("必须字段检查", ["缺少必须字段"]),
            ("gitcode_id存在性检查", ["gitcode_id不存在"]),
            ("仓库存在性检查", ["仓库不存在"]),
            ("文件位置检查", ["文件位置错误"]),
            ("字段一致性检查", ["字段不一致"]),
            ("maintainer数量检查", ["数量检查错误"]),
            ("仓库类型检查", ["仓库类型错误"]),
            ("sig名唯一性检查", ["sig名重复"]),
            ("sig目录注册检查", ["sig目录未注册"]),
        ]
        
        # 生成表格行
        for item_name, error_categories in check_items:
            # 收集该检查项的所有错误
            item_errors = []
            for category in error_categories:
                if category in self.errors_by_category:
                    item_errors.extend(self.errors_by_category[category])
            
            if item_errors:
                # 有错误的情况
                error_count = len(item_errors)
                error_summary = self.get_error_summary_for_category(item_errors)
                results.append(f"{item_name} | ❌ 未通过 ({error_count}个错误) | {error_summary}")
            else:
                # 无错误的情况
                results.append(f"{item_name} | ✅ 已通过 | -")
        
        # 写入result.md文件
        try:
            with open("result.md", "w", encoding="utf-8") as f:
                f.write("\n".join(results))
            
            # 控制台输出
            print("\n" + "="*60)
            print("门禁检查结果")
            print("="*60)
            print("\n".join(results))
            
            # 如果有错误，输出错误详情
            if total_errors > 0:
                print(f"\n{'='*60}")
                print("错误详情")
                print(f"{'='*60}")
                
                # 按类别输出错误详情
                for category, errors in self.errors_by_category.items():
                    if errors:  
                        print(f"\n{category} ({len(errors)}个):")
                        for i, error in enumerate(sorted(errors)[:20], 1):  # 最多显示前20  个错误
                            print(f"  {i:2d}. {error}")
                        if len(errors) > 20:
                            print(f"  ... 还有 {len(errors) - 20} 个错误未显示")
            
            print(f"\n{'='*60}")
            print(f"详细结果已保存到 result.md")
            print("="*60)
            
        except Exception as e:
            print(f"写入result.md失败: {e}")
            # 仍然打印到控制台
            print("\n".join(results))
        
        return total_errors == 0


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='Gitcode门禁检查脚本 - 完整版')
    parser.add_argument('paths', nargs='*', default=['.'], 
                       help='要检查的文件或目录路径，默认为当前目录')
    parser.add_argument('--root', default='.', 
                       help='本地仓库根目录路径，如果同时使用--clone-url则此参数无效')
    parser.add_argument('--cache_ttl', type=int, default=300,
                       help='缓存有效期（秒），默认为300秒')
    parser.add_argument('--token', 
                       default=os.environ.get("GITCODE_TOKEN"),
                       help='GitCode API访问令牌')
    parser.add_argument('--namespace', 
                       default=os.environ.get("GITCODE_NAMESPACE", "ascend"),
                       help='GitCode命名空间/组织名')
    parser.add_argument('--project', 
                       default=os.environ.get("GITCODE_PROJECT", "community"),
                       help='GitCode项目名')
    parser.add_argument('--clone_url', 
                       help='直接指定要克隆的仓库URL（优先级高于namespace/project组合）')
    parser.add_argument('--no-cleanup', action='store_true',
                       help='检查完成后保留克隆的临时目录（用于调试）')
    
    args = parser.parse_args()

    # 创建检查器
    checker = GitcodeGateCheck(
        repo_root=args.root,
        gitcode_token=args.token ,
        gitcode_namespace=args.namespace,
        gitcode_project=args.project,
        clone_url=args.clone_url,
        cache_ttl=args.cache_ttl,
    )
    
    try:
        # 如果需要克隆，先执行克隆
        if args.clone_url or (args.namespace and args.project and args.root == '.'):
            print("检测到远程仓库信息，尝试克隆...")
            if not checker.clone_repository():
                print("❌ 克隆失败，终止检查")
                sys.exit(1)

        checker.check_all_files(args.paths if args.paths != ['.'] else None)
        
        final_success = checker.print_results()
        
        if not args.no_cleanup:
            checker.cleanup()
        elif checker.temp_dir:
            print(f"\n临时目录已保留（用于调试）: {checker.temp_dir}")
        
        sys.exit(0 if final_success else 1)
        
    except KeyboardInterrupt:
        print("\n\n检查被用户中断")
        checker.cleanup()
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ 检查过程中发生未预期错误: {str(e)}")
        import traceback
        traceback.print_exc()
        checker.cleanup()
        sys.exit(1)


if __name__ == "__main__":
    main()
