---
name: mukidoc-init
description: 初始化或补齐项目的 MukiDoc 固定目录与骨架文档，安装随包提供的 AGENTS.md，并识别旧版协议以便由用户决定是否更新。用于用户要求初始化、接入、补齐 MukiDoc 骨架或更新 MukiDoc 协议；不负责重写项目知识、旧文档迁移或日常开发。
metadata:
  version: "0.1.0"
---

# MukiDoc 初始化

使用随包脚本建立结构，不能让模型临时重新生成 AGENTS.md 或另写一套初始化逻辑。本 Skill、脚本和 assets 可整体复制使用，不依赖 MukiDoc 源仓库或在线服务。需要 Python 3.9 或更新版本，无第三方运行依赖。

## 初始化

1. 从用户请求确定目标项目目录；明确指当前项目时使用当前工作目录。目标仍有歧义时先澄清，不把 Skill 安装目录误当项目目录。
2. 定位本 SKILL.md 同目录下的 `scripts/init_mukidoc.py`，以目标绝对路径调用：

   ```sh
   python3 /absolute/path/to/mukidoc-init/scripts/init_mukidoc.py /absolute/path/to/project
   ```

   用户只要求预览时加 `--dry-run`，不执行实际初始化。路径含空格时正确引用路径。
3. 阅读脚本的 JSON 结果，报告创建、保留和需处理的内容。脚本出错时按实际错误排查，不改用覆盖写入绕过保护。I/O 错误可能留下部分新骨架或备份，不能声称已自动回滚。

脚本建立固定目录及骨架文档，空目录放 `.gitkeep`，骨架文档只放标题，AGENTS.md 复制完整模板。保留已有文档与代码；不填写产品事实，不创建可选文档、Area、Evaluation Suite 或 MukiCheck，不执行文档迁移。

## 协议版本与更新

`assets/manifest.json` 保存 Skill 版本、协议版本、骨架清单及模板校验值，完整协议位于 `assets/template/AGENTS.md`。比较的是随当前 Skill 提供的版本，不代表互联网上的最新版本。

脚本默认只补缺失项，已有 AGENTS.md 保持原样。按结果中的 `agent.state` 处理：

| 状态 | 行为 |
|---|---|
| `missing` | 本次初始化复制内置协议；dry-run 仅预览 |
| `current` | 版本及完整内容一致，保留，不询问更新 |
| `older` | 说明旧版本和内置版本，询问是否更新 |
| `same_version_modified` | 同版本但内容不同，保留并说明差异，不称为旧版 |
| `unversioned` | 无唯一可识别版本，包括早期未标版本的协议；保留，不猜测版本 |
| `newer` | 保留更高版本，不降级；需要更新 Skill 才能提供相应版本 |

需要替换时，先阅读目标 AGENTS.md 与内置模板的差异，简短说明实际改变，特别指出替换会影响的项目附加规则。默认更新为完整内置协议，不自动语义合并。明确告诉用户原文件将完整备份，并询问是否替换；若用户已经明确授权这次替换，则直接执行，不重复询问。拒绝或未回答时保留原文件，骨架补齐结果仍有效。

旧版经确认后使用 `--update-agent`；无版本或同版修改文件经明确确认替换后使用 `--replace-agent`。两者都必须带上审查时报告中的原文件 `agent.sha256`：

```sh
python3 /absolute/path/to/mukidoc-init/scripts/init_mukidoc.py /absolute/path/to/project --update-agent --expected-agent-sha256 ORIGINAL_SHA256
```

不能把“初始化项目”本身当作覆盖已有 AGENTS.md 的授权。若文件自审查后发生改变，重新检查实际差异，不能只取新哈希绕过检查。脚本会在目标根目录保存带时间和唯一后缀的 `AGENTS.md.bak.*`，然后替换协议。完成后报告实际旧版、新版和备份路径；替换只更新协议，不代表项目文档已完成迁移或符合新规范。

## 完成边界

初始化完成意味着固定骨架存在、已有内容被保留、协议处理结果清楚。正文可以只有标题；AGENTS.md 被保留时，应说明它是否仍待用户决定更新。不要将骨架齐全表述为项目知识已经完整、运行系统已经验证或旧文档已经迁移。
