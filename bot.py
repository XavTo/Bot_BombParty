from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import random
import time
import sys

bot_name = "boto"
if (len(sys.argv) < 2):
  print("Add room link in arguments")
  exit()
url = sys.argv[1]
humain_like = True

def get_all_word(driver, dico):
  lang = driver.find_element(By.XPATH, "//div[2]/div[2]/div[2]/div[1]/div/span[1]").text
  print(lang)
  if (lang == "Anglais" or lang == "English"):
    dictionary = "dicoen.txt"
  if (lang == "Français" or lang == "French"):
    dictionary = "dicofr.txt"
  if (lang == "Pokémon (Anglais)" or lang == "Pokémon (English)"):
    dictionary = "dicopokeen.txt"
  if (lang == "Pokémon"):
    dictionary = "dicopokefr.txt"
  fin = open(dictionary)
  rm_nl = fin.readline()
  while (len(rm_nl) > 1):
    clean_word = rm_nl[:-1]
    clean_word = clean_word.upper()
    dico.append(clean_word)
    rm_nl = fin.readline()
  random.shuffle(dico)

def enter_game(dico):
  s=Service(ChromeDriverManager().install())
  driver = webdriver.Chrome(service=s)
  driver.get(url)
  time.sleep(0.3)
  name = driver.find_element(By.XPATH, "//div[2]/div[3]/form/div[2]/input")
  time.sleep(1)
  name.send_keys(bot_name + Keys.ENTER)
  time.sleep(1)
  driver.switch_to.frame(0)
  get_all_word(driver, dico)
  while (1):
    check = driver.find_element(By.XPATH, "//div[2]/div[3]/div[1]/div[1]/button")
    if (check.is_displayed() == True):
      break
    time.sleep(0.5)
  join = driver.find_element(By.XPATH, "//div[2]/div[3]/div[1]/div[1]/button")
  time.sleep(0.3)
  join.send_keys(Keys.ENTER)
  return (driver)

def wait_turn(driver, already_use):
  check = False
  while (check == False):
    check = driver.find_element(By.CLASS_NAME, "selfTurn").is_displayed()
    time.sleep(0.005)
    if (driver.find_element(By.CLASS_NAME, "join").is_displayed() == True):
      time.sleep(0.3)
      try:
        join = driver.find_element(By.XPATH, "//div[2]/div[3]/div[1]/div[1]/button")
      except: continue
      time.sleep(1)
      try:
        join.send_keys(Keys.ENTER)
      except: continue
      time.sleep(0.3)
      already_use[:] = []
      wait_turn(driver, already_use)
      break

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

def play_game(driver, dico):
  already_use = []
  while(1):
    wait_turn(driver, already_use)
    syll = driver.find_element(By.CLASS_NAME, "syllable")
    word = find_word_dic(syll.text, dico, already_use)
    already_use.append(word)
    res = driver.find_element(By.XPATH, "//div[2]/div[3]/div[2]/div[2]/form/input")
    if (humain_like == True):
      rand = random.uniform(0.2, 1)
      time.sleep(rand)
      for letters in word:
        try:
          res.send_keys(letters)
        except: continue
        rand = random.uniform(0.02, 0.15)
        time.sleep(rand)
      time.sleep(0.1)
    else:
      try:
          time.sleep(0.01)
          res.send_keys(word)
      except: continue
    try:
      time.sleep(0.01)
      res.send_keys(Keys.ENTER)
    except: continue
    if (humain_like == True):
      time.sleep(0.3)

dico = []
driver = enter_game(dico)
play_game(driver, dico)
