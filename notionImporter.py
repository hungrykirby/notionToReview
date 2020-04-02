import csv
import datetime
import glob
import os
import re

class NotionImporter:
    def __init__(self):
        pass

    def call(self):
        r = self.__date_sort()
        for _r in r:
            # print(_r)
            print(_r['datetime'].strftime('%Y-%m-%d') + ':' + ','.join(_r['reviewed']))

    def __date_sort(self):
        # return [[title => str, d => datetime, mothin => str], [], ... ]
        results = self.__analyze_md_files()
        results_sorted = sorted(results, key=lambda r: r['datetime'])
        return results_sorted

    def __md_files(self):
        path_to_md = os.path.join(os.path.abspath(os.path.dirname(__file__)), "md")
        md_files = glob.glob(os.path.join(path_to_md, '*.md'))
        return md_files

    def __analyze_md_files(self):
        md_files = self.__md_files()
        result = []
        for md_file in md_files:
            with open(md_file, encoding="utf-8") as f:
                lines = f.read()
                # print(lines)
                article_on_review = re.search("## レビューした `PR`([\s\S]*)## 総括", lines)
                date_of_article = re.search('Date: (\D+ \d+), (\d{4})', lines)
                if article_on_review:
                    a = article_on_review.group(1)
                    a = re.sub('^\n+', '', a)
                    a = re.sub('\n+$', '', a)
                    a = re.sub('\n+', '', a)
                    # 記事があれば必ず日付は決まったフォーマットで存在する
                    try:
                        day_month = self.__day_to_date_and_month(date_of_article.group(1))
                        d = datetime.datetime.strptime(date_of_article.group(2) + '/' + str(day_month['month']) + '/' + str(day_month['date']), '%Y/%m/%d')
                    except Exception as e:
                        # テンプレートで日付のないやつがいる
                        continue
                    # print('-----')
                    # print(d)
                    if a == '' or a == '\n':
                        result.append({
                            'datetime': d,
                            'reviewed': ['なし']
                        })
                    else:
                        # print(a.split('\n'))
                        result.append({
                            'datetime': d,
                            'reviewed': a.split('\n')
                        })
        return result

    def __day_to_date_and_month(self, raw_day):
        raw_day_list = raw_day.split(" ")
        dic_str_month = {
            "Feb": 2,
            "Jan": 1,
            "Dec": 12,
            "Nov": 11,
            "Oct": 10,
            "Sep": 9,
            "Aug": 8,
            "Jul": 7,
            "Mar": 3,
            "Apr": 4
        }
        if len(raw_day_list) <= 1:
            return False
        if raw_day_list[0] in dic_str_month:
            month = dic_str_month[raw_day_list[0]]
            return {'month': month, 'date': int(raw_day_list[1])}
        else:
            return False
