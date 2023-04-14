from celery_app import celery_app  # Change this import
from translate import translate_with_gpt

@celery_app.task(name="translation_tasks.perform_translation")
def perform_translation(text, target_language):
    translated_text = translate_with_gpt(text, target_language)
    return translated_text
