import boto3
import json
import sys
import os
from pathlib import Path

bedrock_runtime = boto3.client('bedrock-runtime', region_name='us-east-1')

def read_file(file_path):
    try: 
        with open(file_path, 'r+', encoding='utf-8') as f:
            text = f.read()
    except:
        print('Error: ' + str(sys.exc_info()[0]))
    return text

def get_claude_response(claude_prompt_content):
    model_id = "arn:aws:bedrock:us-east-1:511398855118:inference-profile/us.anthropic.claude-sonnet-4-20250514-v1:0"
    
    body = json.dumps({
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 8192,
        "messages": [
            {"role": "user", "content": claude_prompt_content}
        ]
    })
    
    response = bedrock_runtime.invoke_model(
        modelId=model_id,
        body=body
    )
    
    return json.loads(response['body'].read())

def write_response_to_ouput_file(response, output_path):
    # with open('outputs/greek_output.tex', 'w', encoding="utf-8") as f:
    with open(output_path, 'w', encoding="utf-8") as f:
        # response = get_claude_response(claude_prompt_content=greek_prompt_content)
        print(response)
        f.write(response['content'][0]['text'])

def construct_claude_prompt(input_file):
    prompt_text = read_file('context/prompt.txt')
    template_text = read_file('context/template.tex')
    greek_text = read_file(input_file)

    greek_prompt_content = f"""
    PROMPT: {prompt_text}

    TEXT TO ANALYZE: {greek_text}

    OUTPUT TEMPLATE: {template_text}
    """
    return(greek_prompt_content)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python bedrock.py <input_file_path>")
        sys.exit(1)
    
    input = sys.argv[1]
    filestem = Path(input)
    output_filename = 'outputs/' + str(filestem.stem) + '.tex'
    prompt = construct_claude_prompt(str(input))
    response = get_claude_response(prompt)
    write_response_to_ouput_file(response, output_filename)
