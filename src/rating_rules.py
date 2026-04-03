def calculate_ratings(entity_counts):
    """
    Given a dictionary of entity counts like:
    {"PROFANITY": 5, "VIOLENCE": 2, "GORE": 0, "DRUGS": 1, "NUDITY_SEX": 0}
    
    Returns a dictionary of ratings for the 10 regions.
    """
    
    profanity = entity_counts.get("PROFANITY", 0)
    violence = entity_counts.get("VIOLENCE", 0)
    gore = entity_counts.get("GORE", 0)
    drugs = entity_counts.get("DRUGS", 0)
    sex = entity_counts.get("NUDITY_SEX", 0)
    
    ratings_output = {}

    # 1. India (CBFC): Strict on violence, gore, drugs, sex
    if gore > 5 or sex > 2 or drugs > 5 or profanity > 15:
        ratings_output['India (CBFC)'] = "A (Adults Only)"
    elif gore > 0 or sex > 0 or violence > 10 or drugs > 2 or profanity > 5:
        ratings_output['India (CBFC)'] = "U/A 16+"
    elif violence > 5 or profanity > 2:
        ratings_output['India (CBFC)'] = "U/A 13+"
    elif violence > 0 or profanity > 0:
        ratings_output['India (CBFC)'] = "U/A 7+"
    else:
        ratings_output['India (CBFC)'] = "U (Unrestricted)"

    # 2. USA (MPAA): Strict on profanity ('f-bomb'), sex
    if sex > 5 or gore > 5:
        ratings_output['USA (MPAA)'] = "NC-17"
    elif sex > 1 or profanity > 3 or gore > 2 or drugs > 3:
        ratings_output['USA (MPAA)'] = "R"
    elif profanity > 0 or violence > 5 or drugs > 0:
        ratings_output['USA (MPAA)'] = "PG-13"
    elif violence > 0:
        ratings_output['USA (MPAA)'] = "PG"
    else:
        ratings_output['USA (MPAA)'] = "G"

    # 3. UK (BBFC)
    if gore > 5 or sex > 5:
        ratings_output['UK (BBFC)'] = "18"
    elif gore > 1 or sex > 1 or drugs > 2 or profanity > 5:
        ratings_output['UK (BBFC)'] = "15"
    elif violence > 3 or profanity > 1 or drugs > 0:
        ratings_output['UK (BBFC)'] = "12"
    elif violence > 0:
        ratings_output['UK (BBFC)'] = "PG"
    else:
        ratings_output['UK (BBFC)'] = "U"

    # 4. Australia (ACB)
    if sex > 4 or gore > 4:
        ratings_output['Australia (ACB)'] = "R18+"
    elif sex > 1 or drugs > 3 or profanity > 5:
        ratings_output['Australia (ACB)'] = "MA15+"
    elif violence > 2 or profanity > 1 or drugs > 0:
        ratings_output['Australia (ACB)'] = "M"
    elif violence > 0:
        ratings_output['Australia (ACB)'] = "PG"
    else:
        ratings_output['Australia (ACB)'] = "G"

    # 5. Germany (FSK)
    if gore > 3 or sex > 3:
        ratings_output['Germany (FSK)'] = "FSK 18"
    elif violence > 5 or profanity > 5 or drugs > 2:
        ratings_output['Germany (FSK)'] = "FSK 16"
    elif violence > 2 or profanity > 1 or drugs > 0:
        ratings_output['Germany (FSK)'] = "FSK 12"
    elif violence > 0:
        ratings_output['Germany (FSK)'] = "FSK 6"
    else:
        ratings_output['Germany (FSK)'] = "FSK 0"

    # 6. France (CNC)
    if gore > 4 or sex > 4:
        ratings_output['France (CNC)'] = "-18"
    elif drugs > 3 or violence > 10:
        ratings_output['France (CNC)'] = "-16"
    elif profanity > 5 or violence > 4:
        ratings_output['France (CNC)'] = "-12"
    elif violence > 1:
        ratings_output['France (CNC)'] = "-10"
    else:
        ratings_output['France (CNC)'] = "U"

    # 7. Japan (EIRIN)
    if gore > 4 or sex > 4:
        ratings_output['Japan (EIRIN)'] = "R18+"
    elif drugs > 3 or violence > 8 or sex > 1:
        ratings_output['Japan (EIRIN)'] = "R15+"
    elif violence > 2 or profanity > 2:
        ratings_output['Japan (EIRIN)'] = "PG12"
    else:
        ratings_output['Japan (EIRIN)'] = "G"

    # 8. South Korea (KMRB)
    if gore > 5 or sex > 5:
        ratings_output['South Korea (KMRB)'] = "Restricted"
    elif gore > 1 or sex > 1 or drugs > 2 or violence > 8:
        ratings_output['South Korea (KMRB)'] = "18"
    elif violence > 3 or profanity > 3 or drugs > 0:
        ratings_output['South Korea (KMRB)'] = "15"
    elif violence > 1 or profanity > 1:
        ratings_output['South Korea (KMRB)'] = "12"
    else:
        ratings_output['South Korea (KMRB)'] = "ALL"

    # 9. New Zealand (OFLC)
    if gore > 5 or sex > 5:
        ratings_output['New Zealand (OFLC)'] = "R18"
    elif drugs > 2 or violence > 6 or profanity > 10:
        ratings_output['New Zealand (OFLC)'] = "R16"
    elif violence > 3 or profanity > 3:
        ratings_output['New Zealand (OFLC)'] = "R13"
    elif violence > 1 or profanity > 1:
        ratings_output['New Zealand (OFLC)'] = "M"
    elif violence > 0:
        ratings_output['New Zealand (OFLC)'] = "PG"
    else:
        ratings_output['New Zealand (OFLC)'] = "G"

    # 10. Canada (CHVRS)
    if gore > 5 or sex > 5:
        ratings_output['Canada (CHVRS)'] = "R"
    elif drugs > 2 or violence > 6:
        ratings_output['Canada (CHVRS)'] = "18A"
    elif violence > 3 or profanity > 5 or sex > 0:
        ratings_output['Canada (CHVRS)'] = "14A"
    elif violence > 1 or profanity > 1:
        ratings_output['Canada (CHVRS)'] = "PG"
    else:
        ratings_output['Canada (CHVRS)'] = "G"

    return ratings_output
