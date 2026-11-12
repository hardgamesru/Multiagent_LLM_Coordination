import re

def evaluate_expression(text: str) -> int:
    def tokenize(text):
        # Регулярное выражение для разбивки на токены
        return list(filter(None, re.split(r'(\d+|\+|-|\*|\(|\))', text)))
    
    def parse(tokens):
        # Функция парсинга с использованием стека
        stack = []
        
        for token in tokens:
            if token.isdigit():
                stack.append(int(token))
            elif token in '+-':
                op2 = stack.pop()
                op1 = stack.pop()
                result = op1 + (int(token) * op2)
                stack.append(result)
            elif token == '*':
                op2 = stack.pop()
                op1 = stack.pop()
                stack.append(op1 * op2)
            elif token == '(':
                stack.append(token)
            elif token == ')':
                temp_stack = []
                while stack[-1] != '(':
                    temp_stack.append(stack.pop())
                stack.pop()  # Удаляем открывающую скобку
                
                # Вычисляем выражение в скобках
                while temp_stack:
                    stack.append(temp_stack.pop())
        
        return stack[0]
    
    # Преобразуем входную строку в токены
    tokens = tokenize(text.replace(" ", ""))
    
    try:
        # Парсим выражение и возвращаем результат
        return parse(tokens)
    except IndexError:
        raise ValueError("Invalid expression")
