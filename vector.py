# This is a calculator designed for Vector calculations and analytical geometry
import operator
import math
from time import sleep
import re
operations = [
    "Norm",
    "Add/subtract",
    "Scalar",
    "Dot",
    "Cross",
    "Midpoint",
    "Distance",
    "Slope",
    "Slope eqn",
    "Line eqn",
    "Coefficients",
    "Distance to line",
    "Split line by ratio",
    "Quit"
]
def get_tuple_input(prompt: str) -> tuple:
    while True:
        user_input = input(prompt).strip()
        try:
            parts = [float(x.strip()) for x in user_input.split(",")]
            if len(parts) != 2:
                print("Error: Write the Vector in form x,y\n"+"-"*30)
                continue
            return tuple(parts)
        except ValueError:
            print("-"*30+"\nError: Write the Vector in form x,y\n"+"-"*30)
def norm(vector: tuple) -> float:
    x = vector[0]
    y = vector[1]
    result = round((math.sqrt((x ** 2) + (y ** 2))), 4)
    return result
def add_or_subtract(a: tuple, b: tuple, op: str) -> tuple:
    if op == "add":
        result = tuple(map(operator.add, a, b))
    elif op == "sub":
        result = tuple(map(operator.sub, a, b))
    return result
def scalar_mult(a: tuple, x: float) -> tuple:
    result = tuple(i*x for i in a)
    return result
def dot_prod(a: tuple, b:tuple) -> float:
    dot_product = sum(x * y for x, y in zip(a, b))
    return dot_product
def cross_prod(a: tuple, b:tuple) -> float:
    cross_product = (a[0] * b[1]) - (a[1] * b[0])
    return cross_product
def midpoint(a: tuple, b: tuple) -> tuple:
    vector_sum = add_or_subtract(a, b, "add")
    result = scalar_mult(vector_sum, 0.5)
    return result
def distance(a: tuple, b: tuple) -> float:
    vector = add_or_subtract(b, a, "sub")
    result = norm(vector)
    return result
def slope(a: tuple=None, b: tuple=None, theta:float=None, degree: bool=True) -> float | str:
    if a is not None and b is not None:
        try:
            result = round(((b[1] - a[1]) / (b[0] - a[0])), 4)
            return result
        except ZeroDivisionError:
            return "undefined"
    elif theta is not None:
        theta_rad = math.radians(theta) if degree else theta
        if math.isclose(math.cos(theta_rad), 0.0, abs_tol=1e-9):
            return "undefined"
        result = round(math.tan(theta_rad), 4)
        return result
    return "undefined"
def slope_equation(a: tuple, b: tuple) -> str:
    # find slope
    m = slope(a, b)
    if m == "undefined":
        eqn = f"x = {a[0]}"
    else:
        c = a[1] - (m * a[0])
        if c==0:
            eqn = f"y = {m}x"
        elif c > 0:
            eqn = f"y = {m}x + {c}"
        else:
            eqn = f"y = {m}x - {abs(c)}"
    return eqn
def line_eqn(a:int=0, b:int=0, c:int=0) -> str:
    parts = []
    if a == 0 and b == 0:
        return "0 = 0"
    if a != 0:
        if a == 1:
            parts.append("x")
        elif a == -1:
            parts.append("-x")
        else:
            parts.append(f"{a}x")
    if b !=0:
        if b > 0:
            sign = "+ "
            term = "y" if b == 1 else f"{b}y"
            parts.append(f"{sign}{term}")
        else:
            sign = "- "
            term = "y" if b == 1 else f"{abs(b)}y"
            parts.append(f"{sign}{term}")
    if c !=0:
        if c > 0:
            sign = "+ " if parts else ""
            parts.append(f"{sign}{c}")
        else:
            sign = "- " if parts else "-"
            parts.append(f"{sign}{abs(c)}")

    raw_eqn = "".join(parts).replace("+", " + ").replace("-", " - ")
    if raw_eqn.startswith(" - "): 
        raw_eqn = "-" + raw_eqn[3:]
    return f"{raw_eqn.strip()} = 0"
def extract_coeffiecient(eqn:str) -> list:
    clean_eqn = eqn.split("=")[0].replace(" ","")
    normalized = clean_eqn.replace("-","+-")
    terms = [t for t in normalized.split("+") if t]
    a, b, c = 0,0,0
    for term in terms:
        if "x" in term:
            val = term.replace("x", "")
            if val == "" or val == "+": a = 1
            elif val == "-": a = -1
            else: a = float(val)
        elif "y" in term:
            val = term.replace("y", "")
            if val == "" or val == "+": b = 1
            elif val == "-": b = -1
            else: b = float(val)
        else:
            c = float(term)
    return [a, b, c]
def perpendicular_dist(eqn:str, point:tuple) -> float | str:
    my_coef = extract_coeffiecient(eqn)
    try:
        dist = (abs((my_coef[0] * point[0]) + (my_coef[1] * point[1]) + (my_coef[2]))) / norm(tuple(my_coef[:2]))
        return dist
    except ZeroDivisionError:
        return "Can't measure distance. Enter a proper equation"
def division_of_st_line(a:tuple, b:tuple, ratio:str, type_of_div:str) -> tuple:
    parts = [float(x) for x in ratio.replace(" ","").split(":")]
    match type_of_div:
        case "internally":
            numerator = add_or_subtract(scalar_mult(b, parts[0]), scalar_mult(a, parts[1]), "add")
            denomenator = parts[0] + parts[1]
            if denomenator == 0: return "undefined (division by zero)"
            ans = scalar_mult(numerator, 1/denomenator)
        case "externally":
            numerator = add_or_subtract(scalar_mult(b, parts[0]), scalar_mult(a, parts[1]), "sub")
            denomenator = parts[0] - parts[1]
            if denomenator == 0: return "undefined (division by zero)"
            ans = scalar_mult(numerator, 1/denomenator)
    return ans
def is_standard_eqn(eqn:str) -> bool:
    pattern = r'^\s*([+-]?\s*\d*\.?\d*\s*x)?\s*([+-]?\s*\d*\.?\d*\s*y)?\s*([+-]?\s*\d+\.?\d*)?\s*=\s*0\s*$'
    match = re.match(pattern, eqn, re.IGNORECASE)
    if not match:
        return False
    has_x = 'x' in eqn.lower()
    has_y = 'y' in eqn.lower()
    if not has_x and not has_y:
        return False
    return True
# Main program loop
print("-"*30+"\nWelcome to Vector Calculator\n"+"-"*30)
while True:
    for i in range(len(operations)):
        print(f"{operations[i]} | ", end="")
    print("\n"+"-"*30)
    while True:
        op = input("=> ").strip().capitalize()
        print("-"*30)
        if op not in operations:
            print("This isn't a valid operation\n"+"-"*30)
            continue
        break
    if op == "Quit":
        print("Shutting down...\n"+"-"*30)
        break
    else:
        if op in ["Add/subtract", "Dot","Cross", "Midpoint", "Distance", "Slope eqn"]:
            my_tup = []
            for i in range(2):
                tup = get_tuple_input(f"Enter Vector #{i+1}: ")
                print("-"*30)
                my_tup.append(tup)
            match op:
                case "Add/subtract":
                    while True:
                        oper = input("Enter (+/-): ").strip()
                        print("-"*30)
                        if oper not in ["+", "-"]:
                            print("Not a valid operator\n"+"-"*30)
                            continue
                        break
                    if oper == "+":
                        vect_ans = add_or_subtract(my_tup[0], my_tup[1], "add")
                    else:
                        vect_ans = add_or_subtract(my_tup[0], my_tup[1], "sub")
                    expr = f"{my_tup[0]} {oper} {my_tup[1]} = {vect_ans}"
                case "Dot":
                    vect_ans = dot_prod(my_tup[0], my_tup[1])
                    expr = f"{my_tup[0]} . {my_tup[1]} = {vect_ans}"
                case "Cross":
                    vect_ans = cross_prod(my_tup[0], my_tup[1])
                    expr = f"{my_tup[0]} x {my_tup[1]} = {vect_ans}"
                case "Midpoint":
                    vect_ans = midpoint(my_tup[0], my_tup[1])
                    expr = f"The midpoint between {my_tup[0]} & {my_tup[1]} is {vect_ans}"
                case "Distance":
                    dist = distance(my_tup[0], my_tup[1])
                    expr = f"The distance between {my_tup[0]} & {my_tup[1]} is {dist} length units"
                case "Slope eqn":
                    eqn = slope_equation(my_tup[0], my_tup[1])
                    expr = f"The slope equaution of L that passes through {my_tup[0]} , {my_tup[1]} is {eqn}"
            print(expr+"\n"+"-"*30)
            sleep(1)
        elif op in ["Distance to line", "Scalar","Norm"]:
            my_vect = get_tuple_input("Enter The vector in form of x,y: ")
            print("-"*30)
            match op:
                case "Distance to line":
                    while True:
                        eqn = input("Enter an equation in the general form (ax+by+c=0): ").strip().lower()
                        print("-"*30)
                        is_standard = is_standard_eqn(eqn)
                        if is_standard:
                            break
                        else:
                            print("Not A Valid Equation\n"+"-"*30)
                    vect_ans = perpendicular_dist(eqn, my_vect)
                    expr = f"The Perpendicular distance between {my_vect} and ({eqn}) is {vect_ans} length units"
                case "Scalar":
                    while True:
                        try:
                            x = float(input("Enter the scalar quantity: ").strip())
                            print("-"*30)
                            break
                        except ValueError:
                            print("-"*30+"\nNot A Valid Scalar\n"+"-"*30)
                    vect_ans = scalar_mult(my_vect, x)
                    expr = f"{x}{my_vect} = {vect_ans}"
                case "Norm":
                    vect_ans = norm(my_vect)
                    expr = f"||{my_vect}|| = {vect_ans} length unit"
            print(expr+"\n"+"-"*30)
            sleep(1)
        elif op == "Line eqn":
            coef = []
            name = ["a", "b", "c"]
            for i in range(3):
                while True:
                    try:
                        x = int(input(f"Enter {name[i]}: ").strip())
                        coef.append(x)
                        print("-"*30)
                        break
                    except ValueError:
                        print("-"*30+"\nNot A Valid Coefficient\n"+"-"*30)
            eqn = line_eqn(coef[0], coef[1], coef[2])
            print(eqn+"\n"+"-"*30)
            sleep(1)
        elif op == "Slope":
            while True:
                option = input("By Angle OR By Points: ").strip().lower()
                print("-"*30)
                if option in ['angle', 'points']:
                    break
                else:
                    print("-"*30 +"\nNot A Valid Option\n"+"-"*30)
                    continue
            match option:
                case "angle":
                    while True:
                        try:
                            angle = int(input("Enter angle in degrees: ").strip())
                            print("-"*30)
                            break
                        except ValueError:
                            print("-"*30 +"\nNot A Valid Angle\n"+"-"*30)
                    vect_ans = slope(theta=angle, degree=True)
                case "points":
                    my_points = []
                    for i in range(2):
                        x = get_tuple_input(f"Enter point #{i+1}: ")
                        print("-"*30)
                        my_points.append(x)
                    vect_ans = slope(a=my_points[0], b=my_points[1])
            expr = f"m = {vect_ans}"
            print(expr+"\n"+"-"*30)
        elif op == "Coefficients":
            while True:
                eqn = input("Enter an equation in the general form (ax+by+c=0): ").strip().lower()
                print("-"*30)
                is_standard = is_standard_eqn(eqn)
                if is_standard:
                    break
                else:
                    print("Not A Valid Equation\n"+"-"*30)
            coef = extract_coeffiecient(eqn)
            expr = f"a = {coef[0]} , b = {coef[1]}, c = {coef[2]}"
            print(expr+"\n"+"-"*30)
            sleep(1)
        elif op == "Split line by ratio":
            my_tups = []
            names = ["starting", "terminal"]
            for i in range(2):
                x = get_tuple_input(f"Enter the {names[i]} point: ")
                print("-"*30)
                my_tups.append(x)
            while True:
                ratio = input("Enter the ratio of division in form a:b => ").strip().lower()
                print("-"*30)
                pattern = r"^\s*\d+\s*:\s*\d+\s*$"
                if re.match(pattern , ratio):
                    ratio.strip()
                    break
                else:
                    print("Not A Valid Ratio\n" + "-"*30)
                    continue
            while True:
                type_of_div = input("Enter type of division: ").strip().lower()
                print("-"*30)
                if type_of_div not in ["internally", "externally"]:
                    print("-"*30+"\nNot A Valid type\n"+"-"*30)
                    continue
                break
            vect_ans = division_of_st_line(a=my_tups[0], b=my_tups[1], ratio=ratio, type_of_div=type_of_div)
            expr = f"The point that divides L whose startpoint is {my_tups[0]} and endpoint is {my_tups[1]} by ratio {ratio} {type_of_div} =\n{vect_ans}"
            print(expr+'\n'+"-"*30)