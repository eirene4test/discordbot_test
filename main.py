import discord
from discord import app_commands
from discord.ext import commands
import asyncio
import time
import random
import pickle
import os
def caesar(txt,n):
	result = ""
	for c in txt:
		result += chr(ord(c)+n)
	return result
token =caesar("QXM6RnE4SHQ}RnU}SH]5RX]~Rk2KQJRIH2IqEn8eE8J{izG}l|Vgc~rxm7hOr{RKcqJlUK^{",-4)

'''권한
0b0000001. 대화
0b0000010. 메모
0b0000100. 메모삭제
0b0001000. 활동
0b0010000. 재우기/깨우기
0b0100000. 오지마 / 와도돼
0b1000000. 권한설정
default = 0b0010011

'''

dict_kw = {
"도움말": ["도움말","사용법","설명","설명해줘","?"],
"안녕": ["안녕","안녕!","안녕?","안녕~","오하요", "곤쨔","곤니찌와"],
"어디갔어": ["어디갔어","어디갓어","어디가써","어디갔어?","도꼬","도꼬?","어디가써?"],
"해줘": ["해줘"],
"뭐해": ["뭐해","뭐해?","머해","머해?"],
"생존수칙": ["생존수칙"],
"이야기집": ["이야기집"],
"메모해줘": ["메모해줘","기억해줘"],
"메모장": ["메모장","메모지","까먹었어"],
"메모지워": ["메모지워","까먹어줘"],
"잘자": ["잘자","잘쟈","잘자~","잘자!","오야스미","오야스미~","굿나잇"],
"일어나": ["일어나","일어나!","아침이야","오키나사이","학교가야지"],
"오지마": ["오지마"],
"와도돼": ["와도돼","와"],
"박제해": ["박제해","박제해줘"],
"박제하지마": ["박제하지마","박제하지말아줘"],
"박제하는곳": ["박제하는곳","박제탭"],
"권한설정": ["권한설정"],
"권한보기": ["권한보기"],
"내권한": ["내권한"]
}




info_perm = """0b0000001 : 대화
0b0000010 : 메모 남기기 & 메모 보기
0b0000100 : 메모 지우기
0b0001000 : 활동 설정하기
0b0010000 : 재우기 & 깨우기
0b0100000 : 오지마•와도돼 & 박제해• 박제하지마•박제하는곳
0b1000000 : 도도코 권한 설정"""
dict_info={
"도움말": [["키워드"],1,"도도코 도움말이야!\n키워드가 없으면 키워드가 뭐가 있는지 알려주고,\n키워드가 있으면 설명해줘!"],
"안녕": [[],1,"안녕!"],
"어디갔어": [[],1,"나 여깃어!"],
"해줘": [["내용"],0b1001, "활동상태를 하라고 한걸로 바꿔!"],
"뭐해": [[],1,"활동상태를 알려줘!"],
"생존수칙": [[],1,"케이아 오빠가 만들어준 클레의 기사단 생존수칙이야!"],
"이야기집": [[],1,"\\(^o^)/"],
"메모해줘": [["내용"],0b11,"메모해두께!\n`도도코 메모장`으로 내용을 볼 수 있고 `도도코 메모지워`로 지울 수 있어!"],
"메모장": [[],0b11,"도도코가 메모해둔 내용이야!"],
"메모지워": [[],0b101,"메모해둔 걸 지울께! 지운 메모는 되돌릴 수 없어!"],
"잘자": [[],0b10001,"잘쟈~"],
"일어나": [[],0b10001,"일어날 수 있을지는 모르겠지만 일단 일어나볼께"],
"오지마": [[],0b0100001, "그 방에서는 나 불러도 대답 안할게"],
"와도돼": [[],0b0100001, "그 방에서 나 부르면 대답할게"],
"박제해": [[],0b0100001, "그 방에서 메시지가 삭제되면 뭐였는지 얘기할게!"],
"박제하지마": [[],0b0100001, "그 방에서 메시지가 삭제돼도 뭐였는지 얘기 안할게!"],
"박제하는곳": [["\"없애\" 라고 하면 지정 취소"],0b0100001,"박제는 그 방에서 할게"],
"권한설정": [["대상","권한"],0b1000000,f"대상의 도도코 권한을 설정해! \n\n{info_perm}"],
"권한보기": [["대상"],0b1000000,f"대상의 도도코 권한을 알려줘! \n\n{info_perm}"],
"내권한": [[],0b0000001,f"자신의 도도코 권한을 알려줘! \n\n{info_perm}"],
}





intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(
			command_prefix="도도코 ",
			intents=intents.all(),
			sync_command=True,
			application_id= 1266048326428655636
		)

def log(ctx,message,type = "send message"):
	txt = f"""{time.strftime("%Y/%m/%d %H:%M:%S")}, {ctx.guild}/{ctx.channel} {type}: \"{message}\"\n"""
	print(txt)
	return
	with open("log.txt",mode="a",encoding = "utf-8") as f:
		f.write(txt)

async def say(ctx,message,type = "send message"):
	log(ctx,message,type)
	await ctx.channel.send(message)

is_sleeping = 0
async def sleeping(ctx):
	if is_sleeping:
		await say(ctx,"Zzz...")
	return bool(is_sleeping)




@bot.command(aliases=dict_kw["일어나"][1:])
async def 일어나(ctx,*msg):
	if await check(ctx,dict_info["일어나"][1],*msg,sleepCheck = False): return
	global is_sleeping
	if is_sleeping:
		is_sleeping -= 1
		if is_sleeping:
			await say(ctx,random.choice(["조금만 더...","5분만...","으으에..."]))
		else:
			await say(ctx,"으음... 도도코 일어낫어!")
	else:
		await say(ctx,"으응? 이미 일어나 있었어!")





@bot.command(aliases=dict_kw["잘자"][1:])
async def 잘자(ctx,*msg):
	if await check(ctx,dict_info["잘자"][1],*msg): return
	global is_sleeping
	is_sleeping = random.randint(1,3)
	await say(ctx, "잘쟈"+"~"*is_sleeping)
	





@bot.event
async def setup_hook():
	await bot.tree.sync()

@bot.event
async def on_ready():
	print("ready!")
	activity = discord.Game("클레가 도도코 기여어")
	await loadData()
	await bot.change_presence(status=discord.Status.online, activity=activity)


	


@bot.command(aliases=dict_kw["안녕"][1:])
async def 안녕(ctx,*msg):
	if await check(ctx,dict_info["안녕"][1],*msg): return
	#print(dir(ctx.author))
	await say(ctx,f"{ctx.author.display_name} 안녕!")
	#await say(ctx, f"{msg}")


@bot.command(aliases=dict_kw["어디갔어"][1:])
async def 어디갔어(ctx,*msg):
	if await check(ctx,dict_info["어디갔어"][1],*msg): return
	where = ["클레 등 뒤","클레 가방 안", "클레 손 위"]
	await say(ctx, f"{random.choice(where)}에 잇어")
	#await say(ctx, f"{msg}")





doing = "클레가 도도코 기여어"
@bot.command(aliases=dict_kw["해줘"][1:])
async def 해줘(ctx,*msg):
	if await check(ctx,dict_info["해줘"][1],*msg): return
	global doing
	doing = ' '.join(msg)
	activity = discord.Game(f"""{doing}""")
	await bot.change_presence(status=discord.Status.online, activity=activity)
	await say(ctx, "알앗어")




@bot.command(aliases=dict_kw["뭐해"][1:])
async def 뭐해(ctx,*msg):
	if await check(ctx,dict_info["뭐해"][1],*msg): return
	await say(ctx,f"{doing} 하는중이야!")





@bot.command(aliases=dict_kw["생존수칙"][1:])
async def 생존수칙(ctx,*msg):
	if await check(ctx,dict_info["생존수칙"][1],*msg): return
	delay = 3
	await say(ctx, '성 안 폭탄 투척, 감금실행')
	await asyncio.sleep(delay)
	await say(ctx, '폭탄에 사람 부상, 진이 방문')
	await asyncio.sleep(delay)
	await say(ctx, '산불 방화, 클레 끝장')
	await asyncio.sleep(delay*0.8)
	await say(ctx, "이게 바로 클레의 기사단 생존 수칙이야!")





def 받침(text):
	return bool((ord(text[-1])-0xAC00)%28)


#@bot.event
async def on_command_error(ctx,error):
	if await check(ctx,0b0000001,[]): return
	err = str(error).split(" ")[1][1:-1]
	b = 받침(err)
	print(error)
	await say(ctx,f"""{ctx.author.display_name} 언니? 「{err if err != 'aise' else 'Error'}」{"가" if not b else "이"} 머야?""","error")


debug = ""
@bot.event
async def on_message_delete(message):
	global debug
	debug = (dir(message),"")
	print("에헤")
	if message.author.display_name == "도도코":
		return
	global is_sleeping
	if is_sleeping:
		is_sleeping = 0
		#await say(message,"(화들짝)")
	who = message.author.display_name
	#print(message.content)
	if message.channel.id in data[message.guild.id]["박제해"]:
		if data[message.guild.id]["박제하는곳"]!=0:
			await message.guild.get_channel(data[message.guild.id]["박제하는곳"]).send(f"""{who}{"이" if 받침(who) else "가"} {str(message.channel)}에서 「{message.content}」라고 했었어!""")
		else:
			await message.channel.send(f"""{who}{"이" if 받침(who) else "가"} 「{message.content}」라고 했었어!""")

@bot.event
async def on_bulk_message_delete(messages):
	for message in messages:
		on_message_delete(message)


@bot.command(aliases=dict_kw["박제하는곳"][1:])
async def 박제하는곳(ctx,*msg):
	if await check(ctx,dict_info["박제하는곳"][1],*msg,sleepCheck = False, canGoCheck=False): return
	global data
	if len(msg)>0 and msg[0]=="없애":
		data[ctx.guild.id]["박제하는곳"] = 0
		await say(ctx,"박제는 그러면 삭제된 그 방에다가 할께")
		saveData()
		return
	data[ctx.guild.id]["박제하는곳"] = ctx.channel.id
	await say(ctx, "박제는 이쪽으로 하께")
	saveData()


@bot.command(aliases=dict_kw["메모해줘"][1:])
async def 메모해줘(ctx,*msg):
	if await check(ctx,dict_info["메모해줘"][1],*msg): return
	await say(ctx, "메모해두께")
	with open(file="memo.txt",encoding="utf-8",mode = "a") as f:
		data[ctx.guild.id]["메모"].append(" ".join(msg))
		log(ctx," ".join(msg),"memo")


@bot.command(aliases=dict_kw["메모장"][1:])
async def 메모장(ctx,*msg):
	if await check(ctx,dict_info["메모장"][1],*msg): return
	#await say(ctx, "메모해두께")
	text = data[ctx.guild.id]["메모"]
	await say(ctx, ('>>> ' + '\n'.join(text)) if text != [] else "어라? 메모장이 비어잇서")

@bot.command(name="계산")
async def 계산(ctx,*msg):
	if ctx.author.name != "eirene0507":
		await say(ctx, "시러")
	else:
		result = eval(" ".join(msg))
		print(result)
		await say(ctx, result)

@bot.command(name="실행")
async def 실행(ctx,*msg):
	if ctx.author.name != "eirene0507":
		await say(ctx, "시러")
	else:
		try:
			exec(' '.join(msg).replace("^","\n").replace(";"," "))
		except Exception as e:
			await say(ctx, "에러가 낫어")
			await say(ctx,e)
		else:
			await say(ctx, "에러 안낫어")



def info(kw):
	k = kw
	for keywords in dict_kw.values():
		if kw in keywords:
			k = keywords[0]
	if k in dict_info:
		return arrange_info(kw)
	else:
		return 0

def arrange_info(kw):
	list_info = dict_info[kw]
	result = f'''>>> # ```도도코 {kw} {(" ".join(("<"+x+">") for x in list_info[0]))}```
다른 사용법:
{", ".join(("`도도코 "+k+"`") for k in dict_kw[kw][1:])}

필수 권한: {list_info[1]:#09b}


{list_info[2]}

'''
	return result




	

@bot.command(aliases=["?"])
async def 도움말(ctx,*msg):
	if await check(ctx,0b0000001,*msg): return
	result = info(" ".join(msg))
	if result == 0:
		kws = ', '.join(dict_kw.keys())
		await say(ctx,info("도움말")+f"""키워드:\n{kws}\n\n""")
	else:
		await say(ctx,result)
		



@bot.command(aliases=dict_kw["메모지워"][1:])
async def 메모지워(ctx,*msg):
	if await check(ctx,dict_info["메모지워"][1],*msg): return
	data[ctx.guild.id]["메모"] = []
	await say(ctx,"알앗어")


@bot.command(aliases=dict_kw["이야기집"][1:])
async def 이야기집(ctx,*msg):
	if await check(ctx,dict_info["이야기집"][1],*msg): return
	await say(ctx,":>")




async def check(ctx,perm,*msg,sleepCheck=True,canGoCheck = True):
	if ctx.author.id not in data[ctx.guild.id]["권한"]:
		data[ctx.guild.id]["권한"][ctx.author.id] = 0b0010011
	perm_loaded = data[ctx.guild.id]["권한"][ctx.author.id]
	print(bin(perm),bin(perm_loaded),perm & perm_loaded)
	if canGoCheck:
		if ctx.channel.id in data[int(ctx.guild.id)]["오지마"]:
			return True
	if sleepCheck:
		if await sleeping(ctx):
			return True
	if (perm & perm_loaded) != perm:
		await say(ctx,"시러")
		return True
	return False

		
@bot.command(aliases=dict_kw["권한설정"][1:])
async def 권한설정(ctx,*msg):
	if await check(ctx,dict_info["권한설정"][1],*msg): return
	id = id_by_nick(ctx,msg[0])
	if id == 0:
		await say(ctx, "누구...?")
	perm = int(msg[1],2) if "0b" in msg[1] else int(msg[1])
	data[ctx.guild.id]["권한"][id] = perm
	await say(ctx, f"{msg[0]}의 권한을 {perm:#09b}({perm}){'로' if msg[1][-1]=='1' else '으로'} 설정했어!")
	saveData()
	
@bot.command(aliases=dict_kw["권한보기"][1:])
async def 권한보기(ctx,*msg):
	if len(msg)==0:
		await 내권한(ctx,*msg)
		return
	if await check(ctx,dict_info["권한보기"][1],*msg): return
	id = id_by_nick(ctx,msg[0])
	if id == 0:
		await say(ctx, "누구...?")
	if id not in data[ctx.guild.id]["권한"]:
		data[ctx.guild.id]["권한"][id] = 0b0010011
	perm = data[ctx.guild.id]["권한"][id]
	await say(ctx, f"{msg[0]}의 권한은 {perm:#09b}({perm})이야!")

@bot.command(aliases=dict_kw["내권한"][1:])
async def 내권한(ctx,*msg):
	if await check(ctx,dict_info["내권한"][1],*msg): return
	id = ctx.author.id
	if id not in data[ctx.guild.id]["권한"]:
		data[ctx.guild.id]["권한"][id] = 0b0010011
	perm = data[ctx.guild.id]["권한"][id]
	await say(ctx, f"{ctx.author.display_name}의 권한은 {perm:#09b}({perm})이야!")


def id_by_nick(ctx,nick):
	result = 0
	for member in ctx.guild.members:
		if nick in str(member.display_name):
			result = member.id
			break
	return result

def nick_by_id(ctx,id):
	for member in ctx.channel.members:
		if id == str(member.id):
			return member.display_name
	return 0

def channel_by_id(ctx,id):
	for ch in ctx.guild.channels:
		if id == ch.id:
			return ch.name
	return 0

def ch_instance_by_id(ctx,id):
	for ch in ctx.guild.channels:
		if id == ch.id:
			return ch
	return 0

def id_by_channel(ctx,name):
	for ch in ctx.guild.channels:
		if name == ch.name:
			return ch.id

@bot.command(aliases=dict_kw["오지마"][1:])
async def 오지마(ctx,*msg):
	if await check(ctx,dict_info["오지마"][1],*msg,canGoCheck=False): return
	if ctx.channel.id in data[int(ctx.guild.id)]["오지마"]:
		return
	await say(ctx,"알앗어 여기는 이제 안올께")
	data[int(ctx.guild.id)]["오지마"].append(int(ctx.channel.id))
	saveData()

@bot.command(aliases=dict_kw["와도돼"][1:])
async def 와도돼(ctx,*msg):
	if await check(ctx,dict_info["와도돼"][1],*msg,canGoCheck=False): return
	if ctx.channel.id not in data[int(ctx.guild.id)]["오지마"]:
		await say(ctx,"으응? 여기 와도 되는거 아니었어?")
		return
	await say(ctx,"오예! 와도 된다!")
	del_idx = 0
	for x in range(len(data[int(ctx.guild.id)]["오지마"])):
		id = data[int(ctx.guild.id)]["오지마"][x]
		if id==ctx.channel.id:
			del_idx = x
			break
	del data[int(ctx.guild.id)]["오지마"][del_idx]
	saveData()
	
@bot.command(aliases=dict_kw["박제해"][1:])
async def 박제해(ctx,*msg):
	if await check(ctx,dict_info["박제해"][1],*msg,canGoCheck=False): return
	if ctx.channel.id in data[int(ctx.guild.id)]["박제해"]:
		return
	await say(ctx,"알앗어 여기 박제할게")
	data[int(ctx.guild.id)]["박제해"].append(int(ctx.channel.id))
	saveData()

@bot.command(aliases=dict_kw["박제하지마"][1:])
async def 박제하지마(ctx,*msg):
	if await check(ctx,dict_info["박제하지마"][1],*msg,canGoCheck=False): return
	if ctx.channel.id not in data[int(ctx.guild.id)]["박제해"]:
		await say(ctx,"여기 박제 안하께")
		return
	await say(ctx,"여기 박제 안하께")
	del_idx = 0
	for x in range(len(data[int(ctx.guild.id)]["박제해"])):
		id = data[int(ctx.guild.id)]["박제해"][x]
		if id==ctx.channel.id:
			del_idx = x
			break
	del data[int(ctx.guild.id)]["박제해"][del_idx]
	saveData()






data = {}
async def loadData():
	global data
	if os.path.exists("Data"):
		with open(file = "Data",mode="rb") as f:
			data = pickle.load(f)
	else:
		data = {}
		data["게임"] = {}
	guilds = bot.fetch_guilds()
	async for guild in guilds:
		if guild.id not in data:
			data[guild.id] = {"오지마":[],"권한":{825332370848743435:0b1111111},"박제하는곳":0,"박제해":[]}
		if "박제하는곳" not in data[guild.id]:
			data[guild.id]["박제하는곳"]=0
		if "박제해" not in data[guild.id]:
			data[guild.id]["박제해"]=[]
		if "메모" not in data[guild.id]:
			data[guild.id]["메모"]=[]
		if "게임" not in data[guild.id]:
			data[guild.id]["게임"]={}


	
	

def saveData():
	global data
	with open(file = "Data",mode="wb") as f:
		pickle.dump(data,f)












#물 = "물"
#불= "불"
#풀 = "풀"
#얼음 = "얼음"
#바위 = "바위"
#바람 = "바람"
#번개 = "번개"
#물리 = "물리"
#관통 = "관통"

#class Card:
#	def __init__(self):
#		pass
#	def __getitem__(self,key):
#		return getattr(self, key)
#	def on_normal_hit(self,req,room): return
#	def on_normal_hit_prep(self,req,room): return
#	
#	def on_elemental_skill(self,req,room): return
#	def on_elemental_skill_prep(self,req,room): return
#	
#	def on_elemental_burst_prep(self,req,room): return
#	def on_elemental_burst(self,req,room): return
#	
#	def on_turn_end(self,req,room): return
#	def on_hit(self,req,room): return

#	def on_enemy_skill(self,req,room): return
#	def after_enemy_skill(self,req,room): return
#	def after_action(self,req,room): return
#	
#	def on_room_enter(self,req,room): return
#	def normal(self): return
#	def elemental_skill(self):return
#	def elemental_burst(self): return
#	def on_room_enter(self,room):
#		self.room = room
#	def description(self,foe = False):
#		return ""
#	def on_dice(self,req,room):
#		return
#	

#class Enemies:
#	def __init__(self,room,count,type=-1):
#		self.room = room
#	def hit(self,dmg,element=물리):
#		pass

#class Enemy(Card):
#	pass

#class 츄츄_싸움꾼(Enemy):
#	def __init__(self):
#		self.status = Status(hp=4,maxE = 2)
#		self.ap = 3
#	
#	def normal(self):
#		self.ap -= 1
#		self.room.player.hit(1,물리)
#	


#class Room:
#	def __init__(self,player,type = -1):
#		self.player = player
#		self.enemy = Enemies(self,0)
#		self.loot = []

#class 펑펑_선물(Card):
#	def __init__(self):
#		pass

#class 폭렬_불꽃(Card):
#	def __init__(self):
#		self.stack = 0
#	def on_normal_hit_prep(self,req,room):
#		if self.stack > 0 and room.player.dice %2 == 0:
#			self.used = 1
#			req.dmg_up += 1
#			req.rdc_dice += 1
#	
#	def on_normal_hit(self,req,room):
#		if self.stack > 0 and self.used:
#			self.stack -= 1
#		return
#	
#	def after_action(self,req,room):
#		self.used = 0
#		return
#	def on_elemental_skill(self,req,room):
#		t = room.player.find_effect(펑펑_선물)
#		if t == 0:
#			self.stack = 1
#		else:
#			self.stack = 2
#		return
#		
#class 쾅쾅_불꽃(Card):
#	def after_enemy_skill(self,req,room):
#		room.enemy.hit(2,불)

#class Skill_req:
#	def __init__(self,rqd=0,rdd=0,rqe=0,rde=0,dmg=0,udm=0):
#		self.req_dice = rqd
#		self.rdc_dice = rdd
#		self.req_energy = rqe
#		self.rdc_energy = rde
#		self.dmg = dmg
#		self.up_dmg = udm

#	
#class Status:
#	def __init__(self,maxhp = 10,maxE = 3,max_dice=8):
#		self.maxhp = maxhp
#		self.hp = maxhp
#		self.stack = 0
#		self.effects = []
#		self.element = "none"
#		self.maxStack = 3
#		self.max_dice = max_dice
#		self.dice = 0

#	def stackUp(self,c):
#		self.stack += c
#		if self.stack > self.maxStack:
#			self.stack = self.maxStack
#		if self.stack < 0:
#			self.stack = 0

#class Character(Card):
#	def __init__(self):
#		self.status = Status()
#		self.room = None
#	def find_effect(self,t):
#		for e in self.status.effects:
#			if type(e) == type(t):
#				return e
#		return 0
#	def iter(self,key,req):
#		for x in self.status.effects:
#			x[key](req,self.room)
#	def hit(self,dmg,type=물리):
#		self.status.hp -= dmg
#	def on_room_enter(self,room):
#		self.room = room
#		self.status.stack = 0
#		self.status.dice = 0
#		


#class 클레(Character):
#	def __init__(self):
#		self.status = Status()
#		self.status.effects.append(폭렬_불꽃())
#		self.normal = 펑펑
#		self.elemental_skill = 통통_폭탄
#		self.elemental_burst = 쾅쾅_불꽃
#		self.room = None
#	

#	def 통통_폭탄(self):
#		req = Skill_req(3,0,0,0,3,0)
#		self.iter("on_elemental_skill_prep",req)
#		if self.dice < req.req_dice - req.rdc_dice:
#			return 1
#		
#		self.iter("on_elemental_skill",req)
#		self.status.stackUp(1)
#		self.status.dice -= req.req_dice-req.rdc_dice
#		self.room.enemy.hit(req.dmg + req.dmg_up,불)
#		self.iter("after_action",req)
#		return
#	def 펑펑(self):
#		req = Skill_req(3,0,0,0,3,0)
#		self.iter("on_normal_hit_prep",req)
#		if self.dice < req.req_dice - req.rdc_dice:
#			return 1
#		
#		self.iter("on_normal_hit",req)
#		self.status.stackUp(1)
#		self.status.dice -= req.req_dice-req.rdc_dice
#		self.room.emeny.hit(req.dmg + req.dmg_up,'pyro')
#		
#		self.iter("after_action",req)	
#		return
#	
#	def 쾅쾅_불꽃(self):
#		req = Skill_req(3,0,3,0,3,0)
#		self.iter("on_elemental_burst_prep",req)
#		
#		if self.status.dice < req.req_dice - req.rdc_dice:
#			return 1
#		
#		if self.status.stack < req.req_energy - req.rdc_energy:
#			return 2
#		
#		self.iter("on_elemental_burst",req)
#		self.status.stackUp(-3)
#		self.status.dice -= req.req_dice-req.rdc_dice
#		self.room.ememy.hit(req.dmg+req.dmg_up,'pyro')
#		self.iter("after_action",req)
#		return


#class DodoGame:
#	
#	def __init__(self,owner):
#		self.owner = owner
#		self.player = 클레()
#		self.room = Room(self.player,0)
#		self.displayName = ""
#		self.hand = []
#		self.turn = -1
#	
#	def start_boukenn(self,ctx):
#		self.displayName = nick_by_id(ctx,self.owner)
#	
#	def show_status(self,ctx):
#		status = self.player.status
#		
#		return f"""# >>> ({status.hp:02d}) {self.displayName} {'●'*status.stack}{'○'*(status.maxStack - status.stack)}

#보유 효과:
#{'^'.join(x.description() for x in status.effects)}



#패:
#{'^'.join(x.description() for x in self.hand)}


#Dice: {'◇'*self.dice}
#""".replace("^","\n")
#	
#	


#@bot.command(name="모험")
#async def 모험(ctx,*msg):
#	id = ctx.author.id
#	if len(msg)==0 or id not in data["게임"]:
#		if id not in data["게임"]:
#			data["게임"][id] = DodoGame(id)
#		if id in data[ctx.guild.id]["게임"] and channel_by_id(ctx,data[ctx.guild.id]["게임"][id]) != 0:
#			await ch_instance_by_id(ctx,data[ctx.guild.id]["게임"][id].thread_id).send(data[ctx.guild.id]["게임"][id].show_status())
#		else:
#			thread = await ctx.channel.create_thread(
#			name = ctx.author.display_name + " 이야기집",
#			auto_archive_duration = 60
#			)
#			await say(ctx,thread.jump_url)
#			await thread.send(f"{ctx.author.mention} 안녕!")
#			await thread.send(data["게임"][id].start_boukenn(ctx))
#		return
#	if not (id in data[ctx.guild.id]["게임"] and channel_by_id(ctx,data[ctx.guild.id]["게임"][id]) != 0): return
#	game = data["게임"][id]


#	if msg[0]=="카드사용":
#		pass
#	
#	if "".join(msg) in ["일반공격"]:
#		result = game.player.normal()
#		if result == 1:
#			await say(ctx,"주사위가 업써")
#		else:
#			await say(ctx,"공격!")
#	
#	if "".join(msg) in ["원소스킬"]:
#		result = game.player.elemental_skill()
#		if result == 1:
#			await say(ctx,"주사위가 업써")
#		else:
#			await say(ctx,"공격!")
#	
#	if "".join(msg) in ["원소폭발","궁","궁극기"]:
#		result = game.player.elemental_burst()
#		if result == 1:
#			 await say(ctx,"주사위가 업써")
#		elif result == 2:
#			await say(ctx,"원소 에너지가 모잘라")
#		else:
#			await say(ctx,"공격!")
	

	






bot.run(token)