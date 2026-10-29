# Devlog

### 2026-09-13

1. 从 arc42 出发重新梳理了自己长期使用的软件工程文档习惯。确认 arc42 更适合作为架构视角和检查框架，而我们真正需要的是一套更符合实际思考与 AI 开发过程的项目知识体系。

2. 初步形成项目级文档结构：README、OVERVIEW、PHILOSOPHY、ARCHITECTURE、ROADMAP，以及 Information、Design、Implementation、Evaluation 等区域。开始明确每类文档应该承担不同认知职责，而不是把所有项目知识堆进一个大文档。

3. 明确文档在 AI 开发中的角色发生了变化：Human 可以主要通过文档表达和修改意图，AI 负责把这些意图落实到代码。文档开始被视为 Human 与 AI 之间的主要协作界面，而不只是代码完成后的说明。

### 2026-09-14

1. 原来的 Design / Implementation 二层在讨论 Database 等问题时暴露出明显边界问题：很多稳定的内部系统机制既不属于对象本身的 Design，也不应该被具体技术实现吞掉。最终增加 System Design，形成核心的三层 Design Chain：`Design → System Design → Implementation`。

2. 进一步明确三层的含义：Design 描述对象本身应该是什么，System Design 描述内部系统应该怎样工作，Implementation 描述当前工程具体怎样实现。接受“低层级 Design 同时也是高层级 Implementation”的事实，不再追求机械的绝对分类。

3. 完成 PHILOSOPHY 的结构设计，并用 MukiDoc 自己作为第一个真实对象写出完整版本。PHILOSOPHY 最终采用从处境与问题一路推导到需求本质、核心思路、运行方式、有效性和原则的结构，而不是直接罗列价值观。

4. 完成 OVERVIEW 和 ARCHITECTURE 的基本设计。ARCHITECTURE 最终确定采用从粗到细连续 zoom in 的图形化阅读方式，再从 Runtime 角度观察系统，最后通过架构树和文件结构落地；这一结构在 MukiDoc 自身的 Architecture 中得到验证。

5. Project Context 逐步稳定为 OVERVIEW、PHILOSOPHY、ARCHITECTURE、ROADMAP、DECISION 和项目开发历史等几个不同维度。README 被重新定位为面向使用者的 GitHub 首页，因此保留在仓库根目录，并决定等 MukiDoc 真正可用后再完成。

6. ROADMAP 最初考虑同时维护过去、现在和未来，实际讨论后发现动态维护成本过高，最终改为静态的长期能力演进路线。阶段按“能力或成熟度发生质变”划分，而不是按功能、版本或时间切分。

7. 原本计划用 ADR 记录关键架构决定，后来发现大量决策本身已经可以自然存在于正式文档中，单独 ADR 容易形成重复。最终改为单个 `DECISION.md`，只保留少量没有自然归属、但长期值得记住的关键判断过程，并重点记录“为什么会得到这个决定”。

8. 根目录原有的 `IMPLEMENTATION.md` 与 Design Chain 中的 `implementation/` 产生明显语义冲突。重新梳理后，将项目级时间线改名为 `DEVLOG.md`：DEVLOG 记录整个项目发生了什么，局部 Implementation 则保存具体部分如何实现、debug 和演化。

9. Information 从简单的调研目录逐步分化出 Raw Materials、External Information、Investigations 和实验区域。过程中明确了“证据留在 Information，稳定结论进入正式 Design Chain”的边界。

10. Evaluation 从最初模糊的“测试和性能结果”扩展成一套独立体系。确认 Evaluation 应直接来源于 PHILOSOPHY、Design、System Design 和 Implementation 各层做出的承诺，并区分“承诺来自哪个层级”和“Module / Integration / End-to-End 等评价 Scope”两个正交维度。

11. 明确 Evaluation 应自顶向下设计、自底向上执行：先从最高层目标决定真正值得评价什么，实际运行时则优先执行便宜、确定的低层检查，再逐渐用证据支撑高层判断。同时确立 Playground 用于探索、Tests 用于检查、Evaluation 用于判断。

12. 开始设计 `AGENTS.md`。最终放弃用固定步骤和阅读顺序限制 Agent，转而把 MukiDoc 的详细 Design“编译”为高密度 Agent 协议，只保留项目地图、知识语义和真正不能破坏的不变量，并明确应充分信任强模型自己的判断和执行能力。

### 2026-09-15

1. 将当前 MukiDoc 体系直接应用到一个已有软件项目，让 AI 按新的知识结构重写原有文档。重写结果明显优于原有结构，初步验证了三层 Design Chain、Project Context 和统一写作规则能够被 AI 正确理解并用于真实旧项目迁移。

2. 这次实际迁移使 MukiDoc Evaluation 的目标进一步具体化：除了格式和一致性检查，更重要的是验证新的 Agent 能否只依赖当前项目重新建立上下文、正确定位设计层级并继续开发。Legacy project migration 和 fresh-agent handoff 因此成为后续值得正式化的评价场景。

3. Information 的原有 `test_playground/` 无法容纳一份有价值但既不是实验、调查、外部资料，也不是原始材料的 meta 结构梳理。这个冲突暴露出“尚未成熟、暂时没有正式归属的内部知识”本身就是一种真实状态，因此将目录改为更诚实的 `playground/`，允许思考、草稿、探索和实验在成熟前暂时存在。

4. 明确 Playground 中的内容可以“毕业”：当某类知识反复出现并形成稳定意义时，应进入正式 Design Chain、Information 的新分类或其他更自然的位置，而不是让 Playground 永久成为兜底目录。

### 2026-09-16

1. 增加 `TODO.md` 作为 Project Context 的当前行动面。TODO 只记录已经确定要做的可执行事项，并允许单独维护 Waiting；长期发展方向继续由 ROADMAP 管理，完成历史由 DEVLOG 管理。

2. 增加 `README.md` 的设计，明确 README 是面向使用者的仓库入口，只负责展示和导航，不保存正式项目知识。同时厘清它与 OVERVIEW 的分工：README 帮陌生人快速判断和上手，OVERVIEW 帮准备开发的人建立准确认知；并规定对已有项目不为统一格式强行重写一个仍然有效的 README。

3. 区分了两种容易被混为一谈的 Evaluation：MukiDoc 项目自己对产品和业务的评价，与所有 MukiDoc 项目自带、用来判断项目知识体系是否健康的内置评价，并把后者命名为 MukiCheck。在本仓库这种元项目里，两者从表面上几乎重合，正因如此才需要显式划出边界，避免未来把它们重新合并。

4. 完成 MukiCheck 的设计，分为静态文档检查、文档–代码联合检查和动态理解检查三层，从只读知识逐步加入真实工程和真实使用。静态层的 Philosophy 对齐只检查当前设计是否偏离项目自己声明的 Philosophy，而“陌生 Agent 能否仅凭文档重建上下文”交由动态层用一个没有历史上下文的新 Agent 验证，使此前提出的 fresh-agent handoff 目标落成具体评价。

5. 从交付物视角重新认识 MukiDoc，梳理出 Specification、AGENTS.md、MukiCheck、Bootstrap、Migration 等交付物，并据此在 OVERVIEW 的固定结构中补入“交付物”一节。

6. 发现 Design Chain 每一层内部还缺一个组织维度，最终抽象为“固定 Layer，自由 Area”：纵向三层不变，横向 Area 由项目自然形成，不镜像、按需生长、跨切面 concern 放层根。据此重组 design/，拆成 specification/（方法本身的定义）与 deliverable/（在其之上构建的能力）两组，Project Context 各文档的设计归入 specification/。

### 2026-09-25

1. 明确 AGENTS.md 必须能够独立交付给无法访问 MukiDoc 源规范的其他项目，编译目标从简短摘要收敛为保留影响理解、判断和执行的完整规则，不预设行数上限。必要的结构约束、边界、设计理由和例子均应保留。
2. 写出根目录 AGENTS.md 第一版，覆盖 Role、MukiDoc、Design、Develop、Evaluate，将各类文档规范、知识维护关系和 MukiCheck 检查要求编入单个协议。陌生 Agent 的独立理解及真实项目使用效果仍待验证。
3. 当前协议暂不纳入尚未落地的 MukiCheck，移除其检查章节及目录约定，保留项目自身的 Evaluation 规则；同步明确了 AGENTS.md 当前交付范围。
4. 真实项目审查暴露出协议的骨架要求与使用预期不符：原“按需创建”使缺少 Information 分类目录和 TODO 仍被判为正常。明确基础目录和骨架文档必须存在，即使暂时为空；Area、Evaluation Suite 和可选文档继续按需建立，同步修正规范与协议。
5. 实现仓库内的 `mukidoc-init` Skill，版本 0.1.0，配套独立初始化脚本、骨架模板和版本化 AGENTS.md。补齐 Bootstrap 的 Design、System Design、Implementation 与评价定义；初始化保留已有文件，旧协议经明确确认后先备份再替换，无版本、同版修改和更高版本分别处理。
6. 初始化交付物通过 18 项临时项目测试、资源导出一致性检查和 Skill 结构校验，验证了完整骨架、重复运行、版本识别、备份及独立分发。真实对话中的更新确认行为仍待验证；本轮没有安装个人 Skill 或迁移外部项目。

### 2026-10-29

1. 重新明确 MukiDoc 的定位：为长期、复杂的项目设计的文档协议。AI 让代码变得便宜，稀缺的是项目的理念、决策和方向；MukiDoc 把这些分层交给 AI，使它拥有全局视角，而不只是零散的记忆。

2. 明确人与 AI 的书写梯度：越上层越由人亲自设计和书写，越下层越交给 AI 完成。PHILOSOPHY、OVERVIEW 与 README 据此更新，README 增加与记忆系统、规格驱动开发和约定文件的对比。

3. 中文仓库 mukidoc-zh 与英文仓库 mukidoc 以 v0.1.0 公开发布，中文版为唯一源头。

