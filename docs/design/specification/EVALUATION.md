# EVALUATION Design

Evaluation 用来判断项目在不同层级做出的承诺是否真正成立，并把结果反馈到对应层级，驱动后续迭代。

Evaluation 的核心原则是：

**自顶向下设计，自底向上执行。**

设计 Evaluation 时，从上层承诺出发，逐步把抽象目标转化为可以观察和判断的性质。评价目标通常来自：

**PHILOSOPHY → Design → System Design → Implementation**

越高层越关注最终价值和核心承诺，越低层越接近具体行为、工程约束和规范符合性。这样可以避免只评价“容易测的东西”，而忽略真正重要的目标。

实际执行时则从低层开始。先验证便宜、确定、局部的性质，再逐步进入 Integration、System 和更高层承诺。低层结果既为高层判断提供证据，也帮助高层 Evaluation 失败时定位问题。

Evaluation 按承诺来源组织。`evaluation/` 及 `philosophy/`、`design/`、`system_design/`、`implementation/` 四个承诺来源目录属于固定骨架，即使暂时没有评价也需建立；Git 项目的空目录用 `.gitkeep` 保留。具体 Evaluation Suite 在形成评价主题后创建。MukiCheck 尚未落地，当前初始化骨架不要求建立 `mukicheck/`，下图保留其设计位置：

```text
evaluation/
├── mukicheck/
├── philosophy/
├── design/
├── system_design/
└── implementation/
```

`mukicheck/` 保存所有 MukiDoc 项目自带的标准评价 MukiCheck，用于判断项目的知识体系是否健康、是否与代码一致，以及是否仍能支撑陌生 Agent 接手；其余部分保存具体项目自己的 Evaluation。

### Evaluation Suite

每个独立评价主题建立一个 Evaluation Suite：

```text
<layer>/
└── <evaluation_name>/
    ├── EVALUATION.md
    └── ...
```

`EVALUATION.md` 至少定义：

1. Claim：正在验证什么承诺。
2. Scope：评价覆盖多大的范围。
3. Method：通过什么方式获得证据。
4. Metric / Oracle：如何判断结果。

复杂的 Suite 可以继续拆分不同 Scope 或评价场景，简单的则保持一个文件即可。

### Evaluation Scope

承诺所在的层级和评价覆盖范围是两个独立维度。

同一个 Claim 可以在不同 Scope 下验证：

**Module → Integration → System / End-to-End → Long-term**

高层承诺也可以由低层证据支撑，低层问题也可能只有在更大的系统范围内才能暴露。

只有确实存在不同评价范围时才继续拆分，不为了结构完整人为增加层级。

### Evaluation 与执行

`docs/evaluation/` 保存评价目标、方法和判断标准，不要求执行代码与文档放在一起。

真正产生证据的内容应放在最自然的工程位置，可以是 tests、evals、benchmarks、scripts、CI、Agent task、人工评价或真实使用结果。

Evaluation 定义“为什么测、测什么、怎样判断”；具体工具负责产生证据。

### 与 Playground 和 Tests 的区别

`information/playground/` 用于探索尚未确定的问题，可以保存思考、草稿、实验、失败结果和暂时没有正式归属的知识。

项目的 `tests/` 用于检查已经明确的行为和实现约束，通常可以重复执行并得到明确结果。

Evaluation 综合 Tests、实验、运行结果和其他证据，对项目承诺是否真正成立做出判断。

可以简单理解为：

**Playground 用于探索，Tests 用于检查，Evaluation 用于判断。**

Evaluation 应随着项目设计一起生长。新的重要承诺形成时，需要考虑它最终如何被验证；评价暴露问题后，应把结果反馈到真正需要调整的层级。
