# from expertai.nlapi.cloud.client import ExpertAiClient

# client = ExpertAiClient()

# text = "Michael Jordan was one of the best basketball players of all time. Scoring was Jordan's stand-out skill, but he still holds a defensive NBA record, with eight steals in a half."
# # text = "bitcoin prices will fall down. USA will have big issues. System bad."
# language = "en"

# analysis = client.full_analysis(
#     body={"document": {"text": text}}, params={"language": language}
# )
# classification = client.classification(
#     body={"document": {"text": text}}, params={"taxonomy": "iptc", "language": language}
# )


# example:
# (69, 100, -31)
def get_sentiment(analysis):
    sentiment = (
        analysis.sentiment.overall,
        analysis.sentiment.positivity,
        analysis.sentiment.negativity,
    )
    return sentiment


# example:
# {entity: [type_of_entity, importance]}
# {'Michael Jordan': ['NPH', 15], 'National Basketball Association': ['ORG', 10]}
# {'United States of America': ['GEO', 5]}
def get_entities(analysis):
    entities = analysis.entities
    d = {}
    for word in entities:
        d[word.lemma] = [word.type_, word.relevance]
    return d


# example:
# ['event.outcome', 'action', 'quality.human_feature', 'person.basketball_player', 'object_group.property', 'component.object_part', 'time', 'other', 'other', 'event.happening', 'other', 'organization.sport_association', 'other']
def get_knowledge(analysis, relevant_only=True):
    knawledge = [
        word.label
        for word in analysis.knowledge
        if (not relevant_only) or (relevant_only and word.label != "other")
    ]
    return knawledge


# returns relevant topics only by default
# ['basketball', 'sports']
def get_topics(analysis, relevant_only=True):
    topics = [
        topic.label
        for topic in analysis.topics
        if (not relevant_only) or (relevant_only and topic.winner)
    ]
    return topics


# sentiments = get_sentiment(analysis)
# entities = get_entities(analysis)
# knawledge = get_knowledge(analysis)
# topics = get_topics(analysis)

# print(sentiments)
# print(entities)
# print(knawledge)
# print(topics)

# # [['Sport', 'Competition discipline', 'Basketball']]
# def get_categories(classification):
#     categories = [cat.hierarchy for cat in classification.categories]
#     return categories


def get_classification_taxonomy(client, text, taxonomy, language="en"):
    classification = client.classification(
        body={"document": {"text": text}},
        params={"taxonomy": taxonomy, "language": language},
    )
    categories = [cat.hierarchy for cat in classification.categories]
    return categories


# # categories = get_categories(classification)
# # print(categories)

# results = get_test(classification)
# print(results)
