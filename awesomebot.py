import time
print ('Starting Program...')
import time
import praw
import random
import re
print ('The current date and time is ' + time.strftime("%X"))
print (time.strftime("%X") + ': Imported Successfully!')

# Login in to Reddit and the bot
r = praw.Reddit('Randomactofdogebotby /u/dogetipbot')
r.login("annoysterninator","SECRET")
already_done = set()
print (time.strftime("%X") + ': Successfully logged in!')
prawWords = ['a', 'e', 'i', 'o', 'u']
prawTerms = ['+/u/dogetipbot']
tip_amount_pattern = re.compile("D?(\d+) ?(?:D|doge)?", re.IGNORECASE)

amount_min = 15
amount_max = 20
average_tip = float(amount_min + amount_max) / 2


#Returns amount between 2 numbers, as an integer. Default 15--25
def rand_amount(minimum, maximum):
    return random.randint(minimum, maximum)

#Find comment to tip
def pick_random_comment():
    global amount_min
    global amount_max
    
    subreddit = r.get_subreddit('dogecoin')
    print (time.strftime("%X") + ': Getting Comments...')
    subreddit_comments = subreddit.get_comments(limit=200)
    print (time.strftime("%X") + ': Comments Received!')
    for comment in subreddit_comments:
        op_text = comment.body
        has_praw = any(string in op_text for string in prawWords)
        if comment.id not in already_done and has_praw:
            comment.reply('This is a tip for an awesome user on an awesome subreddit!\n\n  This bot was created by /u/bassguitarman!\n\n +/u/dogetipbot ' + str(rand_amount(amount_min, amount_max)) + ' doge\n\nPlease consider tipping this bot to keep it running!\n\n')
            print (time.strftime("%X") + ': Lottery has been won!')
            already_done.add(comment.id)
            break

def check_inbox():
    messages = r.get_unread('comments')
    for message in messages:
        op_text = message.body
        has_praw = any(string in op_text for string in prawTerms)
        if message.id not in already_done and has_praw:
            amount_matches = tip_amount_pattern.findall(op_text)
            if amount_matches: # found a specified amount in the comment
                tip_allows_hours = float(amount_matches[0]) / average_tip
                message.reply('Thank you! This will help to keep me running for {num_hours} hours!\n\n'.format(num_hours = tip_allows_hours))
                print (time.strftime("%X") + ': Tip Received - Amount Verified')
            else:
                message.reply('Thank you! This will help to keep me running!\n\n')
                print (time.strftime("%X") + ': Tip Received - Amount NOT Verified')
            already_done.add(message.id)
            break



while True:
    check_inbox()
    pick_random_comment()
    time.sleep(360)
