# MukiDoc

> English version: [mukidoc](https://github.com/mukimasta/mukidoc)

**为大型项目设计的结构化文档协议。**

MukiDoc 用结构化的文档保存项目理念、项目架构、项目路线等高层次的项目上下文，以及 Design → System Design → Implementation 三个层级的核心设计链文档。MukiDoc 的协议为这些文档规定了清晰的结构，AI 依据协议掌握项目的全局，并在编写代码的同时维护文档，使其始终保持清晰、优雅和整洁。

### 与其他方案的区别

1. **记忆系统**（如 Cline Memory Bank）让 AI 记住发生过什么；MukiDoc 让 AI 掌握项目是什么、为什么这样设计、现在处在什么状态。
2. **规格驱动开发**（如 GitHub Spec Kit、Kiro）以单个功能为单位，规定“规格 → 计划 → 实现”的工作流；MukiDoc 管理整个项目的长期知识，不规定固定流程，只约束知识的含义、位置和关系。
3. **AGENTS.md / CLAUDE.md 约定文件**通常记录命令和代码规范；MukiDoc 把 AGENTS.md 作为协议入口，项目知识保存在 `docs/` 的分层结构中。

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
