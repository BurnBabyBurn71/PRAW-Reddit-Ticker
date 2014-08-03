import praw, time, html.parser, requests

#this is designed for python 3.3
#for python 2.x you will have to change 'import html.parser' to 'import HTMLParser'.
#You will also have to change 'html.parser.HTMLParser()' to HTMLParser.HTMLParser()'

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
