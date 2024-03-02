from django.shortcuts import render, HttpResponse
from .models import Card, Review, CardState
from django.shortcuts import redirect
from django.utils import timezone
from django.urls import reverse
from bs4 import BeautifulSoup
from sm2_algorithm import sm2_algorithm
from .import_from_obsidian import do_generate



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

def parse_content(content) -> (str, str):
    question, answer = content.split("<br><br>")
    question, answer = clean_latex(question), clean_latex(answer)
    if question != "<br/>" and answer != "<br/>":
        print(question, answer)
        Card.objects.create(question=question, answer=answer, created=timezone.now())
    

def add_cards(request):
    content = request.POST.get('content')
    generate = request.POST.get('generate')
    if content:
        parse_content(content)
    if generate: 
        cards = do_generate()
        for question, answer in cards:
            print(question, answer)
            Card.objects.create(question=question, answer=answer, created=timezone.now())
    return render(request, "add_card.html", {})



# Create your views here.
def review_cards(request):

    # Retrieve the card index from URL parameter, defaulting to 0
    card_index = request.GET.get('index', 0)
    difficulty = request.GET.get('difficulty', None)
    
    try:
        card_index = int(card_index)
    except ValueError:
        card_index = 0
    
    # Get all cards (or a subset if you have too many)
    cards = list(Card.objects.all())
    card_states = list(CardState.objects.all())
    reviews = list(Review.objects.all())
    card_states_indexs = [x.card.id for x in card_states]

    # Clear out cards which aren't ready for review 
    cards_to_review = []
    for card in cards:
        if card.id not in card_states_indexs:
            cards_to_review.append(card)
        else:
            # card has a state, get it 
            card_state = card_states[card_states_indexs.index(card.id)]
            interval = card_state.inter_repetition_interval
            # get reviews then most recent 
            most_recent_review = max([x.date for x in reviews if x.card.id == card.id])

            today = timezone.now()
            if (today - most_recent_review).days >= interval:
                cards_to_review.append(card)

    cards = cards_to_review

    
    # Ensure the index is within bounds
    if card_index < 0:
        card_index = 0
    elif card_index >= len(cards):
        # Optionally loop to start or stop at the last
        card_index = 0  # or len(cards) - 1 for stopping at the last
    
    # Select the card to display
    card = cards[card_index] if cards else None
    card_state = None 
    if card:
        for state in card_states:
            if state.card.id == card.id:
                card_state = state

    if difficulty in ['0', '1', '2', '3', '4', '5']:
        ease = int(difficulty)

        # Create and save the review only if difficulty parameter is present
        Review.objects.create(card=card, date=timezone.now(), ease=ease)

        if not card_state:
            n, ef, i = sm2_algorithm(ease, 0, EASE_FACTOR_INIT, 0)
            print(n, ef,i )
            CardState.objects.create(card=card, repetition_number = n,  ease_factor=ef, inter_repetition_interval=i)
        else:
            # update state 
            record = CardState.objects.get(id=card_state.id)
            n, ef, i = sm2_algorithm(ease, record.repetition_number, record.ease_factor, record.inter_repetition_interval)
            record.repetition_number = n
            record.ease_factor = ef
            record.inter_repetition_interval = i
            record.save()
            record = CardState.objects.get(id=card_state.id)
            print(record)
        
        # Redirect to the next card to prevent resubmission of the review on refresh
        next_index = (card_index + 1) % len(cards)
        url = reverse('review_cards_name') + f'?index={next_index}'
        return redirect(url)
    
    # Pass the card and next index to the template
    context = {
        'card': card,
        'next_index': card_index  # Increment for the next card
    }
    # Pass the random card to the template context
    return render(request, "review_cards.html", context)

