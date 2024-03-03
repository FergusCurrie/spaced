import os 
from enum import Enum

class CardTypes(Enum):
    DEFINITION = 1
    EQUATION = 2



class TemplateAtom:
    def __init__(self, name, args):
        self.name = name
        self.definition = None
        self.base_equation = None
        self.relational_equation = None
        self.type = None
        if 'definition' in args:
            self.definition = args['definition']
            self.type = CardTypes.DEFINITION
        if 'base_equation' in args:
            self.base_equation = args['base_equation']
            self.type = CardTypes.EQUATION
        if 'relational_equation' in args:
            self.relational_equation = args['relational_equation']
        

    def __str__(self):
        return f"""
        Page: '{self.name}'
        Definition: {self.definition}
        Base Equation: {self.base_equation}
        Relational Equation {self.relational_equation}
        """

def equation_to_latex(equation):
    result = ""
    open_equation = False
    for c in equation:
        if c == "$":
            if open_equation:
                result += r"\)"
            else:
                result += r"\("
            open_equation = not open_equation
        else:
            result += c
    return result

def bold_relationships(str):
    result = ""
    skip_next = False
    for char_1, char_2 in zip(str[:len(str)], str[1:]):
        if (char_1 == "[" and char_2 == "[") or (char_1 == "]" and char_2 == "]"):
            result += "*"
            skip_next = True
        else:
            if skip_next:
                skip_next = not skip_next
            else:
                result += char_1 
    return result

def clean_text(str):
    return equation_to_latex(str)


def parse_line(line):
    # if "alias" in line:
    #     return {"alias": line.replace("alias", "")}
    #return {"base_equation" : line.strip().replace("base_equation = ", "").strip()}
    if "definition = "  in line:
        return {"definition" : line.strip().replace("definition = ", "").strip()} 
    if "base_equation = " in line:
        return {"base_equation" : line.strip().replace("base_equation = ", "").strip()}
    if "relational_equation = " in line:
        return {"relational_equation" : line.strip().replace("relational_equation = ", "").strip()}
    return None 

def get_file_contents() -> dict:
    contents = {}
    path = "spaced_vault"
    filenames = [x for x in os.listdir(path) if ".md" in x]
    for filename in filenames:
        with open(f"{path}/{filename}", "r") as file:
            contents[filename.replace(".md", "")] = file.read()  
    return contents 

def do_generate():
    """
    Generate cards from obsidian vault 
    """
    cards = []
    contents = get_file_contents()
    for name, content in contents.items():
        # if name != "anova theorem":
        #         continue
    
        args = {}
        lines = [x for x in content.split('\n') if x != '']
        for line in lines:
            parse = parse_line(line)
            if parse:
                args = {**args, **parse}
        
        atom = TemplateAtom(name=name, args=args)

        if atom.type == CardTypes.DEFINITION:
            question = f"What is {atom.name}"
            answer = clean_text(atom.definition)
            cards.append([atom.name, "DEFINITION", question, answer])
            
            question = f"What atom has this definition: {clean_text(atom.definition)} "
            answer = atom.name
            cards.append([atom.name, "DEFINITION", question, answer])

        if atom.type == CardTypes.EQUATION:
            question = f"What is equation of {atom.name}"
            answer = clean_text(atom.base_equation)
            cards.append([atom.name, "EQUATION", question, answer])

            question = f"What atom is this equation: {clean_text(atom.base_equation)}"
            answer = atom.name
            cards.append([atom.name, "EQUATION", question, answer])

    return cards

def get_all_atoms():
    atoms = []
    contents = get_file_contents()
    for name, content in contents.items():
    
        args = {}
        lines = [x for x in content.split('\n') if x != '']
        for line in lines:
            parse = parse_line(line)
            if parse:
                args = {**args, **parse}
        
        atom = TemplateAtom(name=name, args=args)
        if atom.type:
            atoms.append([atom.name, atom.type])
        else:
            print(atom)
    return atoms
        
    
if __name__ == "__main__":
    cards = do_generate()
    for card in cards:
        print(card)
