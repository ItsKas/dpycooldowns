__version__ = "0.1.5"
__author__ = 'Lukas Canter, Leo Rooney'
__credits__ = 'Authors'
import datetime
from datetime import timedelta
import time
import pymongo
from pymongo import MongoClient


class Cooldown:
    class CooldownManager:
        cooldownslist = []

        def __init__(self, conn, db, cluster):
            self.conn = conn
            self.db = db
            self.cluster = cluster

        @property
        def cooldowns(self):
            return self.cooldownslist

    class DpyCooldown:
        def __init__(self, manager, ctx, cooldown):
            manager.cooldownslist.append(self)
            self.manager = manager
            self.conn = MongoClient(self.manager.conn)
            self.db = self.conn[self.manager.db]
            self.cooldowns = self.db[self.manager.cluster]
            self.ctx = ctx
            self.author = ctx.author
            self.cooldown = cooldown
            self.commandname = ctx.command.name

        def convert(self, seconds):
            seconds = seconds % (24 * 3600)
            hour = seconds // 3600
            seconds %= 3600
            minutes = seconds // 60
            seconds %= 60

            return hour, minutes, seconds

        @property
        def remaining(self):
            commandname = self.ctx.command.name
            author = self.ctx.author
            cooldown = self.cooldown
            result = self.cooldowns.find_one(
                {"user": author.id, "command": f"{commandname}"})
            if result is not None:
                check = timedelta.total_seconds(datetime.datetime.utcfromtimestamp(
                    time.time()) - datetime.datetime.utcfromtimestamp(result["time"]))
                if check < cooldown:
                    secssincerun = check
                    secondscooldown = cooldown*60
                    return secssincerun - secondscooldown
            return 0

        def place_cooldown(self):
            result = self.cooldowns.find_one(
                {"user": self.ctx.author.id, "command": self.ctx.command.name})
            if result is None:
                self.cooldowns.insert_one(
                    {"user": self.ctx.author.id, "time": time.time(), "command": f"{self.ctx.command.name}"})

        @property
        def is_done(self):
            remaining = self.remaining
            result = self.cooldowns.find_one(
                {"user": self.author.id, "command": f"{self.commandname}"})
            if not result:
                return True
            check = timedelta.total_seconds(datetime.datetime.utcfromtimestamp(
                time.time()) - datetime.datetime.utcfromtimestamp(result["time"]))
            val = self.cooldown*60 < check
            if val:
                self.cooldowns.delete_one(
                    {"user": self.author.id, "command": f"{self.commandname}"})
            return val

        @property
        def tostr(self):
            remaining = self.remaining
            result = self.cooldowns.find_one(
                {"user": self.author.id, "command": f"{self.commandname}"})
            if result is not None:
                check = timedelta.total_seconds(datetime.datetime.utcfromtimestamp(
                    time.time()) - datetime.datetime.utcfromtimestamp(result["time"]))
                if check < self.cooldown*60:
                    secssincerun = check
                    secondscooldown = self.cooldown*60
                    hours, minutes, seconds = self.convert(
                        secondscooldown - secssincerun)
                    mins = str(minutes)
                    mins = mins.replace("-", "")
                    mins = float(mins)
                    mins = int(mins)
                    if round(mins) != 0:
                        if round(mins) > 1:
                            a = " minutes "
                            c = "and "
                            minutes = round(mins)
                        else:
                            a = " minute "
                            c = "and "
                            minutes = round(mins)
                    else:
                        a = ""
                        c = ""
                        minutes = ""
                    secs = str(seconds)
                    secs = secs.replace("-", "")
                    secs = float(secs)
                    secs = int(secs)
                    if round(secs) > 1:
                        b = " seconds"
                        seconds = round(secs)
                    else:
                        b = " second"
                        seconds = round(secs)
                    if hours == 0:
                        hours = ""
                    else:
                        hours = str(hours) + " hours,"
                    return f"{hours}{minutes}{a}{c}{seconds}{b}"
            return False
