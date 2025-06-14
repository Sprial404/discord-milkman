"""
This module contains the constants for the bot, including the color constants.
"""

OWNER_COG_NAME = "owner"
GENERAL_COG_NAME = "general"
REACTION_ROLES_COG_NAME = "reaction_roles"
MODERATION_COG_NAME = "moderation"
FUN_COG_NAME = "fun"
TEMPORARY_VOICE_COG_NAME = "temporary_voice"

SUCCESS_COLOR = 0xBEBEFE
ERROR_COLOR = 0xE02B2B

TEMPORARY_VOICE_CHANNEL_NAME = "🕳️ Blackhole"

LYRICS_API_URL = "https://api.lyrics.ovh/v1/{artist}/{title}"

AVATAR_QUOTES = [
    """
    **Moat**: It is hard to fill a cup that is already full.\n
    **Jake Sully**: My cup is empty. Trust me. Just ask Dr. Augustine. I'm no scientist.\n
    **Moat**: Then what are you?\n
    **Jake Sully**: I was a marine. A warrior... of the uh... Jarhead Clan.
    """,
    """
    **Mo'at**: It is decided. My daughter will teach you our ways. Learn well, "Jakesully", and we will see if your insanity can be cured.    
    """,
    """
    **Neytiri**: Eywa has heard you... Eywa has heard you!    
    """,
    """
    *[Grace and Jake spot a Hammerhead Titanothere]*
    **Dr. Grace Augustine**: Don't shoot! Don't shoot. You'll piss him off.\n
    **Jake Sully**: It's already pissed off.\n
    **Dr. Grace Augustine**: Jake, that armor's too thick. Trust me. It's a territorial threat display. Do not run or he'll charge.\n
    **Jake Sully**: What do I do? Dance with it?\n
    **Dr. Grace Augustine**: Just hold your ground.\n
    *[the Hammerhead Titanothere charges and Jake runs towards him and yells to scare him. The Titanothere runs away once seeing the Thanator]*\n
    **Jake Sully**: Ha, ha! Yeah, come on! What you got! Oh yeah, who's bad? That's right. Yeah, that's what I'm talkin' about, bitch. That's right, get your punk ass back to mommy. Yeah? Yeah, you got nothin'. You keep runnin'. Why don't you bring some of your friends, huh?\n
    *[Turns around and sees an angry Thanator standing in front of him]*\n
    **Jake Sully**: *[to Grace]* What about this one? Run? Don't run? What?\n
    **Dr. Grace Augustine**: Run! Definitely run!
    """,
    """
    **Dr. Grace Augustine**: So you just figured you'd come here, to the most hostile environment known to men, with no training of any kind, and see how it went? What was going through your head?\n
    **Jake Sully**: Maybe I was sick of doctors telling me what I couldn't do.
    """,
    """
    **Neytiri**: Now you choose your ikran. This you must feel inside. If he also chooses you, move quick like I showed. You will have one chance, Jake.
    **Jake Sully**: How will I know if he chooses me?\n
    **Neytiri**: He will try to kill you.\n
    **Jake Sully**: *[deadpan]* Outstanding.
    """,
    """
    **Jake Sully**: *[Narrating]* Sometimes your whole life boils down to one insane move.
    """,
    """
    **Neytiri**: I'm with you now, Jake. We are mated for life.\n
    **Jake Sully**: *[to himself]* What the hell are you doin', Jake?
    """,
    """
    **Dr. Grace Augustine**: Just relax and let your mind go blank. That shouldn't be too hard for you.\n
    **Jake Sully**: Kiss the darkest part of my lily white...\n
    *[gets cut off]*
    """,
    """
    **Jake Sully**: *[Narrating]* In cryo, you don't dream at all. It doesn't *feel* like six years - more like a fifth of Tequila and an ass kicking.\n
    **Jake Sully**: Are we there yet?\n
    **Cryo Vault Med Tech**: Yeah, we're there sunshine... We're there.\n
    *[Scene changes to morgue]*\n
    **Suit #2**: It's about your brother...\n
    **Jake Sully**: *[Narrating]* So a week before he was about to ship out... a guy with a gun ends his journey... for the paper in his wallet.\n
    **Cryo Vault Med Tech**: You've been in cryo for five years, nine months and twenty-two days. You will be hungry, you will be weak. If you feel nausea, please use the...\n
    **Jake Sully**: *[Narrating]* Yeah, Tommy was the scientist. Me? I'm just another dumb grunt goin' some place he's gonna regret.
    """,
    """
    **Dr. Grace Augustine**: Don't play with that. You'll go blind.
    """,
    """
    **Jake Sully**: Give it up, Quaritch! It's all over.\n
    **Col. Quaritch**: *[from inside the Amp suit]* Nothin's over while I'm breathin'.\n
    **Jake Sully**: I kinda hoped you'd say that.
    """,
    """
    **Trudy Chacon**: I was hoping for some kind of tactical plan that didn't involve martyrdom.
    """,
    """
    **Jake Sully**: *[to Grace when she interrupts his video log recording to give some extra explanation]* Excuse me, this is my video log here.
    """,
    """
    **Jake Sully**: You wanted to see me, Colonel?\n
    **Col. Quaritch**: This low gravity'll make you soft. And when you get soft, Pandora will eat you and shit you out dead with zero warning.\n
    **Jake Sully**: I read your file, Corporal. Venezuela, that was some mean bush. Nothin' like that here, though. You got some heart, kid, showin' up here.\n
    **Jake Sully**: Figured it was just another hellhole.
    """,
    """
    **Dr. Max Patel**: Grace, this is Jake Sully.\n
    **Jake Sully**: Ma'am.\n
    **Dr. Grace Augustine**: Yeah, yeah, I know who you are and I don't need you. I need your brother. You know, the PhD who trained for 3 years for this mission.\n
    **Jake Sully**: He's dead. I know it's a big inconvenience for everyone.\n
    **Dr. Grace Augustine**: How much lab training have you had?\n
    **Jake Sully**: I dissected a frog once.\n
    **Dr. Grace Augustine**: Ya see, ya see? They're just pissing on us without even giving us the courtesy of calling it rain. I'm going to Selfridge.\n
    **Dr. Max Patel**: Grace. No, I don't think...\n
    **Dr. Grace Augustine**: No, man, this is such bullshit! Gonna kick his corporate butt. He has no business sticking his nose in *my* department.
    """,
    """
    **Col. Quaritch**: *[addressing marines]* Everyone on this base, every one of you, is fighting for survival, and that's a fact.
    There's an aboriginal horde out there massing for an attack. These orbital images tell me that the hostile numbers have gone from a few hundred,
    to well over two thousand in one day. And more are pourin' in. In a week's time there could be 20,000 of 'em. At that point they will overrun our perimeter.
    That's not gonna happen. Our only security lies in preemptive attack. We will fight terror with terror.
    The hostiles believe that this mountain territory is protected by their... deity. And when we destroy it, we will blast a crater in their racial memory so deep,
    that they won't come within 1,000 klicks of this place ever again. And that, too, is a fact.
    """,
    """
    **Col. Quaritch**: You are not in Kansas anymore. You are on Pandora, ladies and gentlemen. Respect that fact every second of every day. If there is a Hell, you might wanna go there for some R & R after a tour on Pandora. Out there beyond that fence every living thing that crawls, flies, or squats in the mud wants to kill you and eat your eyes for jujubes. We have an indigenous population of humanoids called the Na'vi. They're fond of arrows dipped in a neurotoxin that will stop your heart in one minute - and they have bones reinforced with naturally occurring carbon fiber. They are very hard to kill. As head of security, it is my job to keep you alive. I will not succeed. Not with all of you. If you wish to survive, you need to cultivate a strong, mental aptitude. You got to obey the rules: Pandora rules. Rule number one...
    """,
]

SLAP_IMAGES = [
    "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExbW4yYWR6NWZ3eDhjZHIyeXVjMDM1NGNwN2tscTIzdHZrY2I1Z2VpYyZlcD12MV9naWZzX3NlYXJjaCZjdD1n/vxvNnIYFcYqEE/giphy.gif",
    "https://media4.giphy.com/media/v1.Y2lkPTc5MGI3NjExamNjdDN6cDh1anlhd3Y3YTM5Njc3djlhNzQ0ZXUwOHZ3aXFqODhveiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/lX03hULhgCYQ8/giphy.gif",
    "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExbW4yYWR6NWZ3eDhjZHIyeXVjMDM1NGNwN2tscTIzdHZrY2I1Z2VpYyZlcD12MV9naWZzX3NlYXJjaCZjdD1n/xT8qB7Sbwskk27Rdy8/giphy.gif",
    "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExbW4yYWR6NWZ3eDhjZHIyeXVjMDM1NGNwN2tscTIzdHZrY2I1Z2VpYyZlcD12MV9naWZzX3NlYXJjaCZjdD1n/3XlEk2RxPS1m8/giphy.gif",
    "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExbW4yYWR6NWZ3eDhjZHIyeXVjMDM1NGNwN2tscTIzdHZrY2I1Z2VpYyZlcD12MV9naWZzX3NlYXJjaCZjdD1n/RrLbvyvatbi36/giphy.gif",
    "https://media.giphy.com/media/3oEdvdHf6n0US87Tri/giphy.gif?cid=ecf05e47ge0ki71i0ke0in7xqt5wmhc3nw2tj5cy1vss9z92&ep=v1_gifs_search&rid=giphy.gif&ct=g",
    "https://media.giphy.com/media/wXgBk2fM696gM/giphy.gif?cid=ecf05e47ge0ki71i0ke0in7xqt5wmhc3nw2tj5cy1vss9z92&ep=v1_gifs_search&rid=giphy.gif&ct=g",
    "https://media.giphy.com/media/HMyn96bq0nsw8/giphy.gif?cid=ecf05e47e57gjypfzcmq82dles78tvt219aqk92czhnnpvf2&ep=v1_gifs_search&rid=giphy.gif&ct=g",
    "https://media.giphy.com/media/xTiTndZXxiBqFZM7E4/giphy.gif?cid=ecf05e4739yuwt1i8hqhoppqmozjw6rtpeszvfc5z1dke91r&ep=v1_gifs_search&rid=giphy.gif&ct=g",
    "https://media.giphy.com/media/qyjexFwQwJp9yUvMxq/giphy.gif?cid=ecf05e47yoa0ly67hynwcqu6elufvjhh4en6nec1hkn42hqi&ep=v1_gifs_search&rid=giphy.gif&ct=g",
    "https://media.giphy.com/media/AisOYaOZdrS1i/giphy.gif?cid=ecf05e4785igoy1bqcfy227om1i0e7he2qz4rd1r375r3ftr&ep=v1_gifs_search&rid=giphy.gif&ct=g",
    "https://media.giphy.com/media/vcShFtinE7YUo/giphy.gif?cid=ecf05e471gflj7w1bmb6dp42wm4oeebhxm7e2xqd6sdcvfum&ep=v1_gifs_search&rid=giphy.gif&ct=g",
    "https://media.giphy.com/media/nbPw0YmzhdqFm6iOfh/giphy.gif?cid=ecf05e471gflj7w1bmb6dp42wm4oeebhxm7e2xqd6sdcvfum&ep=v1_gifs_search&rid=giphy.gif&ct=g",
    "https://media.giphy.com/media/xT1R9JQ1jUDoF4Ou64/giphy.gif?cid=ecf05e47djs4b1nezacy7pocjxueerlsra9lbk3ve347gqa9&ep=v1_gifs_search&rid=giphy.gif&ct=g",
    "https://media.giphy.com/media/PaC0wbFRxWCkawaNBE/giphy.gif?cid=ecf05e47geecoaawbljr1qnv2il00oh6neobl3ksq4xbd66b&ep=v1_gifs_search&rid=giphy.gif&ct=g",
    "https://media.giphy.com/media/l0IsGT7beaIsHaDv2/giphy.gif?cid=ecf05e47geecoaawbljr1qnv2il00oh6neobl3ksq4xbd66b&ep=v1_gifs_search&rid=giphy.gif&ct=g",
    "https://media.giphy.com/media/ibd2V1YKF8kKVQzPnH/giphy.gif?cid=ecf05e47hvgg6kq6dy4rem06knlbqshye4dosyp8gq98rwwr&ep=v1_gifs_search&rid=giphy.gif&ct=g",
    "https://tenor.com/view/squid-game-slap-slapped-kek-or-cringe-famouszaggy-gif-23535390",
]
