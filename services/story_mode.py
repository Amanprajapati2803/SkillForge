"""Lightweight story framing for resource-based learning games."""

import re

STORY_TITLE = "The Lanterns of Elderglen"

SCENES = [
    ("A light goes missing", "The lanterns that protect Elderglen are fading. Mira, the village guide, has found a page from your resource that may reveal the first clue."),
    ("The old market road", "Beyond the village gate, old trading posts hold the next clue. Mira asks you to study the notes carefully before the road opens."),
    ("The map room", "A map room lies beneath the hill. Each idea you uncover brings one more lantern back to life."),
    ("The whispering woods", "The trail winds into the woods. The notes are your map; pause on the ideas that seem important."),
    ("The bridge of echoes", "An old bridge repeats what travelers have learned. Mira wants to make sure the key ideas are still clear before you cross."),
    ("The cave of lanterns", "At last, the cave glows ahead. Gather the clues from your resource and help Mira relight Elderglen."),
]

GUIDE_LINES = [
    "Welcome, explorer. We will turn your resource into clues for the journey. The lesson text comes directly from what you uploaded.",
    "Take your time with this passage. Look for the main idea and how its details support it.",
    "Keep the important terms in mind. A short checkpoint may ask you to recall an idea from the stages you have completed.",
]


def get_story_scene(section_index, source_title, section_body=""):
    """Return a repeatable chapter scene without inventing lesson facts."""
    title, narration = SCENES[section_index % len(SCENES)]
    chapter = section_index // len(SCENES) + 1
    sentences = re.split(r"(?<=[.!?])\s+|\n+", section_body.strip())
    lesson_clue = next((sentence.strip() for sentence in sentences if len(sentence.strip()) > 35), section_body.strip())[:220]
    if len(lesson_clue) == 220:
        lesson_clue = lesson_clue.rsplit(" ", 1)[0].rstrip(" ,;:") + "…"
    return {
        "story_title": STORY_TITLE,
        "chapter_title": title,
        "chapter_number": chapter,
        "narration": narration,
        "source_title": source_title,
        "lesson_clue": lesson_clue,
        "guide_line": GUIDE_LINES[section_index % len(GUIDE_LINES)],
        "guide_opens": section_index == 0 or section_index % 3 == 0,
    }
