define pc = Character("[player_name]")
define lawyer = Character("Lawyer")
define sal = Character("Sal the Fisher")
define flora = Character("Flora the Gardener")
define saph = Character("Sapphire the Gem Collector")
define alien = Character("Extraterestial Being")

label start:
    $ config.rollback_enabled = False
    $ from utils import PlayerData
    $ pd = PlayerData()
    $ ordinal = lambda n: "%d%s" % (n,"tsnrhtdd"[(n//10%10!=1)*(n%10<4)*n%10::4])
    $ town_first_time = True
    $ fish_store_first_time = True
    $ plant_store_first_time = True
    $ gem_store_first_time = True
    $ crop_circle = False

    lawyer "Ah welcome, please sit."
    $ player_name = renpy.input("I'm glad you could make it Ms... oh, I'm sorry, how would you like to be addressed.")
    pc "My name is [player_name]"
    lawyer "[player_name] it is then."
    lawyer "As we explained in our letter, you, [player_name], have been bequeathed a small parcel of land by our client."
    lawyer "It is quite a nice, cozy cottage out in the country. There's a freshwater stream on the property along with an old tourmaline mine."
    lawyer "You, of course, retain property rights to any fish caught and any gem stones found."
    lawyer "There is also a decent sized garden near the main house. Perfect for a hobbyist who wants to make some money."
    lawyer "The nearby town is full of decent folk and will often have swap meets to buy and sell things."
    lawyer "Unfortunately, [player_name], part of the stipulation in the will, requires that you must live at the property for one year before you may sell."
    lawyer "A strange provision for sure, but I've seen stranger. For example..."
    lawyer "My client instructed me to inform you that he believed this location was the meeting place for several forms of extraterrestrial life."
    lawyer "I can't say I fully believe that myself, but I am bound by contract to inform you. You may do with that information as you please."
    lawyer "And with that [player_name], I will leave you to your new home."

    "One long car ride later..."
    scene cottage with fade
    pc "Well, I guess here it is."
    pc "I can see the mine entrance and the stream. I'm definitely going to have to find some equipment if I want to use these."
    pc "Oh, this must be the garden. It is pretty overgrown. I'll need to spend some time preparing it before I'll be ready to plant anything there."
    pc "Best get what little stuff I could bring moved in."
    "After a long day of unpacking and assembling furniture, you feel your recently set up bed calling your name. Tomorrow if the first day of your year in this cottage."

    jump time_loop

label time_loop:
    while True:
        "[pd.get_day_of_week()], [pd.get_month_of_year()] [ordinal(pd.time_of_day.day)] [pd.time_of_day.year] at [pd.get_oclock()]."
        if pd.time_of_day.year == 2025:
            if pd.time_of_day.month == 5:
                jump one_year_later
        if pd.time_of_day.hour >= 20:
            call sleep_time from _call_sleep_time

        # elif special day

        else:
            call daily_routine from _call_daily_routine
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
    scene cottage with fade
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
                call fishing from _call_fishing
                return

            "Collect some stones from the mine" if not pd.farm.get_worked("mining"):
                call mining from _call_mining
                return

            "Tend to the garden" if not pd.farm.get_worked("gardening"):
                call gardening from _call_gardening
                return

            "Drive into town" if pd.time_of_day.hour == 8:
                $pd.in_town = True
                jump gone_to_town

            "Nothing else. I'm done for the day.":
                return

label gone_to_town:
    scene town with fade
    pc "I drive into town and talk to the locals"
    call in_town from _call_in_town
    $pd.return_from_town()
    jump sleep_time

label fishing:
    scene stream with fade
    pc "Nice day to fish"
    $result = pd.go_fishing()
    if result == 0:
        pc "Unfortunately I don't have a fishing rod yet. I should go pick one up in town."
    if result == 1:
        pc "I actually caught one. Not bad."
    if result == 2:
        pc "This is a decent sized fish. I'm sure Sal will be impressed."
    if result == 3:
        pc "An incredible river monster if I do say so myself."
    return

label mining:
    scene mine with fade
    pc "This cave has a certain haunting beauty."
    $result = pd.mining()
    if result == 0:
        pc "Unfortunately I don't have equipment to harvest these gems yet. I should go pick some up in town."
    if result == 1:
        pc "I managed to get one free."
    if result == 2:
        pc "It took some digging, but this one has some heft to it. I should bring it to Sapphire."
    if result == 3:
        pc "This is quite the impressive gem."
    return

label gardening:
    scene cottage with fade
    pc "Nice day to garden"
    if pd.farm.garden_weeds:
        pc "This garden was way overgrown."
        pc "There, I've removed the weeds and gotten it ready for planting."
        $pd.farm.garden_weeds = False
        $pd.farm.set_worked("gardening")
        return
    elif not pd.crop_planted and "wheat seeds" not in pd.inventory:
        pc "The garden is ready to go, but I'll need some seeds to plant. I should go into town and get some."
        return
    elif not pd.crop_planted:
        $pd.farm.work()
        $pd.advance_time()
        pc "There. All planted. I should tend to this on the next few days and see what grows."
    elif pd.crop_planted:
        if pd.crop_progress >= crop_ready:
            pc "Okay, these plants look ready. I can harvest them and collect the crops. Or I can try to communicate with aliens and make a crop circle, but that will ruin the sale value."
            menu:
                "Okay, these plants look ready."

                "Harvest them":
                    $ pd.harvest()
                    $ pd.advance_time()
                    pc "Whew! That was hard work, but it was worth it. I'll put this in the back of the truck for the next time I need it."
                "Crop circle":
                    $ pd.crop_circle()
                    $ pd.advance_time()
                    $ crop_circle = True
                    pc "Okay... that should do it. If there are any aliens up there, this should get their attention."
        else:
            $pd.work()
            $pd.advance_time()
            pc "Okay, making progress on these plants. Should be just a little bit more."
    return

label in_town:
    if town_first_time:
        call town_tour from _call_town_tour
        $town_first_time = False
    while True:
        pc "This is a nice town."
        menu:
            "What do I need to do while here?"

            "Stop by the bait and tackle store.":
                call fishing_store from _call_fishing_store

            "Go to the florist.":
                call florist from _call_florist

            "Visit the gem and mineral museum":
                call gem_store from _call_gem_store

            "Nothing else. Time to head home":
                scene cottage with fade
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
    scene fish_store with fade
    if fish_store_first_time:
        $fish_store_first_time = False
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
            sal "Welcome, what can I do for you?"

            "sell fish":
                $fish_value = pd.inventory_getter("small fish")*pd.values["small fish"] + pd.inventory_getter("medium fish")*pd.values["medium fish"] + pd.inventory_getter("big fish")*pd.values["big fish"]
                $pd.sell("small fish", pd.inventory_getter("small fish"))
                $pd.sell("medium fish", pd.inventory_getter("medium fish"))
                $pd.sell("big fish", pd.inventory_getter("big fish"))
                sal "Ah, thanks. Here's [fish_value] dollars."

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
                sal "Happy fishing [player_name]!"
                return


label florist:
    scene florist with fade
    if plant_store_first_time:
        $plant_store_first_time = False
        "Smells nice in here with all of the flowers in bloom."
        flora "Oh, a new person in town. Coming to stay or just passing through?"
        pc "I'll be staying here for a bit. I just moved in to a small cottage just outside of town."
        flora "In that case, let me welcome you to our town."
        flora "Something you should know, ever since World War II we've had a big focus on victory gardens."
        flora "The War's long over, of course, but the dedication toward growing your own food never left."
        flora "Let me help you get your own victory garden started with some starter seeds."
        "Obtained 'wheat seeds'"
        $pd.find('wheat seeds', 1)
        pc "Oh, thanks. Yes, I've been meaning to start something in my garden, so I appreciate the encouragement."
        flora "Anytime!"
        flora "By the way, I'll buy anything you grow in your garden. The community brings things together and sells it to hipsters from the city at the farmers market."
    while True:
        menu:
            flora "Hi [player_name]. What are you looking for today?"

            "sell grown food":
                $food_value = pd.inventory_getter("wheat")*pd.values["wheat"]
                $pd.sell("wheat", pd.inventory_getter("wheat"))
                flora "Thank you. This will sell great at the farmer's market. Here's [food_value] dollars."

            "buy more seeds":
                $success = pd.buy('wheat seeds', 1)
                if success:
                    sal "Here you are. Looking forward to seeing how this crop turns out."
                else:
                    "Sorry [player_name]. I don't think you have enough money at the moment. Try selling some other things first."

            "That's all for now.":
                flora "Come back soon!"
                return


label gem_store:
    scene museum with fade
    if gem_store_first_time:
        $gem_store_first_time = False
        "The museum gives off an air of importance."
        "You are quickly greeted by a young woman."
        saph "Welcome to the museum."
        saph "Oh and welcome to town. You are the one who just moved in to the old cottage, right?"
        pc "You've heard of me?"
        saph "I like to keep tabs on everything that happens in town. I heard someone had just moved in."
        pc "Yes, planning to stay for a year, then we'll see."
        saph "Wonderful!"
        saph "Well, this is the museum. I know you have a small mine on your property and we'd love to display any findings you discover in the mine."
        saph "Bring them back here and we'll pay you for them."
        pc "Actually, I don't have any mining equipment."
        saph "Oh, I'd be happy to loan you some."
        "Obtained 'stone pickaxe'"
        $pd.find('stone pickaxe', 1)
        pc "Thanks. I'll definitely find some time to work in my mine now."
    while True:
        menu:
            saph "Welcome, to the museum. What can I do for you?"

            "sell gems":
                $gem_value = pd.inventory_getter("plain gem")*pd.values["plain gem"] + pd.inventory_getter("nice gem")*pd.values["nice gem"] + pd.inventory_getter("perfect gem")*pd.values["perfect gem"]
                $pd.sell("plain gem", pd.inventory_getter("plain gem"))
                $pd.sell("nice gem", pd.inventory_getter("nice gem"))
                $pd.sell("perfect gem", pd.inventory_getter("perfect gem"))
                saph "Ah, thanks. Here's [gem_value] dollars."

            "buy 'iron pickaxe'" if 'iron pickaxe' not in pd.inventory:
                $success = pd.buy('iron pickaxe', 1)
                if success:
                    saph "Here you are. I'm looking forward to seeing what you dig up."
                else:
                    saph "Sorry [player_name]. I don't think you have enough money. Try selling some gems first."

            "buy 'diamond pickaxe'" if 'diamond pickaxe' not in pd.inventory:
                $success = pd.buy('diamond pickaxe', 1)
                if success:
                    saph "Hmm... I think I have to see your ID to verify your age."
                    saph "I think you might be a miner."
                else:
                    "Sorry [player_name]. I don't think you have enough money. Try selling some gems first."
            "That's all for now.":
                sal "Good luck and work hard, [player_name]!"
                return

label aliens:
    if not crop_circle:
        pc "Hmm... no aliens tonight. I'll have to figure out a way to signal them with a crop circle."
        return
    scene black
    if pd.alien_friendship['grey'] == 0:
        "The night stretches on and just when you are about to give up this fantasy that aliens exist, you see it."
        scene ufo_lands with fade
        "A craft about the size of your house lands in the crop circle you've placed in your garden."
        alien "Greetings human. We saw your signal and were happy to see Earth had finally established intelligent life."
        pc "We've had intelligent life for a while. Why just now?"
        alien "Capable, maybe? But intelligent? No. The creation of crop circles is a major step in the advancement of your civilization."
        pc "Is it?"
        alien "You have no idea."
        alien "To further prove that your planet is finally evolved, I will need to run some tests."
        alien "Please provide me with a fish from the local area so I may run these experiments."
        alien "Signal me with another crop circle when you are ready."
        "With that the alien re-enters his ship and flies off."
        pc "Was it just me, or was that alien really muscular?"
        pc "Wow... no one is ever going to believe this."
        $pd.alien_incr()
        $crop_circle = False
    if pd.alien_friendship['grey'] == 1:
        "You wait up at night to see if the alien returns. Maybe it was just a dream?"
        scene ufo_lands with fade
        "Soon enough the impressive craft lands once again."
        alien "You have the agreed upon creature?"
        if "small fish" in pd.inventory or "medium fish" in pd.inventory or "big fish" in pd.inventory:
            pc "Yes. Here it is."
            if "small fish" in pd.inventory:
                $pd.find('small fish', -1)
            elif "medium fish" in pd.inventory:
                $pd.find('medium fish', -1)
            elif "big fish" in pd.inventory:
                $pd.find('big fish', -1)
            alien "Excellent. Now to begin the experiments, I will need a crystal to refract the lasers. Could you provide me with one from the local mine?"
            pc "Yes, of course."
            pc "By the way, you can call me [player_name]."
            alien "It is a pleasure to meet you [player_name]. Thank you for your assistance so far."
            $pd.alien_incr()
            $crop_circle = False
        else:
            pc "No, I haven't been able to catch one yet. I just enjoy your company."
            alien "The feeling might be mutual human. But please, I need that creature to run my experiments."
            $crop_circle = False
    if pd.alien_friendship['grey'] == 2:
        "You await the return of the alien anxiously."
        scene ufo_lands with fade
        "Soon enough the impressive craft lands once again."
        alien "You have the crystal I need for my experiments?"
        if "plain gem" in pd.inventory or "nice gem" in pd.inventory or "perfect gem" in pd.inventory:
            pc "Yes. Here it is."
            if "plain gem" in pd.inventory:
                $pd.find('plain gem', -1)
            elif "nice gem" in pd.inventory:
                $pd.find('nice gem', -1)
            elif "perfect gem" in pd.inventory:
                $pd.find('perfect gem', -1)
            alien "Excellent. This will do nicely. However, the past creature you provided me proved too small. Could you provide me with a larger sample?"
            pc "Yes, of course."
            alien "Thank you. Your help is vital to my work."
            $pd.alien_incr()
            $crop_circle = False
        else:
            pc "No, I haven't been able to mine one yet. I just enjoy your company."
            alien "I enjoy your company as well. But please, I need that crystal to run my experiments."
            $crop_circle = False
    if pd.alien_friendship['grey'] == 3:
        "You wait up at night to see if the alien returns. Maybe it was just a dream?"
        scene ufo_lands with fade
        "Soon enough the impressive craft lands once again."
        alien "You have the agreed upon creature?"
        if "big fish" in pd.inventory:
            pc "Yes. Here it is."
            $pd.find('big fish', -1)
            alien "Excellent. We are very close to finished."
            alien "Now I only require a perfectly pure sample of the crystal you provided to me previously."
            alien "Please provide that and our work together can truly yield results."
            $pd.alien_incr()
            $crop_circle = False
        else:
            pc "No, I haven't been able to catch one yet. I just enjoy your company."
            alien "I enjoy your company as well. But please, I need that creature so we may continue our work."
            $crop_circle = False
    if pd.alien_friendship['grey'] == 4:
        "You wait up at night to see if the alien returns. Maybe it was just a dream?"
        scene ufo_lands with fade
        "Soon enough the impressive craft lands once again."
        alien "You have the agreed upon creature?"
        if "perfect gem" in pd.inventory:
            pc "Yes. Here it is."
            $pd.find('perfect gem', -1)
            alien "Finally. I have all I need. I will begin my work."
            alien "When you are ready to board my ship so I may show you my results, please summon me again with the crop circle."
            $pd.alien_incr()
            $crop_circle = False
        else:
            pc "No, I haven't been able to find one yet. I just enjoy your company."
            alien "I enjoy your company as well. But please, we are so close."
            $crop_circle = False
    if pd.alien_friendship['grey'] == 5:
        pc "This is crazy. I have summoned your alien friend once again in the hopes of boarding their space craft."
        pc "No way this is real."
        scene ufo_lands with fade
        "For the last time the huge ship lands in your yard."
        "The door opens, but the alien doesn't emerge."
        "Hesitantly, you enter the ship."
        "As you walk down this long metalic hall way, you arrive at a door."
        "Sensing your presence, the door slides open with a scifi sound effect revealing... {pause} A ROMANTIC DINNER?"
        scene dinner with fade
        "The alien gestures to your seat."
        alien "I'm glad you have arrived [player_name]. I was very nervous you wouldn't show up."
        "Sitting down you see that the candle on the table is, in fact, the crystal you provided from your mine."
        "The alien places two plates down on the table. They have cooked the fish your provided to perfection."
        alien "Please... eat."
        "The two of you eat the prepared meals. The alien herbs and spices are an amazing match."
        "For the first time, you have a conversation with the alien. The best conversation you've had with another being in months."
        alien "And now, I have one last element to this night."
        "The alien gets down on one knee and produces a small felt box. Opening it, it reveals the perfect gem stone you mined for the alien."
        "The alien says something, but it is all a blur. Before you know it you have agreed to travel the universe with the alien."
        jump end



label one_year_later:
    pc "It has been an exciting year, but it is time to leave the farm behind."
    "Thanks for playing this far. I didn't expect any one to and ran out of time in the jam, so there's no real ending here."
    "Sorry"
    jump end

label end:
    "Thank you for playing."
    "The End"
    return