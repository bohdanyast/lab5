from tabulate import tabulate
import copy
from sympy import *

# константи для таблиць
table_of_3_variables = [
    [0, 0, 0],
    [0, 0, 1],
    [0, 1, 0],
    [0, 1, 1],
    [1, 0, 0],
    [1, 0, 1],
    [1, 1, 0],
    [1, 1, 1]
]
head = ["x", "y", "z", "F"]


# таблиця істинності
def get_table_of_truth(table, f):
    copy_table = copy.deepcopy(table)
    for i in range(len(copy_table)):
        copy_table[i].append(int(f[i]))

    return copy_table


# двоїста функція
def get_dual_function(table, f):
    copy_table = copy.deepcopy(table)

    f = f[::-1]
    for i in range(len(copy_table)):
        copy_table[i].append(str(int(not int(f[i]))))

    return copy_table


# ДДНФ
def get_DDNF(truth_table):
    copy_truth_table = copy.deepcopy(truth_table)
    l = len(copy_truth_table)
    not_sign = '¬'
    array_of_values = []
    for i in range(l):
        if int(f[i]):
            x = 'x' if copy_truth_table[i][0] else not_sign + 'x'
            y = 'y' if copy_truth_table[i][1] else not_sign + 'y'
            z = 'z' if copy_truth_table[i][2] else not_sign + 'z'
            str = x + y + z
            array_of_values.append(str)

    return ' ⋁ '.join(array_of_values)


# ДКНФ
def get_DKNF(truth_table):
    copy_truth_table = copy.deepcopy(truth_table)
    l = len(copy_truth_table)
    not_sign = '¬'
    array_of_values = []
    for i in range(l):
        if not int(f[i]):
            x = 'x' if copy_truth_table[i][0] else not_sign + 'x'
            y = 'y' if copy_truth_table[i][1] else not_sign + 'y'
            z = 'z' if copy_truth_table[i][2] else not_sign + 'z'
            str = f"({x} ⋁ {y} ⋁ {z})"
            array_of_values.append(str)

    return ''.join(array_of_values)


# Поліном Жегалкіна методом трикутника Паскаля
def get_zhegalkin_value(f):
    if len(f) == 1:
        return f

    stringtooperate = ''
    l = len(f)

    for i in range(l - 1):
        stringtooperate += str(int(f[i]) ^ int(f[i + 1]))

    total = f[0] + get_zhegalkin_value(stringtooperate)

    return total


def get_zhegalkin_polynominal(table, f):
    copy_table = copy.deepcopy(get_table_of_truth(table, f))

    array_of_values = []
    for i in range(len(f)):
        if int(f[i]):
            x = 'x' if copy_table[i][0] else ''
            y = 'y' if copy_table[i][1] else ''
            z = 'z' if copy_table[i][2] else ''
            str = x + y + z
            array_of_values.append(str)

    return ' ⊕ '.join(array_of_values)


# зберігає константу 1
def keeps_zero(table):
    x = table[0][0]
    y = table[0][1]
    z = table[0][2]
    f = table[0][3]
    return x == y == z == f


# збергіає константу 0
def keeps_one(table):
    l = len(table) - 1
    x = table[l][0]
    y = table[l][1]
    z = table[l][2]
    f = table[l][3]
    return x == y == z == f


# самодвоїста
def is_self_dual(f):
    reversed_str = f[::-1]
    flipped_str = ''.join(['1' if bit == '0' else '0' for bit in reversed_str])  # Замінюємо 0 на 1 і навпаки
    return flipped_str == f


# скорочена ДНФ для дослідження монотонності
def get_shortened_DDNF(truth_table):
    copy_truth_table = copy.deepcopy(truth_table)
    l = len(copy_truth_table)
    not_sign = '~'
    array_of_values = []
    for i in range(l):
        if int(f[i]):
            x = 'x & ' if copy_truth_table[i][0] else not_sign + 'x & '
            y = 'y & ' if copy_truth_table[i][1] else not_sign + 'y & '
            z = 'z' if copy_truth_table[i][2] else not_sign + 'z'
            str = f"({x + y + z})"
            array_of_values.append(str)

    return ' | '.join(array_of_values)


def is_monotone(truth_table):
    expr = str(simplify(get_shortened_DDNF(get_table_of_truth(table_of_3_variables, f))))
    return "~" in expr

# лінійна
def is_linear(expr):
    arr = expr.split(' ⊕ ')
    for elem in expr.split(' ⊕ '):
        if len(elem) > 1:
            return False

    return True



f = "01011110"
tt = get_table_of_truth(table_of_3_variables, f)

print(f"Ваша булева функція: {f}\n")

table_of_truth = tabulate(tt, headers=head, tablefmt='grid')
print(f"1a. Таблиця істинності:\n{table_of_truth}\n")

table_of_dual = tabulate(get_dual_function(table_of_3_variables, f), headers=head, tablefmt='grid')
print(f"1b. Двоїста функція:\n{table_of_dual}\n")

ddnf = get_DDNF(tt)
print(f"1c-1. ДДНФ:\n{ddnf}\n")

dknf = get_DKNF(tt)
print(f"1с-2. ДKНФ:\n{dknf}\n")

zhegalkin_value = tabulate(get_table_of_truth(table_of_3_variables, get_zhegalkin_value(f)), headers=head,
                           tablefmt='grid')
zhegalkin_polynominal = get_zhegalkin_polynominal(table_of_3_variables, get_zhegalkin_value(f))
print(f"1d. Поліном Жегалкіна:\n{zhegalkin_polynominal}\n{zhegalkin_value}\n")

keeps_zero = keeps_zero(tt)
keeps_one = keeps_one(tt)
is_self_dual = is_self_dual(f)
is_monotone = is_monotone(tt)
is_linear = is_linear(zhegalkin_polynominal)

print(f"""1e. Властивості функції:
— Зберігає константу 0: {'так' if keeps_zero else 'ні'}
— Зберігає константу 1: {'так' if keeps_one else 'ні'}
— Є самодвоїстою: {'так' if is_self_dual else 'ні'}
— Є монотонною: {'так' if not is_monotone else 'ні'}
— Є лінійною: {'так' if is_linear else 'ні'}
""")