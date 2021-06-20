from expertai.nlapi.cloud.client import ExpertAiClient
from expert_ai.helper import (
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


# # EXAMPLE 1:
# text = "Bitcoin prices will fall down. USA will have big issues. System bad!"
# # {'sentiments': (-49.9, 0.0, -49.9), 'entities': {'Bitcoin': ['BLD', 15], 'United States of America': ['GEO', 7]}, 'knowledge': ['situation.issue', 'conceptual_system', 'geographic_element.country', 'property.money', 'event.happening', 'other'], 'topics': []}

# # EXAMPLE 2
# text = "Born in USA, Michael Jordan was one of the best basketball players of all time. Scoring was Jordan's stand-out skill, but he still holds a defensive NBA record, with eight steals in a half."
# # {'sentiments': (10.69, 10.69, 0.0), 'entities': {'Michael Jordan': ['NPH', 15], 'United States of America': ['GEO', 2], 'National Basketball Association': ['ORG', 10]}, 'knowledge': ['event.outcome', 'action', 'quality.human_feature', 'geographic_element.country', 'person.basketball_player', 'object_group.property', 'component.object_part', 'time', 'event.happening', 'organization.sport_association'], 'topics': ['basketball', 'sports']}

# # EXAMPLE 3
# text = "This is a text written from Italy. It is designed by nature to excite the time 9th June, 2021. Its all about the topic of cars, although I still CAN NOT figure out how topics work. I like Bugatti. That is an entity."
# # {'sentiments': (7.0, 7.0, 0.0), 'entities': {'Jun-9-2021': ['DAT', 0], 'Italy': ['GEO', 7], 'Bugatti': ['COM', 13]}, 'knowledge': ['vehicle.car', 'state.situation', 'communication.writing', 'knowledge.form_of_thought', 'geographic_element.country', 'time.definite_time', 'knowledge.reasoning', 'feeling.good_feeling', 'creation.artistic_creation', 'behaviour.physical_behaviour', 'object.natural_object', 'state', 'organization.company'], 'topics': []}

# NOTE: SUMMARY
# sentiments: (overall, positive, negative) -> overall = positive + negative
# entities: Bitcoin, United States of America, Michael Jordan, National Basketball Association (the numbers second in the list, for example 10 in ['ORG', 10] for NBA is the RELEVANCE SCORE. COULD BE SUED LATER). Rest is: ORGanisation/COMpany/GEOpolitical entity/DATe
# knowledge: event.outcome, time, event.happening, organization.sport_association, conceptual_system, geographic_element.country, vehicle.car
# topics: basketball, sports (I CANT FIGURE THIS OUT FFS)


def get_analysis(text, language="en"):
    analysis = client.full_analysis(
        body={"document": {"text": text}}, params={"language": language}
    )
    sentiments = get_sentiment(analysis)
    entities = get_entities(analysis)
    knowledge = get_knowledge(analysis)
    topics = get_topics(analysis)

    data = {
        "sentiments": sentiments,
        "entities": entities,
        "knowledge": knowledge,
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

# NOTE: SUMMARY
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


# NOTE: GET THE OUTPUTS FROM HERE
# print(get_analysis(text))
# print(get_classification(text))
