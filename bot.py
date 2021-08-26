from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

url = "https://jklm.fun/SUDN"
bot_name = "arto_bot"
dictionnary = "dicoen.txt"

def get_all_word():
  dico = []
  fin = open(dictionnary)
  rm_nl = fin.readline()
  while (len(rm_nl) > 1):
    clean_word = rm_nl[:-1]
    clean_word = clean_word.upper()
    dico.append(clean_word)
    rm_nl = fin.readline()
  return (dico)

def enter_game():
  driver=webdriver.Chrome()
  driver.get(url)
  name = driver.find_elements_by_tag_name("input")
  time.sleep(1)
  name[1].send_keys(bot_name + Keys.ENTER)
  time.sleep(1)
  driver.switch_to.frame(0)
  while (1):
    check = driver.find_elements_by_tag_name("button")
    if (check[1].is_displayed() == True):
      break
    time.sleep(0.5)
  join = driver.find_elements_by_tag_name("button")
  time.sleep(0.3)
  join[1].send_keys(Keys.ENTER)
  return (driver)

def wait_turn(driver, already_use):
  check = False
  while (check == False):
    check = driver.find_element_by_class_name("selfTurn").is_displayed()
    time.sleep(0.3)
    if (driver.find_element_by_class_name("join").is_displayed() == True):
      time.sleep(0.3)
      join = driver.find_elements_by_tag_name("button")
      time.sleep(1)
      join[1].send_keys(Keys.ENTER)
      time.sleep(0.3)
      already_use[:] = []
      wait_turn(driver, already_use)
      break

def play_game(driver, dico):
  already_use = []
  while(1):
    wait_turn(driver, already_use)
    syll = driver.find_element_by_class_name("syllable")
    word = find_word_dic(syll.text, dico, already_use)
    already_use.append(word)
    res = driver.find_elements_by_class_name("styled")
    time.sleep(0.3)
    res[2].send_keys(word)
    time.sleep(0.3)
    res[2].send_keys(Keys.ENTER)
    time.sleep(0.3)

def find_syll_in_word(syll, word):
  if (word.find(syll) != -1):
    return (True)
  else:
    return (False)

def not_already_use(word, already_use):
  for match in already_use:
    if match == word:
      return (False)
  return (True)

def find_word_dic(syll, dico, already_use):
  for word in dico:
    if (find_syll_in_word(syll, word) == True):
      if (not_already_use(word, already_use) == True):
        break
  return (word)

dico = get_all_word()
driver = enter_game()
play_game(driver, dico)