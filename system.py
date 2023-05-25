import re
from typing import List

import openai
from common_tool_functions import ask_details, expert, self_reflect, split_by_space, summarize, write

from tools import Tool


def query(text, model, max_tokens):
    output = openai.ChatCompletion.create(
                model=model,
                messages=[{"role":"system", "content":text}],
                max_tokens=max_tokens
            )["choices"][0]["message"]["content"]
    return output

common_toolbox = [Tool("READ", "Reads the content of a document", ["document_name"], summarize),
                  Tool("EXPERT", "Asks a question to an expert.", ["question", "the expert job"], expert),
                  Tool("REFLECT", "Rewrite your answer using self-reflection after getting external thoughts", [], self_reflect),
                  Tool("TRANSLATOR", "Translates a text to another language", ["target_language"], split_by_space),
                  Tool("MORE_DETAILS", "Asks the user for more details", ["subject"], ask_details),
                Tool("WRITE", "Writes about a specific subject using a specific style", ["subject to write about", "writing style"], write)]

def parse_tool(tool_line: str):
    match = re.search(r'- *(\w+)\((.*?)\)', tool_line)
    if match:
        type_request = match.group(1)
        args = match.group(2).strip("'").split("', '")
        return [type_request, args]
    else:
        return []

class System:
    def __init__(self, tools: List, documents: List):
        self.tools = common_toolbox + tools
        self.tools_mapping = {tool.name:tool for tool in self.tools}
        self.documents = documents
        self.documents_mapping = {document.name:document for document in self.documents}

    def run(self, steps: List):
        system_prompt="You are RETINA, an highly intelligent LLM, that is able to reflect on its own thoughts and use tools."
        
        tools_prompt = "You have several tools at your disposal:\n"
        for tool in self.tools:
            tools_prompt += f"<Document> {tool.format}\n"

        documents_prompt = "The user has provided the following documents:\n"
        for document in self.documents:
            documents_prompt += f"{document.format}\n"

        planning_prompt = "The user wants to achieve the following:\n"
        for i, step in enumerate(steps):
            planning_prompt += f"{i+1} - {step}\n"
        
        task_prompt = "Write step by step a plan to answer the user query, making full use of the tools and documents at your disposal. TIP: Best practices say that it's often good to end with the REFLECT() tool."

        example_prompt = "The user wants to achieve the following:\n"\
        "1- Summarize the content of the document about the car accident\n"\
        "2- Translate it into French\n"\
        "3- Send it to my lawyer.\n\n"\
        "PLAN:\n"\
        "-READ(<Document> my_car_accident.txt)\n"\
        "-EXPERT('What do you think about my summary?', 'lawyer')\n"\
        "-REFLECT()\n"\
        "-TRANSLATOR('french')\n"\
        "-MORE_DETAILS('user lawyer email')\n"
        "-REFLECT()\n"

        prompt = f"{tools_prompt}\n\n{documents_prompt}\n\n{task_prompt}\n\nHere's an example:\n{example_prompt}\n\n{planning_prompt}\n\nPLAN:"
        answer = query(prompt, "gpt-4", 512)
        print(answer)
        print("-------------------")
        outputs = ""
        for line in answer.split("\n"):
            parsed_tool = parse_tool(line)
            tool_name, tool_arguments = parsed_tool[0], parsed_tool[1]
            tool_arguments_new = []

            if tool_name == "READ" and "<Document>" not in tool_arguments[0]:
                tool_arguments[0] = "<Document> " + tool_arguments[0]

            for tool_argument in tool_arguments:
                if "<Document> " in tool_argument:
                    tool_argument = self.documents_mapping[tool_argument.replace("<Document> ", "")]
                tool_arguments_new.append(tool_argument)

            tool_arguments = tool_arguments_new

            tool = self.tools_mapping[tool_name]
            output = tool.use(tool_arguments, outputs) # execute tool
            outputs += output + "\n\n---------------\n\n"
