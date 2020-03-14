import discord
from discord.ext import commands
from cogs.utils.db import Connect
import asyncio

class Economy(commands.Cog):
	def __init__(self,bot):
		self.bot=bot
		self.badWords = [
			'блядь',
			'блять',
			'ебать',
			'пидорас',
			'пидр',
			'сука',
			'уебан',
			'лох',
			'хуй',
			'пизда',
			'залупа',
			'пенис',
			'член',
			'манда',
			'еблан',
			'долбаеб',
			'гнида'

		]
		self.color = 0xff7733
			
	@commands.command(aliases=['coin', 'cxtn', 'счет', 'сщшт'])
	async def _checkMoney(self, ctx):
		await ctx.message.delete()
		conn = Connect.conn()
		cur = conn.cursor()
		cur.execute(f"SELECT coins FROM users WHERE id={ctx.author.id}")
		x = cur.fetchall()
		coins = x[0][0]
		if not coins:
			coins = 0
		if coins > 1:
			postfix = "'s"
		else:
			postfix = ''		
		emb = discord.Embed(title='Счет', description=f"{coins} Ravencoin{postfix}", colour = self.color)
		emb.set_author(name= self.bot.user.name, icon_url=self.bot.user.avatar_url)
		emb.set_footer(text= "Запросил " + ctx.message.author.display_name, icon_url= ctx.message.author.avatar_url)

		conn.close()

		await ctx.send(embed=emb)

	@commands.command(aliases=['ctop', 'сещз', 'vnjg', 'мтоп'])
	async def _topMoney(self, ctx):
		await ctx.message.delete()

		conn = Connect.conn()
		cur = conn.cursor()
		cur.execute(f"SELECT * FROM users ORDER BY coins DESC LIMIT 0, 10")
		res = cur.fetchall()
		num = 0
		emb = discord.Embed(title='Счет', colour = self.color)

		for i in res:
			num += 1
			coins = i[3]
			if not coins:
				coins = 0
			if coins > 1:
				postfix = "'s"
			else:
				postfix = ''

			try:
				usr = self.bot.get_user(i[0])
				emb.add_field(name=f"{num}.{usr.name}", value=f"{coins} Ravencoin{postfix}")
			except Exception:
				pass

		emb.set_author(name= self.bot.user.name, icon_url=self.bot.user.avatar_url)
		emb.set_footer(text= "Запросил " + ctx.message.author.display_name, icon_url= ctx.message.author.avatar_url)
		conn.close()
		await ctx.send(embed=emb)

	@commands.command(aliases=['shop', 'vfufpby', 'магазин', 'ырщз'])
	async def _shop(self, ctx):
		await ctx.message.delete()
		emb = discord.Embed(title="Лавка Raven", colour = self.color)
		hasRole = False
		conn = Connect.conn()
		cur = conn.cursor()

		async def reactions():
			cur.execute(f"SELECT isUpped FROM users WHERE id = {ctx.author.id}")
			res = cur.fetchall()[0][0]
			await msg.add_reaction("1️⃣" if hasRole == False else '🔑')
			await msg.add_reaction("2️⃣")
			await msg.add_reaction("3️⃣" if hasRole and res == 0 else "🔒")
			await msg.add_reaction("4️⃣")
			await msg.add_reaction("❌")			

		cur.execute(f"SELECT buyedRole FROM users WHERE id = {ctx.author.id}")

		res = cur.fetchall()[0]

		if res[0] != None:
			hasRole = True

		emb.add_field(name=f"Роль {'1️⃣' if hasRole == False else '🔑'}", value="Своя кастомная роль с цветом на выбор (не должна содержать мата, игроков с этой ролью не показывают отдельно, у них просто добавляеться эта роль в списке) - 25 Ravencoin.")
		emb.add_field(name="Канал 2️⃣", value="Свой приватный канал (вы сами решите кто сможет зайти в этот канал, вам выдадуть роль с название этого канала и вы сможете пригласить в него до 4 человек), канал создаться под категорией 'Разговорчики' - 50 Ravencoin.")
		emb.add_field(name=f"Поднять роль {'3️⃣' if hasRole else '🔒'}", value="Вашу роль выводиться выше стандартных ролей (в списке участников он будет подсвечиваться таким цветом - который выбрал при покупке 1 слота) - 25 Ravencoin.")
		emb.add_field(name=f"Богач 4️⃣", value="Покупка роли `💎Богач💎`  - 1000 Ravencoin.")

		msg = await ctx.send(embed=emb)

		await reactions()

		def check(r, u):
			return u == ctx.author

		while 1:
			try:
				react, user = await self.bot.wait_for('reaction_add', check=check, timeout=60.0)
			except asyncio.TimeoutError:
				conn.close()
				await msg.delete()
				break

			await react.remove(ctx.author)
			
			if react.emoji in ['3️⃣', '🔒'] and hasRole == False:
				newEmbed = discord.Embed(title="Ошибка!", description=f"{ctx.author.mention} Так как у вас нету собственной роли, вы не можете ее поднять!", colour=0xff0000)
				await msg.edit(embed=newEmbed)
				await asyncio.sleep(5)
				await msg.edit(embed=emb)
			elif react.emoji in ["1️⃣", '🔑'] and hasRole == True:
				newEmbed = discord.Embed(title="Ошибка!", description=f"{ctx.author.mention} У вас уже есть роль!", colour=0xff0000)
				await msg.edit(embed=newEmbed)
				await asyncio.sleep(5)
				await msg.edit(embed=emb)
				
			if react.emoji == "1️⃣":
				cur.execute(f"SELECT coins FROM users WHERE id = {ctx.author.id}")
				res = cur.fetchall()
				if res[0][0] < 25:
					newEmbed = discord.Embed(title="Ошибка!", description=f"{ctx.author.mention} У вас не хватает RavenCoins!", colour=0xff0000)
					await msg.edit(embed=newEmbed)
					await asyncio.sleep(5)
					await msg.edit(embed=emb)
					continue

				newEmbed = discord.Embed(title='Кастомная роль', description="отправьте сообщение в формате `color;name`. цвет должен быть в hex(0xXXXXXX) формате", colour = self.color)
				await msg.edit(embed=newEmbed)
				def checker(msg):
					return msg.author == ctx.author
				async def view():
					return await self.bot.wait_for('message', check= checker, timeout=60.0)

				errCode = 0

				while 1:
					try:
						message = await view()
					except asyncio.TimeoutError:
						errCode = 1
						break
					await message.delete()
					color, name = message.content.split(';')
					if name in self.badWords:
						errEmbed = discord.Embed(title="Ошибка!", description=f"{ctx.author.mention} маты в названии запрещенны! Попробуйте снова!", colour=0xff0000)
						await msg.edit(embed=errEmbed)
						await asyncio.sleep(3)
						await msg.edit(embed=newEmbed)
						continue

					try:
						role = await self.bot.get_guild(487688244713095168).create_role(name= name, colour=discord.Colour(int(color, 16)), mentionable =True, hoist=False, reason="Buyed")
					except ValueError:
						errEmbed = discord.Embed(title="Ошибка!", description=f"{ctx.author.mention} формат цвета неправельный! Попробуйте снова!", colour=0xff0000)
						await msg.edit(embed=errEmbed)
						await asyncio.sleep(3)
						await msg.edit(embed=newEmbed)
						continue

					break
				if errCode == 1: continue
				cur.execute(f"UPDATE users SET buyedRole = {role.id}, coins = {res[0][0] - 25} WHERE id = {ctx.author.id}")
				conn.commit()

				await ctx.author.add_roles(role)
				hasRole = True
				newEmbed = discord.Embed(title="Успешно!", description=f"Роль {role.mention} создана!", colour = self.color)
				await msg.edit(embed=newEmbed)
				await asyncio.sleep(5)
				await msg.edit(embed=emb)
				await msg.clear_reactions()
				await reactions()

			elif react.emoji == "2️⃣":
				cur.execute(f"SELECT coins FROM users WHERE id = {ctx.author.id}")
				res = cur.fetchall()[0][0]
				if res < 50:
					newEmbed = discord.Embed(title="Ошибка!", description=f"{ctx.author.mention} У вас не хватает RavenCoins!", colour=0xff0000)
					await msg.edit(embed=newEmbed)
					await asyncio.sleep(5)
					await msg.edit(embed=emb)
					continue

				newEmbed = discord.Embed(title="Канал", description="Отправьте сообщение с желаемым именем канала")
				await msg.edit(embed=newEmbed)
				def checker2(m):
					return m.author == ctx.author
				try:
					message = await self.bot.wait_for('message', check= checker2, timeout=60)
				except asyncio.TimeoutError:
					errEmbed = discord.Embed(title="Ошибка!", description=f"{ctx.author.mention} превышен лимит ожидания!", colour=0xff0000)
					await msg.edit(embed=errEmbed)
					await asyncio.sleep(5)
					await msg.edit(embed=emb)
					continue

				await message.delete()
				ovr = {ctx.author: discord.PermissionOverwrite(manage_permissions = True)}
				cnt = message.content
				cat = self.bot.get_channel(534376287523831808).category
				chan = await self.bot.get_guild(487688244713095168).create_voice_channel(name=cnt, overwrites=ovr, category= cat)
				role = await self.bot.get_guild(487688244713095168).create_role(name=cnt, colour= 0xff0000)
				await ctx.author.add_roles(role)
				newEmbed= discord.Embed(title="Успешно!", description=f"Канал {cnt} создан!", colour = self.color)
				cur.execute(f"UPDATE users SET coins = {int(res) - 50} WHERE id = {ctx.author.id}")
				await msg.edit(embed=newEmbed)
				await asyncio.sleep(5)
				await msg.edit(embed=emb)
			elif react.emoji == "4️⃣":
				cur.execute(f"SELECT coins FROM users WHERE id = {ctx.author.id}")
				res = cur.fetchall()[0][0]
				if res < 1000:
					newEmbed = discord.Embed(title="Ошибка!", description=f"{ctx.author.mention} У вас не хватает RavenCoins!", colour=0xff0000)
					await msg.edit(embed=newEmbed)
					await asyncio.sleep(5)
					await msg.edit(embed=emb)
					continue

				role = self.bot.get_guild(487688244713095168).get_role(677552498680135691)
				await ctx.author.add_roles(role)
				cur.execute(f"UPDATE users SET coins = {int(res) - 1000} WHERE id = {ctx.author.id}")
				conn.commit()
				newEmbed = discord.Embed(title="Успешно!", description="Роль `💎Богач💎` куплена!")
				await msg.edit(embed=newEmbed)
				await asyncio.sleep(5)
				await msg.edit(embed=emb)

			elif hasRole and react.emoji == "3️⃣":
				cur.execute(f"SELECT coins FROM users WHERE id = {ctx.author.id}")
				coins = cur.fetchall()[0][0]
				if coins < 25:
					newEmbed = discord.Embed(title="Ошибка!", description=f"{ctx.author.mention} У вас не хватает RavenCoins!", colour=0xff0000)
					await msg.edit(embed=newEmbed)
					await asyncio.sleep(5)
					await msg.edit(embed=emb)
					continue

				cur.execute(F'SELECT buyedRole FROM users WHERE id = {ctx.author.id}')
				res = cur.fetchall()[0][0]

				role = self.bot.get_guild(487688244713095168).get_role(int(res))

				cur.execute(f"UPDATE users SET coins = {int(coins) - 25}, isUpped = 1 WHERE id = {ctx.author.id}")
				conn.commit()
				rolePos = len(self.bot.get_guild(487688244713095168).roles) - 7

				await role.edit(position=rolePos)
				newEmbed = discord.Embed(title="Успех!", description="Ваша роль поднята!", colour = self.color)
				await msg.edit(embed=newEmbed)
				await asyncio.sleep(5)
				await msg.edit(embed=emb)
				await msg.clear_reactions()
				await reactions()

			elif react.emoji == "❌":
				await msg.delete()
				conn.close()
				break

	@commands.command(aliases=['parse'])
	@commands.has_permissions(administrator=True)
	async def _parser(self, ctx):
		conn = Connect.conn()
		cur = conn.cursor()

		cur.execute(f"SELECT voiceTime, id FROM users")
		result = cur.fetchall()

		for i in result:
			coins = round((i[0] / 60) / 60)
			cur.execute(f"UPDATE users SET coins = {coins} WHERE id = {i[1]}")
			conn.commit()


		conn.close()
def setup(bot):
	bot.add_cog(Economy(bot))
	print('[INFO] Economy loaded!')
