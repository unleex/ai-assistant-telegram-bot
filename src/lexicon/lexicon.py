LEXICON_RU = {
    ### buttons ###
    # delegate
    "delegate_select_all_participants_butt":
    """✅ Выбрать всех""",
    "delegate_add_new_participant_butt":
    """➕Добавить/изменить резюме""",
    ### menu ###
    "start_command_description":
    """Запуск бота.""",

    "help_command_description":
    """Получите информацию о боте.""",

    "prompt_command_description":
    """Отправьте запрос к GPT""",

    "brainstorm_command_description":
    """Бот будет помогать с идеями.""",

    "conclude_command_description":
    """Подвести итоги мозгового штурма""",

    "pause_command_description":
    """Приостановить/вернуть бота к участию в штурме.""",

    "cancel_command_description":
    """отмена операций""",

    "delegate_command_description":
    """Бот декомпозирует и делегирует задачу.""",
    ### errors ###
    "unknown_user":
    """Бот еще не знает этого пользователя! Попросите %s написать сюда в чат, бот его запомнит""",
    # /start
    "start_command":
    'Здравствуйте, это Евпатий.\nДля корректной работы, '
    'попросите каждого пользователя группы написать что-нибудь, я вас так запомню.\nДля дополнительной информации отправьте /help.',
    # / help
    "help_command":
    """/prompt - отправьте запрос к GPT
/brainstorm - мозговой штурм с GPT
Во время штурма:
    /pause - Остановить или продолжить участие бота в штурме. Бот не будет отвечать на сообщения, но запоминать будет все равно.
    /conclude - Подвести итоги штурма: главные идеи и проблемы.
/cancel - отмена операций
/delegate - декомпозиция и делегация задачи
Заметьте, что при окончании команды бот не будет отвечать на ваши сообщения, для запроса напишите /prompt
Если в меню бота вы не находите какие-либо команды, перезапустите Telegram и оно обновится.
для еще более подробной информации, вот ссылка на репозиторий: https://github.com/unleex/ai-assistant-telegram-bot, посмотрите readme
    """,
    # / cancel
    "cancel_command":"""
    Операции отменены.""",
    # /prompt
    "prompt_payload_empty":
    """Введите текст запроса.""",
    # /brainstorm
    "brainstorm_topic_empty":
    """Укажите тему мозгового штурма.""",

    "brainstorm_bot_unpaused":
    """Возвращаюсь к мозговому штурму!""",

    "brainstorm_bot_paused":
    """Бот приостановлен.""",
    # /delegate
    "delegate_task_empty":
    """Укажите задание для декомпозиции и делегации.
    """,
    "delegate_select_participants":
    """Выберите пользователей для делегации. Когда закончите, отправьте /finish!""",
    "delegate_no_user_cvs":
    """
    Не найдены резюме пользователей!
Они могут сейчас сами прислать свои резюме, либо пришлите в разных сообщениях их резюме,
указывая их никнеймы (с '@')
    """,
    "delegate_adding_user_cv":
    """Пользователи могут сейчас сами прислать свои резюме, либо пришлите в разных сообщениях их резюме,
указывая их никнеймы (с '@')""",
    "delegate_user_cv_added":
    """Хорошо! Отправьте /finish, если вы закончили с резюме""",
    "delegate_cv_template":
    """Имя: %s. Резюме: %s""",
    "delegate_finished_adding_user_cvs":
    """Изменения сохранены.""",
    "delegate_selected_user":
    """✅@%s""",
    "unknown_type_of_media": 'Привет! Похоже, что ты прислал(а) контент, с которым я пока не умею работать. Пожалуйста, напиши свой вопрос или сообщение в текстовом формате, и я с радостью помогу!'
}