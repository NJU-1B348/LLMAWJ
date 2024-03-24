# SVF Report Transformer (SRT)

## 功能

使用合适的运行参数运行`IRT.py`，可以在有源代码的情况下将给定的infer_parser报告进行内容扩充，使其包含可疑变量名，可疑部分代码等必要的诊断信息。可以将其作为输入，运行LLMAWJ工具，与大模型进行交互。

## 运行参数

| 运行参数       | 类型   | 描述                                                         | 默认值     |
| -------------- | ------ | ------------------------------------------------------------ | ---------- |
| `--input-file`   | String | 输入JSON文件                                                 | "in.json"  |
| `--output-file`  | String | 输出JSON文件                                                 | "out.json" |
| `--root-dir`     | String | 项目源代码所在目录，仅在需要重新寻找源文件绝对路径时                | "./"       |
| `--copy-range`   | Int    | 可疑代码附近的拷贝行数 >= 0                                  | 5         |
| `--redirect-file` | Bool  | 重新定位所指源文件的绝对路径，在目录下具有多个同名文件时，可能产生问题 | True     |

## 示例

```bash
> python IRT.py --root-dir ./aisleriot
```