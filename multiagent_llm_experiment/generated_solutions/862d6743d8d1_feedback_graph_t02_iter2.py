def parse_csv_line(line: str) -> list[str]:
    result = []
    current_field = ''
    in_quotes = False
    
    i = 0
    while i < len(line):
        char = line[i]
        
        if char == '"':
            # Внутри строки уже идет чтение в кавычках?
            if in_quotes:
                # Следующий символ - еще одна кавычка? Это экранирование
                if i + 1 < len(line) and line[i+1] == '"':
                    current_field += '"'
                    i += 1
                else:
                    in_quotes = False
            else:
                in_quotes = True
        elif char == ',' and not in_quotes:
            result.append(current_field)
            current_field = ''
        else:
            current_field += char
            
        i += 1
    
    # Добавляем последнее поле после обработки всех символов
    result.append(current_field.strip())
    
    return [field for field in result if field != '' or any(result)]
