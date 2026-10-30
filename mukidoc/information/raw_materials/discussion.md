# MukiDoc

MukiDoc 是一套面向软件项目的文档架构方法。

它关注的不是“应该写哪些标准文档”，也不是“如何做软件开发”，而是：

> 一个软件项目中的知识，应该如何按照不同抽象层级和职责被组织起来，使人能够通过文档持续表达设计意图，并让实现者——尤其是 AI Agent——基于这些文档完成实际开发。

MukiDoc 的核心出发点，是把文档从“代码完成后的说明材料”提升为项目中的主要知识载体。

在传统开发中，人通常直接操作代码，文档更多承担解释和补充作用。

在 AI-assisted / agentic development 中，可以采用另一种工作方式：

> 人主要维护意图、设计、约束和判断；  
> Agent 主要负责把这些逐步翻译成具体实现和代码。

在这种模式下，文档不再只是 documentation，而成为人与实现之间的主要接口。

---

## 核心思想

MukiDoc 强调一种逐层细化的知识结构。

一个项目通常从非常高层的意图开始，然后不断向具体实现收敛：

```text
Intent
  ↓
Design
  ↓
System Design
  ↓
Implementation Design
  ↓
Code
```

这些层之间并不存在绝对意义上的“设计”和“实现”边界。

更准确地说：

> 低层级的 Design，往往就是高层级 Design 的 Implementation。

例如，一个书店系统中：

- “用户可以搜索、购买和管理书籍”属于较高层设计；
- “系统由 Catalog、Order、Inventory、Account 等模块组成，并按照某种流程协作”属于 System Design；
- “使用某种数据库、框架、协议和代码结构来落地这些模块”属于 Implementation Design；
- 最终代码则是这些设计的具体 realization。

因此，MukiDoc 并不试图寻找一个绝对的 Design / Implementation 分界。

它更关心：

> 当前这份知识处于哪个抽象层级？

---

## 四个主要知识区域

MukiDoc 的核心文档结构围绕四个区域展开：

```text
design/
system_design/
implementation/
evaluation/
```

### Design

Design 描述的是：

> 被构建的东西本身应该是什么样。

它关注功能、规则、行为、领域逻辑、交互和体验等。

这一层应该尽量独立于具体技术实现。

如果底层技术被替换，而这部分知识依然应该成立，那么它通常属于 Design。

---

### System Design

System Design 描述的是：

> 为了实现 Design，软件系统内部应该如何组织和运行。

这里开始出现内部模块、数据模型、状态、生命周期、运行流程以及模块之间的协作关系。

它已经进入软件内部结构，但仍然不应该过早绑定具体框架、数据库、协议或者代码形式。

它是从领域设计走向工程实现之间的重要中间层。

---

### Implementation

Implementation 在 MukiDoc 中更准确地说是 Implementation Design。

它描述：

> 当前这一版软件，具体选择怎样的技术和工程方案来实现 System Design。

这里可以出现具体的技术栈、框架、协议、代码结构、数据结构、存储方案、序列化方式以及其他工程细节。

它依然是一种设计，只是设计对象已经变成了具体实现。

真正的最终实现则存在于代码中。

---

### Evaluation

Evaluation 不只是测试。

它回答的是：

> 我们凭什么认为前面的设计和实现是正确、有效或者足够好的？

Evaluation 可以针对 Design、System Design 和 Implementation 中任何一层。

不同项目的评价方式可能完全不同，因此 MukiDoc 不强迫 Evaluation 使用统一分类。

它可能关注正确性、性能、系统行为、模型有效性、可用性、体验或者其他项目自身关心的问题。

Evaluation 的结果应该能够反过来推动设计修改，因此整个过程并不是单向的：

```text
Design
   ↓
System Design
   ↓
Implementation
   ↓
Code
   ↓
Evaluation
   └────────→ feedback → Design
```

---

## 项目级知识与局部知识

除了上述四个主要区域，MukiDoc 还区分项目级知识和局部知识。

有些信息并不天然属于某个具体模块，而是整个项目都需要理解的。

例如：

- 项目从外部看是什么；
- 项目的长期理念和原则；
- 系统整体由哪些部分组成；
- 项目目前走到什么阶段；
- 开发过程中发生过哪些关键变化；
- 有哪些值得长期记住的决策。

这些内容适合作为项目级文档存在。

它们的作用不是替代具体 Design 或 Implementation 文档，而是提供整个项目的全局认知框架。

MukiDoc 的一个重要原则是：

> 文档应该待在知识最自然的位置，而不是为了符合模板而被强行分类。

因此，目录是一种认知组织工具，而不是严格的本体论分类。

---

## Information 与实验性知识

MukiDoc 还允许存在一个辅助信息区域。

这里可以保存：

- 可行性调研；
- 工具和依赖能力调查；
- 外部资料；
- 算法或技术笔记；
- 暂时还没有进入正式设计的知识。

其中可以存在一个 `test_playground/`，专门用于探索性实验。

它可以保存：

- benchmark；
- feasibility test；
- 算法正确性实验；
- 性能实验；
- library / API capability test；
- 临时验证。

这里和 Evaluation 的区别是：

> `test_playground/` 用来探索和发现；  
> `evaluation/` 用来形成相对正式的判断和结论。

---

## Architecture 的角色

MukiDoc 认为项目需要一个全局 Architecture 视图。

Architecture 并不是 Design、System Design 和 Implementation 的简单合集。

它的作用是：

> 在进入局部细节之前，提供一张稳定的系统地图。

Architecture 应该帮助读者理解：

- 系统有哪些主要组成部分；
- 各部分的职责是什么；
- 边界在哪里；
- 它们之间存在什么关系。

它是项目级导航结构，也是人或 Agent 开始深入具体文档之前的重要上下文。

---

## 决策与开发历史

MukiDoc 不要求使用复杂的 ADR 体系。

设计决策应该尽可能自然地存在于对应文档中：

```text
背景
→ 约束
→ 问题
→ 推理
→ 设计
→ 影响
```

读者应该能够通过阅读设计本身理解为什么得到某个方案。

对于那些值得长期单独记住、但又没有必要写成完整文档的关键决定，可以使用一个简洁的决策补充文档。

它的角色只是补充，而不是成为所有设计推理的唯一存放位置。

除此之外，MukiDoc 还重视项目的开发演化历史。

一个按时间顺序维护的开发记录可以保存：

- 某一阶段做了什么；
- 发现了什么；
- 解决了什么；
- 为什么发生重要调整。

这和 Git history 不同。

Git history 记录代码变化，而这里保存的是项目认知层面的开发历史。

---

## MukiDoc 与 AI Agent

MukiDoc 并不是一个只能服务于 AI 开发的体系。

但它非常适合 Agent 驱动的软件开发。

其原因在于：

> 项目的关键知识不依赖某一次聊天、某一个开发者的大脑或者某一个 Agent 的临时上下文，而被显式地保存在项目自身的文档中。

因此，一个新的 Agent 接手项目时，可以通过阅读文档重新建立项目认知。

理想状态下：

```text
Human Intent
    ↓
Documentation
    ↓
Agent
    ↓
Code
```

当实现结果不符合意图时，人优先修改文档中的设计或约束，而不是直接在代码中进行大量局部修补。

这样可以减少：

```text
文档说 A
代码实现 B
人的真实意图是 C
```

这种长期漂移。

从这个角度看，MukiDoc 可以把文档视为：

> human–agent collaboration 的 control surface。

---

## 不为了完整而制造文档

MukiDoc 不是 checklist-driven documentation。

一个项目不需要为了“符合 MukiDoc”而创建所有可能存在的文档。

如果某个项目没有复杂的数据模型，就不需要专门创建数据模型文档。

如果没有 API，就不应该为了目录漂亮而创建空的 API 文档。

如果某个知识点足够简单，直接存在于对应模块文档中即可。

核心原则是：

> Structure should serve knowledge, not the other way around.

MukiDoc 提供的是文档架构和抽象层级，而不是要求项目填满一个模板。

---

# MukiDoc 仓库本身

MukiDoc 的开源仓库应该是一个 Meta 项目。

也就是说：

> 这个仓库不仅解释 MukiDoc，它自身也使用 MukiDoc 来描述 MukiDoc。

因此，仓库本身就是这套体系的一个真实实例。

需要注意一个结构约定：

```text
README.md
docs/
```

根目录的 `README.md` 是 GitHub / repository 的入口页面。

它不属于 MukiDoc 文档体系本身，只负责：

- 用极少量文字说明这个仓库是什么；
- 引导读者进入 `docs/`；
- 说明从哪里开始阅读。

真正属于 MukiDoc 方法体系的内容全部位于：

```text
docs/
```

内部。

也就是说，这个仓库自身会形成一种递归结构：

> MukiDoc 使用 MukiDoc 来描述和组织 MukiDoc。

这不是额外的示例工程，而是项目本身的设计。

---

## 最终目标

MukiDoc 希望形成的不是一套繁重的软件工程规范，而是一套轻量、清晰、可演化的软件项目文档架构。

它应该帮助人持续回答：

> 我们在做什么？  
> 为什么这样设计？  
> 系统内部应该怎么工作？  
> 当前具体怎么实现？  
> 我们怎么知道它是对的？  
> 项目是如何走到今天的？

并且让这些答案长期存在于项目本身，而不是散落在人脑、聊天记录或者代码细节中。

MukiDoc 的核心价值可以概括为：

> **将软件项目的意图、设计、实现知识和评价依据按照抽象层级组织起来，使文档成为项目长期可继承的知识结构。**

在 Agent-driven development 中，这进一步意味着：

> **人维护项目知识，Agent 实现项目知识。**