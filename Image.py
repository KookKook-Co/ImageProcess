class Image:
    def __init__(self, data):
        self.cid, self.timestamp, self.url, self.amountDead = data
    
    def __str__(self):
        return ', '.join([str(self.cid), str(self.timestamp), str(self.url), str(self.amountDead)])
    
    def setAmountDead(self, amountDead):
        self.amountDead = amountDead
