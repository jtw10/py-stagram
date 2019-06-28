from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
from random import randint


chromedriver_path = r'C:\Users\Me\Downloads\chromedriver.exe' # replace path with your chromedriver path
webdriver = webdriver.Chrome(executable_path=chromedriver_path)
sleep(2)
webdriver.get('http://www.instagram.com/accounts/login/?source=auth_switcher')
sleep(3)

username = webdriver.find_element_by_name('username')
username.send_keys('YOUR_USERNAME') # replace string with your instagram username
password = webdriver.find_element_by_name('password')
password.send_keys('YOUR_PASSWORD') # replace string with your password

# get login button with css selector
button_login = webdriver.find_element_by_css_selector('#react-root > section > main > div > article > div > div:nth-child(1) > div > form > div.Igw0E.IwRSH.eGOV_._4EzTm.bkEs3.CovQj.jKUp7.DhRcB > button')
button_login.click()
sleep(3)

# Can comment this line out if your account does not have the suspicious login attempt screen
input("Press Enter to continue...")

# click not now button with css selector / comment out the lines if there is no popup
notnow = webdriver.find_element_by_css_selector('body > div.RnEpo.Yx5HN > div > div > div.mt3GC > button.aOOlW.HoLwm')
notnow.click() 

# replace hashtags with the ones you want to follow
hashtag_list = ['follow4follow']

# Open & read list of previously followed users, and add them to prev_user_list
prev_user_list = []

with open('followedlist.txt', 'r') as f:
    x = f.readlines()
    print(x)
    if ',' in x[0]:
        split_list = (x[0]).split(',')
        for i in split_list:
            prev_user_list.append(i)
    print(prev_user_list)

new_followed = []
tag = -1
followed = 0
likes = 0
comments = 0

for hashtag in hashtag_list:
    tag += 1
    webdriver.get('https://www.instagram.com/explore/tags/' + hashtag_list[tag] + '/')
    sleep(5)
    first_thumbnail = webdriver.find_element_by_xpath('//*[@id="react-root"]/section/main/article/div[1]/div/div/div[1]/div[1]/a/div')

    first_thumbnail.click()
    sleep(randint(1, 2))
    try:
        for x in range(1, 200):
            username = webdriver.find_element_by_xpath('/html/body/div[3]/div[2]/div/article/header/div[2]/div[1]/div[1]/h2/a').text

            # Checking to see if username is correct
            print(username)

            # Check to see if we had previous interaction with a specific user
            if username not in prev_user_list:
                if webdriver.find_element_by_xpath('/html/body/div[3]/div[2]/div/article/header/div[2]/div[1]/div[2]/button').text == 'Follow':

                    # Following users
                    button_follow = webdriver.find_element_by_xpath('/html/body/div[3]/div[2]/div/article/header/div[2]/div[1]/div[2]/button')
                    button_follow.click()

                    new_followed.append(username)
                    followed += 1

                    # Liking posts
                    button_like = webdriver.find_element_by_xpath('/html/body/div[3]/div[2]/div/article/div[2]/section[1]/span[1]/button/span')

                    button_like.click()
                    likes += 1
                    sleep(randint(9, 15))

                    # Comments and tracker
                    comm_prob = randint(1, 10)
                    print('{}_{}: {}'.format(hashtag, x, comm_prob))
                    if comm_prob > 7:
                        comments += 1
                        webdriver.find_element_by_xpath('/html/body/div[3]/div[2]/div/article/div[2]/section[1]/span[2]/button/span').click()
                        comment_box = webdriver.find_element_by_xpath('/html/body/div[3]/div[2]/div/article/div[2]/section[3]/div/form/textarea')

                        if (comm_prob < 7):
                            comment_box.send_keys('That\'s totally rad! Love it!') # replace with your own comment
                            sleep(1)
                        elif (comm_prob > 6) and (comm_prob < 9): # replace with your own comment
                            comment_box.send_keys('Love your profile. Let\'s follow each other!')
                            sleep(1)
                        elif comm_prob == 9:
                            comment_box.send_keys('That\'s aMaZiNg!') # replace with your own comment
                            sleep(1)
                        elif comm_prob == 10:
                            comment_box.send_keys('UwU means unhappy without you. Please follow me!') # replace with your own comment
                            sleep(1)
                        # Using python to press enter for us to post comments
                        comment_box.send_keys(Keys.ENTER)
                        sleep(randint(16, 23))

                # Next picture button
                webdriver.find_element_by_link_text('Next').click()
                sleep(randint(13, 19))
            else:
                webdriver.find_element_by_link_text('Next').click()
                sleep(randint(1, 5))

    # If the browser stops refreshing photos, it will move onto the next item in hashtag_list
    except:
        continue

# Append the list of users followed to the existing .txt file
with open('followedlist.txt', 'a+') as followedlist:
    for username in new_followed:
        followedlist.write(username + ',')

print('Liked {} photos.'.format(likes))
print('Commented {} photos.'.format(comments))
print('Followed {} new people.'.format(followed))
