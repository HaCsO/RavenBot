import discord
from discord.ext import commands
from cogs.utils.db import Connect

class Helper(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.msg = None

	@commands.Cog.listener()
	async def on_ready(self):
		conn = Connect.conn()
		cur = conn.cursor()
		cur.execute("SELECT * FROM msg")
		res = cur.fetchall()
		cnt = """
<@&680447153184702486> и <@&680447241693167671> , пожалуйста выберите роль - режим игры который предпочитаете больше. Вас тогда по этим ролям будут пинговать в чате.
<@&680447153184702486> - <:5531_ok_zoomer:677558374078087199> 
<@&680447241693167671> - <:5538_okboomer:677561167534882826> 
Поставьте под этим сообщением реакцию.
		"""
		if not res:
			emb = discord.Embed(title="Роли", description=cnt, colour=0xff7733)
			msg = await self.bot.get_channel(688095053700137049).send(embed=emb)
			await msg.add_reaction(self.bot.get_emoji(677558374078087199))
			await msg.add_reaction(self.bot.get_emoji(677561167534882826))
			cur.execute(f"INSERT INTO msg (id) VALUES ('{msg.id}')")
			conn.commit()
			self.msg = msg 

		else:
			try:
				msg = await self.bot.get_channel(688095053700137049).fetch_message(int(res[0][0]))
			except Exception:
				msg = None

			if not msg:
				emb = discord.Embed(title="Роли", description=cnt, colour=0xff7733)
				msg = await self.bot.get_channel(688095053700137049).send(embed=emb)
				await msg.add_reaction(self.bot.get_emoji(677558374078087199))
				await msg.add_reaction(self.bot.get_emoji(677561167534882826))
				cur.execute(f"UPDATE msg SET id = '{msg.id}'")
				conn.commit()

			self.msg = msg 
		
		conn.close()

	@commands.Cog.listener()
	async def on_raw_reaction_add(self, payload):
		if payload.message_id == self.msg.id:
			if payload.emoji.id == 677558374078087199:
				role = self.bot.get_guild(487688244713095168).get_role(680447153184702486)
#				try:
				await payload.member.add_roles(role)
#				except Exception:
#					pass
			elif payload.emoji.id == 677558374078087199:
				role = self.bot.get_guild(487688244713095168).get_role(680447241693167671)
#				try:
				await payload.member.add_roles(role)
#				except Exception:
#					pass

	@commands.command()
	async def faq(self, ctx):
		cnt = """
Сервер создан для общения, совместных прохождений игр, обсуждений ватников, платы Ведьмаку чеканной монетой, выяснений отношений, словесным перепалкам и шуткам про говно.

$command - мои команды сервера.
$rythmcom - команды бота RYTHM.

Немного о ролях:

- <@&578971421892542474> : Полный доступ к серверу.

- <@&498065105590812672> : Может все что и Доктор + права Администратора которые позволяют обходить правила отдельных каналов. Может банить участников.

- <@&487690940123709460> : Может все что <@&675641777012604949> + создавать новые роли ниже своей и редактировать все роли ниже своей, выключать микрофон и наушники других пользователей, выгонять участников, доступ в канал "tech-test" и "Для админов".

- <@&675641777012604949> : Все что и <@&675641219082092549> + создавать и редактировать каналы.

- <@&675641219082092549> : Все что и <@&675641458488770560> + отключать участникам микрофон, перемещать участников по каналам, отключать у участиков звук, просмотр журнала аудита.

- <@&675641458488770560> : Все что и <@&675641084776546304> + изменять никнеймы пользователям, перемещать участников, использовать внешнее эмодзи.

- <@&675641084776546304> : Все что и <@&675640753942167553> + упоминать всех.

- <@&675640753942167553> : Управлять эмодзи, менять себе никнейм.

- <@&578305659934605352> : Наша кибер-команда по Rainbow six Siege.

- <@&487707601543626762> : Роль которой награждают особо провинившихся.

- <@&657152105114501150> : роль для тех кто был с самого основания или же 360(+/-50) дней.

- <@&580071625370894336> : мастер по мемам.

- <@&675757505900576768> : для тех кто привел 5 или больше людей на сервер.

Список команд

$inv - инвайт в радугу.
$good - поощрение участника.
$links - ссылка-приглос на сервер.
$command - команды бота.
$rythmcom - команды бота RYTHM.

		"""
		emb = discord.Embed(title="FAQ", description= cnt, colour=0xff7733)
		await ctx.send(embed=emb)

	@commands.command()
	async def command(self, ctx):
		cnt = """
Команды для операций с деньгами.
1 Ravencoin начисляет за 1 час проведенный в голосовом канале.

$coin / $счет - проверить свой счет;
$ctop / $мтоп - посмотреть топ самых богатых;
$shop / $лавка - открыть магазин;
$time / время - ваше время проведенное в голосовых каналах;
$top / топ - топ по проведенному времени;
$panel / $панель - панель управления каналами;

		"""
		emb = discord.Embed(title="Команды raven", description=cnt, colour=0xff7733)
		await ctx.author.send(embed=emb)

	@commands.command()
	async def good(self, ctx):
		await ctx.send("Ты сегодня очень хорошо себя вел, держи конфетку :candy: .")

	@commands.command()
	async def links(self, ctx):
		cnt = """
Вот ссылка для ваших друзей, просто скопируйте ее и киньте другу.
Вам приятно, а меня мой хозяин покормит.

https://discord.gg/3SKkjmb		
		"""
		emb = discord.Embed(title="Ссылка", description=cnt, colour=0xff7733)
		await ctx.author.send(embed=emb)

	@commands.command
	async def rythmcom(self, ctx):
		cnt = """
<@235088799074484224> тут вертит пластинками, вот его команды:

!skip – пропуск трека;
!voteskip – проголосовать за пропуск композиции;
!shuffle – перемешивание треков в play-листе;
!volume – изменение громкости текущего трека;
!music_play – воспроизведение музыки;
!music pause – приостановить воспроизведение;
!playskip – текущая песня передвигается в начало очереди;
!clear – очистка очереди;
!replay – сброс прогресса текущей композиции;
!disconnect – для отключения бота от голосовых каналов;
!loop – позволяет зациклить текущую музыкальную композицию;
!remove – для удаления определенных записей из очереди;
!queue – позволяет просматривать очередь;
!removedupes – удаление дубликатов из списка композиций;
!move – перемещение определенной песни на стартовую позицию;
!join – призыв бота на голосовой канал;
!leave_voice – удаление бота из голосовых чатов.		
		"""

		emb = discord.Embed(title="Команды rhytm", description=cnt, colour=0xff7733)
		await ctx.author.send(embed=emb)

	@commands.command()
	async def inv(self, ctx):
		cnt = """
полетели играть!
Заходите в соответствующий канал, там вас уже ждут (или отошли за печеньками и успокоительным).
		"""

		emb = discord.Embed(title="Инвайт", description=cnt, colour=0xff7733)
		#emb.set_image(url='https://tenor.com/view/excited-wink-and-point-lets-go-gif-13160964')
		await ctx.send("<@&578305659934605352>" ,embed=emb)

def setup(bot):
	bot.add_cog(Helper(bot))
	print('[INFO] Helper loaded!')
