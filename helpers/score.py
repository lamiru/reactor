from reactions.models import Reaction, Rating


def calculate_score(reaction):
    rating_list = Rating.objects.filter(reaction=reaction)
    reaction.score = 0
    for rating in rating_list:
        if rating.rating == 'G':
            reaction.score += 2
        else:
            reaction.score += 1
    reaction.save()

def calculate_topic_score(topic):
    reaction_list = Reaction.objects.filter(topic=topic)
    topic.topic_score = 0
    for reaction in reaction_list:
        topic.topic_score += reaction.score
    topic.save()

def calculate_all_score():
    reaction_list = Reaction.objects.all()
    for reaction in reaction_list:
        calculate_score(reaction)

def calculate_all_topic_score():
    topic_list = Reaction.objects.filter(target=None)
    for topic in topic_list:
        calculate_topic_score(topic)
