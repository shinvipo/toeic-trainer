import requests
from bs4 import BeautifulSoup
import re
from utils import *
from cache import insert_into_table

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
    if meaning_b != None:
        if meaning_b.find("span", "lab dlab"):
            usage_b = meaning_b.find("span", "lab dlab")
            usage = replace_all(usage_b.text).strip()
            meaning_words = replace_all(meaning_b.text).split(usage)[-1].strip()
            print(usage + meaning_words.strip())
        else:
            meaning_words = replace_all(meaning_b.text).strip()
            print(meaning_words)

    # Print the meaning's specific language translation if any
    meaning_lan = def_block.find("span", "trans dtrans")
    if meaning_lan:
        meaning_lan_words = replace_all(meaning_lan.text).strip()
        print(" " + meaning_lan_words)

def parse_def_info(def_block):
    x = def_block.find("span", "def-info ddef_i")
    if x == None:
        return
    def_info = replace_all(x.text).strip()
    if def_info == " ":
        def_into = ""
    if def_info:
        if "phrase-body" in def_block.parent.attrs["class"]:
            print("  " + "\033[1m" + def_info + " " + "\033[0m", end="")
        else:
            print(def_info + " ", end="")

def parse_example(def_block):
    # NOTE:
    # suppose the first "if" has already run
    # and, the second is also "if", rather than "elif"
    # then, codes under "else" will also be run
    # meaning two cases took effect at the same time, which is not wanted
    # so, for exclusive cases, you can't write two "ifs" and one "else"
    # it should be one "if", one "elif", and one "else"
    # or three "ifs"
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
                print("  => " + lab + " " + example + " " + example_lan_sent)
            elif e.find("span", "gram dgram"):
                gram = replace_all(e.find("span", "gram dgram").text).strip()
                print("  => " + gram + " " + example + " " + exmaple_lan_sent)
            elif e.find("span", "lu dlu"):
                lu = replace_all(e.find("span", "lu dlu").text).strip()
                print("  => " + lu + " " + example + " " + example_lan_sent)
            else:
                print("  => " + example + " " + example_lan_sent)

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
    CAMBRIDGE_URL = "https://dictionary.cambridge.org"
    CAMBRIDGE_DICT_BASE_URL = CAMBRIDGE_URL + "/dictionary/english/"
    CAMBRIDGE_SPELLCHECK_URL = CAMBRIDGE_URL + "/spellcheck/english/?q="
    CAMBRIDGE_DICT_BASE_URL_VI = CAMBRIDGE_URL + "/dictionary/english-vietnamese/"
    CAMBRIDGE_SPELLCHECK_URL_VI = CAMBRIDGE_URL + "/spellcheck/english-vietnamese/?q="
    
    headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0' }
    response = requests.get(CAMBRIDGE_DICT_BASE_URL_VI + text,headers=headers).text
    soup = BeautifulSoup(response, 'html.parser')

    
    # with open("./data/cambridge_response2.html",encoding="utf8") as fp:
    #     soup = BeautifulSoup(fp, "html.parser")
        
    temp = soup.find("title").text.split("-")[0].strip()

    if "|" in temp:
        response_word = temp.split("|")[0].strip().lower()
    
    first_dicts = soup.find_all("div", "d pr di english-vietnamese kdic")
    for first_dict in first_dicts:
        all_meaning = first_dict.find_all("div", ["pr dsense", "sense-block pr dsense dsense-noh"])
        head = first_dict.find("div","dpos-h di-head normal-entry")
        print(parse_dict_head(head))
        for meaning in all_meaning:
            parse_def_info(meaning)
            parse_meaning(meaning)
            parse_example(meaning)
        print()
fetch_cambridge("hello")