# Echodex

Echodex is a web application which aggregrates data from multiple sources (news websites, reddit, twitter), and uses NLP tools to show structured analysis on the content retrieved. It can be used to get a quick, unbiased look at products, companies or people: and what general sentiments are about them, or which entities are they closely linked to, and various other features. Echodex is built with a clean interface using streamlit.

# Installation and Running

```
pip3 install -r requirements.txt
streamlit run dashboard/app.py
```

# Components

The code can be roughly divided into three components, the scrapper class, the functions to call expert.ai's API, and the streamlit app. The code has largely been abstracted to aid addition of code. 
