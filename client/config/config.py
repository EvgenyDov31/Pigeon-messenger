"""
Консольный мессенджер

Модуль для работы с файлом конфигурации.
"""

import logs

class Config:

    __bool_params = ["AUTO_AUTH"]


    @staticmethod
    def get(param_key: str) -> tuple | None:
        """
        Возвращает ключ и значение указанного параметра.
        Принимает название параметра.
        """
        try:
            with open("config/config.cfg", "r") as file:
                params = file.readlines()

                for param in params:
                    if param.startswith(param_key):
                        key, value = param.split("=")

                        return key, value
                    
            return None
        
        except Exception as err:
            logs.print_error(f"Couldn't open config file")
        

    @staticmethod
    def set(param_key: str, param_value: str) -> tuple | None:
        """
        Изменяет значение указанного параметра.
        Принимает название параметра и его значение.
        """
        try:
            with open("config/config.cfg", "r") as file:
                lines = file.readlines()

            for i, line in enumerate(lines):
                
                if line.startswith(param_key):
                    end = "\n" if line.endswith("\n") else ""

                    if param_key in Config.__bool_params:
                        if param_value in ["true", "false", "0", "1"]:
                            lines[i] = f"{param_key}={param_value}{end}"
                            break
                    
                    else:
                        lines[i] = f"{param_key}={param_value}{end}"
                        break

            with open("config/config.cfg", "w") as file:
                file.writelines(lines)

            return param_key, param_value
        
        except Exception as err:
            logs.print_error(f"Couldn't open or update config file")

            return None
    
