def calculation(a):
    respiration = sum([i[0] for i in a]) / len(a) if len(a) > 0 else 0
    heart_rate = sum([i[1] for i in a]) / len(a) if len(a) > 0 else 0
    blushing = sum([i[2] for i in a]) / len(a) if len(a) > 0 else 0
    pupillary = sum([i[3] for i in a]) / len(a) if len(a) > 0 else 0

    return respiration, heart_rate, blushing, pupillary
