import streamlit as st
from expert_ai.main import get_analysis
from Backend.scrapper import Scrapper

sentence = "I am a good boy."
x = Scrapper('bitcoin')
print(x.scrape_twitter())
print(get_analysis(sentence))
