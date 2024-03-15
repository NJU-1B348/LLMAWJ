from openai import OpenAI
import prompt
import json
import argparse

client = OpenAI(
        base_url='https://api.openai-proxy.org/v1',
        api_key='sk-rgM5v15Cjp1gEFPkn35QNXIiZTUXxfSbL3t9bxw6sAfwMd1G',
    )

PROMPT:list[str] = prompt.Prompt.gpt

def log(success:bool, msg:str, error:str="warning") -> None:
    if success:
        print("\033[32m[LLMAWJ]\033[0m " + msg)
    else:
        if error == "warning":
            print("\033[33m[LLMAWJ Warning]\033[0m " + msg)
        elif error == "fatal":
            print("\033[31m[LLMAWJ Fatal Error]\033[0m " + msg)
        else:
            print("\033[31m[LLMAWJ]\033[0m " + msg)
        

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
    parser.add_argument('--disable-exp', type=str,
                        default=False,
                        help='Set to True if you want to disable the explanation part in the result, which may save some time to execute and save some cost due to less token.')
    parser.add_argument('--disable-other', type=str,
                        default=False,
                        help='Set to True if you want to disable the \'other\' part in the result, which may save some time to execute and save some cost due to less token. See the document for the meaning of \'other\'.')
    # parse the args
    args = parser.parse_args()
    
    # read the input file
    f = None
    try:
        f = open(args.in_file, 'r')
    except FileNotFoundError:
        log(False, f"Input file {args.in_file} not found.", "fatal")
        exit(1)
    cases = json.load(f)
    log(True, f"Input has been read from {args.in_file}")

    log(True, f"Total cases: {len(cases)}")
    tot = len(cases)
    
    ans = []
    
    # fix the prompt
    if args.disable_exp:
        PROMPT[2] = prompt.format_without_exp
    if args.disable_other:
        PROMPT[2] = prompt.format_without_other
    if args.disable_exp and args.disable_other:
        PROMPT[2] = prompt.format_without_all
    
    for i in range(tot):
        log(True, f"Processing case {i+1}/{tot}")
        case = cases[i]
        stream = client.chat.completions.create(
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
        
        print(ans_str)
        
        ans.append(json.loads(ans_str))
        
        log(True, f"Case {i+1}/{tot} processed")
    
    f.close()
    
    try:
        f = open(args.out_file, 'w')
    except FileNotFoundError:
        log(False, f"Output file {args.out_file} not found.", "fatal")
        exit(1)

    json.dump(ans, f)
    f.close()
    log(True, f"Output json has been written to {args.out_file}")
    
    pairs = zip(cases, ans)
    
    # TODO: Sort the cases by the chance of being true 
    
    