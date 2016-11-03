from reactions.models import Reaction, Rating


def calculate_all_score():
    reaction_list = Reaction.objects.all()
    for reaction in reaction_list:
        reaction.score = 0
        reaction.save()

    rating_list = Rating.objects.all()
    for rating in rating_list:
        reaction = Reaction.objects.get(pk=rating.reaction.pk)
        if rating.rating == 'G':
            reaction.score += 2
        else:
            reaction.score += 1
        reaction.save()

def calculate_score(reaction):
    rating_list = Rating.objects.filter(reaction=reaction)
    for rating in rating_list:
        reaction = Reaction.objects.get(pk=rating.reaction.pk)
        if rating.rating == 'G':
            reaction.score += 2
        else:
            reaction.score += 1
        reaction.save()
