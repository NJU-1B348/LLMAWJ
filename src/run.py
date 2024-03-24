import prompts.prompt as prompt
import json
import argparse
import config.api as api
from utils import log

PROMPT:list[str] = prompt.Prompt.gpt

def process_judge(args:argparse.Namespace) -> None:
    # read the input file
    f = None
    try:
        f = open(args.in_file, 'r', encoding='utf-8')
    except FileNotFoundError:
        log.fatal(f"Input file {args.in_file} not found.")
        exit(1)
    cases = json.load(f)
    log.success(f"Input has been read from {args.in_file}")
    log.success(f"Total cases: {len(cases)}")
    tot = len(cases)
    ans = []
    # fix the prompt
    if args.disable_exp:
        PROMPT[2] = prompt.Prompt.format_without_exp
    if args.disable_other:
        PROMPT[2] = prompt.Prompt.format_without_other
    if args.disable_exp and args.disable_other:
        PROMPT[2] = prompt.Prompt.format_without_all
    for i in range(tot):
        log.success(f"Processing case {i+1}/{tot}")
        case = cases[i]
        stream = api.CLIENT.chat.completions.create(
            model="gpt-4-turbo-preview",
            response_format={"type":"json_object"},
            messages=[
                {"role": "system", "content": PROMPT[0] },
                {"role": "system", "content": PROMPT[1] },
                {"role": "system", "content": PROMPT[2] },
                {"role": "user", "content": str(case) }
            ],
            stream=True,
        )

        ans_str = ""
        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                ans_str += chunk.choices[0].delta.content
        # print(ans_str)
        ans.append(json.loads(ans_str))
        log.success(f"Case {i+1}/{tot} processed")
    f.close()
    try:
        f = open(args.out_file, 'w', encoding='utf-8')
    except FileNotFoundError:
        log.fatal(f"Output file {args.out_file} not found.")
        exit(1)

    json.dump(ans, f)
    f.close()
    log.success(f"Output json has been written to {args.out_file}")
    if args.dump_hrr:
        pairs:list[tuple[dict, dict]] = list(zip(cases, ans))
        pairs.sort(key=lambda x: x[1]['Chance'], reverse=True)
        try:
            f = open(args.hrr_file, 'w', encoding='utf-8')
        except FileNotFoundError:
            log.warning("Report file report.md not found. Cancel report generation.")
            exit(0)
        f.write("# LLMAWJ Report  \n")
        f.write("All cases are sorted in the decreasing order of the chance of being true warning.  \n")
        cnt = 0
        for case, ans in pairs:
            cnt += 1
            f.write(f"## Case {cnt}  \n")
            f.write(f"**Chance**: {ans['Chance']}  \n")
            if not args.disable_exp:
                f.write(f"**Explanation**:  {ans['Explanation']}  \n")
            if not args.disable_other:
                f.write(f"**Other Information Suggestted**:  {ans['Other']}  \n")
            f.write(f"**Content**:  \n```json\n{case}\n```  \n")
        log.success(f"Human readable report has been written to { args.hrr_file }")
        
if __name__ == "__main__":
    # set the args
    parser = argparse.ArgumentParser()
    parser.add_argument('--in-file', type=str,
                        default='in.json',
                        help='Set input file directory of the cases.')
    parser.add_argument('--out-file', type=str,
                        default='out.json',
                        help='Set output file directory.')
    parser.add_argument('--single', type=bool,
                        default=False,
                        help='Set to True if you want to process a single case.')
    parser.add_argument('--disable-exp', type=bool,
                        default=False,
                        help='Set to True if you want to disable the explanation part in the result, which may save some time to execute and save some cost due to less token.')
    parser.add_argument('--disable-other', type=bool,
                        default=False,
                        help='Set to True if you want to disable the \'other\' part in the result, which may save some time to execute and save some cost due to less token. See the documentation for the meaning of \'other\'.')
    parser.add_argument('--dump-hrr', type=bool,
                        default=True,
                        help='Set to True if you want to dump a human readable report with markdown format.')
    parser.add_argument('--hrr-file', type=str,
                        default='report.md',
                        help='Set the file directory of the human readable report.')
    # parse the args
    a = parser.parse_args()
    # process the judge
    process_judge(a)
