simulate_dict = {
    "people_num": 10,
    "people_avg": 2,
    "people_freq": {
        "Student": (0, 0.7),
        "Librarian": (0.7, 1)
    },
    "thread_dict": {
        "Controller Server": 1,
        "Service Server": 1,
        "DAO Server": 1,
        "SQL DataBase": 1,
        "Printer": 1
    },
    "network_speed": {
        ("Controller Server", "Service Server"): 100000,
        ("Service Server", "DAO Server"): 100000,
        ("DAO Server", "SQL DataBase"): 100000,
        ("Service Server", "Printer"): 100000,
        ("Printer", "Service Server"): 100000,
        ("Service Server", "Controller Server"): 100000,
        ("DAO Server", "Service Server"): 100000,
        ("SQL DataBase", "DAO Server"): 100000
    },
    "wake_up_time": {
        "Controller Server": 0.001,
        "Service Server": 0.001,
        "DAO Server": 0.001,
        "SQL DataBase": 0.001,
        "Printer": 0.001
    }
}
actor_business = {
    # 初始业务频率
    # "Student": {
    #     "Search Book": (0, 3/7),
    #     "Read Book": (3/7, 5/7),
    #     "Print Book": (5/7, 6/7),
    #     "Download Book": (6/7, 1.0)
    # },
    # "Librarian": {
    #     "Search Book": (0.0, 1/3),
    #     "Add Book": (1/3, 2/3),
    #     "Update Book Info": (2/3, 13/15),
    #     "Delete Book": (13/15, 1.0)
    # },
    # 增大多阶段业务频率
    "Student": {
        "Search Book": (0, 1/7),
        "Read Book": (1/7, 2/7),
        "Print Book": (2/7, 4/7),
        "Download Book": (4/7, 1.0)
    },
    "Librarian": {
        "Search Book": (0.0, 2/15),
        "Add Book": (2/15, 2/3),
        "Update Book Info": (2/3, 13/15),
        "Delete Book": (13/15, 1.0)
    }
}

business_fry = {
    "Add Book": 0.1,
    "Update Book Info": 0.06,
    "Delete Book": 0.04,
    "Search Book": 0.4,
    "Read Book": 0.2,
    "Print Book": 0.1,
    "Download Book": 0.1
}
