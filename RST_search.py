#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import re, os
import pymorphy2
import spacy
import string
from string import punctuation
from langdetect import detect

rus_df = pd.read_csv('data/russian_data.csv')
eng_df = pd.read_csv('data/english_data.csv')


# In[2]:


rus_tags = []
for i, row in rus_df.iterrows():
    tags = row['pos'].split('_')
    rus_tags.extend(tags)
rus_ts = list(set(rus_tags))


# In[3]:


eng_tags = []
for i, row in eng_df.iterrows():
    tags = row['pos'].split('_')
    eng_tags.extend(tags)
eng_ts = list(set(eng_tags))


# In[4]:


tag_list = rus_ts[1:]


# In[5]:


tag_list.extend(eng_ts)


# In[6]:


tag_list = list(set(tag_list))


# In[7]:


tags_abbs = [['Существительное', 'NOUN'], ['Имя собственное', 'PROPN'], ['Местоимение', 'PRON'], ['Глагол', 'VERB'],
             ['Прилагательное', 'ADJ'], ['Наречие', 'ADV'], ['Междометие', 'INTJ'], ['Частица', 'PART'],
             ['Союзы', 'CONJ'], ['Соединительные союзы', 'CCONJ'], ['Подчинительные союзы', 'SCONJ'], 
             ['Вспомогательное слово', 'AUX'], ['Адлог', 'ADP'], ['Детерминатив', 'DET'], ['Числительное', 'NUM'],
             ['Символ', 'SYM'], ['Другое','X'], ['Пунктуация','PUNCT']]


# In[8]:


rels_abbs = [['Фон','background'], ['Контраст','contrast'], ['Уступка','concession'], ['Обоснование','evidence'], 
             ['Причина','cause'], ['Интерпретация','interpretation'], ['Оценка','evaluation'], ['Эффект','effect'],
             ['Детализация','elaboration'], ['Условие','condition'], ['Цель','purpose'], ['Решение','solutionhood'],
             ['Подготовка','preparation'], ['Переформулировка','restatement'], ['Сравнение','comparison'],
             ['Последовательность','sequence'], ['Объединение','joint'], ['Прерывающаяся единица','same-unit']]


# In[9]:


exclude = ['d07', 'k011', 'k022']
drop_ids_rus = []

for i, row in rus_df.iterrows():
    if row['text_id'] in exclude:
        drop_ids_rus.append(i)

drop_ids_eng = []

for i, row in eng_df.iterrows():
    if row['text_id'] in exclude:
        drop_ids_eng.append(i)


# In[10]:


rus_df = rus_df.drop(drop_ids_rus).reset_index(drop=True)
eng_df = eng_df.drop(drop_ids_eng).reset_index(drop=True)


# In[11]:


morph = pymorphy2.MorphAnalyzer()
punct = punctuation+'«»—…“”*№–'


# In[12]:


def norm_rus(text):
    
    words = [word.strip(punct) for word in text.lower().split()]
    words = [morph.parse(word)[0].normal_form for word in words if word]

    return '_'.join(words)


# In[13]:


nlp = spacy.load("en_core_web_sm")


# In[14]:


def norm_eng(text):
    
    doc = nlp(text)

    return "_".join([token.lemma_ for token in doc])


# In[15]:


def lang_detect(query):
    lang = detect(query)
    if lang == 'ru' or lang == 'en':
        return lang
    else:
        if bool(re.search('[а-яА-Я]', query)) == True:
            return 'ru'
        elif bool(re.search('[a-zA-Z]', query)) == True:
            return 'en'
        else:
            return None


# In[16]:


def rst_search(query=None, pos=None, rels=None):
    
    text_ids = []
    
    if query != None:
        lang = lang_detect(query)
        if lang == 'ru':
            df_1 = rus_df
            query_norm = norm_rus(query)
        if lang == 'en':
            df_1 = eng_df
            query_norm = norm_eng(query)
        if lang == None:
            return 'Не удалось определить язык запроса.', 0
        
        for index, row in df_1.iterrows():
            if query_norm in row['lemmas'] and row['text_id'] not in text_ids:
                if pos == None:
                    text_ids.append(row['text_id'])
                if pos != None:
                    lemmas = row['lemmas'].split('_')
                    lemma_ids = [x for x in range(len(lemmas)) if lemmas[x] == query_norm]
                    for lemma_id in lemma_ids:
                        if row['pos'].split('_')[lemma_id] == pos[0]:
                            text_ids.append(row['text_id'])
        
        if rels == None:
            if text_ids == []:
                return 'Совпадения не найдены.', 0
            else:
                return get_texts(text_ids), text_ids
        
        else:
            new_text_ids = rel_check(rels, text_ids)
            if new_text_ids == []:
                return 'Совпадения не найдены.', 0
            else:
                return get_texts(new_text_ids), new_text_ids
    
    else:
        if pos != None:
            pos_check(pos[0], rus_df, text_ids)
            pos_check(pos[0], eng_df, text_ids)
            
            if text_ids == []:
                return 'Совпадения не найдены.', 0
            else:
                return get_texts(text_ids), text_ids
        
        if rels != None:            
            res_ids = rel_check(rels)
            
            if res_ids == []:
                return 'Совпадения не найдены.', 0
            else:
                return get_texts(res_ids), res_ids
        
        if rels == None and pos == None:
            return 'Пустой запрос. Попробуйте еще раз.', 0


# In[37]:


def rel_check(rels, text_ids = None):
    res_files = []
    
    if text_ids == None:
        files = os.listdir('data/rs3_files_rus')
    else:
        files = []
        for i in text_ids:
            file_name = f'tree rule_1__rule_2__rule_3_ar_result_micro_{i}.rs3'
            files.append(file_name)
            
    for file in files:
        path = 'data/rs3_files_rus/' + file
        if file[-8:-4][0] == '_':
            text_id = file[-7:-4]
        else:
            text_id = file[-8:-4]
        with open(path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            for rel in rels:
                for line in lines:
                    if rel in line and text_id not in res_files:
                        res_files.append(text_id)
    return res_files        


# In[38]:


def pos_check(pos, df, text_ids):
    for index, row in df.iterrows():
        if pos in row['pos'] and row['text_id'] not in text_ids:
            text_ids.append(row['text_id'])


# In[39]:


def get_texts(text_ids):
    texts = []
    
    for i in text_ids:
        text_rus = []
        text_eng = []

        for index, row in rus_df.iterrows():
            if row['text_id'] == i:
                text_rus.append(row['segment'])

        for index, row in eng_df.iterrows():
            if row['text_id'] == i:
                text_eng.append(row['edu'])

        texts.append([' '.join(text_rus), ' '.join(text_eng)])
    
    return texts

