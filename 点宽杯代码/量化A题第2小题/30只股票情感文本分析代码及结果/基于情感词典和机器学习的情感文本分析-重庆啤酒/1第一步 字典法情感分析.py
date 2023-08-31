import time

import jieba
import csv
import pandas as pd


class Result(object):
    def __init__(self, score, score_words, not_word, degree_word):
        self.score = score
        self.score_words = score_words
        self.not_word = not_word
        self.degree_word = degree_word


class Score(object):
    # 加载否定词
    negative_word_path = '字典、停止词、否定词、程度副词、用户字典/negative_words.txt'
    not_dict = []
    with open(negative_word_path, 'r', encoding='utf8') as f:
        for line in f:
            line = line.strip()
            not_dict.append(line)
    not_dict = set(not_dict)

    def __init__(self, sentiment_dict_path, degree_dict_path, stop_dict_path):
        self.sentiment_dict = self.load_sentiment_dict(sentiment_dict_path)
        self.degree_dict = self.load_degree_dict(degree_dict_path)
        self.stop_words = self.load_stop_words(stop_dict_path)

    def load_stop_words(self, stop_dict_path):
        stop_words = [w for w in open(stop_dict_path, encoding='UTF-8').readlines()]
        return stop_words

    def remove_stopword(self, words):
        words = [w for w in words if w not in self.stop_words]
        return words

    def load_degree_dict(self, dict_path):
        degree_dict = {}
        with open(dict_path, 'r', encoding='UTF-8') as f:
            for line in f:
                line = line.strip()
                word, degree = line.split('\t')
                degree = float(degree)
                degree_dict[word] = degree
        return degree_dict

    def load_sentiment_dict(self, dict_path):
        sentiment_dict = {}
        dic = pd.read_excel(dict_path)
        for index, line in enumerate(dic.values):
            items = line.tolist()
            word = items[0]  # 单词
            intensity = items[1]  # 程序设计竞赛专题挑战教程, 3, 5, 7, 9五档, 9表示强度最大, 1为强度最小.
            polar = items[2]  # 极性
            intensity = int(intensity)
            polar = int(polar)

            # 转换情感倾向的表现形式, 负数为消极, 0 为中性, 正数为积极
            # 数值绝对值大小表示极性的强度——分成3类，极性：褒(+程序设计竞赛专题挑战教程)、中(0)、贬(-程序设计竞赛专题挑战教程)； 强度为权重值
            value = None  # 极性为3、7的赋情感值none，忽略他并不影响总体情感
            if polar == 0:  # neutral
                value = 0
            elif polar == 1:  # positive
                value = intensity
            elif polar == 2 or polar == -1:  # negtive
                value = -1 * intensity
            else:  # invalid
                continue

            key = word
            sentiment_dict[key] = value
        return sentiment_dict

    def classify_words(self, words):
        # 这3个键是词的序号(索引)
        sen_word = {}
        not_word = {}
        degree_word = {}
        # 找到对应的sent, not, degree;  words 是分词后的列表
        for index, word in enumerate(words):
            if word in self.sentiment_dict and word not in self.__class__.not_dict and word not in self.degree_dict:
                sen_word[index] = self.sentiment_dict[word]
            elif word in self.__class__.not_dict and word not in self.degree_dict:
                not_word[index] = -1
            elif word in self.degree_dict:
                degree_word[index] = self.degree_dict[word]
        return sen_word, not_word, degree_word

    def get_score_position(self, words):
        sen_word, not_word, degree_word = self.classify_words(words)  # 是字典

        score = 0
        start = 0
        # 存所有情感词、否定词、程度副词的位置(索引、序号)的列表
        sen_locs = sen_word.keys()
        not_locs = not_word.keys()
        degree_locs = degree_word.keys()
        senloc = -1
        # 遍历句子中所有的单词words，i为单词的绝对位置
        for i in range(0, len(words)):
            if i in sen_locs:
                W = 1  # 情感词间权重重置
                not_locs_index = 0
                degree_locs_index = 0

                # senloc为情感词位置列表的序号,之前的sen_locs是情感词再分词后列表中的位置序号
                senloc += 1
                # score += W * float(sen_word[i])
                if senloc == 0:  # 第一个情感词,前面是否有否定词，程度词
                    start = 0
                elif senloc < len(sen_locs):  # 和前面一个情感词之间，是否有否定词,程度词
                    # j为绝对位置
                    start = previous_sen_locs

                for j in range(start, i):  # 词间的相对位置
                    # 如果有否定词
                    if j in not_locs:
                        W *= -1
                        not_locs_index = j
                    # 如果有程度副词
                    elif j in degree_locs:
                        W *= degree_word[j]
                        degree_locs_index = j

                    # 判断否定词和程度词的位置：程序设计竞赛专题挑战教程）否定词在前，程度词减半(加上正值)(双重否定要减去？)；不是很   2）否定词在后，程度增强（不变），很不是
                if (not_locs_index > 0) and (degree_locs_index > 0):
                    if not_locs_index < degree_locs_index:
                        degree_reduce = (float(degree_word[degree_locs_index] / 2))
                        if W > 0:
                            W -= degree_reduce
                        elif W < 0:
                            W += degree_reduce
                        # print (W)
                score += W * float(sen_word[i])  # 直接添加该情感词分数
                previous_sen_locs = i
        return score


if __name__ == '__main__':
    start_time = time.time()
    print('------开始进行字典法情感分析\n')
    sentiment_dict_path = "字典、停止词、否定词、程度副词、用户字典/大连理工情感词汇简易拓展.xlsx"
    degree_dict_path = "字典、停止词、否定词、程度副词、用户字典/degree_dict.txt"
    stop_dict_path = "字典、停止词、否定词、程度副词、用户字典/stop_words.txt"

    # 文件读取
    print('------开始读取股吧文本数据')

    # 此处加载要分析的文本数据 #
    # -------------------------------------------------------------------------------------------------
    f = open('重庆啤酒.csv', encoding='utf8')
    data = pd.read_csv(f)
    print('------股吧文本数据读取完毕\n')
    # -------------------------------------------------------------------------------------------------

    # 文件写入
    c = open("情感分析中间数据集/字典法情感分析初步结果.csv", "a+", newline='', encoding='utf-8-sig')
    writer = csv.writer(c)
    writer.writerow(["time", "no", "review", "score", "read_volume"])

    # 分句功能 否定词程度词位置判断
    print('------开始对文本数据进行分词、打分')
    score = Score(sentiment_dict_path, degree_dict_path, stop_dict_path)
    n = 1
    for temp in data['review']:
        tlist = []
        jieba.load_userdict('字典、停止词、否定词、程度副词、用户字典/user_dict.txt')
        words = [x for x in jieba.cut(temp)]  # 分词
        words_ = score.remove_stopword(words)
        result = score.get_score_position(words_)
        tlist.append(data['time'][n - 1])
        tlist.append(str(n))
        tlist.append(words)
        tlist.append(str(result))
        tlist.append(data['read_volume'][n-1])
        writer.writerow(tlist)
        print('------正在操作第 {} 行数据'.format(n))
        n = n + 1

    print('------文本数据分词、打分完毕\n')
    print('------字典法情感分析完毕\n')
    end_time = time.time()
    print('本程序运行时间 {:.2f} s.'.format(end_time - start_time))
    c.close()
