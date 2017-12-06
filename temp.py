
from urllib import request
resp = request.urlopen('https://movie.douban.com/cinema/nowplaying/hangzhou/')
html_data = resp.read().decode('utf-8')
print(html_data)

from bs4 import BeautifulSoup as bs
soup = bs(html_data,'html.parser')
nowplaying_movie = soup.find_all('div',id='nowplaying')
nowplaying_movie_list = nowplaying_movie[0].find_all('li',class_='list-item')
nowplaying_list = [] 
for item in nowplaying_movie_list:        
        nowplaying_dict = {}        
        nowplaying_dict['id'] = item['data-subject']       
        for tag_img_item in item.find_all('img'):            
            nowplaying_dict['name'] = tag_img_item['alt']            
            nowplaying_list.append(nowplaying_dict)
requrl = 'https://movie.douban.com/subject/' + nowplaying_list[0]['id'] + '/comments' +'?' +'start=0' + '&limit=20' 
resp = request.urlopen(requrl) 
html_data = resp.read().decode('utf-8') 
soup = bs(html_data, 'html.parser') 
comment_div_lits = soup.find_all('div', class_='comment')
eachCommentList = []; 
for item in comment_div_lits: 
    if item.find_all('p')[0].string is not None:     
       eachCommentList.append(item.find_all('p')[0].string)

comments = ''

for k in range(len(eachCommentList)):
    comments = comments + (str(eachCommentList[k])).strip()
print(comments)
import re

pattern = re.compile(r'[\u4e00-\u9fa5]+')
filterdata = re.findall(pattern, comments)
cleaned_comments = ''.join(filterdata)
import jieba    #分词包
import pandas as pd  

segment = jieba.lcut(cleaned_comments)
words_df=pd.DataFrame({'segment':segment})
stopwords=pd.read_csv("stopwords.txt",index_col=False,quoting=3,sep="\n",names=['stopword'], encoding='utf-8')#quoting=3全不引用
words_df=words_df[~words_df.segment.isin(stopwords.stopword)]
#print(words_df)

import numpy    #numpy计算包
words_stat=words_df.groupby(by=['segment'])['segment'].agg({"计数":numpy.size})
words_stat=words_stat.reset_index().sort_values(by=["计数"],ascending=False)
print(words_stat)
import matplotlib.pyplot as plt
from IPython import get_ipython
get_ipython().run_line_magic('matplotlib', 'inline')
import matplotlib
matplotlib.rcParams['figure.figsize'] = (10.0, 5.0)
from wordcloud import WordCloud#词云包
#
wordcloud=WordCloud(font_path="TTTongSongJ.ttf",background_color="white",max_font_size=80,scale=10) #指定字体类型、字体大小和字体颜色
word_frequence = {x[0]:x[1] for x in words_stat.head(1000).values}
word_frequence_list = []
for key in word_frequence:
    temp = (key,word_frequence[key])
    word_frequence_list.append(temp)
#
wordcloud=wordcloud.fit_words(word_frequence)
#wordcloud=wordcloud.fit_words(word_frequence_list)
plt.imshow(wordcloud)
plt.savefig('D:/project/py project/temp.jpg',dpi=800)      #dpi和scale对于清晰度有很大影响
#wordcloud.to_file('D:/project/temp1.jpg')
