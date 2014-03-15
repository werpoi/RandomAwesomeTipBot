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

# Keep track of the most recent comment and amount of doge that was given out
selected_comment = None
comment_author = None
doge_amount = None

#Returns amount between 2 numbers, as an integer. Default 15--25
def rand_amount(minimum, maximum):
    return random.randint(minimum, maximum)

#Find comment to tip
def pick_random_comment():
    subreddit = r.get_subreddit('dogecoin')
    print (time.strftime("%X") + ': Getting Comments...')
    subreddit_comments = subreddit.get_comments(limit=200)
    print (time.strftime("%X") + ': Comments Received!')
    for comment in subreddit_comments:
        op_text = comment.body
        has_praw = any(string in op_text for string in prawWords)
        if comment.id not in already_done and has_praw:
            comment.reply('This is a tip for an awesome user on an awesome subreddit!\n\n  This bot was created by /u/bassguitarman!\n\n If you would like the tip of ' + str(doge_amount) + ' doge to go to doge4water, please respond to this comment with "+/u/annoysterninator tip doge4water". Otherwise this bot will tip you ' + str(doge_amount) + ' doge in six minutes.\n\nPlease consider tipping this bot to keep it running!\n\n')
            print (time.strftime("%X") + ': Lottery has been won!')
            return comment

def check_inbox():
    tip_donated = False
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
        # Look for a comment reply that has the string "+/u/annoysterninator tip doge4water"
        elif((selected_comment is not None) and
            (selected_comment.id not in already_done) and              # make sure the comment is not in the already_done list
            (message.body == '+/u/annoysterninator tip doge4water') and # and make sure it has the correct body
            (message.author.name == comment_author)):                        # and make sure the author is the same user that won the most recent lottery
            message.reply('Thank you for donating your tip to doge4water!\n\n +/u/dogetipbot DNfFHTUZ4kkXPnoYUvgt6BGVwonEFB1b2i ' + str(doge_amount) + ' doge verify')
            # add to the already_done list and indicate that the tip was donated
            already_done.add(selected_comment.id)
            tip_donated = True
    # If a previously selected comment exists and the tip wasn't donated, make sure to tip the user of that comment
    if((selected_comment is not None) and (tip_donated == False)):
        selected_comment.reply('+/u/dogetipbot ' + str(doge_amount) + ' doge')
        already_done.add(selected_comment.id)



while True:
    check_inbox()
    
    # Clear the selected_comment if it exists
    selected_comment = None
    
    # Generate random doge amount
    doge_amount = rand_amount(amount_min, amount_max)
    
    selected_comment = pick_random_comment()
    
    # Get the user whose comment was selected
    comment_author = selected_comment.author.name
    
    time.sleep(360)
    
