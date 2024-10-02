from decison import decision
from peremennyie import calculation
from reader import read_json
from user import user


def main():
    question = read_json("questions.json")

    responses = []
    variables = []

    for a in question:
        response, var = user(a["responses"], a["question"])
        responses.append(response)
        variables.append(var)

    averages = calculation(variables)
    decisions = decision(averages)

    print("Based on the variable measurements, the respoding subject is a", decisions)


if __name__ == "__main__":
    main()
