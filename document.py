class Document:
    def __init__(self, name:str, description:str, content:str):
        self.name = name
        self.description = description
        self.content = content
    
    @property
    def format(self):
        return f"{self.name}: {self.description}"