from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
import time

from Player import Player


# Function to initialize the web driver
def init_driver():
    # Set Chrome options to open in incognito mode
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--incognito")

    # Specify the path to the ChromeDriver
    driver = webdriver.Chrome(options=chrome_options)
    return driver


# Function to join a Poker Now table
def join_poker_table(driver, poker_now_link):
    driver.get(poker_now_link)
    time.sleep(5)  # Wait for the page to load

    # Click the "Join Game" button (assuming there's a button with this label)
    join_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Join Game')]")
    join_button.click()
    time.sleep(3)


# Function to pull hand information
def get_hand_info(driver):
    hand_info = {}

    # Locate and extract hand information elements (this will depend on the site's HTML structure)
    try:
        hand_element = driver.find_element(By.CLASS_NAME, 'player-hand')
        hand_info['hand'] = hand_element.text

        # Extract community cards information
        community_cards_element = driver.find_elements(By.CLASS_NAME, 'community-card')
        hand_info['community_cards'] = [card.text for card in community_cards_element]
    except Exception as e:
        print(f"Could not find hand information: {e}")

    return hand_info


# Main function to run the bot
def main(poker_now_link):
    driver = init_driver()
    join_poker_table(driver, poker_now_link)

    # Continuous loop to keep pulling hand information



if __name__ == "__main__":
    driver = init_driver()
    driver.get("https://www.pokernow.club/games/pglEXjApjpuEDo8HmTu0pMoPs")
    time.sleep(5)  # Wait for the page to load
    seats_div = driver.find_element(By.CLASS_NAME, 'seats')
    seat_elements = seats_div.find_elements(By.CLASS_NAME, 'table-player')
    stack_sizes = []
    try:
        seats_div = driver.find_element(By.CLASS_NAME, 'seats')
        seat_elements = seats_div.find_elements(By.CLASS_NAME, 'table-player')

        for seat in seat_elements:
            seat_class = seat.get_attribute('class')
            # Check if seat is occupied and not offline
            if 'table-player-seat' not in seat_class:
                try:
                    # Extract stack size
                    stack_size_element = seat.find_element(By.CLASS_NAME, 'table-player-stack')
                    stack_size_text = stack_size_element.find_element(By.CLASS_NAME, 'normal-value').text
                    stack_sizes.append(float(stack_size_text.replace(',', '')))
                except Exception as e:
                    print(f"Could not find stack size for an active seat: {e}")
    except Exception as e:
        print(f"Could not find seats: {e}")
    if stack_sizes:
        stack_size = sum(stack_sizes) / len(stack_sizes)

        print(len(stack_sizes))
    for seat in seat_elements:
        seat_class = seat.get_attribute('class')
        # Check if seat is unoccupied
        if 'table-player-seat' in seat_class:
            try:
                # Click the seat button to take the seat
                seat_button = seat.find_element(By.CLASS_NAME, 'table-player-seat-button')
                seat.click()
                print(seat.text)
                time.sleep(1)  # Wait for the form to appear

                # Find the input fields and update the value
                nickname_input = seat.find_element(By.XPATH, ".//input[@placeholder='Your Name']")
                stack_input = seat.find_element(By.XPATH, ".//input[@placeholder='Intended Stack']")

                # Update the input fields
                nickname_input.clear()
                nickname_input.send_keys("PokerXPokerBot")
                print(stack_size)
                stack_input.clear()
                stack_size = int(stack_size) * ( 10**2)
                stack_input.send_keys(stack_size)

                # Submit the form
                submit_button = seat.find_element(By.XPATH, ".//button[contains(text(), 'Request the Seat')]")
                submit_button.click()
                empty_seat_found = True
                break
            except Exception as e:
                print(f"Could not click seat button for an empty seat: {e}")

    while True:
        try:
            # Check if the class 'table-player-1 you-player' is present
            player_seat = driver.find_element(By.XPATH, "//div[contains(@class, 'table-player-1 you-player')]")
            if player_seat:
                print("Player has taken the seat.")
                break
        except Exception:
            print("Waiting for the player to take the seat...")
        time.sleep(1)
    driver.find_element(By.TAG_NAME, 'body').send_keys('m')
    time.sleep(1)  # Wait for the chat input to appear

    # Locate the chat input field and type the message
    chat_input = driver.find_element(By.XPATH, "//input[@placeholder='Your Message (press Enter to submit)']")
    chat_input.send_keys("Hello I am the beta version of the PunterXPunter Pokerbot created by Dhananjay Raghu, Goodluck and have fun!")
    chat_input.send_keys(Keys.ENTER)

    players = []
    while True:
        try:
            seats_div = driver.find_element(By.CLASS_NAME, 'seats')
            seat_elements = seats_div.find_elements(By.CLASS_NAME, 'table-player')
            try:
                player_one = driver.find_element(By.CLASS_NAME, 'table-player-1')
                card_elements = player_one.find_elements(By.CLASS_NAME, 'card-container')
                cards = [card.get_attribute('class') for card in card_elements if 'flipped' in card.get_attribute('class')]
                if card_elements:
                    print("cards Found")
                    break
            except Exception as e:
                print(f"Could not find player one's cards: {e}")
            player = Player(position=1, cards=cards, stack_size=stack_size, is_away=False)
            players.append(player)
        except Exception:
            print("Waiting for the player to take the seat...")
        time.sleep(1)
    for idx, seat in enumerate(seat_elements):
        seat_class = seat.get_attribute('class')
        is_away = 'offline' in seat_class

        if not is_away:
            try:
                stack_size_element = seat.find_element(By.CLASS_NAME, 'table-player-stack')
                stack_size_text = stack_size_element.find_element(By.CLASS_NAME, 'normal-value').text
                stack_size = float(stack_size_text.replace(',', ''))
            except Exception as e:
                stack_size = 0
                print(f"Could not find stack size or cards for an active seat: {e}")

        player = Player(position=idx, stack_size=stack_size, is_away=is_away)
        players.append(player)

for player in enumerate(players):
    print(player)
time.sleep(10000)

