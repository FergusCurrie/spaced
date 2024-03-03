from django.shortcuts import render, HttpResponse, get_object_or_404
from .models import Card, Review, AtomState, Atom
from django.shortcuts import redirect
from django.utils import timezone
from django.urls import reverse
from bs4 import BeautifulSoup
from sm2_algorithm import sm2_algorithm
from import_from_obsidian import do_generate, get_all_atoms
import random 
import logging

logger = logging.getLogger(__name__)

# # Step 2: Configure logging
# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', filename='logs.log', filemode='w')

# logging.info('Initalised logger ')

EASE_FACTOR_INIT = 2.5 

def home(request):
    url = reverse('review_cards_name') 
    return redirect('review_cards_name') 

def clean_latex(s: str):
    soup = BeautifulSoup(s, 'html.parser')
    ql_formula_elements = soup.find_all(class_='ql-formula')
    for element in ql_formula_elements:
        data_value = element.get('data-value')
        element.replace_with(f"\({data_value}\)")
    return str(soup).replace("<p>","").replace("</p>","")

def check_if_card_question_exists_in_db(question) -> bool:
    cards = list(Card.objects.all())
    for card in cards:
        if card.question == question:
            return True
    return False 

def check_if_atom_name_exists_in_db(name) -> bool:
    cards = list(Atom.objects.all())
    for card in cards:
        if card.name == name:
            return True
    return False

def add_card(atom_name, atom_type, question, answer):
    if check_if_card_question_exists_in_db(question):
        logging.info(f"card {question} already in db")
        return 
    
    atom = get_object_or_404(Atom, name=atom_name)
    Card.objects.create(atom=atom, question=question, answer=answer, created=timezone.now())
    logging.info(f"created new card: {question} {answer}")

def add_atom(name, atom_type):
    if check_if_atom_name_exists_in_db(name):
        logging.info(f"atom {name} already in db")
        return 

    atom = Atom.objects.create(name=name, type=atom_type, created=timezone.now())
    AtomState.objects.create(
        atom=atom, 
        repetition_number = 0,  
        ease_factor=EASE_FACTOR_INIT, 
        inter_repetition_interval= 0 #random.choice([0,1,2,3])
    )
    logging.info(f"created new atom: {name}")

def parse_content(content) -> (str, str):
    question, answer = content.split("<br><br>")
    question, answer = clean_latex(question), clean_latex(answer)
    if question != "<br/>" and answer != "<br/>":
        print(question, answer)
        raise Exception("Only adding from obisidian currently")
    
def add_cards(request):
    logging.info('add cards called')
    content = request.POST.get('content')
    generate = request.POST.get('generate')
    if content:
        parse_content(content)
    if generate: 
        atoms = get_all_atoms()
        for atom_name, atom_type in atoms:
            add_atom(atom_name, atom_type)
        cards = do_generate()
        for atom_name, type, question, answer in cards:
            add_card(atom_name, type, question, answer)
    return render(request, "add_card.html", {})



# Create your views here.
def review_cards(request):
    difficulty = request.GET.get('difficulty', None)
    
    # Get all cards (or a subset if you have too many)
    atoms = list(Atom.objects.all())
    states = list(AtomState.objects.all())
    reviews = list(Review.objects.all())
    atom_states_indexs = [x.atom.id for x in states]

    # Clear out cards which aren't ready for review 
    atoms_to_review = []
    for atom in atoms:
        if atom.id not in atom_states_indexs:
            atoms_to_review.append(card)
        else:
            # card has a state, get it 
            atom_state = states[atom_states_indexs.index(atom.id)]
            interval = atom_state.inter_repetition_interval
            # get reviews then most recent 
            reviews_of_atom = [x.date for x in reviews if x.atom.id == atom.id]
            if len(reviews_of_atom) > 0:
                most_recent_review = max(reviews_of_atom)
            else:
                most_recent_review = atom.created
            today = timezone.now()
            if (today - most_recent_review).days >= interval:
                atoms_to_review.append(atom)

    atoms = atoms_to_review
    
    # Select the card to display
    atom = atoms[0] if atoms else None
    atom_state = None 
    card = None 
    if atom:
        for state in states:
            if state.atom.id == atom.id:
                atom_state = state
        atom_cards = Card.objects.filter(atom=atom)
        if len(atom_cards) > 0:
            card = random.choice(atom_cards)

    if difficulty in ['0', '1', '2', '3', '4', '5']:
        ease = int(difficulty)

        # Create and save the review only if difficulty parameter is present
        Review.objects.create(card=card, atom=atom, date=timezone.now(), ease=ease)


        # update state 
        record = AtomState.objects.get(id=atom_state.id)
        previous_repetition_number = record.repetition_number
        previous_ease_factor =  record.ease_factor
        previous_interval = record.inter_repetition_interval
        n, ef, i = sm2_algorithm(ease, record.repetition_number, record.ease_factor, record.inter_repetition_interval)
        record.repetition_number = n
        record.ease_factor = ef
        record.inter_repetition_interval = i
        record.save()
        record = AtomState.objects.get(id=atom_state.id)

        # log 
        logging.info(f"Studied atom {atom.name} with previous settings (rep, ease, int)=({previous_repetition_number},{previous_ease_factor},{previous_interval}) ease={ease}, updated to ({n},{ef},{i})")
        url = reverse('review_cards_name')
        return redirect(url)
    
    # Pass the card and next index to the template
    context = {
        'card': card,
    }
    # Pass the random card to the template context
    return render(request, "review_cards.html", context)

