import config

commands = ['**`!help`** - Shows every command with their description',
            '**`!prefix`** - Lists the prefixes currently in use by the server',
            '**`!prefix add {prefix}`** - Adds a prefix to be used by the bot',
            '**`!prefix set {prefix}`** - Sets the specified prefix to be the ONLY prefix in the server',
            '**`!prefix remove {prefix}`** - Removes a prefix (can\'t remove mentioning the bot)',
            '**`!ping`** - Check the bot\'s current ping', 
            '**`!schedule today`** - Shows the schedule for the given day in the user\'s timezone', 
            '**`!schedule date {yy-mm-dd}`** - Shows the schedule for a given date in the user\'s timezone',
            '**`!schedule title {title_name}`** - Gives a list of the scheduled games for the day in the user\'s timezone', 
            '**`!schedule tournament {tournament_name}`** - Returns the schedule for the day for the given tournament in the user\'s timezone', 
            '**`!schedule team {team_name}`** - Gives the schedule for the day for the given team in the user\'s timezone', 
            '**`!stats seriesId`** - Sends a message with some in-game stats',
            '**`!tournament {seriesId}`** - Sends a message with a summary of the series of the given tournament tournament',
            '**`!concurrency {title}`** - Shows the highest number of concurrent series for a given title']

headers = {'x-api-key' : config.API_KEY}

purple = 0x370F65

server_prefixes_file = 'server_prefixes.json'