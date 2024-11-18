"""Database of game character and NPC replicas

The module needs character_classes.Phrases to avoid duplicate phrases.
"""

from character_classes import Phrases  # type: ignore
from typing import Dict, List, Any


def get_phrases(chrs: Dict[str, List[Any]]) -> Dict[str, Any]:
    """Gets NPCs phrases

    Parameters
    ----------
    chrs : Dict[str, List[Any]]
        The dictionary with enemies and NPCs list

    Returns
    -------
    Dict[str, Any]
        The all game phrases data
    """

    all_phrases = {
        Phrases.INIT.value: [
            {
                "text": (
                    "Что, кот? Какая кошка? [ <i>Приглушенное</i> Mяяяу ]"
                    "\n...Гм... аа, слышал, слышал\n"
                    "Передай письмо моему товарищу - Франческо Тотти,\n"
                    "он обычно бывает в трактире на севере, и приходи обратно"
                ),
                "condition": (
                    "npc.name == 'Денис Риччи' and 'Следы кота' in [q.brief"
                    " for q in self.questbook if not q.is_done]"
                ),
                "response": [
                    Phrases.ACCEPT_QUEST.value,
                    Phrases.REFUSE_QUEST.value,
                ],
            },
            {
                "text": (
                    "Аа, письмо [ <i>Пробегает глазами</i> ], спасибо "
                    "за весточку. Получи в награду от меня этот Кортик\n"
                ),
                "condition": (
                    "npc.name == 'Франческо Тотти' and 'Письмо для сослуживца'"
                    " in [q.brief for q in self.questbook] and 'Письмо друга'"
                    " in [item.name for item in self.inventory]"
                ),
                "response": [
                    Phrases.WHATS_NEW.value,
                    Phrases.QUEST_NEW.value,
                    Phrases.END.value,
                ],
            },
            {
                "text": (
                    "Передал письмо? Хорошо.\nЛюди с востока недавно привезли"
                    " интересную игру, обыграй меня и я расскажу, что знаю"
                ),
                "condition": (
                    "npc.name == 'Денис Риччи' and 'Письмо для сослуживца' in"
                    " [q.brief for q in self.questbook if q.is_done] and "
                    "'Выиграй в го у Дениса Риччи' not in [q.description for "
                    "q in self.questbook if q.is_done]"
                ),
                "response": [Phrases.LETS_PLAY.value, Phrases.END.value],
            },
            {
                "text": "Ну что, готов сыграть?",
                "condition": (
                    "npc.name == 'Джанкарло Эспозито' and 'Го' in [q.brief for"
                    " q in self.questbook if not q.is_done]"
                ),
                "response": [Phrases.LETS_PLAY.value, Phrases.END.value],
            },
            {
                "text": (
                    "Слышал ли я про пропажу кота? Нет, но здесь появился"
                    " странный корсар. Если разберешься с ним, возможно "
                    "и найдешь кота"
                ),
                "condition": (
                    "npc.name == 'Николай Сфорца' and 'К озёрам' in [q.brief"
                    " for q in self.questbook if not q.is_done]"
                ),
                "response": [
                    Phrases.ACCEPT_QUEST.value,
                    Phrases.REFUSE_QUEST.value,
                ],
            },
            {
                "text": (
                    "КТО ТЕБЕ ЭТО РАССКАЗАЛ?!..\nДа это правда...Это я украл "
                    "кота короля! И не жалею о проведенных с ним дней и готов"
                    " понести справедливое наказание. Но отдать тебе я его не"
                    " могу - украли его уже у меня! Я уверен, что это происки"
                    " главаря корсаров Доппио Дьяволо - разъяренный я "
                    "взобрался на крышу своего дома и осмотрел окрестности в "
                    "подзорную трубу. И увидел как на восток улепытывают его "
                    "прихвостни с мешком! Одному идти туда бесполезно, а "
                    "рассказать никому я не смог. Пошли со мной и вытащим его"
                    " оттуда!\nРади кота короля!"
                ),
                "condition": (
                    "npc.name == 'Денис Риччи' and 'Откровение' in [q.brief"
                    " for q in self.questbook if not q.is_done]"
                ),
                "response": [
                    Phrases.ACCEPT_QUEST.value,
                    Phrases.REFUSE_QUEST.value,
                ],
            },
            {
                "text": (
                    "Ты наверняка слышал, что у меня пропал Васька - мой"
                    " любимый кот. Верни мне его и получишь награду - "
                    "1000 пиастров!"
                ),
                "condition": (
                    "npc.name == 'Маттео Тапочкин' and 'Возвращение кота' not "
                    "in [q.brief for q in self.questbook]"
                ),
                "response": [
                    Phrases.ACCEPT_QUEST.value,
                    Phrases.REFUSE_QUEST.value,
                ],
            },
            {
                "text": (
                    "Ты наверняка слышал, что у меня пропал...Урааа! Мой"
                    " кот, идём сюда, Васька [ <i>Довольно мурчит и идёт"
                    " к королю </i> ]. Держи свою заслуженную награду, я"
                    " очень благодарен тебе! [ <i> Обнимает </i> ]."
                ),
                "condition": (
                    "npc.name == 'Маттео Тапочкин' and 'Возвращение кота' in "
                    "[q.brief for q in self.questbook if not q.is_done]"
                ),
                "response": [
                    Phrases.END.value,
                ],
            },
            {
                "text": (
                    "Привет, спаситель моего кота! В нашем королевстве "
                    "все хорошо."
                ),
                "condition": (
                    "npc.name == 'Маттео Тапочкин' and 'Возвращение кота' in "
                    "[q.brief for q in self.questbook if q.is_done]"
                ),
                "response": [
                    Phrases.END.value,
                ],
            },
            # corsairs text
            {
                "text": (
                    "Что? Говорят я украл кота короля? "
                    "[Звуки негодования...]\n"
                    "Это все происки гнусных кондотьеров\n"
                    "Передай это известие нашему товарищу Ризотто Неро\n"
                    "Его ты сможешь найти в Коралловом гроте.\n"
                    "А я пока что-нибудь здесь придумаю."
                ),
                "condition": (
                    "npc.name == 'Омар Капоне' and 'Тот самый.. Ризотто Неро'"
                    "not in [q.brief for q in self.questbook] and "
                    "'Финальный бой' not in [q.brief for q in self.questbook]"
                ),
                "response": [
                    Phrases.ACCEPT_QUEST.value,
                    Phrases.REFUSE_QUEST.value,
                    Phrases.END.value,
                ],
            },
            {
                "text": (
                    "Оoo Друживщееее.. иккк.. буээ..\n"
                    "[Судя по всему это был тот самый пьяный из корсаров"
                    " - Ризотто Неро...]\n"
                    "Друживщее, ты кек равз ввреемяяя. Падайдии.. икфф"
                    ".. к Джамалу Корлеоне и папросии.. буээ икфф.. "
                    "у него еще вина\nОн тут где-то не подалеку\n"
                    "И вазьмии вот эту саблю!"
                ),
                "condition": (
                    "npc.name == 'Ризотто Неро' and 'Тот самый.. Ризотто Неро'"
                    " in [q.brief for q in self.questbook] and 'Сильнейший'"
                    " not in [q.brief for q in self.questbook] and 'Бутылка"
                    " вина' not in [item.name for item in self.inventory] and"
                    " 'Бутылка вина' not in [q.brief for q in self.questbook]"
                ),
                "response": [
                    "Ай да по бутылке вина!",
                    Phrases.REFUSE_QUEST.value,
                ],
            },
            {
                "text": (
                    "Категорически приветствую!\n"
                    "[Перед тобой стоит один из генералов корсаров"
                    " - Джамал Корлеоне].\n"
                    "Что же хочет от меня такой молодой сослуживец?"
                ),
                "condition": (
                    "npc.name == 'Джамал Корлеоне' and 'Бутылка вина' in"
                    " [q.brief for q in self.questbook] and 'Испытание"
                    " смелости' not in [q.brief for q in self.questbook]"
                    " and 'Бутылка вина' not in [item.name"
                    " for item in self.inventory] "
                ),
                "response": [
                    "Хочу попросить у Вас бутылку вина.",
                    Phrases.END.value,
                ],
            },
            {
                "text": (
                    "Приветствую!\n"
                    "Я вижу ты смог справиться со своим испытанием!"
                ),
                "condition": (
                    "npc.name == 'Месут Озил' and 'Испытание смелости' in"
                    " [q.brief for q in self.questbook] and 'Бутылка вина' not"
                    " in [item.name for item in self.inventory] and 'Бутылка"
                    " вина' in [q.brief for q in self.questbook if q.is_done]"
                ),
                "response": ["Конечно справился!", Phrases.END.value],
            },
            {
                "text": (
                    "Оооо.. Ты вернулся. Да еще и с бутылкой вина..\n"
                    "Икффф.. буэээ..\n"
                    "Держи за это вот такой подарок"
                ),
                "condition": (
                    "npc.name == 'Ризотто Неро' and 'Сильнейший' in [q.brief"
                    " for q in self.questbook] and 'Бутылка вина'"
                    "in [item.name for item in self.inventory]"
                    " and ('Испытание смелости' and 'Бутылка вина') "
                    "in [q.brief for q in self.questbook if q.is_done]"
                ),
                "response": [
                    "Оу, премного благодарен за столь ценный подарок!",
                    Phrases.END.value,
                ],
            },
            {
                "text": (
                    "Здравствуй, друже!\n"
                    "Пьяница Ризотто предупредил насчет тебя\n"
                    "Что же получи свою награду"
                ),
                "condition": (
                    "npc.name == 'Джорно Джованна' and 'Подготовка' in"
                    " [q.brief for q in self.questbook] and 'Финальный бой' "
                    "not in [q.brief for q in self.questbook]"
                ),
                "response": ["Мешок с мукой?"],
            },
            {
                "text": (
                    "Эй дружище!\nРад тебя видеть снова! Вижу что ты смог"
                    " найти виновного в клевете и разобрался с ним. Так"
                    " держать!"
                ),
                "condition": (
                    "npc.name == 'Омар Капоне' and 'Финальный бой' in [q.brief"
                    " for q in self.questbook] and "
                    "('Сильнейший' and 'Подготовка' and 'Испытание смелости')"
                    " in [q.brief for q in self.questbook if q.is_done]"
                ),
                "response": ["Спасибо за поздравления!", Phrases.END.value],
            },
            {
                "text": "Aве, гражданин!",
                "condition": "npc.class_id == ClassID.CIVIL",
                "response": [
                    Phrases.WHATS_NEW.value,
                    Phrases.QUEST_NEW.value,
                    Phrases.END.value,
                ],
            },
            {
                "text": "Aве, камрад!",
                "condition": (
                    "npc.class_id == ClassID.CONDOTR and type(npc) is not"
                    " Enemy"
                ),
                "response": [
                    Phrases.WHATS_NEW.value,
                    Phrases.QUEST_NEW.value,
                    Phrases.END.value,
                ],
            },
            {
                "text": "Эй, Дружище!",
                "condition": (
                    "npc.class_id == ClassID.CORSAIR and type(npc) is not"
                    " Enemy"
                ),
                "response": [
                    Phrases.WHATS_NEW.value,
                    Phrases.QUEST_NEW.value,
                    Phrases.END.value,
                ],
            },
            {
                "text": Phrases.ANGRY_END_CON.value,
                "condition": (
                    "npc.class_id == ClassID.CONDOTR and type(npc) is Enemy"
                ),
                "response": ["Никогда! Смерть или слава, приятель!"],
            },
            {
                "text": Phrases.ANGRY_END_COR.value,
                "condition": (
                    "npc.class_id == ClassID.CORSAIR and type(npc) is Enemy"
                ),
                "response": ["Может, попробуешь подкрепить слова делом?"],
            },
        ],
        Phrases.WHATS_NEW.value: [
            {
                "text": (
                    "Да вроде все по-прежнему в Датском королевстве...\n"
                    "Аа, ты уже слышал, что пропал кот короля?!\n"
                    "Говорят даже, что его украл капитан корсаров - Омар"
                    " Капоне!\nНо мало ли, что говорят люди"
                ),
                "condition": (
                    "npc.name == 'Джованни Чичиков' and self.class_id =="
                    " ClassID.CONDOTR"
                ),
            },
            {
                "text": (
                    "У меня то ничего нет, попробуй спросить у "
                    "Джанкарло Эспозито. Он тут недалеко."
                ),
                "condition": "npc.name == 'Николай Сфорца'",
                "response": [Phrases.END.value],
            },
            {
                "text": (
                    "Ах, корсар..\n"
                    "Да вроде все по-прежнему в Датском королевстве...\n"
                    "Слышал, что ваш капитан - Омар Капоне похитил кота"
                    " короля.\nИль же это все слухи?"
                ),
                "condition": (
                    "npc.name == 'Джованни Чичиков' and self.class_id =="
                    " ClassID.CORSAIR and"
                    " 'Подстава' not in [q.brief for q in self.questbook]"
                ),
                "response": ["Вздор! Это подстава!", Phrases.END.value],
            },
            {
                "text": (
                    "Я тут подслушал, что ты интересуешься котом короля,"
                    " я кое-что видел и могу рассказать тебе. Только "
                    "уважь старика, со мной давно уже никто не хочет "
                    "играть"
                ),
                "condition": (
                    "npc.name == 'Джанкарло Эспозито' and "
                    "'Откровение' not in [q.brief for q in"
                    " self.questbook]"
                ),
                "response": [Phrases.LETS_PLAY.value, Phrases.END.value],
            },
            {
                "text": Phrases.NOTHING.value,
                "response": [Phrases.QUEST_NEW.value, Phrases.END.value],
            },
        ],
        Phrases.QUEST_NEW.value: [
            {
                "text": (
                    "У меня то ничего нет, попробуй спросить у "
                    "Джанкарло Эспозито. Он тут недалеко."
                ),
                "condition": "npc.name == 'Николай Сфорца'",
                "response": [Phrases.END.value],
            },
            {
                "text": (
                    "Я тут подслушал, что ты интересуешься котом короля,"
                    " я кое-что видел и могу рассказать тебе. Только "
                    "уважь старика, со мной давно уже никто не хочет "
                    "играть"
                ),
                "condition": (
                    "npc.name == 'Джанкарло Эспозито' and "
                    "'Откровение' not in [q.brief for q in"
                    " self.questbook]"
                ),
                "response": [Phrases.LETS_PLAY.value, Phrases.END.value],
            },
            {
                "text": "У меня есть для тебя задание",
                "condition": "[q for q in npc.questbook if not q.is_done]",
                "response": [Phrases.WHATS_QUEST.value, Phrases.END.value],
            },
            {
                "text": "Да нет ничего",
                "condition": "not len(npc.questbook)",
                "response": [Phrases.WHATS_NEW.value, Phrases.END.value],
            },
        ],
        Phrases.END.value: [
            {
                "text": Phrases.END_CIV.value,
                "condition": "npc.class_id == ClassID.CIVIL",
            },
            {
                "text": Phrases.END_CON.value,
                "condition": "npc.class_id == ClassID.CONDOTR",
            },
            {
                "text": Phrases.END_COR.value,
                "condition": "npc.class_id == ClassID.CORSAIR",
            },
        ],
        "Вздор! Это подстава!": [
            {
                "text": npc.questbook[0].description,
                "condition": f"npc.id == '{npc.id}'",
                "response": [
                    Phrases.ACCEPT_QUEST.value,
                    Phrases.REFUSE_QUEST.value,
                ],
            }
            for npc in chrs["NPC"]
            if npc.questbook
        ],
        "Ай да по бутылке вина!": [
            {
                "text": "Принеси вина для Ризотто",
                "condition": f"npc.id == '{npc.id}'",
                "response": [
                    Phrases.ACCEPT_QUEST.value,
                    Phrases.REFUSE_QUEST.value,
                    Phrases.END.value,
                ],
            }
            for npc in chrs["NPC"]
        ],
        "Хочу попросить у Вас бутылку вина.": [
            {
                "text": "ЧТОО??!!\nБутылку вина? И для кого же она?",
                "condition": f"npc.id == '{npc.id}'",
                "response": [
                    "Для господина Ризотто Неро",
                    "Для меня достопочтенного!",
                ],
            }
            for npc in chrs["NPC"]
        ],
        "Для господина Ризотто Неро": [
            {
                "text": (
                    "Ах.. Этому пьянице. Как ему не стыдно просить об этом"
                    " других!\nХмммм.. хмм..\nЧто же, я дам тебе бутылку при"
                    " одном условии\nТебе необходимо одолеть одного из"
                    " кондотьеров. После победы найди Месута Озила на "
                    " банановом острове\n"
                    "И возьми вот это"
                ),
                "condition": f"npc.id == '{npc.id}'",
                "response": [
                    "Кого же?",
                    Phrases.END.value,
                ],
            }
            for npc in chrs["NPC"]
        ],
        "Кого же?": [
            {
                "text": npc.questbook[0].description,
                "condition": f"npc.id == '{npc.id}'",
                "response": [
                    Phrases.ACCEPT_QUEST.value,
                    Phrases.REFUSE_QUEST.value,
                    Phrases.END.value,
                ],
            }
            for npc in chrs["NPC"]
            if npc.questbook
        ],
        "Конечно справился!": [
            {
                "text": npc.questbook[0].description,
                "condition": f"npc.id == '{npc.id}'",
                "response": [
                    Phrases.ACCEPT_QUEST.value,
                    Phrases.REFUSE_QUEST.value,
                    Phrases.END.value,
                ],
            }
            for npc in chrs["NPC"]
            if npc.questbook
        ],
        "Для меня достопочтенного!": [
            {
                "text": (
                    "ЩЕЕЕЕНОК!\nТЫ ХОТЬ ПОНИМАЕШЬ У КОГО ТАКОЕ"
                    " ПРОСИШЬ?\nХМММ.. хмммм..\nЧто же наглец, я дам тебе"
                    " бутылку вина если ты одолеешь кое-кого!"
                ),
                "condition": f"npc.id == '{npc.id}'",
                "response": [
                    "Кто же это?",
                    Phrases.REFUSE_QUEST.value,
                ],
            }
            for npc in chrs["NPC"]
        ],
        "Кто же это?": [
            {
                "text": "Одолей Макскорпоне Палаццо в Базарных переулках",
                "condition": f"npc.id == '{npc.id}'",
                "response": [
                    Phrases.ACCEPT_QUEST.value,
                    Phrases.REFUSE_QUEST.value,
                    Phrases.END.value,
                ],
            }
            for npc in chrs["NPC"]
            if npc.questbook
        ],
        "Оу, премного благодарен за столь ценный подарок!": [
            {
                "text": (
                    "Знаешь что? Икфф.. Направляйся к Джорно Джованне.\n"
                    "Он находится на восток в Базарных переулках."
                ),
                "condition": f"npc.id == '{npc.id}'",
                "response": ["Вперед!", Phrases.END.value],
            }
            for npc in chrs["NPC"]
        ],
        "Вперед!": [
            {
                "text": (
                    "Отправляйся к Джорно Джованне на восток в Базарные"
                    " переулки"
                ),
                "condition": f"npc.id == '{npc.id}'",
                "response": [
                    Phrases.ACCEPT_QUEST.value,
                    Phrases.REFUSE_QUEST.value,
                    Phrases.END.value,
                ],
            }
            for npc in chrs["NPC"]
        ],
        "Мешок с мукой?": [
            {
                "text": (
                    "Трофей достался [Джорно потирает нос покрытый"
                    " мукой...]\nВсе наши сослуживцы видят в тебе большой"
                    " потенциал\nТак пойди же и сокруши главного кондотьера -"
                    " Винсента ван Гога\nЗА КОРСАРОВ!!!"
                ),
                "condition": f"npc.id == '{npc.id}'",
                "response": ["Так тому и быть", Phrases.END.value],
            }
            for npc in chrs["NPC"]
        ],
        "Так тому и быть": [
            {
                "text": npc.questbook[0].description,
                "condition": f"npc.id == '{npc.id}'",
                "response": [
                    Phrases.ACCEPT_QUEST.value,
                    Phrases.REFUSE_QUEST.value,
                    Phrases.END.value,
                ],
            }
            for npc in chrs["NPC"]
            if npc.questbook
        ],
        "Спасибо за поздравления!": [
            {
                "text": (
                    "Теперь у вас есть удостоверение заслуженого корсара\n"
                    "Вы успешно прошли основной квест!\n"
                    "Вы можете покинуть игру или продолжить путешествие."
                ),
                "condition": f"npc.id == '{npc.id}'",
                "response": [
                    Phrases.END.value,
                ],
            }
            for npc in chrs["NPC"]
        ],
        Phrases.WHATS_QUEST.value: [
            {
                "text": (
                    "[q for q in npc.questbook if not"
                    " q.is_done][0].description"
                ),
                "condition": (
                    "len([q for q in npc.questbook if not q.is_done])"
                ),
                "response": [
                    Phrases.ACCEPT_QUEST.value,
                    Phrases.REFUSE_QUEST.value,
                ],
            }
        ],
        Phrases.ACCEPT_QUEST.value: [
            {
                "text": Phrases.GRATITUDE_CIV.value,
                "condition": "npc.class_id == ClassID.CIVIL",
            },
            {
                "text": Phrases.GRATITUDE_CON.value,
                "condition": "npc.class_id == ClassID.CONDOTR",
            },
            {
                "text": Phrases.GRATITUDE_COR.value,
                "condition": "npc.class_id == ClassID.CORSAIR",
            },
        ],
        Phrases.REFUSE_QUEST.value: [
            {
                "text": Phrases.UPSET_CIV.value,
                "condition": "npc.class_id == ClassID.CIVIL",
            },
            {
                "text": Phrases.UPSET_CON.value,
                "condition": "npc.class_id == ClassID.CONDOTR",
            },
            {
                "text": Phrases.UPSET_COR.value,
                "condition": "npc.class_id == ClassID.CORSAIR",
            },
        ],
        Phrases.WIN.value: [
            {
                "text": (
                    "Ого, ты все-таки обыграл меня...Давай сыграем еще раз?\n"
                    "Ну ладно-ладно...Я видел следы, уходящие на запад, и \n"
                    "убегающего корсара, я думаю мой человек в Долине озёр "
                    "может тебе подсказать"
                ),
                "condition": (
                    "npc.name == 'Денис Риччи' and 'Го' in [q.brief for q in"
                    " self.questbook if q.is_done]"
                ),
                "response": [
                    Phrases.ACCEPT_QUEST.value,
                    Phrases.REFUSE_QUEST.value,
                ],
            },
            {
                "text": (
                    "Давно я так не играл, ну слушай.\nДержал я путь на юг - "
                    "продавал южанам мороженое, ха-ха, и засмотрелся на море,"
                    " да шаг не сбавил, а тут БАЦ... Только меня и видели - "
                    "свалился в колодец! Да повезло - запутался ногой в цепи."
                    " Провисел я так, барахтаясь и зовя на помощь до позднего"
                    " вечера, так не достигнув успеха ни в том, ни в другом. "
                    " Проснулся я от звуков умиления и всхлипываний, да так "
                    "удивился, узнав голос помощника короля, что даже забыл о"
                    " моем положении.\nА он в это время сетовал на судьбу, "
                    "что не может в другое время проводить время с таким "
                    "прекрасным котом.\nНаконец я опо мнился, и крикнул - "
                    "'Помогите!'. На что услышал ответный крик и отдаляющийся"
                    " топот сапог. Но я стою перед тобой, ха-ха. И за это "
                    "могу сказать спасибо жителям, которые пришли с утра "
                    "набирать воду. Вот и вся моя история..."
                ),
                "condition": (
                    "npc.name == 'Джанкарло Эспозито' and 'Выиграй в го у"
                    " Джанкарло Эспозито' in [q.description for q in"
                    " self.questbook if q.is_done]"
                ),
                "response": [
                    Phrases.ACCEPT_QUEST.value,
                    Phrases.REFUSE_QUEST.value,
                ],
            },
            {"text": Phrases.WIN_REACT.value},
        ],
    }
    return all_phrases
