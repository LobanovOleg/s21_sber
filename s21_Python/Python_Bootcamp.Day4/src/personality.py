import random


def turrents_generator():
    personality_traits = [
        "neuroticism",
        "openness",
        "conscientiousness",
        "extraversion",
        "agreeableness",
    ]
    actions = ["shoot", "search", "talk"]
    total = 100

    while True:
        if total == 0:
            break

        numbers = [random.randint(0, total) for _ in range(len(personality_traits))]
        summa = sum(numbers)
        correction = [int(i * total / summa) for i in numbers]
        correction[-1] += total - sum(correction)
        personality = dict(zip(personality_traits, correction))

        turret = type("Turret", (), personality)

        for action in actions:

            def action_methods(act=action):
                print(act.capitalize() + "ing")

            setattr(turret, action, action_methods)

        yield turret


if __name__ == "__main__":
    tur = turrents_generator()
    for i in range(10):
        t = next(tur)
        print("-----------------------------------------------")
        print(
            f"Turret {i + 1}:\n"
            f"neuroticism {t.neuroticism}, "
            f"openness {t.openness}, "
            f"conscientiousness {t.conscientiousness}, "
            f"extraversion {t.extraversion}, "
            f"agreeableness {t.agreeableness}"
        )
        t.shoot()
        t.search()
        t.talk()
        print("-----------------------------------------------")
