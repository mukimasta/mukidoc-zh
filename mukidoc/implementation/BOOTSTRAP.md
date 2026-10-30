# Bootstrap Implementation

当前初始化交付物为仓库内的 `skills/mukidoc-init/`，Skill 版本和协议版本均为 `0.2.0`。运行程序使用 Python 3.9+ 标准库，无第三方运行依赖；本仓库保存源文件，不自动安装到个人 Skill 目录。

### 代码与资源

1. `skills/mukidoc-init/SKILL.md` 定义触发范围、运行入口、结果解释和用户确认规则；`agents/openai.yaml` 提供显示元数据。
2. `skills/mukidoc-init/scripts/init_mukidoc.py` 提供唯一初始化实现，Skill 与命令行共用。
3. `skills/mukidoc-init/assets/manifest.json` 保存 schema 版本、Skill 版本、协议版本、全部固定目录和模板文件 SHA-256。
4. `skills/mukidoc-init/assets/template/` 保存完整 AGENTS.md 及仅含标题的八份骨架文档。模板内不包含当前 MukiDoc 项目的知识。
5. 根目录 `AGENTS.md` 为维护中的权威协议，`scripts/sync_skill_assets.py` 将其原样导出到 Skill，并更新模板校验值；目标项目运行时不依赖该导出脚本或源仓库。

### 命令与输出

```sh
python3 skills/mukidoc-init/scripts/init_mukidoc.py /path/to/project
python3 skills/mukidoc-init/scripts/init_mukidoc.py /path/to/project --dry-run
```

目标路径允许尚不存在，支持空格和中文。默认补齐 9 个文件及 14 个目录，11 个叶目录空时写入 `.gitkeep`，不要求已经执行 git init。目录已有内容时不追加标记。既有文件即使为空也原样保留。

版本标记为 `<!-- MukiDoc protocol version: 0.2.0 -->`，仅识别唯一的三段数字版本，按数值元组比较。`agent.state` 返回 `missing`、`current`、`older`、`unversioned`、`same_version_modified` 或 `newer`。标记用于兼容性识别，不是文件来源认证。

确认旧版更新后传 `--update-agent --expected-agent-sha256 HASH`；确认无版本或同版修改文件的完整替换后传 `--replace-agent --expected-agent-sha256 HASH`。HASH 必须来自审查时的报告。目标为更高版本时拒绝替换。备份保存在目标根目录 `AGENTS.md.bak.<UTC时间>.<随机后缀>`，保留原字节和权限；临时文件经 `os.replace` 替换目标。

程序输出 JSON，包含计划或实际文件清单、版本判断、需确认状态及备份路径。正常完成返回 0；保留待确认协议时仍返回 0，状态为 `initialized_agent_preserved`，不表示协议已经更新。`--dry-run` 返回计划状态且不创建目标目录。执行错误返回 1，参数错误由命令行解析器返回 2。

清单校验与路径冲突检查在写入前完成；新文件以独占创建防止覆盖。协议替换前核对内容指纹，替换动作前再次核对。I/O 失败后可能有部分新文件或备份，不提供全项目事务回滚；不支持对运行中的并发写入进程提供锁定保证。

### 版本维护

修改协议时先编辑根目录 AGENTS.md 并提升版本标记，再运行：

```sh
python3 scripts/sync_skill_assets.py
python3 scripts/sync_skill_assets.py --check
```

已有打包协议内容变化却未提升版本时，导出器拒绝同步。脚本或骨架模板变化时更新 manifest 与 SKILL.md 的 Skill 版本；仅执行器变化不要求提升协议版本。模板校验值由导出器重新计算。初始化包版本与协议版本在概念上分开，不依赖同号发布。

### 验证

```sh
python3 -B -m unittest discover -s tests -v
python3 scripts/sync_skill_assets.py --check
```

`tests/test_bootstrap.py` 在临时目录验证完整骨架、重复执行、已有文件保留、版本判断、显式更新及备份、过期指纹、预览和路径冲突，同时验证 Skill 脱离源仓库仍可运行。Skill 格式另用 Skill Creator 的 `quick_validate.py` 检查。具体评价承诺与本轮证据保存在 `mukidoc/evaluation/design/bootstrap/EVALUATION.md`。
