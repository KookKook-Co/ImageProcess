# main project file runs in infinite loop to update the number dead chicken
# from image stored in google drive storage
from Database import Database
from Storage import Storage
import ImageProcessing as ip
import time

class Main:
    def __init__(self):
        self.database = Database()
        self.storage = Storage()
    def loop(self):
        while True:
            cameras = self.database.getCamera()
            for cid in cameras:
                images = self.database.getImage(cid=cid)
                if len(images) < 18: continue
                loadImg = [self.storage.downloadImage(img.url) for img in images]
                for i in range(len(loadImg)):
                    deads, cnts = ip.countDeadChicken(loadImg[i:18])
                    images[i].setAmountDead(deads)
                    self.database.updateAmountDead(images[i])
            time.sleep(60*15)
def main():
    main = Main()
    main.loop()

if __name__ == '__main__':
    main()
