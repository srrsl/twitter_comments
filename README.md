# twitter comments

1. This repository will provide all comments of a specific tweet using its URL address. It is written without twitter API. All we need to continue extracting comments using this part of code will be beautiful soup and selenium and some other libraries. Just alter input URL value in twitter_tweet_whole_cmnts(url)<br>
    - url = "https://twitter.com/NatGeo/status/1302489301268168705"
    - comments = twitter_tweet_whole_cmnts(url)<br>
    - print(comments)<br><br>
    
2. Additionally it can show you some information about a specific tweet (by its URL adress), like its user, the number of likes, retweet and other stuff like this. Uncomment these lines and comment others. Then write your twitter username and password to login <br>
    - url = "https://twitter.com/NatGeo/status/1302489301268168705"<br>
    - username = "USERNAME"<br>
    - password = "PASSWORD"<br>
    - comments = twitter_tweet_detail_data(url, username, password)<br>
    - print(comments)<br><br>
    
3. Also you can search for the latest tweets of a tag. Uncomment two following lines and comment others to do so.<br>
    - tag_twits= search_latest_tag("machinelearning")<br>
    - print(tag_twits)<br><br>
    
4. Uncomment two following lines and comment others. Then write a twitter account to see its profile informations. e.g. @NatGeo <br>
    - profile = twitter_profile_data("NatGeo")<br>
    - print(profile)<br><br>

Hope you enjoy and it can help you

