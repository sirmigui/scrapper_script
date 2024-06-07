from botasaurus_driver.exceptions import ElementWithSelectorNotFoundException, PageNotFoundException, ChromeException
from asyncio import sleep
from botasaurus.browser import browser, Driver, Wait
from time import sleep
from env import properties
from models.mining_machine import MiningMachine

TIME_TO_WAIT = 2.5

def take_data(ip_address: str, driver: Driver) -> MiningMachine:
    hashrate_5min_text = driver.get_text(selector=".speedcss")
    fan_speed_text = driver.get_text(selector = ".volcss", wait = Wait.SHORT)
    miner_temp_text = driver.get_text(selector=".temcss")

    hashrate_5min = driver.get_text(selector = "span[class='nowspeedcss']", wait = Wait.SHORT)
    hashrate_30min = driver.get_text(selector = "span[class='svgspeedcss']", wait = Wait.SHORT)
    pool_rejection_time = driver.get_text(selector = "span[class='rejectcss']", wait = Wait.SHORT)

    fan_values = driver.get_text(selector=".poolcss tbody tr").split("\t")
    fan_keys =  driver.get_text(selector=".poolcss thead tr").lower().split("\t")

    fan = {}
    for i in range(0, len(fan_values)):
        fan[fan_keys[i].replace(" ", "_")] = fan_values[i]

    board_values = driver.get_text(selector=".boardcss tbody ").split("\n")
    board_keys = driver.get_text(selector=".boardcss thead tr").lower().split("\t")

    boards = []

    for i in range(0, len(board_values)):
        values = board_values[i].replace(" ℃", "").split("\t")
        board = {}

        for j in range(0, len(board_keys)):
            board[board_keys[j].replace(" ", "_")] = values[j]

        boards.append(board)

    boards_dict = {"boards" : boards}

    fan_values = driver.get_text(selector=".fancss tbody tr").split("\t")
    fan_keys =  driver.get_text(selector=".fancss thead tr").lower().split("\t")

    fan = {}
    for i in range(1, len(fan_values)):
        fan[fan_keys[i].replace(" ", "_")] = fan_values[i]

    mac = driver.get_text(selector="span[class='maccss']")

    return MiningMachine(ip_address=ip_address, hashrate_5min_text=hashrate_5min_text, fan_speed_text=fan_speed_text, miner_temp_text=miner_temp_text, hashrate_5min=hashrate_5min, hashrate_30min=hashrate_30min, pool_rejection_time=pool_rejection_time, pool=fan, boards=boards_dict, fan=fan, mac=mac)

def interact_with_website(url: str, driver: Driver) -> None:
    driver.get(url)
    driver.type("input[name='user']", f"{properties["username"]}")
    driver.type("input[name='pwd']", f"{properties["password"]}")
    driver.click(selector = "button[class='loginBtn lan-trans']")

def mining_machine_list_to_dict_list(machines: list[MiningMachine]) -> list[dict]:
    if (len(machines) == 0):
        raise Exception("Length is zero!")
    
    machines_in_dict: list[dict] = []
    for m in machines:
        machines_in_dict.append(m.toDict())
    return machines_in_dict

@browser(run_async = True)
def get_data_from_all(driver: Driver, data):
    machines: list[MiningMachine] = []
    
    for i in range(1, 255):
        try:
            ip_address = f"192.168.1.{i}"
            url = f"http://{ip_address}"
            interact_with_website(url=url, driver=driver)

            sleep(TIME_TO_WAIT)
            machine: MiningMachine = take_data(ip_address=ip_address, driver=driver)
            machines.append(machine)
        except ElementWithSelectorNotFoundException:
            continue
        except PageNotFoundException:
            continue

    machines_to_dict: dict = mining_machine_list_to_dict_list(machines)
    return {"machines" : machines_to_dict}

@browser(run_async = True)
def get_data_in_range(driver: Driver, data: dict[str, int]):
    machines: list[MiningMachine] = []
    min: int = data["min"]
    max: int = data["max"]

    if min >= max:
        raise Exception("The min value cannot be greater than the max value")
    
    for i in range(min, max):
        try:
            ip_address = f"192.168.1.{i}"
            url = f"http://{ip_address}"
            interact_with_website(url=url, driver=driver)
            
            sleep(TIME_TO_WAIT)
            machine = take_data(ip_address=ip_address, driver=driver)
            machines.append(machine)
        except ElementWithSelectorNotFoundException:
            continue
        except PageNotFoundException:
            continue

    machines_to_dict: dict = mining_machine_list_to_dict_list(machines)
    return {"machines" : machines_to_dict}

@browser(run_async = True)
def get_data_from_one(driver: Driver, data: str):
    interact_with_website(url=f"http://{data}", driver=driver)
    sleep(TIME_TO_WAIT)
    machine_in_dict = take_data(ip_address=data, driver=driver).toDict()
    return {"machine" : machine_in_dict}

#get_data_from_all().get()
#get_data_in_range(data={"min" : 6, "max": 10}).get()
get_data_from_one(data="192.168.1.6").get()


