import discord
from discord.ext import commands



def convert_to_nums(board):
    output = [[],[],[],[],[],[]]
    i = -1
    for item in board:
        if item == "\n":
            i += 1
        elif item == "⬛":
            output[i].append(0)
        elif item == "🟥":
            output[i].append(1)
        elif item == "🟨":
            output[i].append(2)
    return output

def convert_to_emojis(board):
    output = ""
    for row in board:
        for item in row:
            if item == 0:
                output += "⬛"
            elif item == 1:
                output += "🟥"
            elif item == 2:
                output += "🟨"
        output += "\n"
    return output

def move (board, player, column):
    for i in range(5, -1, -1):
      if board[i][column] == 0:
        board[i][column] = player
        return board
    return False

def horCheck (player, board):
      row = 0
      col = 0
      count = 0
      winner = False
      while row < 6 and winner == False:
        while col < 3 and winner == False:
            count = 0
            if board[row][col] == player:
                count += 1
            if board[row][col+1]==player:
                count += 1
            if board[row][col+2]==player:
                count += 1
            if board[row][col+3]==player:
                count += 1
            if count == 4:
                winner = True
                print("horCheck, row", row, "column", col)
            col += 1
        row += 1
        col = 0
      return winner

def vertCheck (player, board):
    row = 0
    col = 0
    count = 0
    winner = False
    while row < 3 and winner == False:
        while col < 7 and winner == False:
            count = 0
            if board[row][col]==player:
                count = count + 1 
            if board[row+1][col]==player:
                count = count + 1 
            if board[row+2][col]==player:
                count = count + 1 
            if board[row+3][col]==player:
                count = count + 1 
            if count == 4:
                winner = True
                print("vert, row", row, "column", col)
            col += 1
        row += 1
        col = 0
    
    return winner

def diag1Check(player, board):
    row = 0
    col = 0
    count1 = 0
    winner = False
    while row <= 2 and winner == False:
        while col <= 3 and winner == False:
            count1 = 0
            if board[row][col] == player:
                print(board)
                print(board[row])
                print(board[row][col])
                print("row", row, "col", col, "player", player)
                count1 += 1
            if board[row+1][col+1] == player:
                print(board)
                print(board[row])
                print(board[row][col])
                print("row", row, "col", col, "player", player)
                count1 += 1
            if board[row+2][col+2] == player:
                print(board)
                print(board[row])
                print(board[row][col])
                print("row", row, "col", col, "player", player)
                count1 += 1
            if board[row+3][col+3] == player:
                print(board)
                print(board[row])
                print(board[row][col])
                print("row", row, "col", col, "player", player)
                count1 += 1
            if count1 == 4:
                winner = True
                print("Diag1Check, row", row, "column", col)
            print("diag1", "row", row, "column", col, "count1", count1)
            col += 1
        col = 0
        row += 1
    return winner 

def diag2Check(player, board):
    row = 0
    col = 0
    count2 = 0
    winner = False
    while row <= 2 and winner == False:
        while col <= 3 and winner == False:
            count2 = 0
            if board[row][col+3] == player:
                count2 += 1
            if board[row+1][col+2] == player:
                count2 += 1
            if board[row+2][col+1] == player:
                count2 += 1
            if board[row+3][col] == player:
                count2 += 1
            if count2 == 4:
                winner = True
                print("Diag2Check, row", row, "column", col)
            col += 1
        col = 0
        row += 1
    return winner 

def checkWinner(player, board):
        return horCheck(player,board) or vertCheck(player, board) or diag1Check(player,board) or diag2Check(player,board)





class Connectfour(commands.Cog):
    global player1
    global player2
    def __init__(self, bot):
        self.bot = bot

    def convert_to_nums(board):
        output = [[],[],[],[],[],[]]
        i = 0
        for item in board:
            if item == "\n":
                i += 1
            elif item == "⬛":
                output[i].append(0)
            elif item == "🟥":
                output[i].append(1)
            elif item == "🟨":
                output[1].append(2)
        return output


    @commands.command()
    async def say(self, ctx, *, message):
        await ctx.message.delete()
        await ctx.send(content=message, delete_after=2)

    


    @commands.command(aliases=["s"])
    async def start(self, ctx):
        global player1
        global player2
        global turn
        global turnnum
        em = discord.Embed(title = "Waiting for players... 0/2", description = "React below to play Connect Four!", color = discord.Color.green())
        message = await ctx.send(embed=em)
        await message.add_reaction("✅")

        player1 = None
        player2 = None
        turn = 1
        turnnum = 0
        print("\nStarting new game\n")

    @commands.Cog.listener("on_raw_reaction_add")
    async def start_play(self, payload):
        global player1
        global player2
        emoji, member, channel = payload.emoji, payload.member, self.bot.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)

        if member == self.bot.user:
            return

        embed = message.embeds[0]
        if embed.description != "React below to play Connect Four!":
            return

        #Sets reacter to player 1
        if not player1:
            player1 = member
            await channel.send(f'Player 1 is {member.mention}', delete_after=2)
            em = discord.Embed(title = "Waiting for players... 1/2", description = "React below to play Connect Four!", color = discord.Color.green())
            await message.edit(embed=em)

        #Sets reacter to player 2 and starts game
        elif not player2:
            player2 = member
            await channel.send(f'Player 2 is {member.mention}', delete_after=2)
            
            board = f'Turn: Player 1, {player1.mention}\n'
            board += '⬛⬛⬛⬛⬛⬛⬛\n'*6
            board += "1️⃣2️⃣3️⃣4️⃣5️⃣6️⃣7️⃣"
            
            em = discord.Embed(title = "Connect Four", description = board, color=discord.Color.green())
            await message.edit(embed=em)
            await message.clear_reactions()
            numbers = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣"]
            for number in numbers:
                await message.add_reaction(number)
        else:
            await channel.send("There are already two players, need to reset")
       



    @commands.Cog.listener('on_raw_reaction_add')
    async def play(self, payload):
        global turn
        global turnnum
        emoji, member, channel = payload.emoji, payload.member, self.bot.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)

        if member == self.bot.user:
            return

        embed = message.embeds[0]
        emdisc = message.embeds[0].description
        if embed.title != "Connect Four":
            return


        #removes reaction
        await message.remove_reaction(emoji, member)

        emtitle = "Connect Four"

        #Gets column number
        numbers = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣"]
        for i, number in enumerate(numbers):
            if str(emoji) == (number):
                column = i

        #Does turn for player1
        if member == player1:
            if turn != 1:
                await channel.send(f"It is not your turn {member.mention}! Waiting for {player2.mention}", delete_after=3)
                return

            
            print(emdisc)
            nums = move(convert_to_nums(emdisc), 1, column)

            if nums == False:
                await channel.send(f'{member.mention} you cannot go there!', delete_after = 3)
                return

            print(f"Player one, {member}, went in column {column} on turn #{turnnum}")
            turn = 2
            turnnum += 1


            print(convert_to_emojis(nums))
            if checkWinner(1, nums):
                await channel.send(f"{player1.mention} has won!")
                emtitle = "Game Over!"


            board = f'Turn: Player 2, {player2.mention}\n'
            board += convert_to_emojis(nums)
            board += "1️⃣2️⃣3️⃣4️⃣5️⃣6️⃣7️⃣" 

        elif member == player2:
            if turn != 2:
                await channel.send(f"It is not your turn {member.mention}! Waiting for {player1.mention}", delete_after=3)
                return
            
            print(f"Player two, {member}, went in column {column} on turn #{turnnum}")

            

            nums = move(convert_to_nums(emdisc), 2, column)

            if nums == False:
                await channel.send(f'{member.mention} you cannot go there!', delete_after = 3)
                return


            turn = 1
            turnnum += 1

            print(convert_to_emojis(nums))

            if checkWinner(2, nums):
                await channel.send(f"{player2.mention} has won!")
                emtitle = "Game Over!"

            board = f'Turn: Player 1, {player1.mention}\n'
            board += convert_to_emojis(nums)
            board += "1️⃣2️⃣3️⃣4️⃣5️⃣6️⃣7️⃣" 

            


        else:
            await channel.send(f"you are not a player {member}")
            return

        em = discord.Embed(title = emtitle, description = board, color=discord.Color.green())
        await message.edit(embed=em)



    


def setup(bot):
    bot.add_cog(Connectfour(bot))
