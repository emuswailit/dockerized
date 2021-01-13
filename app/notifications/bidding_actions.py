from .models import EmailQueue

class BiddingActions():

    auction = None

    def __init__(self, instance):
        self.auction = instance

    def update_auction(self):
        auction = self.auction
        auction.bid_count = Bid.BidManager.current(auction).count()
        auction.current_bid = format(auction.value, ".2f")
        auction.save()

    def send_email(self):
        EmailQueue(auction=self.auction).save()