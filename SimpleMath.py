
epsilon = 1e-6;

def solve_simple_linear_system_cramer(a1, b1, c1, a2, b2, c2):
    #
    #  a1*x + b1*y = c1
    #  a2*x + b2*y = c2
    #
    det = a1 * b2 - a2 * b1;
    if abs(det) < epsilon:
        return None;
    return [(c1 * b2 - c2 * b1) / det, (a1 * c2 - a2 * c1) / det];
