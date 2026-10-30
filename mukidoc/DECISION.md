# Decision

1. 不采用 arc42 作为顶层文档体系。它从多个角度检查同一个 Architecture，采用它几乎是默认答案，而 MukiDoc 从 Design 向 Implementation 向下展开。最终保留自己的结构，只吸收其中有用的概念，代价是不再复用 arc42 的模板和工具链。

2. 把 Design / Implementation 两层拆成三层。两层足够是设计文档最自然的默认划分，但讨论 Database 时边界反复模糊：数据库模型既像上层 Design 的实现，又像底层代码的 Design。用登录、书店推演后，中间显出一个一直存在的独立问题——“为了实现这个设计，内部系统应该怎样组织和运行”。最终独立出 System Design，并接受“低层级 Design 同时是高层级 Implementation”。代价是层级判断需要人为裁量，文档数量增加。

3. ROADMAP 保持静态，真实开发历史交给 DEVLOG。ROADMAP 最初同时描述“已经做了什么、现在在哪里、以后做什么”，这是多数项目对 roadmap 的默认理解，但这样它会随每天开发变化，容易退化成进度表。最终让它只描述能力和成熟度如何演进，实际怎么走过来的交给按时间追加的开发主线记录。它不能叫 IMPLEMENTATION.md——implementation/ 已是设计链中的正式概念，重名会持续制造歧义。代价是 ROADMAP 不再回答“现在做到哪”。

4. Evaluation 从 PHILOSOPHY 到 Implementation 各层的承诺产生，而不是等同于 Tests。讨论时很容易落到格式检查、unit test、performance test 上，把它们当作同义词，这是很自然的默认理解，但这些只能说明实现的某些性质。真正的标准来自 PHILOSOPHY：新的 Agent 能否接手项目、人能否主要通过文档掌控系统、三层是否真正解耦。“评价哪一层承诺”和“以多大 Scope 去测”是两个正交维度，所有 MukiDoc 项目还自带一套针对文档体系本身的 Evaluation。代价是每层承诺都要单独定义。

5. AGENTS.md 采用“编译”思路，而不是复制完整规范或规定工作流。最初考虑让它教 Agent 先读什么、下一步做什么、按需加载各类 Design，但这样会变成僵硬工作流，也低估了强模型的判断能力。最终把详细 Design 视为源代码，AGENTS.md 是高密度编译结果：只保留影响判断的项目地图、语义边界和关键规则，删掉推导、解释和大部分例子；不规定固定 Runtime，只约束不能破坏的关系。它按 Role、MukiDoc、Design、Develop、Evaluate 组织，放在仓库根目录。代价是 Design 变化后需要重新编译，两者会漂移。

6. Information 与 Project Context 并列，不属于 Project Context。Project Context 是个范围词，“项目级的一切”读起来天然包括 Information——仓库里就是这么理解的，它的 Design 一直放在 design/project_context/ 下。但按这个标准，Evaluation 和 Design Chain 里项目级的内容也该进来，这个区域最终什么也不区分。因此两者按性质而非范围划分：Project Context 是项目自己的正式叙述，Information 是这些叙述所依据的材料与证据。判据是有没有进入正式叙述，与时间无关——DEVLOG 和 investigations 都在讲发生过什么，一个进主线，一个只是证据。由此 ARCHITECTURE 中“项目级上下文”需要收紧成“关于项目自身的权威描述”。

7. Design Chain 内部按 Area 组织，而不是按层镜像或凭感觉平铺。默认要么让三层照着功能各自镜像出同名目录，要么直接平铺；前者制造大量空目录，后者文档一多就成一堆各自为政的文件。推演后确定第二维是 Area——项目自然形成的问题空间——并定为“固定 Layer，自由 Area”：三层纵向恒定，Area 横向自由，不镜像、按需生长、跨切面 concern 放层根。代价是 Area 的划分需要人为判断，各层结构不再对称。

8. 中文版是唯一源头，英文版只做翻译。开源时最自然的做法是维护一份双语仓库，或者让两种语言各自演进；前者让每份文档都要双份维护，后者很快就会分叉。最终中文仓库 `mukidoc-zh` 作为唯一源头，日常思考和迭代都在这里；英文仓库 `mukidoc` 作为对外主仓库，只在中文版发版后整体同步翻译，不直接修改内容，每次同步在提交信息中注明对应的中文版版本与 commit。代价是英文版总会落后于中文版一段时间。

9. 文档根目录叫 `mukidoc/`，不叫 `docs/`。`docs/` 是最自然的默认名，最初也这样定，但它在生态里已经有固定含义：面向使用者的文档，GitHub Pages、MkDocs、Sphinx 都默认用它。MukiDoc 保存的是项目的长期上下文，占用 `docs/` 后，项目自己的文档、文章或文档站只能另起别扭的名字，每个项目都要重新解释一次，迁入已有项目时更会直接撞上原有的 `docs/`。专属名字让 Agent 一眼识别协议，也把 `docs/` 还给项目。代价是名字不如 `docs/` 直观，第一次打开仓库的人需要 README 指路。
