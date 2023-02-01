import requests
from bs4 import BeautifulSoup
import re
from utils import *
from cache import *
import json


CAMBRIDGE_URL = "https://dictionary.cambridge.org"
CAMBRIDGE_DICT_BASE_URL = CAMBRIDGE_URL + "/dictionary/english/"
CAMBRIDGE_SPELLCHECK_URL = CAMBRIDGE_URL + "/spellcheck/english/?q="
CAMBRIDGE_DICT_BASE_URL_VI = CAMBRIDGE_URL + "/dictionary/english-vietnamese/"
CAMBRIDGE_SPELLCHECK_URL_VI = CAMBRIDGE_URL + "/spellcheck/english-vietnamese/?q="

headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0' }

with open("./Data/vocab.json",'r') as f:
    toeic = json.load(f)["TOEIC"]

def spellcheck(txt):
    txt = txt.strip()
    reg = "^[A-Za-z .]*[A-Za-z.][A-Za-z -.]*$"
    res = re.findall(reg,txt)
    return res[0] if len(res) != 0 else None

def fetch_tracau(text, lang = 'en'):
    api_key = "WBBcwnwQpV89"
    value = text
    url = 'https://api.tracau.vn/{}/s/{}/{}'.format(api_key,value,lang)
    response =  requests.get(url=url).text
    soup = BeautifulSoup(response, 'html.parser')
    with open('tracau_response.html','w', encoding='utf-8') as f:
        f.write(soup.prettify())

def fetch_tratu(text):
    url = 'http://tratu.soha.vn/dict/en_vn/'

def parse_meaning(def_block):
    meaning_b = def_block.find("div", "def ddef_d db")
    result = ""
    if meaning_b != None:
        if meaning_b.find("span", "lab dlab"):
            usage_b = meaning_b.find("span", "lab dlab")
            usage = replace_all(usage_b.text).strip()
            meaning_words = replace_all(meaning_b.text).split(usage)[-1].strip()
            result = result + (usage + meaning_words.strip()) + "\n"
        else:
            meaning_words = replace_all(meaning_b.text).strip()
            result = result + (meaning_words) + "\n"

    # Print the meaning's specific language translation if any
    meaning_lan = def_block.find("span", "trans dtrans")
    if meaning_lan:
        meaning_lan_words = replace_all(meaning_lan.text).strip()
        result = result + (" " + meaning_lan_words) + "\n"
    return result

def parse_def_info(def_block):
    x = def_block.find("span", "def-info ddef_i")
    if x == None:
        return
    def_info = replace_all(x.text).strip()
    if def_info == " ":
        def_into = ""
    if def_info:
        if "phrase-body" in def_block.parent.attrs["class"]:
            return (def_info + " ")
        else:
            return (def_info + " ")

def parse_example(def_block):
    # NOTE:
    # suppose the first "if" has already run
    # and, the second is also "if", rather than "elif"
    # then, codes under "else" will also be run
    # meaning two cases took effect at the same time, which is not wanted
    # so, for exclusive cases, you can't write two "ifs" and one "else"
    # it should be one "if", one "elif", and one "else"
    # or three "ifs"
    result = ""
    for e in def_block.find_all("div", "examp dexamp"):
        if e is not None:
            example = replace_all(e.find("span", "eg deg").text).strip()

            # Print the exmaple's specific language translation if any
            example_lan = e.find("span", "trans dtrans dtrans-se hdb break-cj")
            if example_lan is not None:
                example_lan_sent = example_lan.text
            else:
                example_lan_sent = ""

            if e.find("span", "lab dlab"):
                lab = replace_all(e.find("span", "lab dlab").text).strip()
                result = result + ("  => " + lab + " " + example + " " + example_lan_sent) + "\n"
            elif e.find("span", "gram dgram"):
                gram = replace_all(e.find("span", "gram dgram").text).strip()
                result = result + ("  => " + gram + " " + example + " " + example_lan_sent) + "\n"
            elif e.find("span", "lu dlu"):
                lu = replace_all(e.find("span", "lu dlu").text).strip()
                result = result + ("  => " + lu + " " + example + " " + example_lan_sent) + "\n"
            else:
                result = result + ("  => " + example + " " + example_lan_sent) + "\n"
    return result

def parse_head_title(block):
    word = block.find("h2", "tw-bw dhw dpos-h_hw di-title").text
    return word

def parse_dict_head(block):
    word = replace_all(parse_head_title(block)).strip()
    try:    
        vocab_type = replace_all(block.find("div","dpos-g hdib").text).strip()
    except:
        vocab_type = ""
    try:
        spell = block.find("span","pron-info dpron-info").text
        spell = replace_all(spell).strip()
    except:
        spell = ""
    try:
        usage = block.find("div", "irreg-infls hdib dinfls").text
        usage = replace_all(usage).replace("|","\n").strip()
    except:
        usage = ""
    
    return f"* {word} - {vocab_type} - {spell} \n {usage}"
    

def fetch_cambridge(text):
    con,cur = connect_db()
    cachee = get_cache(con,cur,text,CAMBRIDGE_DICT_BASE_URL_VI + text)
    if cachee != None:
        response = cachee[2]
    else:
        req = requests.get(CAMBRIDGE_DICT_BASE_URL_VI + text,headers=headers)
        response = req.content
        insert_into_table(con,cur,text,text,CAMBRIDGE_DICT_BASE_URL_VI + text,response)
    close_db(con,cur)
    
    soup = BeautifulSoup(response, 'html.parser')
    response_word = soup.find("title").text.split("-")[0].strip()
    if response_word.startswith("CAMBRIDGE ENGLISH"):
        return text
    if "|" in response_word:
        response_word = response_word.split("|")[0].strip().lower()
    
    first_dicts = soup.find_all("div", "d pr di english-vietnamese kdic")
    result = response_word.upper() + "\n\n"
    for first_dict in first_dicts:
        all_meaning = first_dict.find_all("div", ["pr dsense", "sense-block pr dsense dsense-noh"])
        head = first_dict.find("div","dpos-h di-head normal-entry")
        result = result + (parse_dict_head(head).strip()) + "\n"
        for meaning in all_meaning:
            result = result + (parse_def_info(meaning))
            result = result + (parse_meaning(meaning))
    return result

def show_full_from_cache(word):
    con,cur = connect_db()
    cachee = get_cache(con,cur,word,CAMBRIDGE_DICT_BASE_URL_VI + word)
    if cachee != None:
        response = cachee[2]
    else:
        return "Data In DB Is Empty\n"
    soup = BeautifulSoup(response, 'html.parser')
    response_word = soup.find("title").text.split("-")[0].strip()

    if "|" in response_word:
        response_word = response_word.split("|")[0].strip().lower()
    
    first_dicts = soup.find_all("div", "d pr di english-vietnamese kdic")
    result = response_word.upper() + "\n\n"
    for first_dict in first_dicts:
        all_meaning = first_dict.find_all("div", ["pr dsense", "sense-block pr dsense dsense-noh"])
        head = first_dict.find("div","dpos-h di-head normal-entry")
        result = result + (parse_dict_head(head).strip()) + "\n"
        for meaning in all_meaning:
            result = result + (parse_def_info(meaning))
            result = result + (parse_meaning(meaning))
            result = result + (parse_example(meaning))
    return result

if __name__ == "__main__":
    print(fetch_cambridge('the Apocalypse'))