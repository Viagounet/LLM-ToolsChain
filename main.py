from document import Document
from system import System

with open("transcript_MAN_annot09.txt", "r") as f:
    content_transcript = f.read()

with open("gawr_gura_thread.txt", "r") as f:
    content_thread = f.read()

with open("rp_character.txt", "r") as f:
    content_rp = f.read()

with open("gura_member_posts.txt", "r") as f:
    gura_posts = f.read()

with open("gura_tweets.txt", "r") as f:
    gura_tweets = f.read()

my_documents = [Document("gura_member_posts.txt", "Gawr Gura member posts. A good way to find out about her writing style", gura_posts),
                Document("gura_tweets.txt", "Gawr Gura tweets. A good way to find out about her writing style", gura_posts)]

sys = System(tools=[], documents=my_documents)
#sys.run([])



