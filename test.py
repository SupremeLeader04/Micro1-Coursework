def longest_repeating_substring(input_string):
    """
    Finds the longest substring in which the same character repeats consecutively.

    Parameters:
        input_string - a string

    Returns:
        The longest substring of consecutive repeating characters. If multiple substrings
        have the same maximum length, the first one is returned.

    Example use:
    >>> longest_repeating_substring("hello")
    'll'
    >>> longest_repeating_substring("aabbcccdddde")
    'dddd'
    >>> large_string = 'a' * 1000000
    >>> longest_repeating_substring(large_string) == large_string
    True
    >>> longest_repeating_substring("a")
    'a'
    >>> longest_repeating_substring("")
    ''
    """
    if type(input_string) != str: # ensures that input is a string
        print("Not a valid string.")
        return None # terminates otherwise
    
    longest_length = 0 # these variables hold data on the longest substring found
    longest_character = ""

    current_length = 0 # these variables hold data on the current substring
    current_character = ""

    for i in input_string: # loop through all characters in string

        if i == current_character: # check if this continues current substring
            current_length += 1 # if so update length of current substring
        else:
            current_length = 1 # if not, start new current substring
            current_character = i

        if current_length > longest_length: # check if current substring exceeds longest, update longest
            longest_length = current_length # we must do this no matter the case above to deal with the first character
            longest_character = current_character
    
    return longest_length * longest_character

print(len(longest_repeating_substring("     aa")))