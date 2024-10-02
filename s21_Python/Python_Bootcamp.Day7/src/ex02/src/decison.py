def decision(a):
    """
    Function: decision
    Determines if the input a represent a replicant or a human based on predetermined ranges.

    Args:
    a: a list of four floats representing the average values of respiration, heart rate, blushing level,
    and pupillary dilation

    Returns:
    A string: either "replicant" or "human", depending on whether the input averages fall outside the predetermined
    normal range for each value.

    Raises:
    TypeError: if the input argument is not a list of floats or ints.
    """

    for word in a:
        if not isinstance(word, float | int):
            raise TypeError("Input argumet must be a list of numbers")

    resp_min = 12
    resp_max = 16
    heart_min = 60
    heart_max = 100
    blushing_min = 1
    blushing_max = 6
    pupillary_min = 2
    pupillary_max = 8

    check = (
        a[0] < resp_min
        or a[0] > resp_max
        or a[1] < heart_min
        or a[1] > heart_max
        or a[2] < blushing_min
        or a[2] > blushing_max
        or a[3] < pupillary_min
        or a[3] > pupillary_max
    )

    if check:
        return "replicant"
    else:
        return "human"
