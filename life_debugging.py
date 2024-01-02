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
 _ _  __           _      _                       _             
| (_)/ _|         | |    | |                     (_)            
| |_| |_ ___    __| | ___| |__  _   _  __ _  __ _ _ _ __   __ _ 
| | |  _/ _ \  / _` |/ _ \ '_ \| | | |/ _` |/ _` | | '_ \ / _` |
| | | ||  __/ | (_| |  __/ |_) | |_| | (_| | (_| | | | | | (_| |
|_|_|_| \___|  \__,_|\___|_.__/ \__,_|\__, |\__, |_|_| |_|\__, |
                                       __/ | __/ |         __/ |
                                      |___/ |___/         |___/          


{RESET}

$whoami?
         """, None),
        (f"""{BLUE}
            _           
           | |          
 _ __ _   _| | ___  ___ 
| '__| | | | |/ _ \/ __|
| |  | |_| | |  __/\__ \\
|_|   \__,_|_|\___||___/
        {RESET}           
#1 no agenda overview, but there's a progress bar!
#2 there's going to be a break (break rules)
#3 make this work for you
#4 use up time
#5 extra time system
#6 no sharing. be honest. be cringe
#7 be kind to your thoughts, but observe them with radical curiosity 

         """, None),
        (f"Operation 1: {PURPLE}RAM clearing{RESET}. Keywords of things that seem to matter or pop up. Duration: 3 minutes.", 3*60),
        (f"Operation 2: {PURPLE}Things that feel right{RESET}. Keywords, sentences, memories, whatever; things that just feel like you. Duration: 5 minutes.", 5*60),
        (f"Operation 3: {PURPLE}Attraction{RESET}. People, concepts, things, qualities. Things you'd secretly like to be. Things you'd secretly want to achieve. Qualities you just always feel drawn to. Duration: 5 minutes.", 5*60),
        (f"Operation 4: {PURPLE}Self-limiting{RESET}. Assumptions about how things are. Duration: 5 minutes.", 5*60),
        (f"Operation 5: {TEAL}Visualize the you 10 years ago{RESET}. What did that person feel and think? Duration: 2 minutes.", 2*60),
        (f"Operation 6: {TEAL}Visualize the you 10 years from now{RESET}. Don't plan; assume. Duration: 2 minutes.", 2*60),
        (f"Operation 7: {PURPLE}Looking back at the present{RESET}. How is the future you judging you? Duration: 5 minutes.", 5*60),
        (f"Operation 8: {PURPLE}Direction mapping{RESET}. What are all the things you could do? Duration: 5 minutes.", 5*60),
        (f"Operation N/A: {GREEN}BREAK{RESET}. Don't distract or be distracted. Duration: 5 minutes.", 5*60),
        (f"Operation 9: {PURPLE}Choosing{RESET}. What is the thing that you need to do? What are you most scared of? Duration: 2 minutes.", 2*60),
        (f"Operation 10: {TEAL}Visualize success{RESET}. How does it feel? Duration: 2 minutes.", 2*60),
        (f"Operation 11: {PURPLE}Deconstruction{RESET}. What are the verbs? What are the real-life actions? Duration: 5 minutes.", 5*60),
        (f"Operation 12: {PURPLE}Specification{RESET}. What is the amount of time? Duration: 2 minutes.", 2*60),
        (f"Operation 13: {PURPLE}Self-hacking{RESET}. Why will you probably not do it? How can you protect your mission? Duration: 5 minutes.", 5*60),
        (f"Operation 14: {PURPLE}Business continuity{RESET}. How can you protect yourself from self-sabotage? How will you keep going? Duration: 4 minutes.", 4*60),
        (f"Operation 14: {PURPLE}Commitment{RESET}. When will you start? What is the first task? Duration: 4 minutes.", 4*60),
        (f"""
Operation 15: {GREEN}Wrap-up{RESET}.
Telegram group link: bit.ly/lifedebug

Instructions:
#1 don't share specifics
#2 don't encourage. don't believe in anyone
#3 expect check-ins every 2 weeks
         """, None),
        (f"Operation 16: {GREEN}Feedback{RESET}. Duration: 3 minutes.", 3*60),
    ]

    display_actions(actions)
