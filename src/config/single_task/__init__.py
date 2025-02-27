import os
import sys
import json
from pathlib import Path

from dynaconf import Dynaconf

_BASE_DIR = Path(__file__).parent


D_SINGLE_TASK_CONFIG = {}

# 读取路径下所有配置
for fname in os.listdir(Path(__file__).parent):
    if not fname.endswith('.yml'):
        continue

    single_task_yml_files = [
        Path(__file__).parent / fname
    ]  # 指定绝对路径加载默认配置

    f_name_upper = fname[:-4].upper()

    single_task_configs = Dynaconf(
        envvar_prefix="CITURS_PRO_{}".format(f_name_upper),  # 环境变量前缀。设置`LLM_BLOG_FOO='bar'`，使用`settings.FOO`
        settings_files=single_task_yml_files,
        environments=False,  # 启用多层次日志，支持 dev, pro
        load_dotenv=True,  # 加载 .env
        env_switcher="CITURS_PRO_{}_ENV".format(f_name_upper),  # 用于切换模式的环境变量名称 LLM_BLOG_ENV=production
        lowercase_read=True,  # 禁用小写访问， settings.name 是不允许的
        includes=[os.path.join(sys.prefix, 'export', 'citrus-pro-training', 'settings.yml')],  # 自定义配置覆盖默认配置
        base_dir=_BASE_DIR,  # 编码传入配置
    )
    stid = single_task_configs['stid']

    D_SINGLE_TASK_CONFIG[stid] = single_task_configs