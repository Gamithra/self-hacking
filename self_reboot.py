import time
import sys
import select


RESET = "\033[0m"
GREEN = "\033[34m"
BLUE = "\033[32m"
YELLOW = "\033[93m"
PURPLE = "\033[95m"
TEAL = "\033[94m"
RED = "\033[31m"
DARK_RED = "\033[91m"  # Bright red
GRAY = "\033[90m"

def display_progress_bar(total_actions, current_action):
    bar_length = 10
    progress = current_action / total_actions
    completed = '▰' * int(round(progress * bar_length))
    remaining = '▱' * (bar_length - len(completed))

    sys.stdout.write("\r[\033[32m{}{}\033[0m] {}% - {}/{} workshop actions completed.\n".format(completed, remaining, int(progress * 100), current_action, total_actions))
    sys.stdout.flush()

def display_remaining_time(seconds_left):
    if seconds_left > 119:
        minutes_left = (seconds_left + 59) // 60  # Round up
        return f"{GREEN}{minutes_left} minute{'s' if minutes_left > 1 else ''} left{RESET}"
    elif seconds_left > 60:
        minutes = seconds_left // 60
        seconds = seconds_left % 60
        return f"{YELLOW}{minutes} minute{'s' if minutes > 1 else ''} and {seconds} second{'s' if seconds > 1 else ''} left{RESET}"
    elif seconds_left > 10:
        return f"{YELLOW}{seconds_left} seconds left{RESET}"
    else:
        return f"{DARK_RED}{seconds_left} seconds left{RESET}"


def countdown_timer(action, duration, is_extra_time=False):
    if not is_extra_time:
        input(f"{action}\n\n{GRAY}press enter to start timer{RESET}")    
    sys.stdout.write("\033[F")  # Cursor up one line
    sys.stdout.write("\033[F")  # Cursor up one line
    sys.stdout.write("\r" + " " * 150 + "\r")
    sys.stdout.write("\r" + " " * 150 + "\r")

    while duration:
        
        message = display_remaining_time(duration)
        sys.stdout.write("\033[F")  # Cursor up one line
        sys.stdout.write("\r" + " " * 150 + "\r")
        sys.stdout.write(f"Timer: {message}. {GRAY}enter 's' to skip {RESET}")
        sys.stdout.flush()

        if duration > 10:
            timeout = duration % 10
            timeout = timeout if timeout else 10
        else:
            timeout = 1

        # Check if 's' is pressed using select
        rlist, _, _ = select.select([sys.stdin], [], [], timeout)
        if rlist:
            input_char = sys.stdin.readline().strip()
            if input_char == 's':
                break

        duration -= timeout

    # Clear the line after the timer ends
    sys.stdout.write("\r" + " " * 150 + "\r")


def display_actions(actions):
    total_actions = len(actions)
    for idx, (action, duration) in enumerate(actions, 1):

        if duration:
            print("")
            countdown_timer(action, duration)

            # Prompt user if they need more time
            more_time = input(f"\033[36mOperation completed!{RESET} Need more time? {GRAY}enter minutes or skip: {RESET}")
            print("")
            try:
                more_minutes = int(more_time)
                countdown_timer(action, more_minutes * 60, True)
            except ValueError:
                pass
        else:
            input(f"{action}\n{GRAY}press any key to continue{RESET}")
            print("")


        display_progress_bar(total_actions, idx)
        print("")

    print(f"{GREEN}W O R K S H O P    C O M P L E T E{RESET}")
    print()




if __name__ == "__main__":

    actions = [
        (f"""

{YELLOW}          

w e l c o m e   t o   g a m i t h r a ' s   w o r k s h o p   o f 

{BLUE}

           _____          __             __  _          
  ___ ___ / / _/ _______ / /  ___  ___  / /_(_)__  ___ _
 (_-</ -_) / _/ / __/ -_) _ \/ _ \/ _ \/ __/ / _ \/ _ `/
/___/\__/_/_/  /_/  \__/_.__/\___/\___/\__/_/_//_/\_, / 
                                                 /___/  


{RESET}

         """, None),
        (f"""{BLUE}
            __      
  ______ __/ /__ ___
 / __/ // / / -_|_-<
/_/  \_,_/_/\__/___/
                    
        {RESET}           
#1 no agenda overview, but there's a progress bar!
#2 there's going to be a break at some point
#3 make this work for you
#4 use up time
#5 extra time system
#6 no sharing. be honest. be cringe
#7 be kind to your thoughts & observe them with radical curiosity. get information from the now, not from pre-defined mental models


         """, None),
        (f"Operation 1: {PURPLE}Clearing RAM.{RESET}. Things that mentally block from being right here. Things that should get done. Worries to postpone. Duration: 3 minutes.", 3*60),
        (f"Operation 2: {TEAL}The 2023 you{RESET}. What did that person feel and think? Duration: 3 minutes.", 3*60),
        (f"Operation 3: {PURPLE}Insights{RESET}. What are the most important things you learned? Duration: 5 minutes.", 5*60),
        (f"Operation 4: {TEAL}The 2025 you{RESET}. Don't plan; assume. Assuming this rate of change, what could that person's mind space feel like? Duration: 4 minutes.", 4*60),
        (f"Operation 5: {PURPLE}This-is-why things{RESET}. Keywords, sentences, memories, whatever; things that feel right. Moments that life feels like it's for. More of what? Memes? Words? Colours? Duration: 7 minutes.", 7*60),
        (f"Operation 6: {PURPLE}EXCITING IDEAS{RESET}. Brainstorm all the things that would be exciting to do this year. Like, the 2025 you will look at this and be like, ok, you actually did that? a m a z i n g. Duration: 6 minutes.", 6*60),
        (f"Operation 7: {PURPLE}EXCITING YEAR{RESET}. Make a 2024 calendar draft dream version 0. Don't worry about the specifics. Duration: 8 minutes.", 8*60),
        (f"Operation 8: {GREEN}Friends{RESET}. Right now go and invite a friend to do something or present a Plan Proposal. Duration: 5 minutes.", 5*60),
        (f"Operation N/A: {GREEN}BREAK{RESET}. Don't be distracted. Duration: 5 minutes.", 5*60),
        (f"Operation 9: {PURPLE}Post-capitalist dream utopia{RESET}. You have endless resources, all of your needs are met, you have infinite time. What does your day look like? Duration: 6 minutes.", 6*60),
        (f"Operation 10: {PURPLE}Burdens{RESET}. Which things feel heavy? Goals, people, commitments, ways of thinking? Duration: 3 minutes.", 3*60),
        (f"Operation 11: {PURPLE}Feedback loops{RESET}. Observe the feedback loops of life and behaviour. Which behaviours lead to which behaviours? Duration: 5 minutes.", 5*60),
        (f"Operation 12: {PURPLE}Change{RESET}. Where can you stop or change the feedback loops? What kind of being and doing can you add to your life, or remove? Duration: 4 minutes.", 4*60),
        (f"Operation 13: {PURPLE}Comfort zone expansion{RESET}. What kind of new things do you want to add? Let go of the 'I was going to' plans. Duration: 4 minutes.", 4*60),
        (f"Operation 14: {GREEN}Add/remove programs{RESET}. What kind of change can you commit to for the next 3 months? Duration: 4 minutes.", 4*60),
        (f"Operation 15: {TEAL}L i v i n g{RESET}. Imagine living this change. Duration: 4 minutes.", 4*60),
        (f"Operation 16: {PURPLE}Self-hacking{RESET}. Why are you probably not going to follow up with all of these plans? What are the blockers? How can you stop self-sabotage? Duration: 8 minutes.", 8*60),
        (f"Operation 17: {GREEN}Commitment{RESET}. When are you going to start? Can you start today? What is the first thing? What are you going to do this week? Duration: 7 minutes.", 7*60),
        (f"""
Operation 18: {GREEN}Wrap-up{RESET}.
Messenger chat!?

         """, None),
        (f"Operation 19: {GREEN}Feedback{RESET}. Duration: 3 minutes.", 3*60),
    ]

    display_actions(actions)
