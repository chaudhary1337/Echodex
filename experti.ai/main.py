from expertai.nlapi.cloud.client import ExpertAiClient
from helper import get_sentiment, get_knowledge, get_entities, get_topics

client = ExpertAiClient()


def get_analysis(sentence, language="en"):
    analysis = client.full_analysis(
        body={"document": {"text": sentence}}, params={"language": language}
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


# # testing
# sentence = "Bitcoin prices will fall down. USA will have big issues. System bad"
# print(get_analysis(sentence))
