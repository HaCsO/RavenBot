import discord
from discord.ext import commands
from cogs.utils.db import Connect
import datetime
import configparser

class Voice(commands.Cog):
	def __init__(self, bot):
		cfg = configparser.ConfigParser()
		cfg.read("cogs/roles.ini")
		self.bot = bot
		self.users = {}
		self.color = 0xff7733
		
		if len(cfg['ROLES']) != len(cfg['PRISE']):
			raise Exception("Config is wrong!")
		else:
			self.roles = {}
			for i in range(1, len(cfg['ROLES'])+1):
				self.roleCount = len(cfg['ROLES'])
				id = int(cfg['ROLES'][f'role{i}'])
				prise = int(cfg['PRISE'][f'role{i}'])
				self.roles[f'role{i}'] = {'id': f'{id}', 'prise': prise}

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
				maxRole = None
				for i in range(1, self.roleCount+1):
					if self.roles[f'role{i}']['prise'] <= timedelta.total_seconds():
						maxRole = f"role{i}"

				if maxRole:
					role = discord.utils.get(member.guild.roles, id=int(self.roles[maxRole]['id']))
					await member.add_roles(role)

					await member.send(f"{member.mention} поздравляю! Ты достиг роли `{role.name}`!")
				cur.execute(f"INSERT INTO users(id, voiceTime) VALUES ({member.id}, {timedelta.total_seconds()})")
				db.commit()
			else:
				maxRole = None
				timeOld = datetime.timedelta(seconds=timeOld_r[0][0])
				timeNew = timeOld + timedelta
				for i in range(1, self.roleCount+1):
					if self.roles[f'role{i}']['prise'] <= timeNew.total_seconds():
						maxRoleN = i-1
						maxRole = f"role{i}"

				if maxRole:
					role = discord.utils.get(member.guild.roles, id=int(self.roles[maxRole]['id']))
					roleOld = discord.utils.get(member.guild.roles, id=int(self.roles[f"role{maxRoleN}"]['id']))
					await member.add_roles(role)
					await member.remove_roles(roleOld)
					await member.send(f"{member.mention} поздравляю! Ты достиг роли `{role.name}`!")


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
		await ctx.send(embed=emb)
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
		
		await ctx.send(embed= emb)

	@commands.command(aliases=['help', 'помощ', 'gjvjo', 'рудз'])
	async def _help(self, ctx):
		emb = discord.Embed(title="Все команды", description="Все что в () тоже работает как команда", colour=self.color)
		emb.set_author(name= self.bot.user.name, icon_url=self.bot.user.avatar_url)
		emb.set_footer(text= "Запросил " + ctx.message.author.display_name, icon_url= ctx.message.author.avatar_url)
		emb.add_field(name= "help(помощ)", value= "Вызвать это сообщение")
		emb.add_field(name= "time(время)", value= "Посмотреть количество времени которые ты провел в голосовых каналах")
		emb.add_field(name= "top(топ)", value= "Топ пользователей по времени")

		try:
			await ctx.message.author.send(embed= emb)
		except Exception:
			async with ctx.message.channel.typing():
				await ctx.send(embed= emb,
				content= f"{ctx.message.author.mention}``, прости но я не могу тебе написать поэтому это сообщение скоро изчезнет чтобы не спамить...``",
				delete_after= 15)
		finally:
			await ctx.message.delete()


def setup(bot):
	bot.add_cog(Voice(bot))
	print("[INFO] Voice loaded!")
