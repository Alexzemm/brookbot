import random

def eb():
    texts = ["yes", "certainly", "indeed", "obviously", "sure", "of course", "yes nigga", "is that even a question?",
                 "maybe", "probably", "I guess", "could happen", "who knows", "maybe in your dreams",
                 "no", "no way", "never", "of course not", "you think that'll ever happen?", "haha", "no gaesaekkya",
                 "your mom", "no nigga", "jjot kka", "in your dreams", "keep dreaming", "are you crazy?", "ask ur mom",
                 "maybe in a parallel universe", "lol nice joke sadly i can't laugh cuz i'm a bot", "cope lol",
                 "I love you", "hoiyaaaaa", "don't let your dreams be dreams 🙏", "why would you ask that ㅠㅠ", "gaesaekki",
                 "die", "good idea", "bad idea", "do you wanna die?", "fuck you", "fuck off", "why not 😳", "😳😳", "😏😏",
                 "its cute you think that", "huh???", "seriously nigga?", "idk but can I see your panties??", "based", "not based"]

    emojis = ["😏😏", "🤣🤣", "😒😒", "🤓🤓", "😳😳", "🥺🥺", "😀😀", "😉😉", "🤥🤥", "💀💀", "🤬🤬", "🤡🤡", "💩💩", "👀👀",
              "🙃🙃", "🥰🥰", "☺☺", "😋😋", "😔😔", "🥵🥵", "😢😢", "😭😭", "😩😩", "😤😤", "❤️‍🔥❤️‍🔥", "❤❤", "💔💔", "💕💕",
              "👍👍", "✨✨", "😁😁", "😆😆", "🙂🙂", "😍😍", "😚😚", "🤭🤭", "🙏🙏", "🤔🤔", "😑😑", "🙄🙄", "😌😌", "🤮🤮",
              "😵‍💫😵‍💫", "😮😮", "😱😱", "💦💦", "🗿"]

    response = random.choice(texts) + " " + random.choice(emojis)

    return response
