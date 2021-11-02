import json


# configuration loaders
def load_configurations(file='fair/configurations.json', block="dummy_listings"):
    """
        Load the configurations from a json file
    """
    with open(file) as json_file:
        configurations = json.load(json_file)
    
    return configurations["dummy_listings"]

# generate random token    
def generate_random_token(length=20, initial='tkn'):
    token = initial
    filled = 0
    
    max_sub_token_size = int(0.25 * length)
    min_sub_token_size = 1
    assert max_sub_token_size >= min_sub_token_size

    import random, string
    
    while len(token) < length:
        method = random.randint(1,5)
        size = random.randint(min_sub_token_size, max_sub_token_size)
        if method == 1: # chars
            sub_token = random.sample(string.ascii_letters, size)
        elif method == 2: # digit
            sub_token = random.sample(string.ascii_letters, size)
        elif method == 3:  # both
            sub_token = random.sample(string.ascii_letters + string.digits, size)
        elif method == 4:   # random pickup
            sub_token = random.sample(token, min(size, len(token)) )
        else:              # dash space
            sub_token = '-'

        token += ''.join(sub_token)
    return token[:length]