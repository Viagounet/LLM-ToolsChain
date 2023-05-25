class Tool:
    def __init__(self, name: str, description: str, inputs:list, func: callable):
        self.name = name
        self.description = description
        self.inputs = inputs
        self.func = func

    @property
    def format(self):
        inputs_format = ", ".join(self.inputs)
        return f"{self.name}({inputs_format}): {self.description}"
    
    def use(self, arguments, context):
        if arguments == [""]:
            arguments = [context]
        else:
            arguments.append(context)
        return self.func(*arguments)