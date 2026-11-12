import re

def evaluate_expression(text: str) -> int:
    def tokenize(text):
        # Регулярка для токенов: числа, операторы и круглые скобки
        return list(filter(None, re.split(r'(\d+|\+|-|\*|\(|\))', text)))
    
    def parse(tokens):
        # Функция парсинга постфиксной нотации
        stack = []
        for token in tokens:
            if token.isdigit():
                stack.append(int(token))
            elif token == '*':
                op2 = stack.pop()
                op1 = stack.pop()
                stack.append(op1 * op2)
            else:
                stack.append(token)
        
        # Вычисляем оставшиеся операции
        while len(stack) > 1:
            op = stack.pop(0)
            if op == '+':
                op2 = stack.pop()
                op1 = stack.pop()
                stack.append(op1 + op2)
            elif op == '-':
                op2 = stack.pop()
                op1 = stack.pop()
                stack.append(op1 - op2)
            else:
                # Сохраняем остаток
                stack.insert(0, op)
                
        return stack[0]
    
    # Преобразуем инфиксную запись в постфиксную
    tokens = tokenize(text.replace(" ", ""))
    postfix_tokens = []
    
    operators = ['+', '-', '*']
    operator_stack = []
    
    for token in tokens:
        if token.isdigit() or (token.startswith('-') and token[1:].isdigit()):
            # Число добавляется в выходной стек
            postfix_tokens.append(token)
        elif token in operators:
            # Операторы обрабатываются по приоритетам
            while (operator_stack and 
                   operator_stack[-1] != '(' and 
                   operators.index(token) <= operators.index(operator_stack[-1])):
                postfix_tokens.append(operator_stack.pop())
            operator_stack.append(token)
        elif token == '(':
            # Левая скобка сохраняется в стеке операторов
            operator_stack.append(token)
        elif token == ')':
            # Закрывающая скобка выталкивает операторы до открывающей
            while operator_stack[-1] != '(':
                postfix_tokens.append(operator_stack.pop())
            operator_stack.pop()  # Удаляем открывающую скобку
    
    # Остаточные операторы
    while operator_stack:
        postfix_tokens.append(operator_stack.pop())
    
    return parse(postfix_tokens)
