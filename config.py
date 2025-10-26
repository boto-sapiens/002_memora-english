import os
from dotenv import load_dotenv

load_dotenv()

# Bot configuration
BOT_TOKEN = os.getenv("BOT_TOKEN")
TIMEZONE = os.getenv("TIMEZONE", "Asia/Bangkok")
DATA_DIR = os.getenv("DATA_DIR", "data")
CHECK_INTERVAL = int(os.getenv("CHECK_INTERVAL", "300"))  # 5 minutes

# ANKI intervals in seconds
INTERVALS = [
    3600,      # 0: 1 час
    14400,     # 1: 4 часа
    86400,     # 2: 1 день
    259200,    # 3: 3 дня
    604800,    # 4: 7 дней
    1209600,   # 5: 14 дней
    2592000,   # 6: 30 дней
    5184000,   # 7: 60 дней
    7776000,   # 8: 90 дней
    15552000,  # 9: 180 дней
    31536000   # 10: 365 дней
]

# Default phrases for learning (with translations and transcriptions)
DEFAULT_PHRASES = [
    {
        "id": 1,
        "text_en": "Charming day it has been, Miss Fairfax.",
        "text_ru": "Какой чудесный сегодня день, мисс Фэрфакс.",
        "transcription": "[ˈʧɑːmɪŋ deɪ ɪt həz bin / mɪs ˈfeəfæks]",
        "audio_teacher": "1_myvoiceEarn.mp3",
        "audio_actor": "1_Earnest.mp3"
    },
    {
        "id": 2,
        "text_en": "Pray don't talk to me about the weather, Mr. Worthing.",
        "text_ru": "Прошу, не говорите со мной о погоде, мистер Уординг.",
        "transcription": "[preɪ dəʊnt tɔːk tə mi əˈbaʊt ðə ˈwɛðə / mɪstə ˈwɜːðɪŋ]",
        "audio_teacher": "2_myvoiceEarn.mp3",
        "audio_actor": "2_Earnest.mp3"
    },
    {
        "id": 3,
        "text_en": "Whenever people talk to me about the weather, I always feel quite certain that they mean something else.",
        "text_ru": "Когда люди говорят со мной о погоде, я всегда совершенно уверена, что они имеют в виду что-то другое.",
        "transcription": "[wɛˈnɛvə ˈpiːpᵊl tɔːk tə mi əˈbaʊt ðə ˈwɛðə / aɪ ˈɔːlweɪz fiːl kwaɪt ˈsɜːtn ðət ðeɪ miːn ˈsʌmθɪŋ ɛls]",
        "audio_teacher": "3_myvoiceEarn.mp3",
        "audio_actor": "3_Earnest.mp3"
    },
    {
        "id": 4,
        "text_en": "And that makes me so nervous.",
        "text_ru": "И это делает меня такой нервной.",
        "transcription": "[ənd ðæt meɪks mi səʊ ˈnɜːvəs]",
        "audio_teacher": "4_myvoiceEarn.mp3",
        "audio_actor": "4_Earnest.mp3"
    },
    {
        "id": 5,
        "text_en": "I do mean something else.",
        "text_ru": "Я и имею в виду что-то другое.",
        "transcription": "[aɪ dʊ miːn ˈsʌmθɪŋ ɛls]",
        "audio_teacher": "5_myvoiceEarn.mp3",
        "audio_actor": "5_Earnest.mp3"
    },
    {
        "id": 6,
        "text_en": "I thought so. In fact, I am never wrong.",
        "text_ru": "Я так и думала. Впрочем, я никогда не ошибаюсь.",
        "transcription": "[aɪ θɔːt səʊ // ɪn fæ.kt / aɪ əm ˈnɛvə rɒŋ]",
        "audio_teacher": "6_myvoiceEarn.mp3",
        "audio_actor": "6_Earnest.mp3"
    },
    {
        "id": 7,
        "text_en": "And I would like to be allowed to take advantage of Lady Bracknel's temporary absence...",
        "text_ru": "И я хотел бы воспользоваться временным отсутствием леди Брэкнелл…",
        "transcription": "[ənd aɪ wəd laɪ.k tə bi əˈlaʊd tə teɪ.k ədˈvɑːntɪʤ əv ˈleɪdi Bra.cknel's ˈtɛmpᵊrᵊri ˈæbsᵊns]",
        "audio_teacher": "7_myvoiceEarn.mp3",
        "audio_actor": "7_Earnest.mp3"
    },
    {
        "id": 8,
        "text_en": "I would certainly advise you to do so.",
        "text_ru": "Я бы вам это определённо посоветовала.",
        "transcription": "[aɪ wəd ˈsɜːtnli ədˈvaɪz jʊ tə dʊ səʊ]",
        "audio_teacher": "8_myvoiceEarn.mp3",
        "audio_actor": "8_Earnest.mp3"
    },
    {
        "id": 9,
        "text_en": "Mamma has a way of coming back suddenly into a room that I have often had to speak to her about.",
        "text_ru": "У мамы есть привычка внезапно возвращаться в комнату, и мне не раз приходилось говорить с ней об этом.",
        "transcription": "[məˈmɑː həz ə weɪ əv ˈkʌmɪŋ bæk ˈsʌdnli ˈɪntə ə ruːm ðət aɪ həv ˈɒfᵊn həd tə spiːk tə hər əˈbaʊt]",
        "audio_teacher": "9_myvoiceEarn.mp3",
        "audio_actor": "9_Earnest.mp3"
    },
    {
        "id": 10,
        "text_en": "Miss Fairfax, ever since I met you I have admired you more than any girl ... I have ever met since ... I met you.",
        "text_ru": "Мисс Фэрфакс, с тех пор как я встретил вас, я восхищался вами больше, чем любой девушкой… которую я когда-либо встречал с тех пор… как встретил вас.",
        "transcription": "[mɪs ˈfeəfæks / ˈɛvə sɪns aɪ mɛt jʊ / aɪ həv ədˈmaɪəd jʊ mɔː ðən ˈɛni ɡɜːl / aɪ həv ˈɛvə mɛt sɪns aɪ mɛt juː]",
        "audio_teacher": "10_myvoiceEarn.mp3",
        "audio_actor": "10_Earnest.mp3"
    },
    {
        "id": 11,
        "text_en": "Yes, I am quite well aware of the fact.",
        "text_ru": "Да, я прекрасно осведомлена об этом факте.",
        "transcription": "[jɛs / aɪ əm kwaɪt wɛl əˈweər əv ðə fækt]",
        "audio_teacher": "11_myvoiceEarn.mp3",
        "audio_actor": "11_Earnest.mp3"
    },
    {
        "id": 12,
        "text_en": "And I often wish that in public, at any rate, you had been more demonstrative.",
        "text_ru": "И мне хотелось бы, чтобы вы, по крайней мере на людях, более наглядно демонстрировали бы (свое ко мне отношение).",
        "transcription": "[ənd aɪ ˈɒfᵊn wɪʃ ðət ɪn ˈpʌblɪk / ət ˈɛni reɪt / jʊ həd biːn mɔː dɪˈmɒnstrətɪv]",
        "audio_teacher": "12_myvoiceEarn.mp3",
        "audio_actor": "12_Earnest.mp3"
    },
    {
        "id": 13,
        "text_en": "For me you have always had an irresistible fascination.",
        "text_ru": "Для меня вы всегда обладали неотразимым обаянием.",
        "transcription": "[fə mi jʊ həv ˈɔːlweɪz həd ən ˌɪrɪˈzɪstəbᵊl ˌfæsɪˈneɪʃᵊn]",
        "audio_teacher": "13_myvoiceEarn.mp3",
        "audio_actor": "13_Earnest.mp3"
    },
    {
        "id": 14,
        "text_en": "Even before I met you I was far from indifferent to you. (Jack looks at her in amazement.)",
        "text_ru": "Ещё до нашей встречи я была далеко не равнодушна к вам. (Джек смотрит на неё с изумлением.)",
        "transcription": "[ˈiːvᵊn bɪˈfɔːr aɪ mɛt jʊ aɪ wəz fɑː frəm ɪnˈdɪfᵊrᵊnt tə juː( ʤæk lʊks ət hər ɪn əˈmeɪzmənt)]",
        "audio_teacher": "14_myvoiceEarn.mp3",
        "audio_actor": "14_Earnest.mp3"
    },
    {
        "id": 15,
        "text_en": "We live, as I hope you know, Mr. Worthing, in an age of ideals.",
        "text_ru": "Мы живём, как вы, надеюсь, знаете, мистер Уординг, в эпоху идеалов.",
        "transcription": "[wi lɪv / əz aɪ həʊp jʊ nəʊ /mɪstə ˈwɜːðɪŋ / ɪn ən eɪʤ əv aɪˈdɪəlz]",
        "audio_teacher": "15_myvoiceEarn.mp3",
        "audio_actor": "15_Earnest.mp3"
    },
    {
        "id": 16,
        "text_en": "The fact is constantly mentioned in the more expensive monthly magazines, and has reached the provincial pulpits, I am told; and my ideal has always been to love some one of the name of Ernest..",
        "text_ru": "Об этом постоянно пишут в самых дорогих ежемесячных журналах и, как мне говорят, это стало темой даже в провинциальных проповедях; моим идеалом всегда было любить кого-то по имени Эрнест.",
        "transcription": "[ðə fækt iz ˈkɒnstᵊntli ˈmɛnʃᵊnd ɪn ðə mɔːr ɪkˈspɛnsɪv ˈmʌnθli ˌmæɡəˈziːnz / ənd həz riːʧt ðə prəˈvɪnʃᵊl ˈpʊlpɪts / aɪ əm təʊld // ənd maɪ aɪˈdɪəl həz ˈɔːlweɪz biːn tə lʌv səm wʌn əv ðə neɪm əv ˈɜːnɪst]",
        "audio_teacher": "16_myvoiceEarn.mp3",
        "audio_actor": "16_Earnest.mp3"
    },
    {
        "id": 17,
        "text_en": "There is something in that name that inspires absolute confidence.",
        "text_ru": "В этом имени есть что-то, внушающее абсолютное доверие.",
        "transcription": "[ðə z ˈsʌmθɪŋ ɪn ðət neɪm ðət ɪnˈspaɪəz ˈæbsəluːt ˈkɒnfɪdᵊns]",
        "audio_teacher": "17_myvoiceEarn.mp3",
        "audio_actor": "17_Earnest.mp3"
    },
    {
        "id": 18,
        "text_en": "The moment Algernon first mentioned to me that he had a friend called Ernest, I knew I was destined to love you.",
        "text_ru": "С того момента, как Алджернон впервые упомянул мне, что у него есть друг по имени Эрнест, я поняла, что обречена вас полюбить.",
        "transcription": "[ðə ˈməʊmənt ˈælʤənən fɜːst ˈmɛnʃᵊnd tə mi ðət hi həd ə frɛnd kɔːld ˈɜːnɪst / aɪ njuː aɪ wəz ˈdɛstɪnd tə lʌv juː]",
        "audio_teacher": "18_myvoiceEarn.mp3",
        "audio_actor": "18_Earnest.mp3"
    },
    {
        "id": 19,
        "text_en": "You really love me, Gwendolen?",
        "text_ru": "Вы и правда любите меня, Гвенделен?",
        "transcription": "[jʊ ˈrɪəli lʌv miː / 'gwendələn]",
        "audio_teacher": "19_myvoiceEarn.mp3",
        "audio_actor": "19_Earnest.mp3"
    },
    {
        "id": 20,
        "text_en": "Passionately!",
        "text_ru": "Страстно!",
        "transcription": "[ˈpæʃᵊnətli]",
        "audio_teacher": "20_myvoiceEarn.mp3",
        "audio_actor": "20_Earnest.mp3"
    },
    {
        "id": 21,
        "text_en": "Darling! You don't know how happy you've made me.",
        "text_ru": "Дорогая! Вы не представляете, как вы меня осчастливили.",
        "transcription": "[ˈdɑːlɪŋ / jʊ dəʊnt nəʊ haʊ ˈhæpi juːv meɪd miː]",
        "audio_teacher": "21_myvoiceEarn.mp3",
        "audio_actor": "21_Earnest.mp3"
    },
    {
        "id": 22,
        "text_en": "My own Ernest!",
        "text_ru": "Мой (собственный) Эрнест!",
        "transcription": "[maɪ əʊn ˈɜːnɪst]",
        "audio_teacher": "22_myvoiceEarn.mp3",
        "audio_actor": "22_Earnest.mp3"
    },
]

