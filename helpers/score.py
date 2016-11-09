from reactions.models import Reaction, Rating


def calculate_score(reaction):
    rating_list = Rating.objects.filter(reaction=reaction)
    reaction.score = 0
    for rating in rating_list:
        if rating.rating == 'G':
            reaction.score += 2
        else:
            reaction.score += 1
    reacction_score = reaction.score
    reaction.save()

    topic = reaction.topic
    reaction_list = Reaction.objects.filter(topic=topic)
    topic.topic_score = 0
    for reaction in reaction_list:
        topic.topic_score += reaction.score
    topic.score = reacction_score
    topic.save()

def calculate_all_score():
    reaction_list = Reaction.objects.all()
    for reaction in reaction_list:
        calculate_score(reaction)
