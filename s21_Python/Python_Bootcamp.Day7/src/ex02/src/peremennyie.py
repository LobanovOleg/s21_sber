def calculation(a):
    """
    Function: calculation Calculates the average values of respiration, heart rate, blushing level,
    and pupillary dilation from a list of variables.

    Args:
    a: a list of tuples, where each tuple contains four values (respiration, heart rate, blushing level,
    and pupillary dilation)

    Returns:
    A tuple containing four floats: the average respiration, average heart rate, average blushing level, and average
    pupillary dilation. If the input list is empty, all values will be zero.
    """
    respiration = sum([i[0] for i in a]) / len(a) if len(a) > 0 else 0
    heart_rate = sum([i[1] for i in a]) / len(a) if len(a) > 0 else 0
    blushing = sum([i[2] for i in a]) / len(a) if len(a) > 0 else 0
    pupillary = sum([i[3] for i in a]) / len(a) if len(a) > 0 else 0

    return respiration, heart_rate, blushing, pupillary
