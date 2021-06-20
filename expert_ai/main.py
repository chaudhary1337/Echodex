from expertai.nlapi.cloud.client import ExpertAiClient
from helper import (
    get_sentiment,
    get_knowledge,
    get_entities,
    get_topics,
    get_classification_taxonomy,
)

client = ExpertAiClient()

# text = "I experience a mix of conflicting emotions: the approach of the fateful date scares me, but at the same time I can't wait for it to arrive. I have moments of elation and others of pure panic, but I would say that I am mostly happy."
# text = "Born in USA, Michael Jordan was one of the best basketball players of all time. Scoring was Jordan's stand-out skill, but he still holds a defensive NBA record, with eight steals in a half."
# text = "Bitcoin prices will fall down. USA will have big issues. System bad"
# print(get_analysis(text))
# sample output = {
#     "sentiments": (-49.9, 0.0, -49.9),
#     "entities": {"Bitcoin": ["BLD", 15], "United States of America": ["GEO", 7]},
#     "knowledge": [
#         "situation.issue",
#         "conceptual_system",
#         "geographic_element.country",
#         "property.money",
#         "event.happening",
#         "other",
#     ],
#     "topics": [],
# }


# EXAMPLE 1:
text = "Bitcoin prices will fall down. USA will have big issues. System bad!"
# {'sentiments': (-49.9, 0.0, -49.9), 'entities': {'Bitcoin': ['BLD', 15], 'United States of America': ['GEO', 7]}, 'knowledge': ['situation.issue', 'conceptual_system', 'geographic_element.country', 'property.money', 'event.happening', 'other'], 'topics': []}


def get_analysis(text, language="en"):
    analysis = client.full_analysis(
        body={"document": {"text": text}}, params={"language": language}
    )
    sentiments = get_sentiment(analysis)
    entities = get_entities(analysis)
    knawledge = get_knowledge(analysis)
    topics = get_topics(analysis)

    data = {
        "sentiments": sentiments,
        "entities": entities,
        "knowledge": knawledge,
        "topics": topics,
    }

    return data


# EXAMPLE 1: made from different texts, i just concat them together.
# {
# 'geo': [['United States of America']],
# 'iptc': [['Sport', 'Competition discipline', 'Basketball']],
# 'behaviour': [['Capability', 'Capability high', 'Competence']],
# 'emotional': [
#   ['Group Apprehension', 'Fear'],
#   ['Group Delight', 'Happiness'],
#   ['Group Delight', 'Excitement'],
#   ['Group Delight', 'Joy']]
# }

# # EXAMPLE 2:
# text = "Hello, I am a happy man from India. I travel to USA frequently. I ran a fintech startup which was bought by Google. I am industrious and I love to be prepared for the future. "
# # {'geo': [['India'], ['United States of America']], 'iptc': [], 'behaviour': [['Action', 'Action high', 'Dynamism']], 'emotional': [['Group Delight', 'Happiness']]}

# # EXAMPLE 3: italy is not a country, Italy is.
# text = "My girl from italy left me lmaoo. Im literally crying."
# # {'geo': [['Italy']], 'iptc': [], 'behaviour': [], 'emotional': [['Group Dejection', 'Sadness']]}

# SUMMARY
# geo: countries - United States of America, India
# behaviour: behavioral-traits - Action, Competence, Capability
# iptc: I HAVE NO IDEA HOW IPTC WORKS
# emotional: Group Dejection/Delight/Apprehension, Sadness/Happiness/Joy
def get_classification(text, language="en"):
    data = {
        "geo": get_classification_taxonomy(client, text, "geotax", language),
        "iptc": get_classification_taxonomy(client, text, "iptc", language),
        "behaviour": get_classification_taxonomy(
            client, text, "behavioral-traits", language
        ),
        "emotional": get_classification_taxonomy(
            client, text, "emotional-traits", language
        ),
    }
    return data


print(get_analysis(text))
# print(get_classification(text))
