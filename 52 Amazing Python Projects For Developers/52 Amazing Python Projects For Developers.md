# 52 Amazing Python Projects For Developers

## 1. LinkedIn Email Scraper  

### Prerequisites:

1. Do `pip install -r requirements.txt` to make sure you have the necessary libraries.
2. Make sure you have a **chromedriver** installed and added to PATH.
3. Have the **URL** to your desired LinkedIn post ready (*make sure the post has some emails in the comments
section*)
4. Have your **LinkedIn** account credentials ready
### Executing Application
1. Replace the values of the URL, email and password variables in the code with your own data
2. Either hit **run** if your IDE has the option or just type in `python main.py` in the terminal.
3. The names and corresponding email address scraped from the post should appear in the **emails.csv** file.

### Requirements:

```
selenium
email-validator
```

### Source Code:  

```python
from selenium import webdriver
from selenium.webdriver.common.by import By
from email_validator import validate_email, EmailNotValidError
import csv
import os

def LinkedInEmailScraper(userEmail, userPassword):
    """
    使用 Selenium 登录 LinkedIn 帐号，访问指定帖子并抓取评论中的邮箱地址
    """
    emailList = {}  # 用于存储姓名和邮箱
    browser = webdriver.Chrome()

    # LinkedIn 帖子的链接（请替换为目标帖子链接）
    url = '[INSERT URL TO LINKEDIN POST]'
    browser.get(url)
    browser.implicitly_wait(5)  # 等待页面加载

    # 找到“查看评论”按钮并获取登录链接
    commentDiv = browser.find_element(By.XPATH, '/html/body/main/section[1]/section[1]/div/div[3]/a[2]')
    loginLink = commentDiv.get_attribute('href')
    browser.get(loginLink)

    # 填写用户名和密码，提交登录表单
    email = browser.find_element(By.XPATH, '//*[@id="username"]')
    password = browser.find_element(By.XPATH, '//*[@id="password"]')
    email.send_keys(userEmail)
    password.send_keys(userPassword)

    submit = browser.find_element(By.XPATH, '//*[@id="app__container"]/main/div[3]/form/div[3]/button')
    submit.click()
    browser.implicitly_wait(5)

    # 找到评论区的 HTML 元素
    commentSection = browser.find_element(By.CSS_SELECTOR, '.comments-comments-list')

    # 尝试展开更多评论（可自行修改循环次数）
    for _ in range(3):
        try:
            moreCommentsButton = commentSection.find_element(By.CLASS_NAME, 'comments-comments-list__show-previous-container') \
                                               .find_element(By.TAG_NAME, 'button')
            moreCommentsButton.click()
            browser.implicitly_wait(5)
        except Exception:
            print('已加载所有可见评论')
            break

    # 获取所有评论元素
    comments = commentSection.find_elements(By.TAG_NAME, 'article')

    for comment in comments:
        try:
            # 获取评论者名字
            commenterName = comment.find_element(By.CLASS_NAME, 'hoverable-link-text')

            # 获取评论内容
            commentText = comment.find_element(By.TAG_NAME, 'p')

            # 获取评论中的邮箱链接（假设评论中包含 <a> 标签且为邮箱）
            commenterEmail = commentText.find_element(By.TAG_NAME, 'a').get_attribute('innerHTML')

            # 校验邮箱格式合法性
            validEmail = validate_email(commenterEmail)
            commenterEmail = validEmail.email

            # 将姓名和邮箱加入字典
            emailList[commenterName.get_attribute('innerHTML')] = commenterEmail
        except Exception:
            continue

    browser.quit()
    return emailList


def DictToCSV(input_dict):
    """
    将字典写入 CSV 文件
    """
    os.makedirs('./LinkedIn Email Scraper', exist_ok=True)
    with open('./LinkedIn Email Scraper/emails.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['name', 'email'])
        for key, value in input_dict.items():
            writer.writerow([key, value])


if __name__ == '__main__':
    # 请将下面的登录凭证替换为你的 LinkedIn 帐号和密码
    userEmail = '[INSERT YOUR EMAIL ADDRESS FOR LINKEDIN ACCOUNT]'
    userPassword = '[INSERT YOUR PASSWORD FOR LINKEDIN ACCOUNT]'

    # 抓取评论中的邮箱地址
    emailList = LinkedInEmailScraper(userEmail, userPassword)

    # 输出结果为 CSV
    DictToCSV(emailList)
```



## 2. Cricbuzz scrapper  

This python script will scrap cricbuzz.com to get live scores of the matches.  
### Setup
* Install the dependencies
`pip install -r requirements.txt`
* Run the file
`python live_score.py`

### Requirement:

```
beautifulsoup4==4.9.3
bs4==0.0.1
pypiwin32==223
pywin32==228
soupsieve==2.0.1
urllib3==1.26.5
win10toast==0.9
```

### Source Code:  

```python
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
from win10toast import ToastNotifier
import time

# 要抓取的比赛比分页面
URL = 'http://www.cricbuzz.com/cricket-match/live-scores'

def notify(title, score):
    """
    在 Windows 桌面上弹出比分通知
    """
    toaster = ToastNotifier()
    toaster.show_toast(
        "CRICKET LIVE SCORE",     # 通知标题
        f"{title} - {score}",     # 通知内容
        duration=30,              # 显示时间（秒）
        icon_path='ipl.ico'       # 图标路径（确保文件存在）
    )

# 无限循环，每隔一段时间抓取一次比分信息
while True:
    try:
        # 向服务器发送请求，模拟浏览器访问（防止被拒绝）
        request = Request(URL, headers={'User-Agent': 'XYZ/3.0'})
        response = urlopen(request, timeout=20).read()

        # 使用 BeautifulSoup 解析 HTML 页面
        soup = BeautifulSoup(response, 'html.parser')

        # 查找比分信息
        for score_block in soup.find_all(
            'div',
            attrs={'class': 'cb-col cb-col-100 cb-plyr-tbody cb-rank-hdr cb-lv-main'}
        ):
            # 提取比赛标题（如 "MI vs CSK"）
            header_div = score_block.find('div', attrs={'class': 'cb-col-100 cb-col cb-schdl'})
            if header_div:
                header = header_div.text.strip()
            else:
                continue

            # 提取比赛比分状态（如 "MI 145/4 (18.2)"）
            status_div = score_block.find('div', attrs={'class': 'cb-scr-wll-chvrn cb-lv-scrs-col'})
            if status_div:
                status = status_div.text.strip()
                notify(header, status)  # 弹出通知

        time.sleep(10)  # 等待10秒后再次抓取

    except Exception as e:
        print(f"发生错误: {e}")
        time.sleep(30)  # 出错时等待30秒再试
```



## 3. Lyrics Download  

This script can be used to download lyrics of any number of songs, by any number of Artists, until the API Limit is met.
The script uses [Genius API] (https://docs.genius.com/). It is a dedicated platform meant for music only.  

### Setup Instruction
- You need an API client, (it's free) follow the steps [here](https://docs.genius.com/).
- `pip install lyricsgenius` to install dedicated package.
- Good to go, follow guidelines mentioned as comments in code.
- The script is pretty much interactive, ensure you follow the guidelines.

### Source Code:  

```python
import lyricsgenius as lg

# 获取用户输入的文件名，若为空则默认使用 'Lyrics.txt'
filename = input('Enter a filename: ') or 'Lyrics.txt'
file = open(filename, "w+", encoding="utf-8")

# 创建 Genius API 实例（需要替换 Access Token）
genius = lg.Genius(
    'Client_Access_Token_Goes_Here',  # <-- 替换为你自己的 Genius API token
    skip_non_songs=True,              # 跳过非歌曲（如采访等）
    excluded_terms=["(Remix)", "(Live)"],  # 排除包含这些词的歌曲标题
    remove_section_headers=True       # 保留歌词段落标题，如 [Chorus]
)

# 用户输入多个艺术家名字（以空格分隔）
input_string = input("Enter name of Artists separated by spaces: ")
artists = input_string.split(" ")

def get_lyrics(artist_list, max_songs):
    """
    抓取每位艺术家的最多 max_songs 首热门歌曲，并写入歌词文件。
    
    参数:
    artist_list : list[str] - 艺术家名称列表
    max_songs : int - 每位艺术家要抓取的最大歌曲数量
    """
    count = 0  # 成功抓取的艺术家计数器

    for name in artist_list:
        try:
            # 搜索艺术家及其热门歌曲
            artist = genius.search_artist(name, max_songs=max_songs, sort='popularity')
            if artist is None:
                print(f"No songs found for {name}")
                continue

            # 提取歌词并写入文件
            lyrics_list = [song.lyrics for song in artist.songs]
            file.write("\n\n<|endoftext|>\n\n".join(lyrics_list))  # 自定义分隔符
            file.write("\n\n<|artist-end|>\n\n")  # 用于标记该艺术家的结束
            print(f"Songs grabbed for {name}: {len(lyrics_list)}")
            count += 1
        except Exception as e:
            print(f"Exception occurred while processing {name}: {e}")

    print(f"Finished grabbing lyrics for {count} artists.")

# 调用函数抓取每位艺术家的 3 首歌曲
get_lyrics(artists, 3)

# 关闭文件
file.close()
```



## 4. Merge CSV files  

With the help of the following simple python script, one would be able to merge CSV files present in the directory.  
### Dependencies
Requires Python 3 and `pandas`
Install requirements: `pip install -r "requirements.txt"`
OR
Install pandas: `pip install pandas`

### How to use
#### Running
Put all the CSVs which are to be merged in a directory containing the script.
Either run it from your code editor or IDE or type `python merge_csv_files.py` in your command line.
The final output would be a `combined_csv.csv` file in the same directory.

### Requirements:
```
pandas==1.1.0
```

### Source Code:  

```python
import glob
import pandas as pd

# 设置目标文件的扩展名（这里是 CSV）
extension = 'csv'

# 使用 glob 模块查找当前目录下所有 CSV 文件
all_filenames = [i for i in glob.glob(f'*.{extension}')]

# 使用 pandas 读取每个 CSV 文件并合并为一个 DataFrame
combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames])

# 将合并后的 DataFrame 写入一个新的 CSV 文件
combined_csv.to_csv("combined_csv.csv", index=False, encoding='utf-8-sig')
```



## 5. Merge pdfs

A simple python script which when executed merges two pdfs.
### Prerequisites
Run - "pip install PyPDF2"
### How to run the script
It can be executed by running "python merge_pdfs.py"

### Requirements:
```
PyPDF2==1.26.0
```

 ### Source Code:   

```python
#!/usr/bin/env python
from PyPDF2 import PdfFileMerger

# By appending in the end
def by_appending():
    """
    将多个 PDF 文件合并为一个文件，按顺序添加每个 PDF 文件。
    """
    # 创建一个 PdfFileMerger 实例
    merger = PdfFileMerger()
    
    # 通过文件流提供第一个 PDF 文件
    with open("samplePdf1.pdf", "rb") as f1:
        merger.append(f1)
    
    # 直接通过文件路径添加第二个 PDF 文件
    merger.append("samplePdf2.pdf")
    
    # 写入合并后的 PDF 文件
    merger.write("mergedPdf.pdf")
    print("Merged PDFs by appending into 'mergedPdf.pdf'.")

# By inserting at a specific page number
def by_inserting():
    """
    将第二个 PDF 文件插入到第一个 PDF 文件的特定页面后。
    """
    # 创建一个 PdfFileMerger 实例
    merger = PdfFileMerger()
    
    # 先将第一个 PDF 文件添加到合并器
    merger.append("samplePdf1.pdf")
    
    # 在指定页码后插入第二个 PDF 文件，这里将其插入到第 0 页后
    merger.merge(0, "samplePdf2.pdf")
    
    # 写入合并后的 PDF 文件
    merger.write("mergedPdf1.pdf")
    print("Merged PDFs by inserting into 'mergedPdf1.pdf'.")

# 主程序
if __name__ == "__main__":
    # 合并 PDF 文件，按顺序附加
    by_appending()
    
    # 合并 PDF 文件，通过插入
    by_inserting()
```



## 6. Message Spam Detection  

Short description of package/script  
- Libraries Used:
  - pandas
  - string
  - re
  - nltk
  - sklearn
  - pickle
- The python code contains script for message spam detection based on Kaggle Dataset (dataset link inside the
code)
### Setup instructions
- Download the code
- Download the dataset
- Run the cells in the notebook
### Detailed explanation of script, if needed
NA
### Output
- Hello, I am James Bond: Not Spam
- Winner! Winner! Winner! Congrats! Call at xyz or email us at to claim your prize! Limited Time Offer!: Spam

### Message Spam Detection Source Code:  

```python
# Importing required libraries
import pandas as pd
import string
import nltk
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.ensemble import RandomForestClassifier
import pickle
import warnings
import re

# Ignore warnings
warnings.filterwarnings("ignore")

# Reading the dataset
msg = pd.read_csv("./Message_Spam_Detection/Cleaned_Dataset.csv", encoding='latin-1')

# Dropping the unnecessary 'Unnamed' column
msg.drop(['Unnamed: 0'], axis=1, inplace=True)

# Separating the target variable (label) and features
y = pd.DataFrame(msg.label)  # Target variable
x = msg.drop(['label'], axis=1)  # Features

# CountVectorization to convert text data into numerical format
cv = CountVectorizer(max_features=5000)
temp1 = cv.fit_transform(x['final_text'].values.astype('U')).toarray()

# TF-IDF Transformation to scale the term frequencies
tf = TfidfTransformer()
temp1 = tf.fit_transform(temp1)
temp1 = pd.DataFrame(temp1.toarray(), index=x.index)

# Concatenate the TF-IDF transformed data to the original features
x = pd.concat([x, temp1], axis=1, sort=False)

# Drop the 'final_text' column as it is no longer needed
x.drop(['final_text'], axis=1, inplace=True)

# Converting target variable 'y' to integer datatype
y = y.astype(int)

# Building and training the RandomForestClassifier model
model = RandomForestClassifier(n_estimators=100, random_state=0)
model.fit(x, y)

# User input for spam detection
text = input("Enter text: ")

# Data cleaning/preprocessing - removing punctuation and digits
updated_text = ''
for i in range(len(text)):
    if text[i] not in string.punctuation and not text[i].isdigit():
        updated_text = updated_text + text[i]

# Assign the cleaned text back to 'text'
text = updated_text

# Data cleaning/preprocessing - Tokenization and converting to lowercase
text = re.split("\W+", text.lower())

# Data cleaning/preprocessing - Removing stopwords
updated_list = []
stopwords = nltk.corpus.stopwords.words('english')
for word in text:
    if word not in stopwords:
        updated_list.append(word)

# Data cleaning/preprocessing - Lemmatization
wordlem = nltk.WordNetLemmatizer()
text = [wordlem.lemmatize(word) for word in updated_list]

# Merging the tokens back into a string
text = " ".join(text)

# Transform the text to the feature vector space (same as training data)
text = cv.transform([text])
text = tf.transform(text)

# Predicting the class (spam or not spam)
pred = model.predict(text)

# Output the result
if pred == 0:
    print("Not Spam")
else:
    print("Spam")
```



### Data Cleaning Source Code:  

```python
# Importing required libraries
import pandas as pd
import string
import nltk
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.ensemble import RandomForestClassifier
import pickle
import warnings
import re

# Suppress warnings
warnings.filterwarnings("ignore")

# Download necessary NLTK resources
nltk.download('stopwords')
nltk.download('wordnet')

# Reading the dataset (source: https://www.kaggle.com/uciml/sms-spam-collection-dataset)
msg = pd.read_csv("./Message_Spam_Detection/dataset.csv", encoding='latin-1')

# Dropping unnecessary columns
msg.drop(['Unnamed: 2', 'Unnamed: 3', 'Unnamed: 4'], axis=1, inplace=True)

# Renaming columns for better clarity
msg.rename(columns={"v1": "label", "v2": "text"}, inplace=True)

# Mapping 'ham' to 0 and 'spam' to 1
for i in msg.index:
    if msg['label'][i] == 'ham':
        msg['label'][i] = 0
    else:
        msg['label'][i] = 1

# Dropping duplicate rows
msg = msg.drop_duplicates()

# Data cleaning/preprocessing - Removing punctuation and digits
msg['cleaned_text'] = ""
for i in msg.index:
    updated_list = []
    for j in range(len(msg['text'][i])):
        if msg['text'][i][j] not in string.punctuation:
            if msg['text'][i][j].isdigit() == False:
                updated_list.append(msg['text'][i][j])
    updated_string = "".join(updated_list)
    msg['cleaned_text'][i] = updated_string

# Dropping the original 'text' column as we have the cleaned version
msg.drop(['text'], axis=1, inplace=True)

# Data cleaning/preprocessing - Tokenization and converting to lower case
msg['token'] = ""
for i in msg.index:
    msg['token'][i] = re.split("\W+", msg['cleaned_text'][i].lower())

# Data cleaning/preprocessing - Removing stopwords
msg['updated_token'] = ""
stopwords = nltk.corpus.stopwords.words('english')
for i in msg.index:
    updated_list = []
    for j in range(len(msg['token'][i])):
        if msg['token'][i][j] not in stopwords:
            updated_list.append(msg['token'][i][j])
    msg['updated_token'][i] = updated_list

# Dropping the 'token' column as we now have the 'updated_token' column
msg.drop(['token'], axis=1, inplace=True)

# Data cleaning/preprocessing - Lemmatization
msg['lem_text'] = ""
wordlem = nltk.WordNetLemmatizer()
for i in msg.index:
    updated_list = []
    for j in range(len(msg['updated_token'][i])):
        updated_list.append(wordlem.lemmatize(msg['updated_token'][i][j]))
    msg['lem_text'][i] = updated_list

# Dropping the 'updated_token' column as we now have the 'lem_text' column
msg.drop(['updated_token'], axis=1, inplace=True)

# Data cleaning/preprocessing - Merging tokens into a final cleaned string
msg['final_text'] = ""
for i in msg.index:
    updated_string = " ".join(msg['lem_text'][i])
    msg['final_text'][i] = updated_string

# Dropping intermediate columns as we no longer need them
msg.drop(['cleaned_text', 'lem_text'], axis=1, inplace=True)

# Saving the cleaned dataset to a new CSV file
msg.to_csv('Cleaned_Dataset.csv', index=False)

# The dataset is now cleaned and saved as 'Cleaned_Dataset.csv'
```



## 7. Movie Information Scraper 

This script obtains movie details by scraping IMDB website.  

### Prerequisites
* beautifulsoup4
* requests
* Run `pip install -r requirements.txt` to install required external modules.
### How to run the script
Execute `python3 movieInfoScraper.py` and type in the movie name when prompted.

### Requirements:
```
beautifulsoup4
requests==2.23.0
```

### Source Code:  

```python
# Importing necessary libraries
import os
import zipfile
import sys
import argparse

# Setting up command-line argument parser
parser = argparse.ArgumentParser()
parser.add_argument("-l", "--zippedfile", required=True, help="Path to the zipped file")
args = vars(parser.parse_args())

# Catching the user-defined zip file
zip_file = args['zippedfile']
file_name = zip_file  # Storing the file name

# Check if the entered zip file is present in the directory
if not os.path.exists(zip_file):
    sys.exit("No such file present in the directory")

# Function to extract the zip file
def extract(zip_file):
    # Checking if the file is a zip file
    if zip_file.endswith(".zip"):
        # Splitting the zip file name to create a folder with the same name as the zip file (without extension)
        file_name = zip_file.split(".zip")[0]
        
        # Get the current working directory to save the unzipped file
        current_working_directory = os.getcwd()
        new_directory = os.path.join(current_working_directory, file_name)

        # Create the new directory if it doesn't exist
        if not os.path.exists(new_directory):
            os.makedirs(new_directory)

        # Logic to unzip the file
        with zipfile.ZipFile(zip_file, 'r') as zip_object:
            zip_object.extractall(new_directory)  # Extract all contents to the new directory
            print(f"Extracted successfully to: {new_directory}")
    else:
        print("Not a zip file")

# Calling the extract function
extract(zip_file)
```



## 8. Movie Info Telegram Bot  
### Description
A telegram Bot made using python which scrapes IMDb website and has the following functionalities
1. Replies to a movie name with genre and rating of the movie
2. Replies to a genre with a list of top movies and tv shows belonging to that genre
### Setup Instructions
1. Install required packages:
pip install -r requirements.txt
2. Create a bot in telegram:
1. Go to @BotFather and click /start and type /newbot and give it a name.
2. Choose a username and get the token
3. Paste the token in a .env file (Take [.env.example](.env.example) as an example)
4. Run the python script to start the bot
5. Type /start command to start conversation with the chatbot.
6. Type /name <movie_name> to get the genre and Rating of the movie. The bot replies with at most three results.
7. Type /genre \<genre> to get a list of movies and TV shows belonging to that genres

### Requirements:
```
APScheduler==3.6.3
beautifulsoup4==4.9.3
certifi==2020.12.5
python-dateutil==2.8.1
python-decouple==3.4
python-telegram-bot==13.1
pytz==2020.4
requests==2.25.1
six==1.15.0
soupsieve==2.1
tornado==6.1
urllib3==1.26.2
```

### Source Code:  

```python
import logging
import requests
import re
import urllib.request
import urllib.parse
import urllib.error
from bs4 import BeautifulSoup
import ssl
import itertools
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import decouple

# Enable logging for the bot activity
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Fetch the API token for the bot from environment variables
TOKEN = decouple.config("API_KEY")

# Define a few command handlers. These usually take the two arguments `update` and `context`.

def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text(
        'What can this bot do?\n\nThis bot gives brief information about any movie from IMDb website'
        + '\nSend /name movie_name to know the genre and rating of the movie.'
        + '\nSend /genre genre_name to get the list of movies belonging to that genre'
    )

def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')

def genre(update, context):
    """Send a list of movies of a specific genre when the command /genre is issued."""
    url = 'https://www.imdb.com/search/title/'
    genre = str(update.message.text)[7:]  # Extract the genre from the message
    print(genre)
    r = requests.get(url + '?genres=' + genre)
    soup = BeautifulSoup(r.text, "html.parser")
    title = soup.find('title')

    if title.string == 'IMDb: Advanced Title Search - IMDb':
        update.message.reply_text("Sorry, No such genre. Try again")
    else:
        res = []
        res.append(title.string + '\n')
        tags = soup('a')
        for tag in tags:
            movie = re.search('<a href=\"/title/.*>(.*?)</a>', str(tag))
            try:
                if "&amp;" in movie.group(1):
                    movie.group(1).replace("&amp;", "&")
                res.append(movie.group(1))
            except:
                pass
        stri = ""
        for i in res:
            stri += i + '\n'
        update.message.reply_text(stri)

def name(update, context):
    """Send the genre and rating of the movie when the command /name is issued."""
    movie = str(update.message.text)[6:]  # Extract the movie name from the message
    print(movie)
    res = get_info(movie)  # Call get_info function to fetch the movie data
    stri = ""
    for i in res:
        for a in i:
            stri += a + '\n'
        stri += '\n'
    update.message.reply_text(stri)

def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def get_info(movie):
    """Scrape IMDb and get the genre and rating of the movie."""
    url = 'https://www.imdb.com/find?q='
    r = requests.get(url + movie + '&ref_=nv_sr_sm')
    soup = BeautifulSoup(r.text, "html.parser")
    title = soup.find('title')
    tags = soup('a')

    pre_url = ""
    count = 0
    lis = []
    res = []

    for tag in tags:
        if count > 2:
            break
        m = re.search('<a href=.*>(.*?)</a>', str(tag))
        try:
            lis = []
            link = re.search('/title/(.*?)/', str(m))
            new_url = 'https://www.imdb.com' + str(link.group(0))

            if new_url != pre_url:
                html = requests.get(new_url)
                soup2 = BeautifulSoup(html.text, "html.parser")
                movietitle = soup2.find('title').string.replace('- IMDb', ' ')
                a = soup2('a')
                span = soup2('director')

                genrestring = "Genre : "
                for j in a:
                    genre = re.search('<a href=\"/search/title\?genres=.*> (.*?)</a>', str(j))
                    try:
                        genrestring += genre.group(1) + ' '
                    except:
                        pass

                atag = soup2('strong')
                for i in atag:
                    rating = re.search('<strong title=\"(.*?) based', str(i))
                    try:
                        rstring = "IMDb Rating : " + rating.group(1)
                    except:
                        pass

                details = "For more details : " + new_url
                lis.append(movietitle)
                lis.append(genrestring)
                lis.append(rstring)
                lis.append(details)
                pre_url = new_url
                count += 1
            res.append(lis)
        except:
            pass
    return res

def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token
    updater = Updater(TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Register command handlers for different commands
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("name", name))
    dp.add_handler(CommandHandler("genre", genre))

    # Log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT, SIGTERM, or SIGABRT
    updater.idle()

if __name__ == '__main__':
    main()
```



## 9. snapshot of given website  
### Set up
`pip install selenium`
`pip install chromedriver-binary==XX.X.XXXX.XX.X`
- 'XX.X.XXXX.XX.X' is chrome driver version.
- The version of 'chrome driver' need to match the version of your google chrome.

**How to find your google chrome version**

1. Click on the Menu icon in the upper right corner of the screen.
2. Click on Help, and then About Google Chrome.
3. Your Chrome browser version number can be found here.
### Execute
`python snapshot_of_given_website.py <url>`
Snapshot is in current directory after this script runs.

### Requirements:
```
selenium==3.141.0
chromedriver-binary==85.0.4183.38.0
```

### Source Code:  

```python
# -*- coding: utf-8 -*-
import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import chromedriver_binary  # This imports the necessary binary for chromedriver

# Get the script name (file name) from command line arguments
script_name = sys.argv[0]

# Set up Chrome options to run in headless mode (without a GUI)
options = Options()
options.add_argument('--headless')

# Initialize the Chrome WebDriver with the specified options
driver = webdriver.Chrome(options=options)

try:
    # Get the URL from the command line argument
    url = sys.argv[1]
    
    # Open the URL in the browser
    driver.get(url)

    # Get the width and height of the page using JavaScript
    page_width = driver.execute_script('return document.body.scrollWidth')
    page_height = driver.execute_script('return document.body.scrollHeight')

    # Set the browser window size to match the full page size
    driver.set_window_size(page_width, page_height)

    # Take a screenshot of the page and save it as 'screenshot.png'
    driver.save_screenshot('screenshot.png')

    # Close the browser
    driver.quit()

    print("SUCCESS")  # Indicate success in capturing the screenshot

except IndexError:
    # Handle the case when the URL is not provided as a command line argument
    print('Usage: %s URL' % script_name)
```



## 10. Music Player with Python  

以下是格式化后的 Python 代码，并加上了必要的注释，便于理解和运行：

```python
import pygame
import tkinter as tkr
from tkinter.filedialog import askdirectory
import os

# 初始化 tkinter 窗口
music_player = tkr.Tk()
music_player.title("My Music Player")
music_player.geometry("450x350")

# 弹出文件选择对话框，选择音乐文件所在目录
directory = askdirectory()
os.chdir(directory)  # 切换到选定的目录

# 获取目录中的所有文件
song_list = os.listdir()

# 创建 Listbox 显示歌曲列表
play_list = tkr.Listbox(music_player, font="Helvetica 12 bold", bg='yellow', selectmode=tkr.SINGLE)
for item in song_list:
    play_list.insert(tkr.END, item)  # 将每个歌曲添加到列表框中

# 初始化 pygame 和 pygame.mixer
pygame.init()
pygame.mixer.init()

# 定义播放音乐的函数
def play():
    # 加载选中的歌曲并播放
    pygame.mixer.music.load(play_list.get(tkr.ACTIVE))  # 获取当前选择的歌曲
    var.set(play_list.get(tkr.ACTIVE))  # 更新歌曲标题
    pygame.mixer.music.play()  # 播放音乐

# 定义停止音乐的函数
def stop():
    pygame.mixer.music.stop()

# 定义暂停音乐的函数
def pause():
    pygame.mixer.music.pause()

# 定义恢复播放音乐的函数
def unpause():
    pygame.mixer.music.unpause()

# 创建控制按钮
Button1 = tkr.Button(music_player, width=5, height=3, font="Helvetica 12 bold", text="PLAY", command=play, bg="blue", fg="white")
Button2 = tkr.Button(music_player, width=5, height=3, font="Helvetica 12 bold", text="STOP", command=stop, bg="red", fg="white")
Button3 = tkr.Button(music_player, width=5, height=3, font="Helvetica 12 bold", text="PAUSE", command=pause, bg="purple", fg="white")
Button4 = tkr.Button(music_player, width=5, height=3, font="Helvetica 12 bold", text="UNPAUSE", command=unpause, bg="orange", fg="white")

# 创建显示当前播放歌曲标题的标签
var = tkr.StringVar()
song_title = tkr.Label(music_player, font="Helvetica 12 bold", textvariable=var)
song_title.pack()

# 布局按钮和歌曲列表
Button1.pack(fill="x")
Button2.pack(fill="x")
Button3.pack(fill="x")
Button4.pack(fill="x")
play_list.pack(fill="both", expand="yes")

# 启动 tkinter 主循环，显示音乐播放器窗口
music_player.mainloop()
```

### 代码说明：

1. **`pygame` 和 `tkinter`**：
   - `pygame` 用于处理音频的播放。
   - `tkinter` 用于创建图形化用户界面。
2. **`askdirectory()`**：
   - 弹出文件选择对话框，让用户选择包含音乐文件的文件夹。
3. **Listbox**：
   - 使用 `Listbox` 显示文件夹中的所有音乐文件，并让用户选择想要播放的歌曲。
4. **播放、暂停、停止、恢复播放**：
   - 定义了 4 个按钮，分别用于播放、暂停、停止和恢复播放当前选择的歌曲。
5. **`pygame.mixer`**：
   - 使用 `pygame.mixer` 模块加载和播放音乐，控制音频的暂停与恢复。

### 运行方法：

1. 确保已安装 `pygame` 和 `tkinter` 库。
   - 安装 `pygame`：`pip install pygame`
   - `tkinter` 通常与 Python 一起安装，但如果没有，可以通过安装 `tk` 来获得。
2. 运行代码时，程序会弹出文件选择框，用户可以选择包含音乐文件的目录。选择后，目录中的所有音乐文件将显示在列表框中。
3. 使用控制按钮来播放、停止、暂停或恢复播放所选的音乐。





