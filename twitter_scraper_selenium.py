import re
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup as BS

from twitter_scraper import get_tweets
from getpass import getpass


def twitter_profile_data(username):
    url = "https://twitter.com/"+username
    print(url)

    options = Options()
    # options.add_argument("--headless")
    driver = webdriver.Chrome('chromedriver', options=options)
    driver.get(url)
    page_state = driver.execute_script('return document.readyState;')
    html = driver.page_source

    soup = BS(html, "html.parser")

    data = soup.find('div', {"data-testid":"UserProfileHeader_Items"})
    user_add_info =[]
    for tag in data.contents:
        user_add_info.append(tag.text)

    user_desc = soup.find('div', {"data-testid":"UserDescription"}).text

    user_follow_data = soup.find('div', {"class":"css-1dbjc4n r-18u37iz r-1w6e6rj"})
    links = user_follow_data.findAll('a', title=True)
    follow = []
    for a in links:
        follow.append(a['title'])
        
    profile = {
        'username' : username,
        'url'  : url,
        'user additional infos' : user_add_info,
        'User Description' : user_desc,
        'following' : follow[0],
        'followers' : follow[1],
    }

    driver.close()
    driver.quit()

    return profile


def search_latest_tag(tag):
    tag = '#' + tag
    tweets = get_tweets(tag, pages = 1)

    all_tweets = []
    for tweet in tweets:
        twits_dict = {'text' : [tweet['text']],
                      'isRetweet' : tweet['isRetweet'],
                      'replies' : tweet['replies'],
                      'retweets' : tweet['retweets'],
                      'likes' : tweet['likes'],
                      'tweetId' :  tweet['tweetId'], 
                      'tweetUrl' :  tweet['tweetUrl'], 
                      'username' :  tweet['username'], 
                      'userId' :  tweet['userId'], 
                      'isRetweet' :  tweet['isRetweet'], 
                      'isPinned' :  tweet['isPinned'], 
                      'time' :  tweet['time']
                    }
        all_tweets.append(twits_dict)
    return all_tweets


def twitter_tweet_detail_data(url, username, password):
    print(url)

    options = Options()
    driver = webdriver.Chrome('chromedriver.exe', options=options)
    driver.get("https://twitter.com/login")
    time.sleep(1)

    username_field = driver.find_element_by_name("session[username_or_email]")
    password_field = driver.find_element_by_name("session[password]")

    username_field.send_keys(username)
    driver.implicitly_wait(1)
    
    password_field.send_keys(password)
    driver.implicitly_wait(1)
    driver.find_element_by_xpath("//div[contains(@data-testid,'LoginForm_Login_Button')]").click()

    driver.get(url)
    time.sleep(3)

    html = driver.page_source
    time.sleep(10)

    soup = BS(html, "html.parser")
    time.sleep(10)

    caption = soup.find('div', {"class":"css-901oao r-hkyrab r-1qd0xha r-1b6yd1w r-16dba41 r-ad9z0x r-bcqeeo r-bnwqim r-qvutc0"}).text
    comments = [d.text for d in soup.find_all('div',{'class':'css-901oao r-hkyrab r-1qd0xha r-a023e6 r-16dba41 r-ad9z0x r-bcqeeo r-bnwqim r-qvutc0'})] 
    date = [d['title'] for d in soup.find_all('a',{'class':'r-1re7ezh r-1loqt21 r-1q142lx r-1qd0xha r-a023e6 r-16dba41 r-ad9z0x r-bcqeeo r-3s2u2q r-qvutc0 css-4rbku5 css-18t94o4 css-901oao'})] 
    users = [d.text for d in soup.find_all('div',{'class':'css-901oao css-bfa6kz r-1re7ezh r-18u37iz r-1qd0xha r-a023e6 r-16dba41 r-ad9z0x r-bcqeeo r-qvutc0'})] 
    
    comments_datas = []
    for i in range(len(comments)):
        comm = {}
        comm['comment text'] = comments[i]
        comm['comment date'] = date[i]
        comm['comment user ID'] = users[i+1]
        comments_datas.append(comm)

    likes = soup.find('div', {"data-testid":"like"}).text
    retweets = soup.find('div', {"data-testid":"retweet"}).text
    replies = soup.find('div', {"data-testid":"reply"}).text
    
    twits_dict = {'user ID' :  users[0], 
                  'caption' : caption,
                  'No. of likes' : likes,
                  'No. of retweets' : retweets,
                  'No. of replies' : replies,
                  'comments' : comments_datas,
                }
    driver.close()
    driver.quit()

    return twits_dict


def twitter_tweet_whole_cmnts(url):
    comments_datas = []

    options = Options()
    driver = webdriver.Chrome('chromedriver.exe', options=options)

    driver.get(url)
    time.sleep(3)

    last_height = driver.execute_script("return document.documentElement.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        time.sleep(5)

        new_height = driver.execute_script("return document.body.scrollHeight")

        if new_height == last_height:
            try:
                driver.implicitly_wait(8)
                html = driver.page_source
                time.sleep(5)

                soup = BS(html, "html.parser")
                time.sleep(5)

                driver.find_element_by_xpath("//span[text()='Show more replies']").click()
                time.sleep(5)
            except:
                break
            
        last_height = new_height
        
        html = driver.page_source
        time.sleep(5)
        soup = BS(html, "html.parser")
        time.sleep(5)

        data = [d for d in soup.find_all('article',{'role':'article'})] 
        
        for i in data:
            try:
                comments = i.find('div',{'class':'css-901oao r-hkyrab r-1qd0xha r-a023e6 r-16dba41 r-ad9z0x r-bcqeeo r-bnwqim r-qvutc0'}).text
                date = i.find('a',{'class':'r-1re7ezh r-1loqt21 r-1q142lx r-1qd0xha r-a023e6 r-16dba41 r-ad9z0x r-bcqeeo r-3s2u2q r-qvutc0 css-4rbku5 css-18t94o4 css-901oao'})['title']
                users = i.find('div',{'class':'css-901oao css-bfa6kz r-1re7ezh r-18u37iz r-1qd0xha r-a023e6 r-16dba41 r-ad9z0x r-bcqeeo r-qvutc0'}).text

                comm = {}
                comm['comment text'] = comments
                comm['comment date'] = date
                comm['comment user ID'] = users
                
                if comm not in comments_datas :
                    comments_datas.append(comm)
            except:
                pass
    
    driver.close()
    driver.quit()

    return comments_datas


if __name__ == "__main__":
    # profile = twitter_profile_data("NatGeo")
    # print(profile)

    # tag_twits= search_latest_tag("machinelearning")
    # print(tag_twits)

    url = "https://twitter.com/NatGeo/status/1302489301268168705"
    # username = "USERNAME"
    # password = "PASSWORD"
    # comments = twitter_tweet_detail_data(url, username, password)
    # print(comments)

    comments = twitter_tweet_whole_cmnts(url)
    print(comments)
