import discord
from discord.ext import commands
from discord import utils
import datetime, pytz

tz = pytz.timezone('Asia/Bangkok')

token = "MTM4MDAwNzY0NjI3ODcxMzQ2NA.GVvx8g.i8iH2J120kfqwW44i3UsSruIl7CVL5BvYqzyB8"  # โทเค่นบอท

channelid = 1379352777863467052  # ไอดี log
channelCategory = 1379352532970766336  # ไอดีหมวดหมู่
adminid = 1289596952903942146  # ไอดีแอดมิน
owner_id = 1289596952903942146  # ไอดีเจ้าของดิส

def now():
    now1 = datetime.datetime.now(tz)
    month_name = now1.month
    thai_year = now1.year
    time_str = now1.strftime('%H:%M:%S')
    return "%d/%s/%d %s" % (now1.day, month_name, thai_year, time_str)

class Message(discord.ui.Modal, title='ระบบแจ้งปัญหานักเรียน'):
    def __init__(self):
        super().__init__(timeout=None, custom_id='ticket_model_001')

        self.message = discord.ui.TextInput(
            label='แจ้งปัญหาหรือส่งคำติชมถึงสภานักเรียน',
            style=discord.TextStyle.long,
            placeholder='โปรดเขียนรายละเอียดของปัญหาหรือข้อเสนอแนะอย่างสุภาพ',
        )
        self.add_item(self.message)

    async def on_submit(self, interaction: discord.Interaction):
        guild = interaction.guild
        category = guild.get_channel(channelCategory)
        admin = guild.get_member(adminid)
        owner = guild.get_member(owner_id)

        existing = utils.get(interaction.guild.text_channels, name=f"{interaction.user.name.lower().replace(' ', '-')}-{interaction.user.discriminator}")
        if existing is not None:
            embed = discord.Embed(
                title="ระบบแจ้งปัญหา",
                description=f"คุณได้สร้าง Ticket ไว้แล้ว กรุณารอการตอบกลับก่อนสร้างใหม่ที่ {existing.mention}!",
                color=0xfa0d0d
            )
            embed.set_footer(text=now())
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            interaction.user: discord.PermissionOverwrite(read_messages=True, send_messages=True),
        }

        if admin:
            overwrites[admin] = discord.PermissionOverwrite(read_messages=True, send_messages=True)
        else:
            print(f"⚠️ ไม่พบ admin ID {adminid} ใน server นี้")

        if owner:
            overwrites[owner] = discord.PermissionOverwrite(read_messages=True, send_messages=True)
        else:
            print(f"⚠️ ไม่พบ owner ID {owner_id} ใน server นี้")

        # เพิ่ม role ที่ดูแลได้
        allowed_roles = [1380155970390462537, 1379405248107384923]
        for role_id in allowed_roles:
            role = interaction.guild.get_role(role_id)
            if role is not None:
                overwrites[role] = discord.PermissionOverwrite(
                    view_channel=True,
                    send_messages=True,
                    read_message_history=True
                )
            else:
                print(f"⚠️ ไม่พบ role ID {role_id} ใน server นี้")

        channel = await guild.create_text_channel(
            name=f"ticket-{interaction.user.id}",
            category=category,
            overwrites=overwrites
        )

        embed_ticket = discord.Embed(
            title="📮 สร้างตั๋ว",
            description=f"""{interaction.user.mention}
        แอดมิน <@{adminid}>
        ```🎀 ติดต่อเรื่อง {self.message.value}```
        🍧 โปรดรอแอดมินมาตอบนะครับ""",
            color=0xdddddd
        )

        embed_ticket.set_image(url="https://your_image_url_here")

        embed_ticket.set_image(url="https://cdn.discordapp.com/attachments/1166453203764789410/1176917209554092133/7cfef8409d92517cc9ab6a2ecf8730de.gif")
        # ลองไม่ส่ง embed2 ซ้ำอีกครั้ง เพราะเราใช้ embed_ticket ไปแล้วข้างบน
        embed_ticket.set_image(url="https://cdn.discordapp.com/attachments/1166453203764789410/1176917209554092133/7cfef8409d92517cc9ab6a2ecf8730de.gif")
        try:
            await channel.send(embed=embed_ticket, view=Close_ticket())
        except Exception as e:
            print(f"เกิดข้อผิดพลาดตอนส่ง embed ไปยังห้อง ticket: {e}")

        embed_log = discord.Embed(
            title="เปิด Ticket",
            description=f"เปิด Ticket โดย <@{interaction.user.id}> ห้อง {channel.mention}",
            color=0x1BE51B
        )
        embed_log.set_footer(text=now())
        log_channel = guild.get_channel(channelid)
        await log_channel.send(embed=embed_log)

        await interaction.response.send_message(
            f"✅ Ticket ถูกสร้างแล้ว! ไปที่ห้อง {channel.mention}",
            ephemeral=True
        )

class Create_ticket(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(emoji="🎫", label="สร้างตั๋ว", style=discord.ButtonStyle.green, custom_id="ticket_button_001")
    async def create_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(Message())

class Close_ticket(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(emoji="🎫", label="ปิด Ticket", style=discord.ButtonStyle.red, custom_id="ticket_button_002")
    async def close_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        member = interaction.user
        await interaction.response.send_message(view=Confirm_close_ticket(), ephemeral=True)

        embed = discord.Embed(
            title="ปิด Ticket",
            description=f"ปิด Ticket โดย <@{member.id}> ห้อง {interaction.channel.mention}",
            color=0xfa0d0d
        )
        embed.set_footer(text=now())
        log_channel = interaction.guild.get_channel(channelid)
        await log_channel.send(embed=embed)

class Confirm_close_ticket(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(emoji="✅", label="ลบ Ticket", style=discord.ButtonStyle.red, custom_id="ticket_button_003")
    async def close_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        # ✅ ตรวจสอบว่าเป็นเจ้าของห้องหรือ admin
        try:
            ticket_owner_id = int(interaction.channel.name.split("-")[-1])
        except ValueError:
            ticket_owner_id = None

        if interaction.user.id != ticket_owner_id and not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message(
                "❌ คุณไม่มีสิทธิ์ลบ Ticket นี้",
                ephemeral=True
            )
            return

        await interaction.response.send_message("🗑️ กำลังลบ Ticket...", ephemeral=True)

        embed = discord.Embed(
            title="ลบ Ticket",
            description=f"ลบ Ticket โดย <@{interaction.user.id}>",
            color=0xfa0d0d
        )
        embed.set_footer(text=now())

        log_channel = interaction.guild.get_channel(channelid)
        if log_channel:
            await log_channel.send(embed=embed)

        # ✅ ใช้บอทลบ ไม่อิง permission ของคนกด
        await interaction.channel.delete()

class MyBot(commands.Bot):
    def __init__(self) -> None:
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(
            command_prefix='!',
            help_command=None,
            case_insensitive=True,
            intents=intents,
        )
        self.owner_id = owner_id

    async def on_ready(self) -> None:
        print(f'Logged in as: {self.user}')

    async def setup_hook(self) -> None:
        self.add_view(Create_ticket())

bot = MyBot()

@bot.command()
@commands.has_permissions(administrator=True)
async def setup(ctx: commands.Context):
    await ctx.message.delete()

    embed = discord.Embed(
        title="📣 เเจ้งปัญหา / ติดต่อสภา",
        description="\n\n🎀 สำหรับ สอบถาม แจ้งปัญหา \n เราจะปิด ticket ภายใน 30นาที หากไม่มีการตอบกลับจากนักเรียน\nกรุณาอย่ากดเล่นนะครับ..",
        color=0xdddddd
    )
    embed.set_image(url='https://cdn.discordapp.com/attachments/1166453203764789410/1176917209554092133/7cfef8409d92517cc9ab6a2ecf8730de.gif')
    embed.set_footer(text="BOT SEVER  © discord.gg/")

    await ctx.send(embed=embed, view=Create_ticket())

bot.run(token)
