Dpycooldowns is easy to use, simply create a cooldown manager, then create a cooldown with the manager as an argument.
To make a cooldown, see below
```python
cooldown = Cooldown.DpyCooldown(cooldownmanager, ctx, time)
```
```python
import discord
from discord.ext import commands
from cooldown import Cooldown

bot = commands.Bot(command_prefix="prefix")
cooldownmanager = Cooldown.CooldownManager("mongodb connection string", "mongodb database", "mongodb collection")
@bot.command()
async def test(ctx):

    cooldown = Cooldown.DpyCooldown(cooldownmanager, ctx, 1)
    if not cooldown.is_done:
        return await ctx.send(f"You cannot use this command for another {cooldown.tostr}")
    await ctx.send("Test")

bot.run("token")
```
