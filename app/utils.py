import string
import random


def generate_tracking_number(prefix='CLRD', sections=3, section_length=4):
    parts = [
        ''.join(random.choices(string.ascii_uppercase + string.digits, k=section_length)) for _ in range(sections)
    ]
    
    return f"{prefix}-{'-'.join(parts)}"