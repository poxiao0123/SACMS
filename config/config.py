class Config:
    def __init__(self) -> None:
        self.env = ""
        self.project = ""

    def get_configcenter_info(self):  # 从配置中心返回配置数据
        res = {
            "mysql": "mysql://root:159630sk@192.168.159.134/test",
            "USERNAME": "lwl_0123@yeah.net",
            "PASSWORD": "111111",
        }
        return res


config = Config().get_configcenter_info()
