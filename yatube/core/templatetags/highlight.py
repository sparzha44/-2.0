from django import template
import re

register = template.Library()


@register.filter
def highlight(text, keyword):
    """
    Кастомный фильтр для выделения найденного слова в тексте.
    
    Использование в шаблоне:
    {{ post.text|highlight:keyword }}
    
    Найденное слово будет обёрнуто в <mark> tag для выделения жёлтым.
    """
    if not keyword or not text:
        return text
    
    # Используем регулярные выражения для поиска слова (без учёта регистра)
    # re.IGNORECASE - поиск без учёта регистра
    # re.escape - экранирует специальные символы в keyword
    pattern = re.compile(re.escape(keyword), re.IGNORECASE)
    
    # Заменяем найденное слово на версию с тегом <mark>
    # re.sub возвращает строку с заменами
    highlighted = pattern.sub(lambda m: f'<mark style="background-color: yellow;">{m.group()}</mark>', text)
    
    return highlighted
