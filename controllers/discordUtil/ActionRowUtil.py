from util import GenreUtil, DateUtil
from data.MovieData import MovieData
from typing import List
from interactions import EmbedFooter, ActionRow, Button, ButtonStyle, PartialEmoji
import interactions


def create_source_buttons(s: List) -> ActionRow:
    s.sort(key=lambda x: x['seeds'], reverse=True)
    action_row = ActionRow()
    for source in s:
        action_row.add_component(Button(
            style=ButtonStyle.URL,
            label=f"{source['quality']}: {str(source['seeds'])} Seeds",
            url=source['url'],
            emoji=PartialEmoji(name="🔗"),
        ))

    return action_row


def create_movie_buttons() -> ActionRow:
    add_emoji = PartialEmoji.from_str("➕")
    add = interactions.Button(label="Add Movie", style=interactions.ButtonStyle.GREEN, custom_id='add_to_list',
                              emoji=add_emoji)
    eye_emoji = PartialEmoji.from_str("👁️")
    watched = interactions.Button(label="Watch", style=interactions.ButtonStyle.BLUE, custom_id='add_to_watched',
                                  emoji=eye_emoji)
    action_row = ActionRow(add, watched)
    return action_row


def create_movie_list_buttons() -> ActionRow:
    eye_emoji = PartialEmoji.from_str("👁️")
    watched = interactions.Button(label="Watch", style=interactions.ButtonStyle.BLUE, custom_id='add_to_watched',
                                  emoji=eye_emoji)
    vote_emoji = PartialEmoji.from_str("🗳️")
    vote_button = interactions.Button(
        label="+ Vote",
        style=interactions.ButtonStyle.GREY,
        custom_id='add_to_vote_list',
        emoji=vote_emoji)

    action_row = ActionRow(watched, vote_button)
    return action_row


def create_vote_button() -> ActionRow:
    vote_emoji = PartialEmoji.from_str("📨")
    vote_button = interactions.Button(
        label="Rank Movies",
        style=interactions.ButtonStyle.BLURPLE,
        custom_id='start_ranking',
        emoji=vote_emoji)

    action_row = ActionRow(vote_button)
    return action_row
