"""
    SVF report transformer (SRT)
    Created By: Wenze Jin
    Date: 1/17/2024

    对于已有的SVF报告，做以下工作:
    1. 保留现有的所有信息
    2. 将文件名转换为文件实际的绝对路径（因为SVF提供的报告中只能指出文件名，不便于定位实际的位置）
    3. 自动从缺陷警告位置获取可能的变量名
    4. 将缺陷附近的代码摘录
    5. 为每一条警报添加标签，反映其是否正确地被处理并生成中间格式

"""
import json
import argparse
from Tag import *
from C_CXX_Helper import *
from log import *
from File_Helper import *

trans_dict = InferTag_to_IWFTag_dict

if __name__ == '__main__':
    # hello message
    SRT_log(True, "Infer_Parser Report Transformer")

    # set the args
    parser = argparse.ArgumentParser()
    parser.add_argument('--input-file', type=str,
                        default='in.json',
                        help='Set input json file directory. (It should be a svf report)')
    parser.add_argument('--output-file', type=str,
                        default='out.json',
                        help='Set output file directory.')
    parser.add_argument('--root-dir', type=str,
                        default='./',
                        help='Set the root directory of the source code.')
    parser.add_argument('--copy-range', type=int,
                        default=5,
                        help='Set the range of lines that will be copied around the line of warning.')
    parser.add_argument('--redirect-file', type=bool,
                        default=True,
                        help='If the absolute directories has been changed, enable this option to redirect file directories.')

    # parse the args
    args = parser.parse_args()
    rdir = args.root_dir

    with open(args.input_file, 'r') as jsonf:
        report = json.load(jsonf)
        SRT_log(True, "Successfully loaded JSON file: " + str(args.input_file))
        SRT_log(True, f"There are {len(report)} warnings in this report.")
        cnt = 0
        out_report:list[dict] = []
        
        for warn in report:
            # 0. 初始化输出JSON格式
            cnt += 1
            out_warn:dict = {}
            out_warn[IWFTag.DT] = trans_dict[warn[InferTag.TYPE]]
            out_warn[IWFTag.LOC] = {
                IWFTag.l: "",
                IWFTag.c: "",
                IWFTag.f: "",
            }
            out_warn[IWFTag.Func] = ""
            out_warn[IWFTag.Des] = ""
            out_warn[IWFTag.E] = []
            out_warn[IWFTag.V] = []
            out_warn[IWFTag.Code] = ""
            out_warn[IWFTag.Flag] = ""
            out_warn[IWFTag.Msg] = ""
            
            var_set = set()
            code_near = ""
            
            for loc in warn[InferTag.LOC]:
                adir = loc[InferTag.LocTag.F]
                if args.redirect_file:
                    try:
                        adir = redirect_absolute_dir(adir, args.root_dir)
                    except DuplicatedFiles as df:
                        SRT_log(False, str(df), "warning")
                        continue
                    except FileNotExist as fne:
                        SRT_log(False, str(fne), "warning")
                        continue
                if InferTag.LocTag.V in loc.keys():
                    var_set.add(loc[InferTag.LocTag.V])
                l = loc[InferTag.LocTag.L]
                part_code = "/* ...... */ \n " + "/* Code_Near for part: " + loc[InferTag.LocTag.TYPE] + "*/ \n"
                
                try:
                    code_file = open(adir)
                except FileNotFoundError:
                    SRT_log(False, f"Cannot open file: {adir}", "fatal")
                    continue
                
                lines = code_file.readlines()
                start_line = max(0, l - args.copy_range)
                end_line = min(len(lines) - 1, l + args.copy_range)
                for each in lines[start_line:end_line]:
                    part_code += each
                part_code += "/* ...... */ \n"
                code_near += part_code
                
                if loc[InferTag.LocTag.TYPE] == InferTag.LocTag.SRC :
                    out_warn[IWFTag.LOC] = {
                        IWFTag.l: loc[InferTag.LocTag.L],
                        IWFTag.c: loc[InferTag.LocTag.C],
                        IWFTag.f: adir,
                    }
            out_warn[IWFTag.Flag] = "True"
            out_warn[IWFTag.Code] = code_near
            out_warn[IWFTag.V] = list(var_set)
            out_report.append(out_warn)
            

        with open(args.output_file, 'w') as outf:
            json.dump(out_report, outf, indent=4)
            SRT_log(True, "Successfully dumped JSON output: " + str(args.output_file))

