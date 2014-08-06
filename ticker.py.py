import praw, time, html.parser, requests, sched

"""
-------------------------------------------------------------------------------------------------------------------------------
This is designed for python 3.3 and for the /r/BytecoinBCN subreddit, to use for your own subreddit, change where necessary   |
                                                                                                                              |
for python 2.x you will have to change the following:                                                                         |
                                                                                                                              |
1. 'import html.parser' to 'import HTMLParser'                                                                                |
2. 'html.parser.HTMLParser()' to 'HTMLParser.HTMLParser()'                                                                    |
3. print() to print ''                                                                                                        |
-------------------------------------------------------------------------------------------------------------------------------
"""

s = sched.scheduler(time.time, time.sleep)
def do_something(sc):
    print("Updating the stuff...") #This message will show up each time the script is looped (in other words each time the ticker is updated)

if __name__=="__main__":

    req = requests.get('http://www.cryptocoincharts.info/v2/api/tradingPair/bcn_btc') #change 'bcn' to your coin symbol (e.g, btc)
    req = req.json()
    volume =  req['volume_btc']
    price =  req['price']
    pricebefore = req['price_before_24h']
    change = ((float(req['price'])/float(req['price_before_24h']))*100)-100

    start = '[](/start)'
    end = '[](/end)'
    content = start + '\n\n' + '####[Poloniex Exchange: ](http://www.poloniex.com/exchange/btc_bcn)' + ' ' + '**1 BCN =** ' + price + ' BTC' + ' | ' + '**Volume (24h)** = ' + volume + ' BTC' + ' | ' + '**Change (24h)** = ' + "{0:.2f}".format(change) + '%' +  ' | ' + '*' + time.strftime("%c") + ' UTC*'

    r = praw.Reddit(user_agent='/u/reddituser for /r/subreddit') #change /u/reddituser to your reddit username and /r/subreddit to your subreddit
    r.login('username','password') #change username to your reddit username and password to you reddit password

    sub = r.get_subreddit('subreddit') #change 'subreddit' to the name of your subreddit
    desc = sub.get_settings()['description']

    html_parser = html.parser.HTMLParser()
    desc = html_parser.unescape(desc)

    before = desc.split(start)
    after = desc.split(end)

    if before[1] and after[1]:
        new_desc = before[0] + content + end + after[1]
        sub.update_settings(description=new_desc)
        
    sc.enter(600, 1, do_something, (sc,)) #Change 600 to how often you want the script to loop in seconds (600 = 10 minutes)
s.enter(600, 1, do_something, (s,)) #Change 600 to how often you want the script to loop in seconds (600 = 10 minutes)
s.run()

#This Python script was made by BurnBabyBurn71
