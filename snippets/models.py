from django.db import models
from pygments import highlight
from pygments.formatters.html import HtmlFormatter
from pygments.lexers import get_all_lexers, get_lexer_by_name
from pygments.styles import get_all_styles

# ლექსერების და სტილების მომზადება არჩევანისთვის
LEXERS = [item for item in get_all_lexers() if item[1]]
LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])
STYLE_CHOICES = sorted([(item, item) for item in get_all_styles()])

class Snippet(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=True, default='')
    code = models.TextField()
    linenos = models.BooleanField(default=False)
    
    # აქ გასწორებულია LANGUAGE_CHOICES-ის სახელი (typo)
    language = models.CharField(choices=LANGUAGE_CHOICES, default='python', max_length=100)
    style = models.CharField(choices=STYLE_CHOICES, default='friendly', max_length=100)
    
    # მომხმარებელთან კავშირი (Permissions-ისთვის საჭირო ველი)
    owner = models.ForeignKey('auth.User', related_name='snippets', on_delete=models.CASCADE)
    highlighted = models.TextField()

    class Meta:
        ordering = ['created']

    def save(self, *args, **kwargs):
        """
        იყენებს 'pygments' ბიბლიოთეკას კოდის HTML ჰაილაითინგისთვის.
        """
        lexer = get_lexer_by_name(self.language)
        linenos = 'table' if self.linenos else False
        options = {'title': self.title} if self.title else {}
        formatter = HtmlFormatter(style=self.style, linenos=linenos,
                                  full=True, **options)
        self.highlighted = highlight(self.code, lexer, formatter)
        
        # აუცილებელი ხაზი: ბაზაში ფიზიკურად შენახვა
        super().save(*args, **kwargs)

    def __str__(self):
        # თუ სათაური ცარიელია, გამოიტანს ID-ს, რომ ადმინ პანელში არ დაიბნე
        return self.title if self.title else f"Snippet #{self.id}"