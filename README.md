# LLMAWJ LLM Asisted Warning Judger

针对静态分析中的警报误报问题(False Positive)，尝试使用GPT辅助进行警报真实性的判断。

我们期望GPT从我们规定的中间格式(IR)所包含的信息出发，借助合适的Prompt设计，最终以JSON格式输出警报的真实性判断，并自动化这一过程。

**IR**是指我们规定的警报中间格式，包含了警报的位置、所在函数、附近代码、可疑变量、警报类型等信息。它可能从任一一种静态分析工具的输出中生成。在我们的项目中，我们提供了**SRT**(SVF Report Transformer)作为一个例子，用于自动化地将SVF工具的`saber`内存泄漏分析报告转化为IR。

