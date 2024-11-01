def handle_response(text: str) -> str:
    processed: str = text.lower()
    if 'hello' == processed:
        return 'Hey there'
    if 'how are you' == processed:
        return 'I am good'
    
   