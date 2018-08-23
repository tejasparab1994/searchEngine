#encoding: utf-8
from bs4 import BeautifulSoup
import regex as re

def read_html_file(path):
    soup = BeautifulSoup(open(path),"lxml")
    pre = soup.find("pre").contents[0]
    prelist = []
    prelist.append(pre.split("\n"))
    list_without_numbers = []
    for item in prelist[0]:
        if "\t" in item and any(c.isdigit() for c in item):
            continue
        else:
            list_without_numbers.append(filter(None,item))
    withoutNone = [x.strip() for x in list_without_numbers if x.strip()]
    return withoutNone

def remove_tabs(html_content):
    html_content_without_tab = []
    for element in html_content:
        html_content_without_tab.append(element.split("\t"))
    return make_flat_list(html_content_without_tab)

def split_by_space(html_content):
    splitted = []
    for element in html_content:
        splitted.append(element.split(" "))
    return make_flat_list(splitted)

def make_flat_list(blown_list):
    flat_list = [item for sublist in blown_list for item in sublist]
    return filter(None,flat_list)

def case_fold(html_content):
    case_folded = []
    for element in html_content:
        case_folded.append(element.lower())
    return case_folded

def punctuation_remover(word):
    rx = re.compile(r'\w+[-–]+\w+(*SKIP)(*FAIL)|\d+[-.–/,:;]+\d+(*SKIP)(*FAIL)|[^a-zA-Z\d\s]+')
    return rx.sub("",word)

def remove_punctuations(html_content):
    without_punctuations = []
    for element in html_content:
        without_punctuations.append(punctuation_remover(element))
    return without_punctuations

def parse_html(path):
    return filter(None,remove_punctuations(remove_bullets(case_fold(split_by_space(remove_tabs(read_html_file(path)))))))

def remove_bullets(html_content):
    without_bullet = []
    for element in html_content:
        if "(" in element and ")" in element:
            startIndex = element.index("(")
            endIndex = element.index(")")
            newWord = element[:startIndex] + element[endIndex + 1:]
            without_bullet.append(newWord)
        else:
            without_bullet.append(element)
    return without_bullet

def remove_stopwords(html_content):
    f = open("common_words.txt","r")
    raw_words = f.readlines()
    stop_words = []
    removed = []
    for word in raw_words:
        stop_words.append(word.strip("\n"))
    for element in html_content:
        if element not in stop_words:
            removed.append(element)
    return removed

def parse_html_without_stopwords(path):
    return filter(None,remove_stopwords(remove_punctuations(remove_bullets(case_fold(split_by_space(remove_tabs(read_html_file(path))))))))