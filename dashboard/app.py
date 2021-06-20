import streamlit as st
from expert_ai.main import get_analysis

sentence = "I am a good boy."
print(get_analysis(sentence))
