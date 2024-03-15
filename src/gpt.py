from openai import OpenAI
import prompt
import json
import argparse

client = OpenAI(
        base_url='https://api.openai-proxy.org/v1',
        api_key='sk-rgM5v15Cjp1gEFPkn35QNXIiZTUXxfSbL3t9bxw6sAfwMd1G',
    )

PROMPT = prompt.Prompt.gpt

CASE = """
{
    "DefectType": "Never Free",
    "Location": {
        "ln": 27,
        "cl": 5,
        "fl": "malloc9.c"
    },
    "Function": "main",
    "Description": {},
    "Events": [],
    "Var": [
        "rr_node[i].edges"
    ],
    "CodeNear": [
        "	return MACROMALLOC(10);",
        "}",
        "",
        "int main(){",
        "	//rr_node = malloc(sizeof(struct s_rr_node)*10);",
        "	int i;",
        "	rr_node[i].edges = alloc();",
        "",
        "	//free(rr_node[i].edges);",
        "",
        "}"
    ],
    "SuccessTransform": "True",
    "TransformMessage": ""
}
"""


if __name__ == "__main__":
    # set the args
    parser = argparse.ArgumentParser()
    parser.add_argument('--in-file', type=str,
                        default='in.json',
                        help='Set input file directory of the cases.')
    parser.add_argument('--out-file', type=str,
                        default='out.json',
                        help='Set output file directory.')
    # parse the args
    args = parser.parse_args()


    stream = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": PROMPT[0] },
            {"role": "assistant", "content": PROMPT[1] },
            {"role": "assistant", "content": PROMPT[2] },
            {"role": "user", "content": CASE }
        ],
        stream=True,
    )

    ans_str = ""
    
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            print(chunk.choices[0].delta.content, end="")
            ans_str += chunk.choices[0].delta.content
    
    with open(args.out_file, 'w') as f:
        f.write(ans_str)
        