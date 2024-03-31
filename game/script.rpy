define pc = Character("[player_name]")
define lawyer = Character("Lawyer")
define sal = Character("Sal the Fisher")

label start:
    $ config.rollback_enabled = False
    $ from utils import PlayerData
    $ pd = PlayerData()
    $ ordinal = lambda n: "%d%s" % (n,"tsnrhtdd"[(n//10%10!=1)*(n%10<4)*n%10::4])
    town_first_time = True
    fish_store_first_time = True
    plant_store_first_time = True
    gem_store_first_time = True

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
    lawyer "A strange provision for sure, but I've seen stranger. For example..."
    lawyer "My client instructed me to inform you that he believed this location was the meeting place for several forms of extraterrestrial life."
    lawyer "I can't say I fully believe that myself, but I am bound by contract to inform you. You may do with that information as you please."
    lawyer "And with that [player_name], I will leave you to your new home."

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
        town_first_time = False
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
    pc "The town is a bit of a drive away. Definitely not something I'll be making more than once per day."
    pc "But the lawyer was right, this is a pretty nice little town. I'll take a walk around and see the sights."
    pc "First up is Sal's Bait and Tackle. Looks like a fishing supply store. Probably a good place to get a pole so I can go fishing in my stream."
    pc "Next up is Flora's Nursery. Everything I might need to get my garden up and running."
    pc "Finally the Gem and Mineral museum. I guess this town has a history of mining. The current curator appears to be named Sapphire."
    pc "Well, I guess these are my neighbors for the next year."
    return

label fishing_store:
    if fish_store_first_time:
        "Smells like fish in here."
        "Which I guess is to be expected."
        sal "Heya! A new face in town. Welcome to the store. What can I help you with?"
        pc "Hi. Nice to meet you. I just inherited a cottage just outside of town..."
        sal "Oh, I know that place. I'm guessing you are coming in here for some gear to fish that nice stream on your land."
        pc "Yes. That's exactly right."
        sal "Well, I always like to encourage the hobby, so here's a little starter kit for you."
        "Obtained 'poor fishing rod'"
        $pd.find('poor fishing rod', 1)
        pc "Oh, thank you, but you don't have to..."
        sal "I insist. And if you catch anything please come back and show me. I have a connection to a restaurant one town over that I routinely sell my catch to. I'd be happy to sell yours also."
        sal "Also I have some much better gear available for sale. So check that out when you are interested in getting further into the hobby."
    while True:
        menu:
            sal "Welcome, what can I do for you."

            "sell fish":
                "done"

            "buy 'good fishing rod'" if 'good fishing rod' not in pd.inventory:
                $success = pd.buy('good fishing rod', 1)
                if success:
                    sal "Sold. Glad to see you are getting into the hobby."
                else:
                    sal "Sorry [player_name]. I don't think you have enough money. Try catching some fish in your stream and selling them to me."

            "buy 'great fishing rod'" if 'great fishing rod' not in pd.inventory:
                $success = pd.buy('great fishing rod', 1)
                if success:
                    sal "Sold. You are quite the master baiter now..."
                    sal "What? Did I say something funny?"
                else:
                    "Sorry [player_name]. I don't think you have enough money. Try catching some fish in your stream and selling them to me."
            "That's all for now.":
                return


label florist:
    if plant_store_first_time:
        "Smells nice"

label gem_store:
    if gem_store_first_time:
        "Smells like rock?"

label one_year_later:
    pc "Bye farm"