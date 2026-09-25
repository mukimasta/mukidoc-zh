# 这玩意儿到底几层

写 MukiDoc 的感觉有点怪。一边写规则，一边发现自己在遵守这些规则；一边描述这个仓库，一边描述的就是描述本身。照着镜子照镜子，很容易看晕。

乱了半天，把它拆成三条轴，就不晕了。

## 三条轴

**纵向那条，是往下走，不是往下钻。**

```
design/          Design
system_design/   System Design
implementation/  Implementation
src/             Code
```

逐层细化，有方向、有尽头，走到代码就停。它不递归，它只是下楼梯。

**横向那条，是并排摆，不是分上下。**

OVERVIEW、PHILOSOPHY、ARCHITECTURE、ROADMAP、DECISION、DEVLOG——同一个项目的六个侧面，谁也不领导谁。

**第三条是个环，不是塔。**

```
design/project_context/OVERVIEW.md   规定  docs/OVERVIEW.md 怎么写
design/project_context/DEVLOG.md     规定  docs/DEVLOG.md 怎么写
```

而 `design/project_context/` 恰好是纵向和横向的交叉点：用 Design 这一层，去设计 Project Context 那一批文档。镜子对镜子的地方就在这儿。

## 不是无限递归，是自举

递归会发散。自举会停下来。

```
design/DOC.md  ← 被 design/DOC.md 规定怎么写
```

到这里闭合了。地板是自然语言——你不可能再写一份"DOC.md 的 Design"，因为规则本身就是人话，人话就是底。编译器用自己编译自己，没人会要求再写一个"编译编译器的编译器"。

所以深度有限，只有一个环，一个自指的点。不吓人。

## 为什么改一下 design，整个项目就跟着变

普通项目里这条因果也有，只是慢：改设计 → 写代码 → 几天后项目变了。

这里被设计的对象就是文档本身，设计和产物重合，编译距离是零。于是一改 `docs/design/`，整个项目当场全变。

不是发明了新因果，是把设计到产物之间的距离压没了。

## 那个真的一直在转的环

```
design/project_context/AGENTS.md.md ──规定──▶ AGENTS.md
AGENTS.md ──指导──▶ Agent
Agent ──修改──▶ docs/design/**
docs/design/** ──重新编译──▶ AGENTS.md   ← 回来了
```

一个运行时控制回路。Agent 靠 AGENTS.md 干活，干活的内容就是维护那些定义 AGENTS.md 的文档。

进来的时候根目录的 `AGENTS.md` 是 0 字节——回路正在接通的那一瞬。

## 乱了就问三句话

1. 这是**内容**，还是**规定内容长什么样的规则**？
2. 它规定的是**形状**还是**内容**？（这条区分是关键，不然环就糊成一坨）
3. 它站在**哪条轴**上？

## 顺便，这个目录本身也是个案例

原来这儿叫 `test_playground`，名字预设了"这里放要被验证的实验"。结果塞进来一份结构梳理——不是实验，不产生事实，名不副实。

改成 `playground` 就对了。问题从来不是它该进哪个分类，是原来根本没有"不分类"这个格子。

现在有了。于是这里躺着一个自举的样本、一套还没被承认的规则、还有一个空着的政策位置。

环又转了一圈，这次转得慢。

## 一句话

塔只有几层，环只有一个，地板是人话。
