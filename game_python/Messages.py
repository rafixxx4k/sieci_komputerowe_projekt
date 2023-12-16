import random


class Messages:
    answers = {
        0: [" "],
        1: ["wziąłeś totem",
            "udało ci się wyrwać totem",
            "po prostu wziąłeś totem",
            "wziąłeś totem, ale nie wiem czy to humanitarne zagranie",
            "w elegancki sposób, popijając herbatkę chwyciłeś totem",
            "wszyscy rzucili się na totem, ale ty byłeś najszybszy",
            "zagadałeś wszystkich i wziąłeś totem",
            "totem po prostu wpadł ci w ręce",
            "dzwoń po ambulans, ale nie dlamnie tylko dla przeciwników, bo wziąłem totem"
            ],
        2: ["ktoś wyrwał ci totem",
            "po prostu zaspałeś",
            "ja ninja twój przeciwnik wyskoczył z cienia i zabrał totem",
            "przeciwnik zabrał ci totem",
            "przeciwnik zabrał ci totem, ale nie wiem czy to humanitarne zagranie",
            "po co wstawałeś, i tak nie miałeś szans",
            "nie tym razem, ale nie mart się to tylko gra"
            ],
        3: ["niestety to nie te same karty",
            "coś chyba zaburza twoją percepcję rzeczywistości",
            "brawo, byłeś pierwszy w kolejce po więcej kart",
            "w tej grze trzeba być szybkim i spostrzegawczym, a tobie tego drugiego brakuje"]
    }

    @staticmethod
    def get(message):
        return random.choice(Messages.answers[message])


# Usage example:
random_answer = Messages.get(1)
print(random_answer)
