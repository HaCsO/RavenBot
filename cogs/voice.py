import discord
from discord.ext import commands
from cogs.utils.db import Connect
import datetime

class Voice(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.users = {}
		self.color = 0xff7733

	@commands.Cog.listener()
	async def on_command_error(self, ctx, error):
		print(f"<{error}>")
		ctx_command = str(ctx.message.content.split(" ")[0])
		if isinstance(error, commands.CommandNotFound):
			await ctx.message.delete()
			await ctx.send(f"{ctx.message.author.mention} ``Прости ,но команды нету ¯\_(ツ)_/¯``", delete_after= 3)
	
			
	@commands.Cog.listener()
	async def on_voice_state_update(self, member, before, after):
		if member == self.bot.user:
			return
		
		if after.channel and before.channel:
			pass
		elif before.channel:
			if not self.users[f"{member.id}"]:
				return

			time = datetime.datetime.now()
			time_old = self.users[f"{member.id}"]

			timedelta = time - time_old
			db = Connect.conn()
			cur = db.cursor()
			cur.execute(f'SELECT voiceTime FROM users WHERE id = {member.id}')
			timeOld_r = cur.fetchall()
			if not timeOld_r:
				cur.execute(f"INSERT INTO users(id, voiceTime) VALUES ({member.id}, {timedelta.total_seconds()})")
				db.commit()
			else:
				timeOld = datetime.timedelta(seconds=timeOld_r[0][0])
				timeNew = timeOld + timedelta
				
				cur.execute(f"UPDATE users SET voiceTime = {timeNew.total_seconds()} WHERE id = {member.id}")
				db.commit()
			
			db.close()

		elif after.channel:
			time = datetime.datetime.now()
			self.users[f"{member.id}"] = time

	@commands.command(aliases=["время", "time", "dhtvz", "ешьу"])
	async def _time(self, ctx):
		await ctx.message.delete()
		emb = discord.Embed(title="voice time", colour= self.color)
		db = Connect.conn()
		cur = db.cursor()
		cur.execute(f"SELECT voiceTime FROM users WHERE id = {ctx.author.id}")
		f = cur.fetchall()
		if not f:
			res = "Вы еще не заходили в голосовой канал!"
		else:
			time = datetime.timedelta(seconds=f[0][0])
			res = f"{time}"

		emb.add_field(name="Голосовой онлайн", value= res)
		await ctx.send(embed=emb,delete_after=30)
		db.close()
		

	@commands.command(aliases=['top', 'топ', 'еоз', 'njg'])
	async def _top(self, ctx):
		await ctx.message.delete()
		emb = discord.Embed(title= "top", colour=self.color)
		db = Connect.conn()
		cur = db.cursor()
		cur.execute(f'SELECT * FROM users ORDER BY voiceTime DESC LIMIT 0, 10')
		res = cur.fetchall()
		for i in res:
			try:
				usr = self.bot.get_user(i[0])
				time = datetime.timedelta(seconds=int(i[1]))
				emb.add_field(name=f"{usr.name}", value=f"{time}", inline=False)
			except Exception:
				pass
		
		await ctx.send(embed= emb,delete_after=30)



def setup(bot):
	bot.add_cog(Voice(bot))
	print("[INFO] Voice loaded!")
