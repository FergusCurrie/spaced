from django.shortcuts import render, HttpResponse
from .models import Card, Review 
from django.shortcuts import redirect
from django.utils import timezone
from django.urls import reverse
from bs4 import BeautifulSoup

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
    if content:
        parse_content(content)
    return render(request, "add_card.html", {})

def sort_cards_by_ease(cards, reviews):

    to_review = []
    to_review_weight = []
    for card in cards: 
        card_reviews = sorted([r for r in reviews if r.card == card], key=lambda review: review.date)
        if len(card_reviews) ==0:
            to_review.append(card)
            to_review_weight.append(0)
            continue 
        interval = 0 
        for review in card_reviews:
            if review.ease == 3:
                interval = 0
            if review.ease == 2:
                interval += 1
            if review.ease == 1:
                if interval == 0:
                    interval = 1
                interval *= 1.5 
        days_since_first_review = (timezone.now() - card_reviews[0].date).seconds / (60 * 24)
        
        remaining_interval = days_since_first_review - interval 
        if remaining_interval > 0:
            # add to review stack, weighted by diff 
            to_review.append(card)
            to_review_weight.append(remaining_interval)
        else:
            # else pass 
            pass

    sorted_pairs = sorted(zip(to_review, to_review_weight), key=lambda x: x[1], reverse=True)
    sorted_to_review = [pair[0] for pair in sorted_pairs]
    return sorted_to_review


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
    reviews = list(Review.objects.all())
    
    cards = sort_cards_by_ease(cards, reviews)

    # Ensure the index is within bounds
    if card_index < 0:
        card_index = 0
    elif card_index >= len(cards):
        # Optionally loop to start or stop at the last
        card_index = 0  # or len(cards) - 1 for stopping at the last
    
    # Select the card to display
    card = cards[card_index] if cards else None

    if difficulty in ['easy', 'medium', 'hard']:
        ease = {'easy': 1, 'medium': 2, 'hard': 3}.get(difficulty)
        # Create and save the review only if difficulty parameter is present
        Review.objects.create(card=card, date=timezone.now(), ease=ease)
        
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

