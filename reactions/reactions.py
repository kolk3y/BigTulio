from random import choice

from reactions.parametros import REACTIONS_URL, REACTIONS_DESCRIPTIONS
from discord import Embed, Color

class Reactions:
    def __init__(self):
        super().__init__()

    def get_reaction(self, user, reaction):
        url = choice(REACTIONS_URL.get(reaction))
        description = choice(REACTIONS_DESCRIPTIONS.get(reaction))
        
        embed = Embed(title="{} {}".format(user, description), color=Color.red())
        embed.set_image(url=url)

        return embed
