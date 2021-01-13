from django.db import models
from django.contrib.auth import get_user_model


User= get_user_model()


class AuctionManager(models.Manager):
    def active(self):
        return super().get_queryset().filter(active=True)

    def expired(self):
        return super().get_queryset().filter(active=False)


class Auction(models.Model):
    title = models.CharField(max_length=255)
    current_bid = models.FloatField()
    bid_count = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    live_date = models.DateTimeField()
    expiry_date = models.DateTimeField()
    active = models.BooleanField()
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def __unicode__(self):
        return self.title

    objects = models.Manager()
    AuctionManager = AuctionManager()


class BidManager(models.Manager):
    def current(self, auction):
        return super().get_queryset().filter(auction=auction).order_by('-created_at')


class Bid(models.Model):
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)
    value = models.FloatField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    email_sent = models.BooleanField(default=False)
    email_sent_time = models.DateTimeField(blank=True, null=True)
    

    objects = models.Manager()
    BidManager = BidManager()



class EmailManager(models.Manager):
    def emails(self):
        return super().get_queryset().order_by('-created_at')

class EmailQueue(models.Model):
    auction = models.ForeignKey(Auction, on_delete=models.SET_NULL, blank=True, null=True)
    bid = models.ForeignKey(Bid, on_delete=models.SET_NULL, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    objects = models.Manager()
    EmailManager = EmailManager()