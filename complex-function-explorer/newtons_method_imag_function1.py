import ast
import json
import numpy as np

_ALLOWED_NAMES = {
    "z", "np", "sin", "cos", "tan", "exp", "log", "sqrt",
    "sinh", "cosh", "tanh", "pi", "e", "abs"
}
_ALLOWED_NP_ATTRS = {
    "sin", "cos", "tan", "exp", "log", "sqrt", "sinh", "cosh",
    "tanh", "abs", "real", "imag"
}
_ALLOWED_NODES = (
    ast.Expression, ast.BinOp, ast.UnaryOp, ast.Call, ast.Name,
    ast.Load, ast.Constant, ast.Add, ast.Sub, ast.Mult, ast.Div,
    ast.Pow, ast.Mod, ast.USub, ast.UAdd, ast.Attribute
)

def _compile_function(expression):
    """Compile a restricted mathematical expression using z as its variable."""
    tree = ast.parse(expression, mode="eval")

    for node in ast.walk(tree):
        if not isinstance(node, _ALLOWED_NODES):
            raise ValueError("Unsupported syntax in function.")
        if isinstance(node, ast.Name) and node.id not in _ALLOWED_NAMES:
            raise ValueError(f"Name '{node.id}' is not allowed.")
        if isinstance(node, ast.Attribute):
            if not isinstance(node.value, ast.Name) or node.value.id != "np" or node.attr not in _ALLOWED_NP_ATTRS:
                raise ValueError("Only supported np mathematical functions can be used.")
        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name):
                if node.func.id not in _ALLOWED_NAMES - {"z", "np", "pi", "e"}:
                    raise ValueError("Unsupported function call.")
            elif isinstance(node.func, ast.Attribute):
                if not (isinstance(node.func.value, ast.Name) and
                        node.func.value.id == "np" and
                        node.func.attr in _ALLOWED_NP_ATTRS):
                    raise ValueError("Unsupported function call.")
            else:
                raise ValueError("Unsupported function call.")

    code = compile(tree, "<user_function>", "eval")
    namespace = {
        "np": np, "sin": np.sin, "cos": np.cos, "tan": np.tan,
        "exp": np.exp, "log": np.log, "sqrt": np.sqrt,
        "sinh": np.sinh, "cosh": np.cosh, "tanh": np.tanh,
        "pi": np.pi, "e": np.e, "abs": np.abs
    }

    def f(z):
        return eval(code, {"__builtins__": {}}, {**namespace, "z": z})
    return f

def _newton_method(f, x0, tol, max_iterations):
    h = 1e-8
    z = complex(x0)
    for _ in range(max_iterations):
        try:
            fz = f(z)
            derivative = (f(z + h) - fz) / h
            if not np.isfinite(fz.real) or not np.isfinite(fz.imag):
                return None
            if not np.isfinite(derivative.real) or not np.isfinite(derivative.imag):
                return None
            if abs(derivative) < 1e-14:
                return None
            next_z = z - fz / derivative
            if not np.isfinite(next_z.real) or not np.isfinite(next_z.imag):
                return None
            if abs(next_z - z) < tol:
                # Check that the candidate is actually close to a zero.
                if abs(f(next_z)) <= max(tol * 10, 1e-7):
                    return complex(next_z)
                return None
            z = next_z
        except (ArithmeticError, ValueError, TypeError, OverflowError, FloatingPointError):
            return None
    return None

def run_analysis(expression, tolerance=1e-4, max_iterations=100,
                 real_min=-2, real_max=2, imag_min=-2, imag_max=2,
                 points_per_direction=35, show_roots=True,
                 show_fractal=True, show_real=True):
    """Run Newton's method over a complex grid and return plot-ready JSON."""
    if not isinstance(expression, str) or not expression.strip():
        raise ValueError("Enter a function of z.")
    if tolerance <= 0:
        raise ValueError("Tolerance must be greater than zero.")
    if max_iterations < 1 or max_iterations > 500:
        raise ValueError("Maximum iterations must be between 1 and 500.")
    if points_per_direction < 5 or points_per_direction > 150:
        raise ValueError("Resolution must be between 5 and 150.")
    if real_min >= real_max or imag_min >= imag_max:
        raise ValueError("Each minimum must be smaller than its maximum.")

    f = _compile_function(expression)
    axis_real = np.linspace(real_min, real_max, int(points_per_direction))
    axis_imag = np.linspace(imag_min, imag_max, int(points_per_direction))

    starts_real = []
    starts_imag = []
    converged_real = []
    converged_imag = []
    basin_ids = []
    unique_roots = []

    for real in axis_real:
        for imag in axis_imag:
            start = complex(real, imag)
            root = _newton_method(f, start, tolerance, int(max_iterations))
            if root is None:
                continue

            root_id = None
            for idx, known_root in enumerate(unique_roots):
                if np.isclose(root, known_root, rtol=1e-5, atol=max(tolerance * 10, 1e-7)):
                    root_id = idx
                    break
            if root_id is None:
                root_id = len(unique_roots)
                unique_roots.append(root)

            starts_real.append(float(real))
            starts_imag.append(float(imag))
            converged_real.append(float(root.real))
            converged_imag.append(float(root.imag))
            basin_ids.append(int(root_id))

    if not unique_roots:
        raise ValueError("No convergent roots were found. Try a different range, tolerance or iteration limit.")

    roots = [
        {"real": float(root.real), "imag": float(root.imag)}
        for root in unique_roots
    ]

    result = {
        "roots": roots,
        "starting_points": {
            "real": starts_real,
            "imag": starts_imag,
            "basin": basin_ids
        },
        "converged_points": {
            "real": converged_real,
            "imag": converged_imag,
            "basin": basin_ids
        },
        "show_roots": bool(show_roots),
        "show_fractal": bool(show_fractal),
        "show_real": bool(show_real),
        "real_curve": None
    }
    
    if show_real:
        real_x = np.linspace(real_min, real_max, 500)
    
        try:
            # Calculate function values
            real_y = np.asarray(f(real_x))
    
            if np.iscomplexobj(real_y):
                if np.max(np.abs(np.imag(real_y))) > 1e-10:
                    real_y = np.real(real_y)
                    note = "Only the real part is shown because the function returns complex values for real inputs."
                else:
                    real_y = np.real(real_y)
                    note = None
            else:
                note = None
    
            # Calculate numerical derivative
            h = 1e-8
            derivative_y = (np.asarray(f(real_x + h)) - np.asarray(f(real_x - h))) / (2 * h)
    
            if np.iscomplexobj(derivative_y):
                derivative_y = np.real(derivative_y)
    
            result["real_curve"] = {
                "x": real_x.tolist(),
                "y": real_y.tolist(),
                "derivative_y": derivative_y.tolist(),
                "note": note,
                "legend": ["Function", "Derivative"]
            }
    
        except Exception:
            result["real_curve"] = None

    return json.dumps(result)
