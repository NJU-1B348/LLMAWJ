# LLMAWJ LLM Asisted Warning Judger

针对静态分析中的警报误报问题(False Positive)，尝试使用GPT辅助进行警报真实性的判断。

我们期望GPT从我们规定的中间格式(IR)所包含的信息出发，借助合适的Prompt设计，最终以JSON格式输出警报的真实性判断，并自动化这一过程。

**IR**是指我们规定的警报中间格式，包含了警报的位置、所在函数、附近代码、可疑变量、警报类型等信息。它可能从任一一种静态分析工具的输出中生成。在我们的项目中，我们提供了**SRT**(SVF Report Transformer)作为一个例子，用于自动化地将SVF工具的`saber`内存泄漏分析报告转化为IR。

## 文件结构

```text
- llmawj/
    - report/  # 主要是一些已经完成的工作报告
        - GPT3.5Prompt.md # 用于GPT3.5的Prompt设计 该Prompt是在还没有迁移至GPT API之前设计的，在将其迁移到GPT API之后，我们进行了略微的修改。
        - prompt_evaluate.md # 在将Prompt迁移至GPT API之前，我们人工对Prompt进行的一次评估，之后我们将在GPT API上进行更多的评估。
    - src/
        - utils/     # 一些工具函数
            - log.py # 日志
            - get_func_def.py # 从源码中获取函数定义交给GPT
        - prompts/   # Prompt的设计
            - prompt.py  # Prompt的设计
        - test/
            - test_case.md  # 上述prompt_evaluate.md中提到的测试用例
            - prompt_evaluate.py   # 对Prompt进行评估
            - test_get_func_def.py # 测试get_func_def.py的实现
        - run.py     # LLMAWJ的主要代码
    - srt/          # 上文提到的SRT的子仓库
    - res/          # 一些输入和输出文件
```