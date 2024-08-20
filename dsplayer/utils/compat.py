from dsplayer.utils.lib_exceptions import LibraryNotFound

try:
    import disnake as discord_lib
    from disnake.ext import commands
except ImportError:
    try:
        import nextcord as discord_lib
        from nextcord.ext import commands
    except ImportError:
        try:
            import discord as discord_lib
            from discord.ext import commands
        except BaseException:
            raise LibraryNotFound("")

__all__ = ['commands', 'discord_lib']
