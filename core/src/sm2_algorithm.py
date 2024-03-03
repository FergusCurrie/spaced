def sm2_algorithm(q, n, EF, I):
    """
    Implements the SM-2 algorithm used in spaced repetition systems.

    Parameters:
    q (int): User grade (quality response to the flashcard, typically from 0 to 5)
    n (int): Repetition number for the current flashcard
    EF (float): Current easiness factor of the flashcard
    I (int): Current interval before the flashcard is to be reviewed again

    Returns:
    tuple: Updated values of n, EF, and I
    """
    
    # Check if the response was correct
    if q >= 3:
        if n == 0:
            I = 1
        elif n == 1:
            I = 6
        else:
            I = round(I * EF)
        n += 1
    else:  # Incorrect response
        n = 0
        I = 1

    # Update the easiness factor
    EF = EF + (0.1 - (5 - q) * (0.08 + (5 - q) * 0.02))
    if EF < 1.3:
        EF = 1.3

    return n, EF, I