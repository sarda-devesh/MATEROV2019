import parser 
def run_euler(x, y, formula, step_size, number, end_point = None): 
    code = parser.expr(formula). compile()
    if end_point is None: 
        end_point = x + step_size * number 
    while(x < end_point): 
        y += eval(code) * step_size
        x += step_size
        print(str(round(x,3)) + " " + str(round(y,3)))

run_euler(0, 25, "0.264 * y * (1 - y/200)", 1, 5)