# from django.db import models
# from django.core.cache import cache
# from ckeditor.fields import RichTextField
# from googletrans import Translator
# from django.conf import settings

# LANGUAGE_CHOICES = (
#     ('en', 'English'),
#     ('hi', 'Hindi'),
#     ('bn', 'Bengali'),
# )

# class FAQ(models.Model):
#     question = models.TextField(help_text="Enter the question in English")
#     answer = RichTextField(help_text="Format your answer using the editor")
    
#     # Store translations directly
#     question_hi = models.TextField(blank=True, verbose_name="Question (Hindi)")
#     question_bn = models.TextField(blank=True, verbose_name="Question (Bengali)")
#     answer_hi = RichTextField(blank=True, verbose_name="Answer (Hindi)")
#     answer_bn = RichTextField(blank=True, verbose_name="Answer (Bengali)")
    
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     class Meta:
#         verbose_name = "FAQ"
#         verbose_name_plural = "FAQs"
#         ordering = ['-created_at']

#     def __str__(self):
#         return self.question[:50]

#     def get_translated_content(self, field, lang):
#         """
#         Get translated content with caching support
#         """
#         if lang == 'en':
#             return getattr(self, field)

#         cache_key = f'faq_{self.id}_{field}_{lang}'
#         cached_content = cache.get(cache_key)

#         if cached_content:
#             return cached_content

#         translated_field = f'{field}_{lang}'
#         content = getattr(self, translated_field)

#         if not content:
#             # Fallback to English if translation is not available
#             content = getattr(self, field)
#         else:
#             # Cache the translation
#             cache.set(cache_key, content, timeout=86400)  # Cache for 24 hours

#         return content

#     def save(self, *args, **kwargs):
#         """
#         Override save to handle translations
#         """
#         is_new = self.pk is None
#         super().save(*args, **kwargs)

#         if is_new:
#             self._translate_content()

#     def _translate_content(self):
#         """
#         Translate content to supported languages
#         """
#         translator = Translator()
        
#         for lang_code, _ in LANGUAGE_CHOICES:
#             if lang_code != 'en':
#                 if not getattr(self, f'question_{lang_code}'):
#                     translated_question = translator.translate(
#                         self.question, dest=lang_code
#                     ).text
#                     setattr(self, f'question_{lang_code}', translated_question)

#                 if not getattr(self, f'answer_{lang_code}'):
#                     translated_answer = translator.translate(
#                         self.answer, dest=lang_code
#                     ).text
#                     setattr(self, f'answer_{lang_code}', translated_answer)

#         self.save()


from django.db import models
from django.core.cache import cache
from ckeditor.fields import RichTextField

class FAQ(models.Model):
    question = models.TextField(help_text="Enter the question in English")
    answer = RichTextField(help_text="Format your answer using the editor")
    
    question_hi = models.TextField(blank=True, verbose_name="Question (Hindi)")
    question_bn = models.TextField(blank=True, verbose_name="Question (Bengali)")
    answer_hi = RichTextField(blank=True, verbose_name="Answer (Hindi)")
    answer_bn = RichTextField(blank=True, verbose_name="Answer (Bengali)")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "FAQ"
        verbose_name_plural = "FAQs"
        ordering = ['-created_at']

    def __str__(self):
        return self.question[:50]

    def get_translated_content(self, field, lang):
        if lang == 'en':
            return getattr(self, field)

        cache_key = f'faq_{self.id}_{field}_{lang}'
        cached_content = cache.get(cache_key)

        if cached_content:
            return cached_content

        translated_field = f'{field}_{lang}'
        content = getattr(self, translated_field)

        if not content:
            content = getattr(self, field)
        else:
            cache.set(cache_key, content, timeout=86400)

        return content