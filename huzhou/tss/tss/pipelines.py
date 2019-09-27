# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import re
import jieba
import pandas as pd
import numpy
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from os import path
import numpy as np
from PIL import Image


class TssPipeline(object):
    commons = ''

    def process_item(self, item, spider):
        print('print item')
        common = item['item']['commons']
        self.sum_commons(common)
        print(self.commons)
        self.make_wordclouds(self.commons)
        return item

    def data_clear(self, commons):
        pattern = re.compile(r'[\u4e00-\u9fa5]+')
        file_data = re.findall(pattern, commons)
        file_data = ''.join(file_data)
        clear = jieba.lcut(file_data)  # 切分词
        cleared = pd.DataFrame({'clear': clear})
        stopwords = pd.read_csv("C:/Users/27438/PycharmProjects/huzhou/tss/asset/chineseStopWords.txt", index_col=False,
                                quoting=3, sep="\t", names=['stopword'], encoding='GBK')
        cleared = cleared[~cleared.clear.isin(stopwords.stopword)]
        count_words = cleared.groupby(by=['clear'])['clear'].agg({"num": numpy.size})
        count_words = count_words.reset_index().sort_values(by=["num"], ascending=False)
        return count_words

    def make_wordclouds(self, commons):
        d = path.dirname(__file__)
        msk = np.array(Image.open(path.join(d, "C:/Users/27438/PycharmProjects/huzhou/tss/asset/me.jpg")))
        wordcloud = WordCloud(font_path="simhei.ttf", background_color="#DDDDDD", max_font_size=250,
                              width=1920, height=1080, mask=msk)  # 指定字体类型、字体大小和字体颜色
        word_frequence = {x[0]: x[1] for x in self.data_clear(commons).head(200).values}
        wordcloud = wordcloud.fit_words(word_frequence)
        plt.imshow(wordcloud)
        plt.axis("off")
        plt.show()

    def sum_commons(self, common):
        self.commons += common

    def write_document(self, common):
        file = r'tss/asset/commons'
        with open(file, 'a+') as f:
            f.write('x')
        return 'success'
