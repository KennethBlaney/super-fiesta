define pc = Character("[player_name]")
define lawyer = Character("Lawyer")

label start:
    $ config.rollback_enabled = False
    $ from utils import PlayerData
    $ pd = PlayerData()
    $ ordinal = lambda n: "%d%s" % (n,"tsnrhtdd"[(n//10%10!=1)*(n%10<4)*n%10::4])
    town_first_time = True

    lawyer "Ah welcome, please sit."
    $ player_name = renpy.input("I'm glad you could make it Mr... oh, I'm sorry, how would you like to be addressed.")
    pc "My name is [player_name]"
    lawyer "[player_name] it is then."
    lawyer "As we explained in our letter, you, [player_name], have been bequeathed a small parcel of land by our client."
    lawyer "It is quite a nice, cozy cottage out in the country. There's a freshwater stream on the property along with an old tourmaline mine."
    lawyer "You, of course, retain property rights to any fish caught and any gem stones found."
    lawyer "There is also a decent sized garden near the main house. Perfect for a hobbyist who wants to make some money."
    lawyer "The nearby town is full of decent folk and will often have swap meets to buy and sell things."
    lawyer "Unfortunately, [player_name] part of the stipulation in the will, requires that you must live at the property for one year before you may sell."
    lawyer "A strange provision for sure, but I've seen stranger."
    lawyer "Finally, the really strange part. My client instructed me to inform you that he believed this location was the meeting place for several forms of extraterrestrial life."
    lawyer "I can't say I fully believe that myself, but I am bound by contract to inform you. You may do with that information as you please."
    lawyer "If you have any questions, please feel free to contact me. I'm only a phone call away."

    "One long car ride later..."
    pc "Well, I guess here it is."
    pc "I can see the mine entrance and the stream. I'm definitely going to have to find some equipment if I want to use these."
    pc "Oh, this must be the garden. It is pretty overgrown. I'll need to spend some time preparing it before I'll be ready to plant anything there."
    pc "Best get what little stuff I could bring moved in."
    "After a long day of unpacking and assembling furniture, you feel your recently set up bed calling your name. Tomorrow if the first day of your year in this cottage."

    jump time_loop

label time_loop:
    while True:
        pc "[pd.get_day_of_week()], [pd.get_month_of_year()] [ordinal(pd.time_of_day.day)] [pd.time_of_day.year] at [pd.get_oclock()]."
        if pd.time_of_day.year == 2025 AND pd.time_of_day.month == 5:
            jump one_year_later
        if pd.time_of_day.hour >= 20:
            call sleep_time

        # elif special day

        else:
            call daily_routine
            $pd.advance_time()

label sleep_time:
    pc "*Yawn* It is getting late."
    menu:
        "What should I do with the evening?"

        "Go to sleep to prep for the next day.":
            $pd.well_rested = True
            $pd.sleep_for_the_night()
            pc "What a good night's rest. I'm ready for the day."

        "Stay up and watch for aliens.":
            $pd.well_rested = False
            $pd.sleep_for_the_night()
            pc "I'm a little groggy today, but I'm glad I kept watch."
    return

label daily_routine:
    if pd.time_of_day.hour == 8:
        "Always nice to see the farm first thing in the morning. What are we doing?"
    elif pd.time_of_day.hour <= 12:
        "Still have a little time before lunch."
    else:
        "What else can I get done today?"

    if pd.in_town:
        jump gone_to_town

    else:
        menu:
            "What would you like to do?"

            "Catch some fish" if not pd.farm.get_worked("fishing"):
                call fishing
                return

            "Collect some stones from the mine" if not pd.farm.get_worked("mining"):
                call mining
                return

            "Tend to the garden" if not pd.farm.get_worked("gardening"):
                call gardening
                return

            "Drive into town" if pd.time_of_day.hour == 8:
                $pd.in_town = True
                jump gone_to_town

            "Nothing else. I'm done for the day.":
                return

label gone_to_town:
    pc "I drive into town and talk to the locals"
    call in_town
    $pd.return_from_town()
    jump sleep_time

label fishing:
    pc "Nice day to fish"
    $pd.farm.set_worked("fishing")
    return

label mining:
    pc "Nice day to mine"
    $pd.farm.set_worked("mining")
    return

label gardening:
    pc "Nice day to garden"
    $pd.farm.set_worked("gardening")
    return

label in_town:
    if town_first_time:
        call town_tour
    while True:
        pc "This is a nice town."
        menu:
            "What do I need to do while here?"

            "Stop by the bait and tackle store.":
                call fishing_store

            "Go to the florist.":
                call florist

            "Visit the gem and mineral museum":
                call gem_store

            "Nothing else. Time to head home":
                return

label town_tour:
    "Yep... tour of the town."

label fishing_store:
    "Smells like fish"

label florist:
    "Smells nice"

label gem_store:
    "Smells like rock?"

label one_year_later:
    pc "Bye farm"