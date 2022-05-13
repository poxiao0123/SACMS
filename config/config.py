class Config:
    def __init__(self) -> None:
        self.env = ""
        self.project = "SACMS"
        self.db_host = "124.220.158.116"
        self.db_name = "sacms",
        self.db_user = "sacms",
        self.db_pass = "159630sk"
        self.SECRET = "poxiao"

    def get_configcenter_info(self):  # 从配置中心返回配置数据
        res = {
            "mysql": "mysql://sacms:159630sk..@124.220.158.116/sacms",
            "USERNAME": "lwl_0123@yeah.net",
            "PASSWORD": "111111",
            "SECRET": "poxiao"
        }
        print(res)
        return res


config = Config().get_configcenter_info()
