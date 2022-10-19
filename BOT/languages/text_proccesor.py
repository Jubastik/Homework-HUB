from languages.language_pack_ru import LanguageRussian


# Языковой обработчик
def process_text(key, msg, **kwargs) -> str:
    locale = msg.from_user.locale
    if locale == "ru":
        language_pack = LanguageRussian
    else:
        language_pack = LanguageRussian
    text = getattr(language_pack, key)
    return text.format(**kwargs)