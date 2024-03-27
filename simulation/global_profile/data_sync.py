business_sync = {
    "business": {
        "Add Book": {
            "prob": {
                "path0": (0.0, 0.2),
                "path1": (0.2, 1.0)
            },
            "path0": [
                ("Actor", "Controller Server.Controller.BookController", "create(Book)", "Synchronous", 0.1, 10, 1000),
                ("Controller Server.Controller.BookController", "Service Server.Service.BookService", "query(Book)", "Synchronous", 0.1, 10, 1000),
                ("Service Server.Service.BookService", "DAO Server.Mapper.BookMapper", "query(Book)", "Synchronous", 0.1, 10, 1000),
                ("DAO Server.Mapper.BookMapper", "SQL DataBase.DataComponent.DataBase", "query(String)", "Synchronous", 0.1, 10, 1000)
            ],
            "path1": [
                ("Actor", "Controller Server.Controller.BookController", "create(Book)", "Synchronous", 0.1, 10, 1000),
                ("Controller Server.Controller.BookController", "Service Server.Service.BookService", "query(Book)", "Synchronous", 0.1, 10, 1000),
                ("Service Server.Service.BookService", "DAO Server.Mapper.BookMapper", "query(Book)", "Synchronous", 0.1, 10, 1000),
                ("DAO Server.Mapper.BookMapper", "SQL DataBase.DataComponent.DataBase", "query(String)", "Synchronous", 0.1, 10, 1000),
                ("Controller Server.Controller.BookController", "Service Server.Service.BookService", "create(Book)", "Synchronous", 0.1, 10, 1000),
                ("Service Server.Service.BookService", "DAO Server.Mapper.BookMapper", "create(Book)", "Synchronous", 0.1, 10, 1000),
                ("DAO Server.Mapper.BookMapper", "SQL DataBase.DataComponent.DataBase", "add(String)", "Synchronous", 0.1, 10, 1000)
            ]
        },
        "Delete Book": {
            "prob": {
                "path0": (0.0, 0.1),
                "path1": (0.1, 0.64),
                "path2": (0.64, 1.0)
            },
            "path0": [
                ("Actor", "Controller Server.Controller.BookController", "delete(String)", "Synchronous", 0.1, 10, 1000),
                ("Controller Server.Controller.BookController", "Service Server.Service.BookService", "query(Book)", "Synchronous", 0.1, 10, 1000),
                ("Service Server.Service.BookService", "DAO Server.Mapper.BookMapper", "query(Book)", "Synchronous", 0.1, 10, 1000),
                ("DAO Server.Mapper.BookMapper", "SQL DataBase.DataComponent.DataBase", "query(String)", "Synchronous", 0.1, 10, 1000)
            ],
            "path1": [
                ("Actor", "Controller Server.Controller.BookController", "delete(String)", "Synchronous", 0.1, 10, 1000),
                ("Controller Server.Controller.BookController", "Service Server.Service.BookService", "query(Book)", "Synchronous", 0.1, 10, 1000),
                ("Service Server.Service.BookService", "DAO Server.Mapper.BookMapper", "query(Book)", "Synchronous", 0.1, 10, 1000),
                ("DAO Server.Mapper.BookMapper", "SQL DataBase.DataComponent.DataBase", "query(String)", "Synchronous", 0.1, 10, 1000),
                ("Controller Server.Controller.BookController", "Service Server.Service.BookService", "deleteById(String)", "Synchronous", 0.1, 10, 1000),
                ("Service Server.Service.BookService", "DAO Server.Mapper.BookMapper", "deleteById(String)", "Synchronous", 0.1, 10, 1000),
                ("DAO Server.Mapper.BookMapper", "SQL DataBase.DataComponent.DataBase", "delete(String)", "Synchronous", 0.1, 10, 1000)
            ],
            "path2": [
                ("Actor", "Controller Server.Controller.BookController", "delete(String)", "Synchronous", 0.1, 10, 1000),
                ("Controller Server.Controller.BookController", "Service Server.Service.BookService", "query(Book)", "Synchronous", 0.1, 10, 1000),
                ("Service Server.Service.BookService", "DAO Server.Mapper.BookMapper", "query(Book)", "Synchronous", 0.1, 10, 1000),
                ("DAO Server.Mapper.BookMapper", "SQL DataBase.DataComponent.DataBase", "query(String)", "Synchronous", 0.1, 10, 1000),
                ("Controller Server.Controller.BookController", "Service Server.Service.BookService", "deleteByTitle(String)", "Synchronous", 0.1, 10, 1000),
                ("Service Server.Service.BookService", "DAO Server.Mapper.BookMapper", "deleteByTitle(String)", "Synchronous", 0.1, 10, 1000),
                ("DAO Server.Mapper.BookMapper", "SQL DataBase.DataComponent.DataBase", "delete(String)", "Synchronous", 0.1, 10, 1000)
            ]
        },
        "Download Book": {
            "prob": {
                "path0": (0.0, 0.3),
                "path1": (0.3, 1.0)
            },
            "path0": [
                ("Actor", "Controller Server.Controller.BookController", "download(String)", "Synchronous", 0.1, 10, 1000),
                ("Controller Server.Controller.BookController", "Service Server.Service.BookService", "query(Book)", "Synchronous", 0.1, 10, 1000),
                ("Service Server.Service.BookService", "DAO Server.Mapper.BookMapper", "query(Book)", "Synchronous", 0.1, 10, 1000),
                ("DAO Server.Mapper.BookMapper", "SQL DataBase.DataComponent.DataBase", "query(String)", "Synchronous", 0.1, 10, 1000)
            ],
            "path1": [
                ("Actor", "Controller Server.Controller.BookController", "download(String)", "Synchronous", 0.1, 10, 1000),
                ("Controller Server.Controller.BookController", "Service Server.Service.BookService", "query(Book)", "Synchronous", 0.1, 10, 1000),
                ("Service Server.Service.BookService", "DAO Server.Mapper.BookMapper", "query(Book)", "Synchronous", 0.1, 10, 1000),
                ("DAO Server.Mapper.BookMapper", "SQL DataBase.DataComponent.DataBase", "query(String)", "Synchronous", 0.1, 10, 1000),
                ("Controller Server.Controller.BookController", "Service Server.Service.BookService", "readFile(String)", "Synchronous", 0.1, 10, 1000),
                ("Controller Server.Controller.BookController", "Service Server.Service.BookService", "readPicture(String)", "Synchronous", 0.1, 10, 1000)
            ]
        },
        "Print Book": {
            "prob": {
                "path0": (0.0, 0.5),
                "path1": (0.5, 1.0)
            },
            "path0": [
                ("Actor", "Controller Server.Controller.BookController", "printBook(Book)", "Synchronous", 0.1, 10, 1000),
                ("Controller Server.Controller.BookController", "Service Server.Service.BookService", "printAll(Book)", "Synchronous", 0.1, 10, 1000),
                ("Service Server.Service.BookService", "Printer.BookPrinter.Printerervice", "printAll(Book)", "Synchronous", 0.1, 10, 1000)
            ],
            "path1": [
                ("Actor", "Controller Server.Controller.BookController", "printBook(Book)", "Synchronous", 0.1, 10, 1000),
                ("Controller Server.Controller.BookController", "Service Server.Service.BookService", "printPages(Book, int, int)", "Synchronous", 0.1, 10, 1000),
                ("Service Server.Service.BookService", "Printer.BookPrinter.Printerervice", "printPages(Book, int, int)", "Synchronous", 0.1, 10, 1000)
            ]
        },
        "Read Book": {
            "prob": {
                "path0": (0.0, 1.0)
            },
            "path0": [
                ("Actor", "Controller Server.Controller.BookController", "detail(String)", "Synchronous", 0.1, 10, 1000),
                ("Controller Server.Controller.BookController", "Service Server.Service.BookService", "detail(String)", "Synchronous", 0.1, 10, 1000),
                ("Service Server.Service.BookService", "DAO Server.Mapper.BookMapper", "detail(String)", "Synchronous", 0.1, 10, 1000),
                ("DAO Server.Mapper.BookMapper", "SQL DataBase.DataComponent.DataBase", "query(String)", "Synchronous", 0.1, 10, 1000)
            ]
        },
        "Search Book": {
            "prob": {
                "path0": (0.0, 1.0)
            },
            "path0": [
                ("Actor", "Controller Server.Controller.BookController", "query(Book)", "Synchronous", 0.1, 10, 1000),
                ("Controller Server.Controller.BookController", "Service Server.Service.BookService", "query(Book)", "Synchronous", 0.1, 10, 1000),
                ("Service Server.Service.BookService", "DAO Server.Mapper.BookMapper", "query(Book)", "Synchronous", 0.1, 10, 1000),
                ("DAO Server.Mapper.BookMapper", "SQL DataBase.DataComponent.DataBase", "query(String)", "Synchronous", 0.1, 10, 1000)
            ]
        },
        "Update Book Info": {
            "prob": {
                "path0": (0.0, 0.9),
                "path1": (0.9, 1.0)
            },
            "path0": [
                ("Actor", "Controller Server.Controller.BookController", "update(Book)", "Synchronous", 0.1, 10, 1000),
                ("Controller Server.Controller.BookController", "Service Server.Service.BookService", "query(Book)", "Synchronous", 0.1, 10, 1000),
                ("Service Server.Service.BookService", "DAO Server.Mapper.BookMapper", "query(Book)", "Synchronous", 0.1, 10, 1000),
                ("DAO Server.Mapper.BookMapper", "SQL DataBase.DataComponent.DataBase", "query(String)", "Synchronous", 0.1, 10, 1000),
                ("Controller Server.Controller.BookController", "Service Server.Service.BookService", "update(Book)", "Synchronous", 0.1, 10, 1000),
                ("Service Server.Service.BookService", "DAO Server.Mapper.BookMapper", "update(Book)", "Synchronous", 0.1, 10, 1000),
                ("DAO Server.Mapper.BookMapper", "SQL DataBase.DataComponent.DataBase", "update(String)", "Synchronous", 0.1, 10, 1000)
            ],
            "path1": [
                ("Actor", "Controller Server.Controller.BookController", "update(Book)", "Synchronous", 0.1, 10, 1000),
                ("Controller Server.Controller.BookController", "Service Server.Service.BookService", "query(Book)", "Synchronous", 0.1, 10, 1000),
                ("Service Server.Service.BookService", "DAO Server.Mapper.BookMapper", "query(Book)", "Synchronous", 0.1, 10, 1000),
                ("DAO Server.Mapper.BookMapper", "SQL DataBase.DataComponent.DataBase", "query(String)", "Synchronous", 0.1, 10, 1000)
            ]
        }
    }
}
