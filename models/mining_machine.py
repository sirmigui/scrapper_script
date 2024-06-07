class MiningMachine():
    ip_address: str

    fan_speed_text: str
    hashrate_5min_text: str
    miner_temp_text: str

    hashrate_5min: str
    hashrate_30min: str
    pool_rejection_time: float

    pool: dict
    boards: dict
    fan: dict

    mac: str

    def __init__(self, ip_address: str, fan_speed_text: str, hashrate_5min_text: str, miner_temp_text: str, hashrate_5min: str, hashrate_30min: str, pool_rejection_time: float, pool: dict, boards: dict, fan:dict, mac: str) -> None:
        self.ip_address = ip_address

        self.fan_speed_text = fan_speed_text
        self.hashrate_5min_text = hashrate_5min_text
        self.miner_temp_text = miner_temp_text

        self.hashrate_5min = hashrate_5min
        self.hashrate_30min = hashrate_30min
        self.pool_rejection_time = pool_rejection_time

        self.pool = pool
        self.boards = boards
        self.fan = fan

        self.mac = mac

    def __str__(self) -> str:
        return f"{self.fan_speed_text} {self.hashrate_5min}GH/s {self.hashrate_30min}GH/s {self.pool_rejection_time:.2f}%"

    def toDict(self) -> dict:
        return {
            "ip_address": self.ip_address,
            "fan_speed_text": self.fan_speed_text,
            "hashrate_5min_text": self.hashrate_5min_text,
            "miner_temp_text": self.miner_temp_text,
            "hashrate_5min": self.hashrate_5min,
            "hashrate_30min": self.hashrate_30min,
            "pool_rejection_time": self.pool_rejection_time,
            "pool": self.pool,
        }





