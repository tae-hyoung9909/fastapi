def truncate_text(text, max_length=150):
    if text is not None:
        if len(text) > max_length:
            return text[:max_length] + "..."
        else:
            return text