# Echodex
Social Media Search Engine

## Demonstration
[![echodex](https://user-images.githubusercontent.com/51963164/127771258-d9132e24-0287-4f23-b85f-79f797f1e38d.png)](https://www.youtube.com/watch?v=PLx53XLQqig)

[Devpost Submission Link](https://devpost.com/software/echodex)

## Introduction
Echodex is a web application which aggregrates data from multiple sources (news websites, reddit, twitter), and uses NLP tools to show structured analysis on the content retrieved. It can be used to get a quick, unbiased look at products, companies or people: and what general sentiments are about them, or which entities are they closely linked to, and various other features. Echodex is built with a clean interface using streamlit.

The code can be roughly divided into three components, the scrapper class, the functions to call expert.ai's API, and the streamlit app. The code has largely been abstracted to aid addition of code. Each of the modules can be edited independently. You will need api keys from both expert.ai and newsapi to run the code, instructions for which can be followed on their websites.

## Installation and Running
```
pip3 install -r requirements.txt
streamlit run dashboard/app.py
```
