import pandas as pd
import os, os.path
import random
import re
import email, email.policy

words_vec = ['a', 'about', 'address', 'aligncenter', 'aligncenterfont', 'all', 'also', 'an', 'and', 'any', 'are',
             'arial', 'as', 'at', 'be', 'because', 'been', 'body', 'border', 'br', 'business', 'but', 'by', 'can',
             'cellpadding', 'cellspacing', 'color', 'could', 'date', 'div', 'do', 'dont', 'email', 'emails', 'even',
             'facearial', 'facetahoma', 'faceverdana', 'first', 'font', 'for', 'free', 'from', 'get', 'government',
             'had', 'has', 'have', 'he', 'head', 'height', 'helvetica', 'here', 'his', 'how', 'html', 'i', 'if', 'im',
             'in', 'information', 'into', 'is', 'it', 'its', 'just', 'know', 'like', 'list', 'mailing', 'make', 'me',
             'message', 'money', 'more', 'most', 'mv', 'my', 'name', 'new', 'no', 'not', 'now', 'of', 'on', 'one',
             'only', 'option', 'or', 'order', 'other', 'our', 'out', 'p', 'people', 'please', 'receive', 'report',
             'said', 'same', 'sansserif', 'see', 'send', 'should', 'size', 'so', 'some', 't', 'table', 'td', 'than',
             'that', 'the', 'their', 'them', 'then', 'there', 'they', 'think', 'this', 'time', 'to', 'tr', 'up',
             'url', 'us', 'use', 'was', 'way', 'we', 'were', 'what', 'when', 'which', 'who', 'width', 'will', 'with',
             'would', 'wrote', 'you', 'your']
d_types = ['text/plain', 'text/html', 'multipart/signed', 'multipart/alternative', 'multipart/mixed',
           'multipart/related', 'multipart/report']

random.seed(42)

def load_email(is_spam, filename):
    directory = "./spam" if is_spam else "./easy_ham"
    with open(os.path.join(directory, filename), "rb") as f:
        return email.parser.BytesParser(policy=email.policy.default).parse(f)

def keep_only_words(mail):
    return re.sub(r'[^a-zA-Z\s]', '', mail)


def str_to_list(mail):
    return re.split(r'\s+|\n|\r', mail)


def replace_urls(mail):
    lst = []
    for row in mail:
        if 'http' in row:
            lst.append('url')
        elif '@' in row:
            lst.append('e-mail')
        else:
            lst.append(row)
    return lst


def preprocessing(mail):
    d_type = str(mail.get_content_type())
    try:
        mail = mail.get_content()
        mail = mail.lower()
        mail = ' '.join(replace_urls(mail.split()))
        mail = keep_only_words(mail)
        mail = str_to_list(mail)
    except:
        mail = ['nottext']
    return d_type, mail


current = os.getcwd()
spams_list = os.listdir('./spam')
hams_list = os.listdir('./easy_ham')

n_spams = len(spams_list)
n_hams = len(hams_list)

idx_train_spam = random.sample(range(0, 501), 350)
idx_train_spam.sort()
idx_test_spam = [i for i in list(range(0, 501)) if i not in idx_train_spam]
idx_test_spam.sort()
idx_train_ham = random.sample(range(0, 2551), 1785)
idx_train_ham.sort()
idx_test_ham = [i for i in list(range(0, 2551)) if i not in idx_train_ham]
idx_test_ham.sort()

train_spam = [spams_list[i] for i in idx_train_spam]
test_spam = [spams_list[i] for i in idx_test_spam]
train_ham = [hams_list[i] for i in idx_train_ham]
test_ham = [hams_list[i] for i in idx_test_ham]

train_ham_emails = [load_email(is_spam=False, filename=name) for name in train_ham]
train_spam_emails = [load_email(is_spam=True, filename=name) for name in train_spam]

X = []
y = []

for mail in train_ham_emails:
    row = {key: 0 for key in d_types + words_vec}
    d_type, message = preprocessing(mail)
    row[d_type] = 1
    for word in words_vec:
        count = message.count(word)
        row[word] = count
    X.append(row)
    y.append(0)

for mail in train_spam_emails:
    row = {key: 0 for key in d_types + words_vec}
    d_type, message = preprocessing(mail)
    row[d_type] = 1
    for word in words_vec:
        count = message.count(word)
        row[word] = count
    X.append(row)
    y.append(1)

X = pd.DataFrame(X)
y = pd.DataFrame(y)

X.to_csv('features_train.csv', index=False)
y.to_csv('target_train.csv', index=False)

"""d_types_freq = dict()
word_dict = dict()

for ham_mail in train_ham_emails:
    d_type, message = preprocessing(ham_mail)
    if d_type not in d_types_freq:
        d_types_freq[d_type] = 1
    else:
        d_types_freq[d_type] += 1
    for word in message:
        if word not in word_dict:
            word_dict[word] = 1
        else:
            word_dict[word] += 1

for key, value in d_types_freq.items():
    print(f"{key}: {value}")"""
#sorted_items = sorted(word_dict.items(), key=lambda x: x[1], reverse=True)

#print('HAMS')
"""for key, value in sorted_items[:100]:
    print(f"{key}: {value}")"""
#ham_words = [key for key, value in sorted_items[:100]]

"""d_types_freq = dict()
word_dict = dict()
for ham_mail in train_spam_emails:
    d_type, message = preprocessing(ham_mail)
    if d_type not in d_types_freq:
        d_types_freq[d_type] = 1
    else:
        d_types_freq[d_type] += 1
    for word in message:
        if word not in word_dict:
            word_dict[word] = 1
        else:
            word_dict[word] += 1

for key, value in d_types_freq.items():
    print(f"{key}: {value}")"""

#sorted_items = sorted(word_dict.items(), key=lambda x: x[1], reverse=True)
#print('SPAMS')
"""for key, value in sorted_items[:50]:
    print(f"{key}: {value}")"""
"""spam_words = [key for key, value in sorted_items[:100]]
sparse_vec = sorted(set(ham_words + spam_words))
print(sparse_vec)"""




