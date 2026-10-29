import html
import random
import re
from io import BytesIO
from pathlib import Path

STOP_WORDS = {
    "about", "after", "again", "against", "also", "among", "because", "before", "being",
    "between", "could", "every", "first", "from", "have", "into", "itself", "other", "over",
    "same", "should", "since", "some", "such", "than", "that", "their", "there", "these",
    "thing", "this", "those", "through", "under", "until", "using", "very", "what", "when",
    "where", "which", "while", "with", "would", "your", "will", "them", "then", "they",
    "were", "been", "more", "most", "must", "make", "made", "does", "each", "only", "like",
    "many", "much", "once", "upon", "shall", "able", "are", "was", "for", "and", "the",
    "you", "not", "but", "can", "all", "any", "has", "had", "her", "his", "our", "out",
    "its", "may", "use", "how", "why", "who", "she", "him",
}


def extract_text(filename, payload):
    """Extract readable text from supported upload formats."""
    suffix = Path(filename or "").suffix.lower()
    if suffix in {".txt", ".md", ".markdown"}:
        return payload.decode("utf-8-sig", errors="replace")
    if suffix == ".pdf":
        try:
            from pypdf import PdfReader
        except ImportError as exc:
            raise ValueError("PDF support needs pypdf. Install the project requirements and try again.") from exc
        try:
            reader = PdfReader(BytesIO(payload))
            return "\n\n".join(page.extract_text() or "" for page in reader.pages)
        except Exception as exc:
            raise ValueError("I couldn't read that PDF. Try a text-based PDF or upload a .txt/.md file.") from exc
    raise ValueError("Upload a .txt, .md, .markdown, or .pdf resource.")


def _clean_text(text):
    text = html.unescape(text).replace("\x00", " ")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n\s*\n\s*\n+", "\n\n", text)
    return text.strip()


def _split_sections(text):
    blocks = [part.strip() for part in re.split(r"\n\s*\n", text) if part.strip()]
    if len(blocks) < 2:
        blocks = [part.strip() for part in re.split(r"(?<=[.!?])\s+(?=[A-Z0-9#])", text) if part.strip()]

    sections = []
    current = []
    current_length = 0
    for block in blocks:
        if len(block) > 1500:
            sentences = re.split(r"(?<=[.!?])\s+", block)
            pieces, piece = [], ""
            for sentence in sentences:
                if piece and len(piece) + len(sentence) > 1200:
                    pieces.append(piece.strip())
                    piece = ""
                piece = f"{piece} {sentence}".strip()
            if piece:
                pieces.append(piece.strip())
        else:
            pieces = [block]

        for piece in pieces:
            if current and current_length + len(piece) > 1600:
                sections.append("\n\n".join(current))
                current, current_length = [], 0
            current.append(piece)
            current_length += len(piece)
    if current:
        sections.append("\n\n".join(current))
    return sections


def _words(text):
    return re.findall(r"[A-Za-z][A-Za-z0-9+#.-]{2,}", text)


def build_game(text):
    """Turn source text into study stages and source-grounded cloze questions."""
    text = _clean_text(text)
    if len(text) < 120:
        raise ValueError("This resource is too short to build a lesson. Upload at least a short paragraph of text.")
    sections = _split_sections(text)
    if not sections:
        raise ValueError("I couldn't find readable lesson sections in that resource.")

    words = _words(text)
    frequencies = {}
    for word in words:
        key = word.lower().strip(".-")
        if len(key) >= 4 and key not in STOP_WORDS:
            frequencies[key] = frequencies.get(key, 0) + 1
    distractors = sorted(frequencies, key=lambda item: (-frequencies[item], item))

    questions = []
    used_answers = set()
    for section_index, section in enumerate(sections):
        section_question_count = 0
        seen_sentences = set()
        sentences = re.split(r"(?<=[.!?])\s+|\n+", section)
        for sentence in sentences:
            sentence = sentence.strip(" -*#\t")
            if not sentence or sentence in seen_sentences:
                continue
            seen_sentences.add(sentence)
            tokens = _words(sentence)
            candidates = [word for word in tokens if len(word.strip(".-")) >= 5 and word.lower().strip(".-") not in STOP_WORDS]
            if len(tokens) < 8 or not candidates:
                continue
            unused_candidates = [word for word in candidates if word.lower().strip(".-") not in used_answers]
            answer = max(unused_candidates or candidates, key=lambda word: (min(len(word), 14), frequencies.get(word.lower().strip(".-"), 0)))
            answer_key = answer.lower().strip(".-")
            question_text = re.sub(re.escape(answer), "_____", sentence, count=1, flags=re.IGNORECASE)
            choices = [answer]
            for choice in distractors:
                if choice != answer_key and choice.lower() not in {item.lower() for item in choices}:
                    choices.append(choice)
                if len(choices) == 4:
                    break
            if len(choices) < 3:
                continue
            random.SystemRandom().shuffle(choices)
            questions.append({
                "prompt": question_text,
                "options": choices,
                "answer_index": choices.index(answer),
                "section_index": section_index,
            })
            used_answers.add(answer_key)
            section_question_count += 1
            if section_question_count >= 3 or len(questions) >= 12:
                break
        if len(questions) >= 12:
            break

    if not questions:
        raise ValueError("I made study stages, but couldn't build reliable quiz questions from this text. Try a resource with complete explanatory sentences.")

    return [{"title": f"Stage {index + 1}", "body": section} for index, section in enumerate(sections)], questions
