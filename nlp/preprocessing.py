import re
from typing import Tuple

def normalize_text(text: str) -> str:
    if not text:
        return ""
    text = re.sub(r"\s+", " ", text)
    return text.strip()

def remove_urls(text: str) -> str:
    if not text:
        return ""
    return re.sub(r"https?://\S+|www\.\S+", " ", text)

def remove_html_tags(text: str) -> str:
    if not text:
        return ""
    return re.sub(r"<.*?>", " ", text)

def remove_publisher_datelines(text: str) -> str:
    if not text:
        return ""
    text = re.sub(r"^[A-Z\s,]+(?:\s*\([A-Za-z\s]+\)\s*)?\s*[-–—]{1,2}\s*", " ", text)
    text = re.sub(r"\(reuters\)", " ", text, flags=re.IGNORECASE)
    text = re.sub(r"\breuters\b", " ", text, flags=re.IGNORECASE)
    text = re.sub(r"\bassociated press\b", " ", text, flags=re.IGNORECASE)
    return text

def remove_scraping_artifacts(text: str) -> str:
    if not text:
        return ""
    text = re.sub(r"\[(?:video|image|photo|audio|graphic)\]", " ", text, flags=re.IGNORECASE)
    text = re.sub(r"\((?:video|image|photo|audio|graphic)\)", " ", text, flags=re.IGNORECASE)
    text = re.sub(r"\bfeatured image via\b.*", " ", text, flags=re.IGNORECASE)
    text = re.sub(r"\bimage via\b.*", " ", text, flags=re.IGNORECASE)
    text = re.sub(r"\bread more:?.*", " ", text, flags=re.IGNORECASE)
    text = re.sub(r"\bwatch (?:the )?video\b.*", " ", text, flags=re.IGNORECASE)
    return text

def remove_extra_symbols(text: str) -> str:
    if not text:
        return ""
    return re.sub(r"[^\w\s.,!?;:'\"%()\-]", " ", text)

def clean_news_text(text: str) -> str:
    if not text or not isinstance(text, str):
        return ""
    
    text = remove_urls(text)
    text = remove_html_tags(text)
    text = remove_publisher_datelines(text)
    text = remove_scraping_artifacts(text)
    text = remove_extra_symbols(text)
    text = normalize_text(text)
    
    return text.lower()

def clean_text(text: str) -> str:
    return clean_news_text(text)

def validate_input(text: str, min_words: int = 3, min_chars: int = 15) -> Tuple[bool, str]:
    if not text or not isinstance(text, str):
        return False, "Input is empty. Please provide a news headline or article to verify."
    
    stripped = text.strip()
    if not stripped:
        return False, "Input consists solely of whitespace. Please provide text to verify."
    
    content_only = re.sub(r"https?://\S+|www\.\S+|[^\w\s]", "", stripped).strip()
    if not content_only:
        return False, "Input contains only URLs or special symbols with no meaningful text."
    
    if re.fullmatch(r"[\d\s.,]+", stripped):
        return False, "Input contains only numbers. Please provide a factual claim or news article."
    
    words = content_only.split()
    if len(words) < min_words or len(stripped) < min_chars:
        return False, f"Input is too short ({len(words)} words). Please enter at least {min_words} words for meaningful analysis."
    
    return True, ""
