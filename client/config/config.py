"""
Консольный мессенджер

Модуль для работы с файлом конфигурации.
"""

import logs

class Config:

    __bool_params = {"AUTO_AUTH"}
    CONFIG_PATH = "config/config.cfg"


    @staticmethod
    def get(param_key: str) -> tuple | None:
        """
        Возвращает ключ и значение указанного параметра.
        Принимает название параметра.
        """
        try:
            with open(Config.CONFIG_PATH, "r") as file:
                params = file.readlines()

                for param in params:
                    key, value = param.rstrip().split("=", 1)

                    if key == param_key:
                        return key, value
                    
            return None
        
        except Exception as err:
            logs.print_error(f"Couldn't open config file {str(err)}")
        

    @staticmethod
    def set(param_key: str, param_value: str) -> tuple | None:
        """
        Изменяет значение указанного параметра.
        Принимает название параметра и его значение.
        """
        try:
            updated = False
            with open(Config.CONFIG_PATH, "r") as file:
                lines = file.readlines()

            for i, line in enumerate(lines):
                key, value = line.rstrip().split("=", 1)

                if key == param_key:
                    end = "\n" if line.endswith("\n") else ""

                    if param_key in Config.__bool_params:
                        if param_value not in {"true", "false", "0", "1"}:
                            return None
                    
                    lines[i] = f"{param_key}={param_value}{end}"
                    updated = True

            with open(Config.CONFIG_PATH, "w") as file:
                file.writelines(lines)

            return (param_key, param_value) if updated else None
        
        except Exception as err:
            logs.print_error(f"Couldn't open or update config file {str(err)}")

            return None
    
