from django.db import models

class Lyric(models.Model):
    title  = models.TextField()
    artist = models.TextField()
    lyrics = models.TextField()

    def __str__(self):
        return "{} - {}".format(self.artist, self.title)