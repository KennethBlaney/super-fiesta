define pc = Character("[player_name]")


label start:
    $ config.rollback_enabled = False
    $ from utils import PlayerData
    $ pd = PlayerData()
    $ ordinal = lambda n: "%d%s" % (n,"tsnrhtdd"[(n//10%10!=1)*(n%10<4)*n%10::4])

    $ player_name = renpy.input("Who will be the owner of this farm?")
    pc "My name is [player_name]"

    jump time_loop

label time_loop:
    while True:
        pc "[pd.get_day_of_week()], [pd.get_month_of_year()] [ordinal(pd.time_of_day.day)] [pd.time_of_day.year] at [pd.get_oclock()]."
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