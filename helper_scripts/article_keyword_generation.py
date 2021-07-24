# Functions and variables to generate keywords from the title and summary

# required libraries
import time
from typing_extensions import final
import gc

# NLP Libraries
import newspaper
from newspaper import Article

import nltk
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

import spacy
# downloading spacy model
spacy_nlp_keyword_extractor=spacy.load("en_core_web_sm")

# base functions to find intersection and union between lists
def intersection_list(list1, list2):  
   list3 = [value for value in list1 if value in list2]  
   return list3  

def union_list(lst1, lst2):
    final_list = lst1 + lst2
    return list(set(final_list))


# Cleanup functions for text and keywords for stopwords removal, stemming etc
# cleans api summary output
def clean_text(summary):
	summary=summary.replace('[BREAK] ',' ')
	summary=summary.replace('[BREAK]',' ')

	return summary

# removes stopwords from keywords
def cleanup_keywords(keywords):

    merged_keywords=" ".join(list(keywords))
    merged_keywords=merged_keywords.lower()

    text_tokens = word_tokenize(merged_keywords)

    stopwords_list=["a","a's" , "able" , "about" , "above" , "according" , "accordingly" , "across" , "actually" , "after" , "afterwards" , "again" , "against" , "ain't" , "all" , "allow" , "allows" , "almost" , "alone" , "along" , "already" , "also" , "although" , "always" , "am" , "among" , "amongst" , "an" , "and" , "another" , "any" , "anybody" , "anyhow" , "anyone" , "anything" , "anyway" , "anyways" , "anywhere" , "apart" , "appear" , "appreciate" , "appropriate" , "are" , "aren't" , "around" , "as" , "aside" , "ask" , "asking" , "associated" , "at" , "available" , "away" , "awfully" , "be" , "became" , "because" , "become" , "becomes" , "becoming" , "been" , "before" , "beforehand" , "behind" , "being" , "believe" , "below" , "beside" , "besides" , "best" , "better" , "between" , "beyond" , "both" , "brief" , "but" , "by" , "c'mon" , "c's" , "came" , "can" , "can't" , "cannot" , "cant" , "cause" , "causes" , "certain" , "certainly" , "changes" , "clearly" , "co" , "com" , "come" , "comes" , "concerning" , "consequently" , "consider" , "considering" , "contain" , "containing" , "contains" , "corresponding" , "could" , "couldn't" , "course" , "currently" , "definitely" , "described" , "despite" , "did" , "didn't" , "different" , "do" , "does" , "doesn't" , "doing" , "don't" , "done" , "down" , "downwards" , "during" , "each" , "edu" , "eg" , "eight" , "either" , "else" , "elsewhere" , "enough" , "entirely" , "especially" , "et" , "etc" , "even" , "ever" , "every" , "everybody" , "everyone" , "everything" , "everywhere" , "ex" , "exactly" , "example" , "except" , "far" , "few" , "fifth" , "first" , "five" , "followed" , "following" , "follows" , "for" , "former" , "formerly" , "forth" , "four" , "from" , "further" , "furthermore" , "get" , "gets" , "getting" , "given" , "gives" , "go" , "goes" , "going" , "gone" , "got" , "gotten" , "greetings" , "had" , "hadn't" , "happens" , "hardly" , "has" , "hasn't" , "have" , "haven't" , "having" , "he" , "he's" , "hello" , "help" , "hence" , "her" , "here" , "here's" , "hereafter" , "hereby" , "herein" , "hereupon" , "hers" , "herself" , "hi" , "him" , "himself" , "his" , "hither" , "hopefully" , "how" , "howbeit" , "however" , "i'd" , "i'll" , "i'm" , "i've" , "ie" , "if" , "ignored" , "immediate" , "in" , "inasmuch" , "inc" , "indeed" , "indicate" , "indicated" , "indicates" , "inner" , "insofar" , "instead" , "into" , "inward" , "is" , "isn't" , "it" , "it'd" , "it'll" , "it's" , "its" , "itself" , "just" , "keep" , "keeps" , "kept" , "know" , "known" , "knows" , "last" , "lately" , "later" , "latter" , "latterly" , "least" , "less" , "lest" , "let" , "let's" , "like" , "liked" , "likely" , "little" , "look" , "looking" , "looks" , "ltd" , "mainly" , "many" , "may" , "maybe" , "me" , "mean" , "meanwhile" , "merely" , "might" , "more" , "moreover" , "most" , "mostly" , "much" , "must" , "my" , "myself" , "name" , "namely" , "nd" , "near" , "nearly" , "necessary" , "need" , "needs" , "neither" , "never" , "nevertheless" , "new" , "next" , "nine" , "no" , "nobody" , "non" , "none" , "noone" , "nor" , "normally" , "not" , "nothing" , "novel" , "now" , "nowhere" , "obviously" , "of" , "off" , "often" , "oh" , "ok" , "okay" , "old" , "on" , "once" , "one" , "ones" , "only" , "onto" , "or" , "other" , "others" , "otherwise" , "ought" , "our" , "ours" , "ourselves" , "out" , "outside" , "over" , "overall" , "own" , "particular" , "particularly" , "per" , "perhaps" , "placed" , "please" , "plus" , "possible" , "presumably" , "probably" , "provides" , "que" , "quite" , "qv" , "rather" , "rd" , "re" , "really" , "reasonably" , "regarding" , "regardless" , "regards" , "relatively" , "respectively" , "right" , "said" , "same" , "saw" , "say" , "saying" , "says" , "second" , "secondly" , "see" , "seeing" , "seem" , "seemed" , "seeming" , "seems" , "seen" , "self" , "selves" , "sensible" , "sent" , "serious" , "seriously" , "seven" , "several" , "shall" , "she" , "should" , "shouldn't" , "since" , "six" , "so" , "some" , "somebody" , "somehow" , "someone" , "something" , "sometime" , "sometimes" , "somewhat" , "somewhere" , "soon" , "sorry" , "specified" , "specify" , "specifying" , "still" , "sub" , "such" , "sup" , "sure" , "t's" , "take" , "taken" , "tell" , "tends" , "th" , "than" , "thank" , "thanks" , "thanx" , "that" , "that's" , "thats" , "the" , "their" , "theirs" , "them" , "themselves" , "then" , "thence" , "there" , "there's" , "thereafter" , "thereby" , "therefore" , "therein" , "theres" , "thereupon" , "these" , "they" , "they'd" , "they'll" , "they're" , "they've" , "think" , "third" , "this" , "thorough" , "thoroughly" , "those" , "though" , "three" , "through" , "throughout" , "thru" , "thus" , "to" , "together" , "too" , "took" , "toward" , "towards" , "tried" , "tries" , "truly" , "try" , "trying" , "twice" , "two" , "un" , "under" , "unfortunately" , "unless" , "unlikely" , "until" , "unto" , "up" , "upon" , "us" , "use" , "used" , "useful" , "uses" , "using" , "usually" , "value" , "various" , "very" , "via" , "viz" , "vs" , "want" , "wants" , "was" , "wasn't" , "way" , "we" , "we'd" , "we'll" , "we're" , "we've" , "welcome" , "well" , "went" , "were" , "weren't" , "what" , "what's" , "whatever" , "when" , "whence" , "whenever" , "where" , "where's" , "whereafter" , "whereas" , "whereby" , "wherein" , "whereupon" , "wherever" , "whether" , "which" , "while" , "whither" , "who" , "who's" , "whoever" , "whole" , "whom" , "whose" , "why" , "will" , "willing" , "wish" , "with" , "within" , "without" , "won't" , "wonder" , "would" , "wouldn't" , "yes" , "yet" , "you" , "you'd" , "you'll" , "you're" , "you've" , "your" , "yours" , "yourself" , "yourselves" , "zero"]

    tokens_without_sw = [word for word in text_tokens if not word in stopwords_list]
    tokens_without_sw = [word for word in tokens_without_sw if not word in stopwords.words("english")]  
    tokens_without_sw=" ".join(tokens_without_sw)

    porter_stemmer=PorterStemmer()
    after_stemming=porter_stemmer.stem(tokens_without_sw)
    after_stemming=after_stemming.strip(' ')

    return after_stemming



# Function returns title keywords by removing all the stopwords from the
def get_title_keywords(title):
    title=title.lower()

    title_alphanumeric=""
    for char in title:
        # if (char>='a' and char<='z') or (char>='0' and char<='9') or char==" ":
        if (char>='a' and char<='z') or  char==" ":
            title_alphanumeric+=char

    text_tokens = word_tokenize(title_alphanumeric)

    stopwords_list=["a's" , "able" , "about" , "above" , "according" , "accordingly" , "across" , "actually" , "after" , "afterwards" , "again" , "against" , "ain't" , "all" , "allow" , "allows" , "almost" , "alone" , "along" , "already" , "also" , "although" , "always" , "am" , "among" , "amongst" , "an" , "and" , "another" , "any" , "anybody" , "anyhow" , "anyone" , "anything" , "anyway" , "anyways" , "anywhere" , "apart" , "appear" , "appreciate" , "appropriate" , "are" , "aren't" , "around" , "as" , "aside" , "ask" , "asking" , "associated" , "at" , "available" , "away" , "awfully" , "be" , "became" , "because" , "become" , "becomes" , "becoming" , "been" , "before" , "beforehand" , "behind" , "being" , "believe" , "below" , "beside" , "besides" , "best" , "better" , "between" , "beyond" , "both" , "brief" , "but" , "by" , "c'mon" , "c's" , "came" , "can" , "can't" , "cannot" , "cant" , "cause" , "causes" , "certain" , "certainly" , "changes" , "clearly" , "co" , "com" , "come" , "comes" , "concerning" , "consequently" , "consider" , "considering" , "contain" , "containing" , "contains" , "corresponding" , "could" , "couldn't" , "course" , "currently" , "definitely" , "described" , "despite" , "did" , "didn't" , "different" , "do" , "does" , "doesn't" , "doing" , "don't" , "done" , "down" , "downwards" , "during" , "each" , "edu" , "eg" , "eight" , "either" , "else" , "elsewhere" , "enough" , "entirely" , "especially" , "et" , "etc" , "even" , "ever" , "every" , "everybody" , "everyone" , "everything" , "everywhere" , "ex" , "exactly" , "example" , "except" , "far" , "few" , "fifth" , "first" , "five" , "followed" , "following" , "follows" , "for" , "former" , "formerly" , "forth" , "four" , "from" , "further" , "furthermore" , "get" , "gets" , "getting" , "given" , "gives" , "go" , "goes" , "going" , "gone" , "got" , "gotten" , "greetings" , "had" , "hadn't" , "happens" , "hardly" , "has" , "hasn't" , "have" , "haven't" , "having" , "he" , "he's" , "hello" , "help" , "hence" , "her" , "here" , "here's" , "hereafter" , "hereby" , "herein" , "hereupon" , "hers" , "herself" , "hi" , "him" , "himself" , "his" , "hither" , "hopefully" , "how" , "howbeit" , "however" , "i'd" , "i'll" , "i'm" , "i've" , "ie" , "if" , "ignored" , "immediate" , "in" , "inasmuch" , "inc" , "indeed" , "indicate" , "indicated" , "indicates" , "inner" , "insofar" , "instead" , "into" , "inward" , "is" , "isn't" , "it" , "it'd" , "it'll" , "it's" , "its" , "itself" , "just" , "keep" , "keeps" , "kept" , "know" , "known" , "knows" , "last" , "lately" , "later" , "latter" , "latterly" , "least" , "less" , "lest" , "let" , "let's" , "like" , "liked" , "likely" , "little" , "look" , "looking" , "looks" , "ltd" , "mainly" , "many" , "may" , "maybe" , "me" , "mean" , "meanwhile" , "merely" , "might" , "more" , "moreover" , "most" , "mostly" , "much" , "must" , "my" , "myself" , "name" , "namely" , "nd" , "near" , "nearly" , "necessary" , "need" , "needs" , "neither" , "never" , "nevertheless" , "new" , "next" , "nine" , "no" , "nobody" , "non" , "none" , "noone" , "nor" , "normally" , "not" , "nothing" , "novel" , "now" , "nowhere" , "obviously" , "of" , "off" , "often" , "oh" , "ok" , "okay" , "old" , "on" , "once" , "one" , "ones" , "only" , "onto" , "or" , "other" , "others" , "otherwise" , "ought" , "our" , "ours" , "ourselves" , "out" , "outside" , "over" , "overall" , "own" , "particular" , "particularly" , "per" , "perhaps" , "placed" , "please" , "plus" , "possible" , "presumably" , "probably" , "provides" , "que" , "quite" , "qv" , "rather" , "rd" , "re" , "really" , "reasonably" , "regarding" , "regardless" , "regards" , "relatively" , "respectively" , "right" , "said" , "same" , "saw" , "say" , "saying" , "says" , "second" , "secondly" , "see" , "seeing" , "seem" , "seemed" , "seeming" , "seems" , "seen" , "self" , "selves" , "sensible" , "sent" , "serious" , "seriously" , "seven" , "several" , "shall" , "she" , "should" , "shouldn't" , "since" , "six" , "so" , "some" , "somebody" , "somehow" , "someone" , "something" , "sometime" , "sometimes" , "somewhat" , "somewhere" , "soon" , "sorry" , "specified" , "specify" , "specifying" , "still" , "sub" , "such" , "sup" , "sure" , "t's" , "take" , "taken" , "tell" , "tends" , "th" , "than" , "thank" , "thanks" , "thanx" , "that" , "that's" , "thats" , "the" , "their" , "theirs" , "them" , "themselves" , "then" , "thence" , "there" , "there's" , "thereafter" , "thereby" , "therefore" , "therein" , "theres" , "thereupon" , "these" , "they" , "they'd" , "they'll" , "they're" , "they've" , "think" , "third" , "this" , "thorough" , "thoroughly" , "those" , "though" , "three" , "through" , "throughout" , "thru" , "thus" , "to" , "together" , "too" , "took" , "toward" , "towards" , "tried" , "tries" , "truly" , "try" , "trying" , "twice" , "two" , "un" , "under" , "unfortunately" , "unless" , "unlikely" , "until" , "unto" , "up" , "upon" , "us" , "use" , "used" , "useful" , "uses" , "using" , "usually" , "value" , "various" , "very" , "via" , "viz" , "vs" , "want" , "wants" , "was" , "wasn't" , "way" , "we" , "we'd" , "we'll" , "we're" , "we've" , "welcome" , "well" , "went" , "were" , "weren't" , "what" , "what's" , "whatever" , "when" , "whence" , "whenever" , "where" , "where's" , "whereafter" , "whereas" , "whereby" , "wherein" , "whereupon" , "wherever" , "whether" , "which" , "while" , "whither" , "who" , "who's" , "whoever" , "whole" , "whom" , "whose" , "why" , "will" , "willing" , "wish" , "with" , "within" , "without" , "won't" , "wonder" , "would" , "wouldn't" , "yes" , "yet" , "you" , "you'd" , "you'll" , "you're" , "you've" , "your" , "yours" , "yourself" , "yourselves" , "zero"]

    tokens_without_sw = [word for word in text_tokens if not word in stopwords_list]
    keywords = [word for word in tokens_without_sw if not word in stopwords.words("english")]

    return keywords


def get_summary_base_keywords(URL):
    page=Article(URL)
    page.download()
    page.parse()
    page.nlp()

    keyworks=page.keywords
    
    
    del page
    _=gc.collect()

    return keyworks


def get_summary_keywords(URL):
    start_time=time.time()
    print("Starting search for keywords")
    keywords=get_summary_base_keywords(URL)
    cleaned_keywords=cleanup_keywords(keywords).split(" ")
    print("Keywords found")
    end_time=time.time()
    print(f"Time taken to find keywords {round(end_time-start_time,4)} seconds\n")

    return cleaned_keywords


def get_keywords_spacy(text):
    text=clean_text(text)
    doc=spacy_nlp_keyword_extractor(text)
    intermediate_keywords=list(doc.ents)

    keywords=[]
    for keyword in intermediate_keywords:
        keywords.append(str(keyword).lower())

    
    return keywords


# final_summary={'title': 'Omi: Tokyo could approach 3,000 new infections in early August', 'text': 'Tokyo will likely see a single-day record of nearly 3,000 new COVID-19 cases in early August, putting an enormous strain on the medical system, the chief of the government\'s anti-virus task force said.[BREAK] "It is possible that new cases will double in two weeks\' time, topping the peak of the third infection wave that occurred around the New Year holidays," Shigeru Omi said on a Nippon Television Network news program on July 20.[BREAK] The program host asked Omi, "Will the number of new cases reach nearly 3,000 in the first week of August?".[BREAK] Tokyo confirmed a record-high 2,520 new cases on Jan. 7.[BREAK] Omi noted that an increasing number of people have been vaccinated since then, but "More people are now being hospitalized in Tokyo."[BREAK] Tokyo is currently under a COVID-19 state of emergency, but the public appears more lackadaisical in guarding against infections, while thousands of people from overseas are arriving in Japan for the Tokyo Olympics and Paralympics, which end in early September.[BREAK] Omi called on the public to cooperate with anti-virus measures.[BREAK]'}
# final_summary={'title': 'Dan Harmon Reveals His Biggest Challenge in Developing a Community Movie', 'text': 'Dan Harmon has said that the Community movie has presented a few creative challenges, but that hasn\'t stopped him from continuing to think about the project.[BREAK] According to Syfy Wire, Harmon got onto the topic of the long-discussed Community movie when he recently appeared as a guest on an episode of Vulture\'s Good One podcast.[BREAK] "The obvious, dogmatic, practical, off-the-street answer is like, no, you don\'t. It\'s fan service. Why would there be a Community movie? Who do you think is going to walk in off the street and buy popcorn and sit and watch a Community movie like that?".[BREAK] "Saying that that person doesn\'t exist is a lot different from asking yourself structurally if you\'re supposed to design the movie for them, because there\'s a new viewer inside of all of us," he explained, likening it to a Marvel movie starting with "Inside references to all 90 other Marvel movies" but losing part of the audience because it ends up "Speaking in gibberish."[BREAK] "Formalistically, you owe a movie that I think the fans can not only enjoy, but they can stand back and go, \'you know, the crazy thing about this Community movie is that if you didn\'t know there was a show, this is an insanely good movie," he added.[BREAK] Despite these creative challenges and dilemmas, Harmon remained positive about the possibility of a Community movie happening in the future.[BREAK] All six seasons of the quick-witted, meta-riffic comedy series - including the one season without Harmon and the final season that aired on the now-defunct Yahoo Screen - became available on Netflix last year, causing fans to shout from the virtual rooftops for a follow-up movie, especially since most of the cast have expressed a desire to enrol in the project.[BREAK]'}
# final_summary={'title': 'Steam Deck: How SteamOS Bridges the Gap Between Console and PC', 'text': 'This isn\'t Valve\'s first attempt to make PC gaming more accessible on controllers, with the Steam Link and Steam Big Picture mode providing a similarly console-esque interface when playing away from your desktop.[BREAK] That means where Big Picture Mode didn\'t get all of Steam\'s recent improvements because development couldn\'t necessarily be easily shared between the two versions, the Steam Deck will naturally be able to inherit everything - and features Valve develops for the Deck will also go toward improving Steam in return.[BREAK] Big Picture Mode is still completely serviceable for what it needs to do, but I was struck by just how much more approachable the Steam Deck UI felt to use by comparison.[BREAK] The Steam Workshop will remember the mods you have installed, the Steam Cloud will keep your saves synced, Steam Achievements are tracked across your profile as usual, Steam\'s extensive controller customization is fully accessible whether you\'re playing handheld or docked, Steam Remote Play will let you stream games from another computer to the Deck or vice versa, and so on and so forth.[BREAK] While all those features were already available on a regular computer, Valve has also worked hard to give the Steam Deck one of the signature features console players have learned to rely on and PC gamers have previously only envied: suspending games.[BREAK] "One of the features that we\'ve been trying to figure out how to bring to the Steam platform for a long time is the home screen that you see in Steam on Deck," Spofford explained.[BREAK] You could even wipe your Steam Deck entirely and install windows if you\'d prefer - creating a "Walled garden" that disregards the openness of the PC platform is the opposite of what Valve tells me it wants to do.[BREAK]'}
# final_summary={'title': "China's Most Direct Pushback To Probe On Coronavirus Origin", 'text': 'While China has consistently rejected the lab hypothesis, officials sought to draw a line today.[BREAK] China pushed back against the World Health Organization\'s call for another probe into the coronavirus\'s origins that includes examining whether it leaked from a lab, saying there\'s no evidence for the theory and it defies common sense.[BREAK] The premise subsequently gained traction as scientists questioned China\'s reluctance to provide access to primary source material, attention grew over efforts among some virologists to make viruses stronger, called "Gain of function" work, and some world leaders called for a deeper probe.[BREAK] While China has consistently rejected the lab hypothesis, officials sought to draw a line in the sand Thursday, signaling Beijing won\'t engage on the origin hunt if the theory remained in play.[BREAK] It was China\'s most direct pushback to date on calls from the WHO and others to investigate the Wuhan Institute of Virology\'s high-level lab, which studied bat-borne pathogens and other coronaviruses.[BREAK] The WHO\'s plans to make the lab leak hypothesis a priority for the next stage of research has been contaminated by political posturing and displays "Arrogance against science," Zeng said.[BREAK] WHO Director-General Tedros Adhanom Ghebreyesus in March said the global body\'s first probe didn\'t adequately analyze the possibility of a lab accident before deciding it\'s most likely the pathogen spread from bats to humans via another animal.[BREAK]'}
# URL="https://www.ndtv.com/world-news/chinas-most-direct-pushback-to-probe-on-coronavirus-origin-2492002?pfrom=home-ndtv_topscroll"

# title_keywords=list(get_keywords_spacy(clean_text(final_summary["title"])))
# summary_keywords=list(get_keywords_spacy(clean_text(final_summary["text"])))
# print(title_keywords)
# print(summary_keywords)

# print(cleanup_keywords(title_keywords))
# print(cleanup_keywords())



