﻿using System.Linq;
using DSharpPlus.Entities;
using Lilia.Database.Models;

namespace Lilia.Database.Extensions;

public static class UserDbAccess
{
    public static DbUser GetOrCreateUserRecord(this LiliaDatabaseContext ctx, DiscordUser discordUser)
    {
        var users = ctx.Users;
        var user = users.FirstOrDefault(entity => entity.DiscordUserId == discordUser.Id);

        if (user == default(DbUser))
        {
            user = new DbUser
            {
                DiscordUserId = discordUser.Id,
                OsuMode = string.Empty,
                OsuUsername = string.Empty,
                WarnCount = 0
            };

            users.Add(user);
        }

        ctx.SaveChanges();
        return user;
    }
}