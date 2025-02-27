import os
import sys
import json
from pathlib import Path

from dynaconf import Dynaconf

_BASE_DIR = Path(__file__).parent


# 数据预处理配置
data_config_files = [
    Path(__file__).parent / 'data.yml'
]  # 指定绝对路径加载默认配置

data_configs = Dynaconf(
    envvar_prefix="CITURS_PRO_DATA_CONFIG",  # 环境变量前缀。设置`LLM_BLOG_FOO='bar'`，使用`settings.FOO`
    settings_files=data_config_files,
    environments=False,  # 启用多层次日志，支持 dev, pro
    load_dotenv=True,  # 加载 .env
    env_switcher="CITURS_PRO_DATA_CONFIG_ENV",  # 用于切换模式的环境变量名称 LLM_BLOG_ENV=production
    lowercase_read=True,  # 禁用小写访问， settings.name 是不允许的
    includes=[os.path.join(sys.prefix, 'export', 'citrus-pro-training', 'settings.yml')],  # 自定义配置覆盖默认配置
    base_dir=_BASE_DIR,  # 编码传入配置
)

# 模型调用配置
data_config_files = [
    Path(__file__).parent / 'model_api.yml'
]  # 指定绝对路径加载默认配置

model_api_configs = Dynaconf(
    envvar_prefix="CITURS_PRO_MODEL_API_CONFIG",  # 环境变量前缀。设置`LLM_BLOG_FOO='bar'`，使用`settings.FOO`
    settings_files=data_config_files,
    environments=False,  # 启用多层次日志，支持 dev, pro
    load_dotenv=True,  # 加载 .env
    env_switcher="CITURS_PRO_MODEL_API_CONFIG_ENV",  # 用于切换模式的环境变量名称 LLM_BLOG_ENV=production
    lowercase_read=True,  # 禁用小写访问， settings.name 是不允许的
    includes=[os.path.join(sys.prefix, 'export', 'citrus-pro-training', 'settings.yml')],  # 自定义配置覆盖默认配置
    base_dir=_BASE_DIR,  # 编码传入配置
)