from requests import get
from re import findall
from smtplib import SMTP, SMTP_SSL
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import time


class FenerbahceBot():
    URL = "https://fenerbahce.org/controls/listxml/haberler-futbol.xml"
    temp = ""

    def get_last_post(self): 
        resp = get(
            self.URL, headers={
                "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Mobile Safari/537.36"
            }
        )

        return findall("<loc>(.*)</loc>", resp.text)[0].replace(
            "httpss://", "https://"
        )
    

    def setup(self):
        self.temp = self.get_last_post()
    

    def send_notification(self, url: str) -> None:
        client = SMTP_SSL("smtp.gmail.com", 465)
        client.login("tekyolfenercom@gmail.com", open("sifre.txt", "r", encoding="utf-8").read().replace("\n", ""))

        message = MIMEMultipart("alternative")
        message["Subject"] = "Yeni bir haber paylaşıldı!"
        message["From"] = "tekyolfenercom@gmail.com"
        message["To"] = "tekyolfenercom@gmail.com"

        part1 = MIMEText(f"Yeni haber linki: {url}", "plain")
        message.attach(part1)

        client.sendmail(
            "tekyolfenercom@gmail.com", "tekyolfenercom@gmail.com", message.as_string(

            )
        )
        print("Mail yollandı", url)
        

    def check(self) -> None:
        last = self.get_last_post()
        if last != self.temp:
            self.send_notification(
                last
            )
            self.temp = last
        
        else:
            pass


bot = FenerbahceBot()
bot.setup()
while True:
    bot.check()
    print("Kontrol edildi", bot.temp)
    time.sleep(2)