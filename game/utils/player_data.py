import math

from dataclasses import dataclass
from collections import defaultdict
from datetime import datetime, timedelta

values = {
    "wheat": 10,
    "small fish": 5,
    "medium fish": 10,
    "big fish": 15,
    "plain gem": 5,
    "nice gem": 10,
    "perfect gem": 15
}

prices = {
    "wheat seeds": 5,
    "poor fishing rod": 0,
    "good fishing rod": 20,
    "great fishing rod": 40,
    "stone pickaxe": 0,
    "iron pickaxe": 20,
    "diamond pickaxe": 40
}

crop_time = 3


@dataclass
class Farm:
    crop_level = defaultdict(lambda: 1)
    crop_progress = 0
    crop_planted = False
    crop_ready = math.inf
    garden_weeds = True
    worked_today = {
        "gardening": False,
        "fishing": False,
        "mining": False
    }

    def work(self):
        if not self.worked_today["gardening"]:
            if not self.crop_planted:
                self.crop_planted = True
                self.crop_ready = crop_time
            self.crop_progress += 1
            self.worked_today["gardening"] = True

    def get_worked(self, activity: str = ""):
        return self.worked_today.get(activity, False)

    def set_worked(self, activity: str = ""):
        self.worked_today[activity] = True

    def reset_crop_progress(self):
        self.crop_progress = 0
        self.crop_planted = False
        self.crop_ready = math.inf

    def reset_worked(self):
        self.worked_today = {
            "gardening": False,
            "fishing": False,
            "mining": False
        }


@dataclass
class PlayerData:
    inventory = defaultdict(lambda: 0)
    well_rested: bool = True
    in_town: bool = False
    time_of_day = datetime(2024, 5, 1, 8, 0, 0)
    cash = 0
    farm = Farm()

    alien_friendship = {
        "grey": 0,
        "lizard": 0,
        "nordic": 0,
        "insect": 0
    }

    # Time functions
    def advance_time(self):
        if self.well_rested:
            self.time_of_day += timedelta(hours=4)
        else:
            self.time_of_day += timedelta(hours=6)

    def sleep_for_the_night(self):
        self.time_of_day = datetime(self.time_of_day.year,
                                    self.time_of_day.month,
                                    self.time_of_day.day + 1,
                                    8,
                                    0,
                                    0)
        self.farm.reset_worked()
        self.in_town = False
        self.inventory_cleaner()

    def return_from_town(self):
        self.time_of_day = datetime(self.time_of_day.year,
                                    self.time_of_day.month,
                                    self.time_of_day.day,
                                    10,
                                    0,
                                    0)
        self.in_town = False

    def get_day_of_week(self):
        return self.time_of_day.strftime('%A')

    def get_month_of_year(self):
        return self.time_of_day.strftime('%B')

    def get_oclock(self):
        am = "AM"
        hour = self.time_of_day.hour
        if hour > 12:
            hour -= 12
            am = "PM"
        return f"{hour} o'clock {am}"

    # Farming functions
    def harvest(self):
        if self.farm.crop_progress >= self.farm.crop_ready:
            self.farm.reset_crop_progress()
            self.inventory[self.farm.crop_planted] += self.farm.crop_level

    def crop_circle(self):
        if self.farm.crop_progress >= self.farm.crop_ready:
            self.farm.reset_crop_progress()

    def go_fishing(self):
        if self.farm.worked_today["fishing"]:
            return 0
        else:
            self.farm.worked_today["fishing"] = True
        if "great fishing rod" in self.inventory:
            self.inventory["big fish"] += 1
            return 3
        elif "good fishing rod" in self.inventory:
            self.inventory["medium fish"] += 1
            return 2
        elif "poor fishing rod" in self.inventory:
            self.inventory["small fish"] += 1
            return 1

    def mining(self):
        if self.farm.worked_today["mining"]:
            return 0
        else:
            self.farm.worked_today["mining"] = True
        if "diamond pickaxe" in self.inventory:
            self.inventory["perfect gem"] += 1
            return 3
        elif "iron pickaxe" in self.inventory:
            self.inventory["nice gem"] += 1
            return 2
        elif "stone pickaxe" in self.inventory:
            self.inventory["plain gem"] += 1
            return 1


    # Merchant functions
    def sell(self, item: str = "", quantity: int = 0) -> bool:
        if self.inventory[item] >= quantity:
            self.inventory[item] -= quantity
            self.cash += values.get(item, 0) * quantity
            return True
        return False

    def give(self, item: str = "", quantity: int = 0) -> bool:
        if self.inventory[item] >= quantity:
            self.inventory[item] -= quantity
            return True
        return False

    def buy(self, item: str = "", quantity: int = 0) -> bool:
        if self.cash >= prices.get(item, math.inf) * quantity:
            self.cash -= prices.get(item, math.inf) * quantity
            self.inventory[item] += quantity
            return True
        return False

    def find(self, item: str = "", quantity: int = 0):
        self.inventory[item] += quantity

    def inventory_getter(self, item: str = ""):
        return self.inventory.get(item, 0)

    def inventory_cleaner(self):
        inventory = self.inventory
        for key in self.inventory:
            if self.inventory[key] == 0:
                del inventory[key]
        self.inventory = inventory

    # alien romance
    def alien_getter(self, alien: str = "grey") -> int:
        return self.alien_friendship.get(alien, 0)

    def alien_incr(self, alien: str = "grey"):
        if alien in self.alien_friendship:
            self.alien_friendship[alien] += 1
