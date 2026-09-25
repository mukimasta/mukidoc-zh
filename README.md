# MukiDoc

让项目自己保存意图、设计与实现上下文，使人和 AI 能够持续协作。

### 初始化项目

仓库提供 `skills/mukidoc-init/`，包含初始化 Skill、脚本与完整协议模板。Skill 与协议的首个版本均为 **0.1.0**。

直接从本仓库运行，要求 Python 3.9+，无需第三方依赖：

```sh
python3 skills/mukidoc-init/scripts/init_mukidoc.py /path/to/project
```

加 `--dry-run` 可以预览。脚本创建固定目录与骨架文档，保留已有内容；发现旧版 AGENTS.md 时报告可更新状态，由用户决定。确认后的更新会完整备份原协议。初始化只建立结构，不自动填充项目知识或迁移旧文档。

也可将整个 `skills/mukidoc-init/` 目录交给支持 Skill 的 Agent，按 [Skill 说明](skills/mukidoc-init/SKILL.md) 执行。该目录可独立复制使用；本仓库没有自动安装个人 Skill 的步骤。

### 了解与开发

1. [项目概览](docs/OVERVIEW.md)、[核心思想](docs/PHILOSOPHY.md)、[整体架构](docs/ARCHITECTURE.md)。
2. 初始化设计链：[Design](docs/design/deliverable/BOOTSTRAP.md) → [System Design](docs/system_design/BOOTSTRAP.md) → [Implementation](docs/implementation/BOOTSTRAP.md)。
3. [初始化评价与验证](docs/evaluation/design/bootstrap/EVALUATION.md)、[开发历史](docs/DEVLOG.md)。

维护协议与验证资源包：

```sh
python3 scripts/sync_skill_assets.py --check
python3 -B -m unittest discover -s tests -v
```

协议更新时先提升根目录 AGENTS.md 的版本标记，再运行 `python3 scripts/sync_skill_assets.py` 导出到 Skill。
