def get_sect_title(level):
    if level >= 50:
        return "Sect Founder"
    elif level >= 35:
        return "Grand Elder"
    elif level >= 20:
        return "Inner Elder"
    elif level >= 10:
        return "Core Disciple"
    elif level >= 5:
        return "Sect Disciple"
    else:
        return "Outer Disciple"