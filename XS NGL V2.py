import asyncio
import httpx
import uuid
from colorama import Fore, init
from datetime import datetime

init()

# Rainbow banner
def print_banner():
    rainbow_text = '''
███████╗██████╗░░█████╗░███╗░░░███╗███╗░░██╗░██████╗░██╗░░░░░
██╔════╝██╔══██╗██╔══██╗████╗░████║████╗░██║██╔════╝░██║░░░░░
╚█████╗░██████╔╝███████║██╔████╔██║██╔██╗██║██║░░██╗░██║░░░░░
░╚═══██╗██╔═══╝░██╔══██║██║╚██╔╝██║██║╚████║██║░░╚██╗██║░░░░░
██████╔╝██║░░░░░██║░░██║██║░╚═╝░██║██║░╚███║╚██████╔╝███████╗
╚═════╝░╚═╝░░░░░╚═╝░░╚═╝╚═╝░░░░░╚═╝╚═╝░░╚══╝░╚═════╝░╚══════╝
'''
    rainbow_colors = [Fore.RED, Fore.YELLOW, Fore.GREEN, Fore.CYAN, Fore.BLUE, Fore.MAGENTA]
    for i, line in enumerate(rainbow_text.split("\n")):
        print(rainbow_colors[i % len(rainbow_colors)] + line)

# Send message function
async def send_message(url, headers, payload):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=headers, data=payload)
            if response.status_code == 200:
                print(f"{Fore.LIGHTBLACK_EX}[{Fore.LIGHTGREEN_EX}/{Fore.LIGHTBLACK_EX}] {Fore.WHITE}Message sent successfully.")
            else:
                print(f"{Fore.LIGHTBLACK_EX}[{Fore.YELLOW}!{Fore.LIGHTBLACK_EX}] {Fore.LIGHTRED_EX}Error: {response.status_code}")
    except Exception as e:
        print(f"{Fore.LIGHTRED_EX}Error: {e}")

# Delay function
async def delay_function(seconds):
    print(f"{Fore.LIGHTBLUE_EX}Delaying for {seconds} seconds...")
    await asyncio.sleep(seconds)

# Speed levels
speed_levels = {
    "1": 10,
    "2": 20,
    "3": 50,
    "4": 100
}

# Main function
async def main():
    print_banner()  # Display banner at the start

    # Show current UTC time
    current_time = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    print(f"{Fore.LIGHTCYAN_EX}🌍 Current UTC Time: {current_time} {Fore.RESET}")

    # Check program status
    is_active = True
    if is_active:
        print(f"{Fore.LIGHTGREEN_EX}Program Status: Active ✅")
    else:
        print(f"{Fore.LIGHTRED_EX}Program Status: Inactive ❌")

    # Choose speed level
    print(f"{Fore.LIGHTGREEN_EX}Choose Speed Level:")
    for level in speed_levels:
        print(f"{Fore.LIGHTGREEN_EX}- {level}")

    speed_choice = input(f"{Fore.LIGHTWHITE_EX}Select Speed (1-4) > ")
    speed = speed_levels.get(speed_choice, 10)

    # Choose delay mode
    print(f"{Fore.LIGHTWHITE_EX}Choose Delay Mode:")
    print(f"1: Delay Mode (Delay between requests)")
    print(f"2: No Delay Mode (Maximum speed)")
    delay_choice = input(f"{Fore.LIGHTWHITE_EX}Select Mode (1 or 2) > ")

    delay_time = 0
    if delay_choice == "1":
        delay_time = float(input(f"{Fore.LIGHTWHITE_EX}Enter delay time (seconds, e.g., 0.5) > "))

    # Choose shooting mode
    print(f"{Fore.LIGHTWHITE_EX}Choose Shooting Mode:")
    print(f"1: Normal Mode (Shoot 1 message per round)")
    print(f"2: Ultra Mode (Shoot 2 messages per round)")
    print(f"3: Super Ultra Mode (Shoot 3 messages per round)")
    print(f"4: Base Ultra Mode (Shoot 5 messages per round)")
    print(f"5: God Ultra Mode (Shoot 10 messages per round)")
    mode_choice = input(f"{Fore.LIGHTWHITE_EX}Select Mode (1-5) > ")

    target = input(f"{Fore.LIGHTWHITE_EX}Enter NGL username or URL > ")
    message = input(f"{Fore.LIGHTWHITE_EX}Enter message to send > ")
    count = int(input(f"{Fore.LIGHTWHITE_EX}Number of requests > "))

    # Determine number of messages per round
    message_count = {
        '1': 1,
        '2': 2,
        '3': 3,
        '4': 5,
        '5': 10
    }.get(mode_choice, 1)

    headers = {"User-Agent": "Mozilla/5.0"}
    payload = {
        "username": target,
        "question": message,
        "deviceId": str(uuid.uuid4()),
        "gameSlug": None,
        "referrer": None,
    }

    # Sending Messages
    for i in range(count):  # Loop จำนวนครั้งที่กำหนดใน count
        tasks = []
        for _ in range(message_count):  # ส่งข้อความตามจำนวนที่เลือกใน Shooting Mode
            tasks.append(send_message("https://ngl.link/api/submit", headers, payload))
        await asyncio.gather(*tasks)

        # Handle delay if selected
        if delay_choice == "1":
            print(f"{Fore.LIGHTBLUE_EX}Delaying for {delay_time} seconds...")
            await asyncio.sleep(delay_time)

# Run the main function
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"{Fore.LIGHTRED_EX}Error: {e}")