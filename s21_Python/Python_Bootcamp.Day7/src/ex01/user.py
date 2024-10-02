def user(responses, question):
    print(question)
    for i, r in enumerate(responses):
        print(f"{i + 1}. {r}")

    response = None
    while response is None:
        try:
            response = int(input("Enter your respons: "))
            if response < 1 or response > 3:
                print("Invalid number of response.")
                response = None
        except ValueError:
            print("Invalid input.")

    respiration = None
    while respiration is None:
        try:
            respiration = int(input("Enter your respiration: "))
            if respiration < 0 or respiration > 30:
                print("Invalid respiration measurement.")
                respiration = None
        except ValueError:
            print("Invalid input.")

    heart = None
    while heart is None:
        try:
            heart = int(input("Enter you heart rate: "))
            if heart < 0 or heart > 150:
                print("Invalid heart rate.")
                heart = None
        except ValueError:
            print("invalid input.")

    blushing = None
    while blushing is None:
        try:
            blushing = int(input("Enter your blushing level: "))
            if blushing < 1 or blushing > 6:
                print("Invalid blushing level.")
                blushing = None
        except ValueError:
            print("Invalid input.")

    pupillary = None
    while pupillary is None:
        try:
            pupillary = int(input("Enter your pupillary dilation: "))
            if pupillary < 2 or pupillary > 8:
                print("invalid pupillary dilation.")
                pupillary = None
        except ValueError:
            print("Invalid input.")

    return responses[response - 1], (respiration, heart, blushing, pupillary)