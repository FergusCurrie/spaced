import os 
import logging

# Step 2: Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', filename='logs.log', filemode='w')

class Atom:
    def __init__(self, name, args):
        self.name = name
        self.definition = None
        self.base_equation = None
        self.relational_equation = None
        if 'definition' in args:
            self.definition = args['definition']
        if 'base_equation' in args:
            self.base_equation = args['base_equation']
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
    path = "/Users/ferguscurrie/spaced_vault"
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
        
        atom = Atom(name=name, args=args)
        logging.info(f"{atom}")

        question = f"What is {atom.name}"
        if not (atom.definition or atom.base_equation):
            continue
        if atom.definition:
            answer = equation_to_latex(atom.definition)
        else:
            answer = equation_to_latex(atom.base_equation)
        
        cards.append([question, answer])
    return cards
        
    
if __name__ == "__main__":
    cards = do_generate()
    for card in cards:
        print(card)
