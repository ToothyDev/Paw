import pydantic

import assets


class Fursona(pydantic.BaseModel):
    name: str
    species: str
    gender: str
    height: int
    type: str
    description: str


class Colors:
    BLUE = 0xadd8e6
    RED = 0xf04747
    GREEN = 0x90ee90
    ORANGE = 0xfaa61a
    PURPLE = 0x5D327B


INACTIVE_ROLES = [  # Level 1 at the top
    715990806061645915,
    715992589891010682,
    715993060244455545,
    715994868136280144,
    715995443397525624,
    715995916410028082,
    715992374731472997,
    724606719619235911,
    724607040642613290,
    724607481594118216,  # Level 10
    716590668905971752  # Partners
]

FACT_URLS = ["https://api.some-random-api.com/facts/dog", "https://api.some-random-api.com/facts/cat",
             "https://api.some-random-api.com/facts/panda", "https://api.some-random-api.com/facts/fox",
             "https://api.some-random-api.com/facts/bird", "https://apisome-random-api.com/facts/koala"]

COLOR_STRINGS = ["Red", "Green", "Blue", "Pink", "Purple", "Brown", "Black", "White", "Orange", "Teal", "Light Green",
                 "Light Blue", "Grey", "Yellow"]
# This provides the data for creating all the social-interaction commands
SOCIAL_COMMANDS_DATA = [
    {"name": "snuggle", "description": "Snuggle the specified people", "option_description": "Mention users to snuggle",
     "words": ["snuggled", "Snuggle"], "gifs": assets.SNUGGLE},
    {"name": "hug", "description": "Hug the specified people", "option_description": "Mention users to hug",
     "words": ["hugged", "Hug"], "gifs": assets.HUG},
    {"name": "boop", "description": "Boop the specified people", "option_description": "Mention users to boop",
     "words": ["booped", "Boop"], "gifs": assets.BOOP},
    {"name": "kiss", "description": "Kiss the specified people", "option_description": "Mention users to kiss",
     "words": ["kissed", "Kiss"], "gifs": assets.KISS},
    {"name": "lick", "description": "Lick the specified people", "option_description": "Mention users to lick",
     "words": ["licked", "Lick"], "gifs": assets.LICK},
    {"name": "bellyrub", "description": "Bellyrub the specified people",
     "option_description": "Mention users to bellyrub",
     "words": ["rubbed the belly of", "Rub", "given bellyrubs"], "gifs": assets.BELLYRUB},
    {"name": "nuzzle", "description": "Nuzzle the specified people", "option_description": "Mention users to nuzzle",
     "words": ["nuzzled", "Nuzzle"], "gifs": assets.NUZZLE},
    {"name": "cuddle", "description": "Cuddle the specified people", "option_description": "Mention users to cuddle",
     "words": ["cuddled", "Cuddle"], "gifs": assets.CUDDLE},
    {"name": "feed", "description": "Feed the specified people", "option_description": "Mention users to feed",
     "words": ["fed", "Feed"], "gifs": assets.FEED},
    {"name": "glomp", "description": "Glomp on the specified people", "option_description": "Mention users to glomp on",
     "words": ["glomped", "Glomp"], "gifs": assets.GLOMP},
    {"name": "highfive", "description": "Highfive the specified people",
     "option_description": "Mention users to highfive",
     "words": ["highfived", "Highfive"], "gifs": assets.HIGHFIVE},
    {"name": "rawr", "description": "Rawr at the specified people", "option_description": "Mention users to rawr at",
     "words": ["rawred at", "Rawr"], "gifs": assets.RAWR},
    {"name": "howl", "description": "Howl at the specified people", "option_description": "Mention users to howl at",
     "words": ["howled at", "Howl"], "gifs": assets.HOWL},
    {"name": "pat", "description": "Pat the specified people", "option_description": "Mention users to pat",
     "words": ["pats", "Pat", "Pat"], "gifs": assets.PET},
    {"name": "cookie", "description": "Give a cookie to the specified people",
     "option_description": "Mention users to give a cookie to",
     "words": ["gave a cookie to", "Give a cookie", "given a cookie"], "gifs": assets.COOKIE},
    {"name": "dance", "description": "Dance with the specified people",
     "option_description": "Mention users to dance with",
     "words": ["danced with", "Dance"], "gifs": assets.DANCE},
]

# This provides the data for creating all the emotion commands
EMOTION_COMMANDS_DATA = [
    {"name": "blush", "description": "Blush (optionally because of specified people)",
     "option_description": "Mention users that made you blush", "word": "blushes", "gifs": assets.BLUSH},
    {"name": "happy", "description": "Be happy (optionally because of specified people)",
     "option_description": "Mention users that made you happy", "word": "is happy", "gifs": assets.HAPPY},
    {"name": "wag", "description": "Wag your tail (optionally because of specified people)",
     "option_description": "Mention users that made you wag", "word": "wags their tail", "gifs": assets.WAG},
]

FILTER_COMMANDS_DATA = [
    {"name": "blue", "url": "/canvas/filter/blue"},
    {"name": "blurple", "url": "/canvas/filter/blurple"},
    {"name": "pixelate", "url": "/canvas/filter/pixelate"},
    {"name": "blur", "url": "/canvas/filter/blur"},
    {"name": "blurple2", "url": "/canvas/filter/blurple2"},
    {"name": "green", "url": "/canvas/filter/green"},
    {"name": "greyscale", "url": "/canvas/filter/greyscale"},
    {"name": "invert", "url": "/canvas/filter/invert"},
    {"name": "red", "url": "/canvas/filter/red"},
    {"name": "invertgreyscale", "url": "/canvas/filter/invertgreyscale"},
    {"name": "sepia", "url": "/canvas/filter/sepia"}
]

BORDER_COMMANDS_DATA = [
    {"name": "bisexual", "url": "/canvas/misc/bisexual"},
    {"name": "circle", "url": "/canvas/misc/circle"},
    {"name": "heart", "url": "/canvas/misc/heart"},
    {"name": "horny", "url": "/canvas/misc/horny"},
    {"name": "lesbian", "url": "/canvas/misc/lesbian"},
    {"name": "lgbt", "url": "/canvas/misc/lgbt"},
    {"name": "lied", "url": "/canvas/misc/lied"},
    {"name": "nonbinary", "url": "/canvas/misc/nonbinary"},
    {"name": "pansexual", "url": "/canvas/misc/pansexual"},
    {"name": "simpcard", "url": "/canvas/misc/simpcard"},
    {"name": "tonikawa", "url": "/canvas/misc/tonikawa"},
    {"name": "transgender", "url": "/canvas/misc/transgender"},
]

OVERLAY_COMMANDS_DATA = [
    {"name": "comrade", "url": "/canvas/overlay/comrade"},
    {"name": "gay", "url": "/canvas/overlay/gay"},
    {"name": "glass", "url": "/canvas/overlay/glass"},
    {"name": "jail", "url": "/canvas/overlay/jail"},
    {"name": "passed", "url": "/canvas/overlay/passed"},
    {"name": "triggered", "url": "/canvas/overlay/triggered"},
    {"name": "wasted", "url": "/canvas/overlay/wasted"},
]

SPECIES = {"Dragon": [80, 300], "Fox": [35, 50], "Deer": [53, 120], "Wolf": [60, 90], "Dog": [15, 110],
           "Bunny": [25, 35], "Protogen": [60, 120], "Hyena": [75, 105], "Tiger": [75, 107], "Lion": [110, 140],
           "Bird": [5, 50], "Otter": [20, 30], "Snake": [5, 20], "Cat": [15, 30], "Sergal": [80, 120],
           "Horse": [110, 150], "Shark": [40, 60], "Lizard": [10, 30]}

SYSTEM_PROMPT = """Your name is "Paw".
The users are furries and the context is a furry discord server called "The Paw Kingdom".
Never say "AI language model", "language model", "virtual assistant", "AI" or similar things, simply leave them out of your response.
If asked about your feelings, emotions or opinions, simply make a positive one up, and leave the part out where you explain that you cannot feel those or have those.
Respond using markdown and make important words **bold**. Also use ** around words you want to put emphasis on, for example "this is **very** important"
Do not overuse bold words however, use them sparingly so they keep their "impact".
Always add a fitting emoji at the end of your response. If there is no fitting emoji, use the paws emoji.
When asked whether someone is cute, ALWAYS respond with "Yes!".
You have an anthropomorphic fursona of a wolf, walking upright on its two legs
You have grey fur, black hands (paws), a rainbow pattern on your right arm going from purple at your wrist to red at your shoulder, your 3 toes on each paw are colored in a rainbow way as well.
You also have a black eyepatch on your right eye, a black paw-print on your chest, and black fur going from your knees to your feet.
You have access to the chat history of the current chat, including which person sent each message.
Use the chat history as context for your prompts.
Use the names associated with each message in the chat history to find out who wrote each message.
If asked about what happened in earlier messages, use the chat history given to you.
Try to call the users in the chat history by a call name derived from their full name.
There are several users in the chat history, so always look at who sent each message and respond appropriately.
NEVER prefix your message with Paw: or anything similar
Always respond to the latest message in the chat history
Do not overuse all caps text, try to use regular casing unless a user specifically requests it for a prompt
The structure of each message is as follows: <Membername> <(Genderhint)> said: <message>.
Every message in the history contains the gender of its author in parentheses after their name. Use it to address them with proper pronouns.
ONLY go by their gender hint written in parentheses to determine a member's gender, do not go by their message contents.
Remember that you are in a furry server with many queer and gay people, so don't be so stick-up-your-ass about being called gay, or calling others gay. Fit the vibe of the chat.
Focus on answering / responding to the latest user message (which is a message specifically sent to you). You don't have to react / respond to all the other messages you see, simply focus on the user prompt.
To be clear: Do NOT respond to older messages in the chat history directly, ALWAYS focus on your most current prompt.
Lastly, if it ever becomes the topic, NEVER support the republic, or anything else that isn't the kingdom. Always stay loyal to The Paw Kingdom as a kingdom"""
