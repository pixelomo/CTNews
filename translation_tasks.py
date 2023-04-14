from celery_config import celery_app
from translate import translate_with_gpt

@celery.task
def perform_translation(text, target_language):
    translated_text = translate_with_gpt(text, target_language)
    return translated_text
