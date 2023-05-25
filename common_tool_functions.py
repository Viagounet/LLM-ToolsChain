import openai


def split_by_space(text):
    return text.split("\n")

def expert(question, expert_role, context):
    output = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role":"system", "content":f"{context}\nYou are a {expert_role}. Answer the following question : {question}"}],
            max_tokens=256
        )["choices"][0]["message"]["content"]
    return f"Here's what the answer from a {expert_role} to the following question {question} -> {output}"

def summarize(document, context):
    text = document.content
    #output = openai.ChatCompletion.create(
    #        model="gpt-3.5-turbo",
    #        messages=[{"role":"system", "content":f"{context}\nSummarize the following : '{text}'.\n\nSummary:"}],
    #        max_tokens=256
    #    )["choices"][0]["message"]["content"]
    return f"Here's the content of the document named '{document.name}' that you provided : {document.content}"

def self_reflect(context):
    output = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role":"system", "content":f"CONTEXT: {context}\nUsing this context, rewrite your original answer. ANSWER:"}],
            max_tokens=512
        )["choices"][0]["message"]["content"]
    return output

def ask_details(subject, context):
    output = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role":"system", "content":f"{context}\n\nWrite a question asking the user for more details about the following : {subject}. Question:"}],
            max_tokens=128
        )["choices"][0]["message"]["content"]
    user_details = input(output + " ")
    output = f"The user answered the question : {output} with the following answer : {user_details}"
    return self_reflect(context + f"\n{output}")

def write(subject, style, context):
    output = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role":"system", "content":f"{context}\n\nWrite about {subject} in the style of {style}.\nPost content:"}],
            max_tokens=1024
        )["choices"][0]["message"]["content"]
    user_details = input(output + " ")
    print(output)
    output = f"Here's a rewriting of {subject} in the style of {style} -> {output}"
    return self_reflect(context + f"\n{output}")