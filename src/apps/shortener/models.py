from django.db import models
from .utils import shortcode_generator,create_shortcode
from django.conf import settings
# Create your models here.
SHORTCODE_MAX = getattr(settings, "SHORTCODE_MAX", 15)
class KirrURLManager(models.Manager):
    def all(self,*args,**kwargs):
        qs_main = super(KirrURLManager,self).all(*args,**kwargs)
        qs = qs_main.filter(active = True)
        return qs
    def refresh_shortcodes(slef):
        qs = KirrURL.objects.filter(id__gte=1)
        new_codes = 0
        for q in qs:
            q.shortcode = create_shortcode(q)
            q.save()
            new_codes +=1
        return "New codes made: {}".format(new_codes)
        
class KirrURL(models.Model):
    url = models.CharField(max_length=220)
    shortcode = models.CharField(max_length=SHORTCODE_MAX,unique = True, blank=True)
    updated = models.DateTimeField(auto_now = True) #everytime the model is saved
    timestamp = models.DateTimeField(auto_now_add = True) # when model was created
    active = models.BooleanField(default = True)

    objects = KirrURLManager()
    def __str__(self):
        return str(self.url)
    def save(self,*args,**kwags):
        if self.shortcode is None or self.shortcode == "":
            print("something")
            self.shortcode = create_shortcode(self)
        super(KirrURL,self).save(*args,**kwags)
    