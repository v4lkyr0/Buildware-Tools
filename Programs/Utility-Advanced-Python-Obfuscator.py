# Copyright (c) 2025-2026 v4lkyr0 — Buildware-Tools
# See the file 'LICENSE' for copying permission.
# --------------------------------------------------------
# EN: Non-commercial use only. Do not sell, remove credits
#     or redistribute without prior written permission.
# FR: Usage non-commercial uniquement. Ne pas vendre, supprimer
#     les crédits ou redistribuer sans autorisation écrite.

from Core.Utils import *
from Core.Config import *

try:
    import ast
    import base64
    import builtins
    import hashlib
    import io
    import marshal
    import random
    import string
    import tokenize
    import zlib
except Exception as e:
    MissingModule(e)

Title("Advanced Python Obfuscator")

Scroll(GradientBanner(utilities_banner))

protected_names = set(dir(builtins)) | {
    "self", "cls", "__name__", "__main__", "__file__", "__doc__",
    "__init__", "__new__", "__del__", "__repr__", "__str__", "__len__",
    "__iter__", "__next__", "__getitem__", "__setitem__", "__delitem__",
    "__contains__", "__call__", "__enter__", "__exit__", "__eq__", "__ne__",
    "__lt__", "__le__", "__gt__", "__ge__", "__hash__", "__bool__",
    "__add__", "__sub__", "__mul__", "__truediv__", "__floordiv__",
    "__mod__", "__pow__", "__and__", "__or__", "__xor__", "__lshift__",
    "__rshift__", "__neg__", "__pos__", "__abs__", "__invert__",
    "__class__", "__dict__", "__module__", "__qualname__", "__slots__",
    "__all__", "__version__", "__author__", "__annotations__",
    "__getattr__", "__setattr__", "__delattr__", "__get__", "__set__",
    "__delete__", "__instancecheck__", "__subclasscheck__",
    "__prepare__", "__init_subclass__", "__class_getitem__",
    "__import__", "__loader__", "__spec__", "__path__", "__package__",
    "__builtins__", "__cached__", "__bases__", "__mro__",
    "True", "False", "None",
}

anti_debug_code = '''
import sys as _s0, os as _o0, time as _t0, ctypes as _c0, platform as _p0
def _chk():
    if _s0.gettrace() is not None: _o0._exit(0)
    if _p0.system() == "Windows":
        try:
            if _c0.windll.kernel32.IsDebuggerPresent(): _o0._exit(0)
        except: pass
    _a = _t0.perf_counter()
    for _i in range(2000): pass
    if (_t0.perf_counter() - _a) > 0.5: _o0._exit(0)
    for _v in ("PYTHONBREAKPOINT", "PYTHONINSPECT", "PYTHONDEBUG"):
        if _o0.environ.get(_v): _o0._exit(0)
    try:
        import psutil
        _bl = {"x32dbg","x64dbg","ollydbg","ida","ida64","ghidra","dnspy","windbg","cheatengine","frida","procexp","wireshark"}
        for _pr in psutil.process_iter(["name"]):
            try:
                if _pr.info["name"].lower().replace(".exe","") in _bl: _o0._exit(0)
            except: continue
    except: pass
_chk()
del _chk
'''

def RandomName(length=12):
    prefix = random.choice(["_O", "_l", "_I", "_0O", "_Il", "_oO", "_lI"])
    return prefix + "".join(random.choices("OIl10", k=length))

def RandVar():
    return "_" + "".join(random.choices("OIl10", k=10))

def RemoveComments(source):
    result = []
    try:
        tokens = tokenize.generate_tokens(io.StringIO(source).readline)
        for tok_type, tok_string, _, _, _ in tokens:
            if tok_type != tokenize.COMMENT:
                result.append((tok_type, tok_string))
    except tokenize.TokenError:
        return source
    return tokenize.untokenize(result)

def RemoveDocstrings(tree):
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef, ast.Module)):
            if (node.body and isinstance(node.body[0], ast.Expr)
                and isinstance(node.body[0].value, ast.Constant)
                and isinstance(node.body[0].value.value, str)):
                node.body.pop(0)
                if not node.body:
                    node.body.append(ast.Pass())
    ast.fix_missing_locations(tree)
    return tree

class IdentifierCollector(ast.NodeVisitor):
    def __init__(self):
        self.defined    = set()
        self.imported   = set()
        self.attributes = set()
        self.globals_   = set()

    def visit_FunctionDef(self, node):
        if not node.name.startswith("__"):
            self.defined.add(node.name)
        for arg in node.args.args + node.args.kwonlyargs + node.args.posonlyargs:
            self.defined.add(arg.arg)
        if node.args.vararg:
            self.defined.add(node.args.vararg.arg)
        if node.args.kwarg:
            self.defined.add(node.args.kwarg.arg)
        self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node):
        self.visit_FunctionDef(node)

    def visit_ClassDef(self, node):
        if not node.name.startswith("__"):
            self.defined.add(node.name)
        self.generic_visit(node)

    def visit_Assign(self, node):
        for target in node.targets:
            self.CollectTargets(target)
        self.generic_visit(node)

    def visit_AnnAssign(self, node):
        self.CollectTargets(node.target)
        self.generic_visit(node)

    def visit_AugAssign(self, node):
        self.CollectTargets(node.target)
        self.generic_visit(node)

    def visit_For(self, node):
        self.CollectTargets(node.target)
        self.generic_visit(node)

    def visit_With(self, node):
        for item in node.items:
            if item.optional_vars:
                self.CollectTargets(item.optional_vars)
        self.generic_visit(node)

    def visit_ExceptHandler(self, node):
        if node.name:
            self.defined.add(node.name)
        self.generic_visit(node)

    def visit_Global(self, node):
        for name in node.names:
            self.globals_.add(name)
        self.generic_visit(node)

    def CollectTargets(self, target):
        if isinstance(target, ast.Name):
            self.defined.add(target.id)
        elif isinstance(target, (ast.Tuple, ast.List)):
            for elt in target.elts:
                self.CollectTargets(elt)

    def visit_Import(self, node):
        for alias in node.names:
            name = alias.asname if alias.asname else alias.name.split(".")[0]
            self.imported.add(name)
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        for alias in node.names:
            if alias.name == "*":
                continue
            name = alias.asname if alias.asname else alias.name
            self.imported.add(name)
        self.generic_visit(node)

    def visit_Attribute(self, node):
        self.attributes.add(node.attr)
        self.generic_visit(node)

class Renamer(ast.NodeTransformer):
    def __init__(self, mapping):
        self.mapping = mapping

    def visit_Name(self, node):
        if node.id in self.mapping:
            node.id = self.mapping[node.id]
        return node

    def visit_FunctionDef(self, node):
        if node.name in self.mapping:
            node.name = self.mapping[node.name]
        for arg in node.args.args + node.args.kwonlyargs + node.args.posonlyargs:
            if arg.arg in self.mapping:
                arg.arg = self.mapping[arg.arg]
        if node.args.vararg and node.args.vararg.arg in self.mapping:
            node.args.vararg.arg = self.mapping[node.args.vararg.arg]
        if node.args.kwarg and node.args.kwarg.arg in self.mapping:
            node.args.kwarg.arg = self.mapping[node.args.kwarg.arg]
        self.generic_visit(node)
        return node

    def visit_AsyncFunctionDef(self, node):
        return self.visit_FunctionDef(node)

    def visit_ClassDef(self, node):
        if node.name in self.mapping:
            node.name = self.mapping[node.name]
        self.generic_visit(node)
        return node

    def visit_arg(self, node):
        if node.arg in self.mapping:
            node.arg = self.mapping[node.arg]
        return node

    def visit_ExceptHandler(self, node):
        if node.name and node.name in self.mapping:
            node.name = self.mapping[node.name]
        self.generic_visit(node)
        return node

    def visit_Global(self, node):
        node.names = [self.mapping.get(n, n) for n in node.names]
        return node

def RenameIdentifiers(tree):
    collector  = IdentifierCollector()
    collector.visit(tree)
    renamable  = collector.defined - collector.imported - protected_names - collector.globals_
    renamable  = {n for n in renamable if not n.startswith("__")}
    renamable -= collector.attributes
    used_names = set()
    mapping    = {}
    for name in sorted(renamable):
        while True:
            new = RandomName()
            if new not in used_names:
                used_names.add(new)
                mapping[name] = new
                break
    tree = Renamer(mapping).visit(tree)
    ast.fix_missing_locations(tree)
    return tree

class ImportHider(ast.NodeTransformer):
    def __init__(self):
        self.hidden_imports = {}
        self.import_vars    = {}

    def visit_Import(self, node):
        replacements = []
        for alias in node.names:
            var_name = RandVar()
            name     = alias.asname if alias.asname else alias.name
            self.import_vars[name] = var_name
            assign = ast.Assign(
                targets=[ast.Name(id=var_name, ctx=ast.Store())],
                value=ast.Call(
                    func=ast.Name(id="__import__", ctx=ast.Load()),
                    args=[ast.Constant(value=alias.name)],
                    keywords=[],
                ),
            )
            replacements.append(assign)
        return replacements

    def visit_ImportFrom(self, node):
        if any(a.name == "*" for a in node.names):
            return node
        replacements = []
        mod_var = RandVar()
        mod_assign = ast.Assign(
            targets=[ast.Name(id=mod_var, ctx=ast.Store())],
            value=ast.Call(
                func=ast.Name(id="__import__", ctx=ast.Load()),
                args=[ast.Constant(value=node.module or "")],
                keywords=[
                    ast.keyword(arg="fromlist", value=ast.List(
                        elts=[ast.Constant(value=a.name) for a in node.names],
                        ctx=ast.Load()
                    ))
                ],
            ),
        )
        replacements.append(mod_assign)
        for alias in node.names:
            name     = alias.asname if alias.asname else alias.name
            var_name = RandVar()
            self.import_vars[name] = var_name
            attr_assign = ast.Assign(
                targets=[ast.Name(id=var_name, ctx=ast.Store())],
                value=ast.Attribute(
                    value=ast.Name(id=mod_var, ctx=ast.Load()),
                    attr=alias.name,
                    ctx=ast.Load(),
                ),
            )
            replacements.append(attr_assign)
        return replacements

    def visit_Name(self, node):
        if node.id in self.import_vars:
            node.id = self.import_vars[node.id]
        return node

def HideImports(tree):
    hider = ImportHider()
    new_body = []
    for node in tree.body:
        result = hider.visit(node)
        if isinstance(result, list):
            new_body.extend(result)
        else:
            new_body.append(result)
    tree.body = new_body
    for node in ast.walk(tree):
        if isinstance(node, ast.Name) and node.id in hider.import_vars:
            node.id = hider.import_vars[node.id]
    ast.fix_missing_locations(tree)
    return tree

class LiteralObfuscator(ast.NodeTransformer):
    def visit_Import(self, node):
        return node

    def visit_ImportFrom(self, node):
        return node

    def visit_JoinedStr(self, node):
        return node

    def visit_FormattedValue(self, node):
        return node

    def visit_Expr(self, node):
        if isinstance(node.value, ast.Constant) and isinstance(node.value.value, str):
            return node
        self.generic_visit(node)
        return node

    def visit_Constant(self, node):
        if isinstance(node.value, str) and len(node.value) > 0:
            return self.EncodeString(node.value)
        if isinstance(node.value, int) and not isinstance(node.value, bool):
            return self.EncodeInt(node.value)
        return node

    def EncodeString(self, s):
        method = random.choice(["b64", "hex", "rot", "xor", "split"])

        if method == "b64":
            encoded = base64.b64encode(s.encode()).decode()
            return ast.Call(
                func=ast.Attribute(
                    value=ast.Call(
                        func=ast.Attribute(
                            value=ast.Call(
                                func=ast.Name(id="__import__", ctx=ast.Load()),
                                args=[ast.Constant(value="base64")],
                                keywords=[],
                            ),
                            attr="b64decode", ctx=ast.Load(),
                        ),
                        args=[ast.Constant(value=encoded)], keywords=[],
                    ),
                    attr="decode", ctx=ast.Load(),
                ),
                args=[], keywords=[],
            )

        elif method == "hex":
            hex_str = s.encode().hex()
            return ast.Call(
                func=ast.Attribute(
                    value=ast.Call(
                        func=ast.Attribute(
                            value=ast.Name(id="bytes", ctx=ast.Load()),
                            attr="fromhex", ctx=ast.Load(),
                        ),
                        args=[ast.Constant(value=hex_str)], keywords=[],
                    ),
                    attr="decode", ctx=ast.Load(),
                ),
                args=[], keywords=[],
            )

        elif method == "rot":
            shift   = random.randint(1, 25)
            shifted = "".join(chr((ord(c) + shift) % 256) for c in s)
            encoded = base64.b64encode(shifted.encode("latin-1")).decode()
            v1      = RandVar()
            code    = f'(lambda {v1}:"".join(chr((ord(c)-{shift})%256)for c in __import__("base64").b64decode({v1}).decode("latin-1")))("{encoded}")'
            return ast.parse(code, mode="eval").body

        elif method == "xor":
            key     = random.randint(1, 255)
            xored   = bytes([b ^ key for b in s.encode()])
            encoded = base64.b64encode(xored).decode()
            v1      = RandVar()
            code    = f'(lambda {v1}:bytes(b^{key} for b in __import__("base64").b64decode({v1})).decode())("{encoded}")'
            return ast.parse(code, mode="eval").body

        else:
            if len(s) < 3:
                encoded = base64.b64encode(s.encode()).decode()
                return ast.Call(
                    func=ast.Attribute(
                        value=ast.Call(
                            func=ast.Attribute(
                                value=ast.Call(
                                    func=ast.Name(id="__import__", ctx=ast.Load()),
                                    args=[ast.Constant(value="base64")],
                                    keywords=[],
                                ),
                                attr="b64decode", ctx=ast.Load(),
                            ),
                            args=[ast.Constant(value=encoded)], keywords=[],
                        ),
                        attr="decode", ctx=ast.Load(),
                    ),
                    args=[], keywords=[],
                )
            chunks    = []
            remaining = s
            while remaining:
                size = random.randint(1, max(1, len(remaining) // 2))
                chunks.append(remaining[:size])
                remaining = remaining[size:]
            random_order = list(range(len(chunks)))
            order_map    = list(range(len(chunks)))
            random.shuffle(random_order)
            shuffled     = [chunks[i] for i in random_order]
            restore      = [0] * len(chunks)
            for new_pos, old_pos in enumerate(random_order):
                restore[old_pos] = new_pos
            parts_str = ",".join(f'"{c}"' for c in shuffled)
            order_str = ",".join(str(i) for i in restore)
            v1        = RandVar()
            code      = f'(lambda {v1}:"".join({v1}[i]for i in[{order_str}]))(({parts_str},))'
            return ast.parse(code, mode="eval").body

    def EncodeInt(self, n):
        if abs(n) > 10_000_000:
            return ast.Constant(value=n)
        strategy = random.choice(["xor", "add_sub", "mul_div", "nested", "neg", "shift"])
        if strategy == "xor":
            key = random.randint(1, 0xFFFF)
            return ast.BinOp(left=ast.Constant(value=n ^ key), op=ast.BitXor(), right=ast.Constant(value=key))
        elif strategy == "add_sub":
            a = random.randint(1, 50000)
            b = random.randint(1, 50000)
            return ast.BinOp(
                left=ast.BinOp(left=ast.Constant(value=n + a + b), op=ast.Sub(), right=ast.Constant(value=a)),
                op=ast.Sub(), right=ast.Constant(value=b),
            )
        elif strategy == "mul_div":
            if n == 0:
                v = random.randint(1, 100)
                return ast.BinOp(left=ast.Constant(value=v), op=ast.Sub(), right=ast.Constant(value=v))
            factor = random.randint(2, 13)
            return ast.BinOp(
                left=ast.BinOp(left=ast.Constant(value=n * factor), op=ast.FloorDiv(), right=ast.Constant(value=factor)),
                op=ast.Add(), right=ast.Constant(value=0),
            )
        elif strategy == "nested":
            k1 = random.randint(1, 0xFF)
            k2 = random.randint(1, 0xFF)
            return ast.BinOp(
                left=ast.BinOp(left=ast.Constant(value=(n ^ k1) ^ k2), op=ast.BitXor(), right=ast.Constant(value=k2)),
                op=ast.BitXor(), right=ast.Constant(value=k1),
            )
        elif strategy == "neg":
            offset = random.randint(1, 10000)
            return ast.UnaryOp(
                op=ast.USub(),
                operand=ast.BinOp(left=ast.Constant(value=-n + offset), op=ast.Sub(), right=ast.Constant(value=offset)),
            )
        else:
            if n < 0 or n > 0xFFFFFF:
                return ast.Constant(value=n)
            shift_amount = random.randint(1, 8)
            return ast.BinOp(
                left=ast.Constant(value=n << shift_amount),
                op=ast.RShift(),
                right=ast.Constant(value=shift_amount),
            )

def ObfuscateLiterals(tree):
    tree = LiteralObfuscator().visit(tree)
    ast.fix_missing_locations(tree)
    return tree

def BuildOpaquePredicate():
    kind = random.choice(["math", "type", "len", "bool"])
    if kind == "math":
        x = random.randint(2, 100)
        return ast.Compare(
            left=ast.BinOp(
                left=ast.BinOp(left=ast.Constant(value=x), op=ast.Mult(), right=ast.Constant(value=x)),
                op=ast.Mod(), right=ast.Constant(value=1)
            ),
            ops=[ast.Eq()],
            comparators=[ast.Constant(value=0)]
        )
    elif kind == "type":
        return ast.Call(
            func=ast.Name(id="isinstance", ctx=ast.Load()),
            args=[ast.Constant(value=random.randint(1, 100)), ast.Name(id="int", ctx=ast.Load())],
            keywords=[],
        )
    elif kind == "len":
        s = "".join(random.choices(string.ascii_letters, k=random.randint(3, 10)))
        return ast.Compare(
            left=ast.Call(func=ast.Name(id="len", ctx=ast.Load()), args=[ast.Constant(value=s)], keywords=[]),
            ops=[ast.Gt()],
            comparators=[ast.Constant(value=0)]
        )
    else:
        return ast.Call(
            func=ast.Name(id="bool", ctx=ast.Load()),
            args=[ast.Constant(value=random.randint(1, 999))],
            keywords=[],
        )

class OpaquePredicateInjector(ast.NodeTransformer):
    def __init__(self, intensity=0.15):
        self.intensity = intensity

    def WrapInOpaque(self, body):
        if not body:
            return body
        new_body = []
        for stmt in body:
            if random.random() < self.intensity and not isinstance(stmt, (ast.Import, ast.ImportFrom)):
                wrapped = ast.If(
                    test=BuildOpaquePredicate(),
                    body=[stmt],
                    orelse=[ast.Pass()],
                )
                ast.fix_missing_locations(wrapped)
                new_body.append(wrapped)
            else:
                new_body.append(stmt)
        return new_body

    def visit_FunctionDef(self, node):
        self.generic_visit(node)
        node.body = self.WrapInOpaque(node.body)
        return node

    def visit_AsyncFunctionDef(self, node):
        return self.visit_FunctionDef(node)

    def visit_Module(self, node):
        self.generic_visit(node)
        node.body = self.WrapInOpaque(node.body)
        return node

def InjectOpaquePredicates(tree):
    tree = OpaquePredicateInjector().visit(tree)
    ast.fix_missing_locations(tree)
    return tree

class ControlFlowFlattener(ast.NodeTransformer):
    def visit_FunctionDef(self, node):
        self.generic_visit(node)
        if len(node.body) < 3:
            return node
        has_complex = any(isinstance(s, (ast.If, ast.For, ast.While, ast.Try, ast.With, ast.Return)) for s in node.body)
        if has_complex:
            return node
        state_var = RandomName(8)
        order     = list(range(len(node.body)))
        shuffled  = order[:]
        random.shuffle(shuffled)
        cases = []
        for new_idx, old_idx in enumerate(shuffled):
            if new_idx < len(shuffled) - 1:
                next_state = shuffled.index(order[order.index(shuffled[new_idx]) + 1]) if order.index(shuffled[new_idx]) + 1 < len(order) else -1
            else:
                next_state = -1
            body = [node.body[shuffled[new_idx]]]
            if next_state >= 0:
                body.append(ast.Assign(
                    targets=[ast.Name(id=state_var, ctx=ast.Store())],
                    value=ast.Constant(value=next_state),
                ))
            else:
                body.append(ast.Break())
            case = ast.If(
                test=ast.Compare(
                    left=ast.Name(id=state_var, ctx=ast.Load()),
                    ops=[ast.Eq()],
                    comparators=[ast.Constant(value=new_idx)]
                ),
                body=body,
                orelse=[],
            )
            cases.append(case)
        start_idx = shuffled.index(0)
        init = ast.Assign(
            targets=[ast.Name(id=state_var, ctx=ast.Store())],
            value=ast.Constant(value=start_idx),
        )
        if len(cases) == 0:
            return node
        dispatcher = cases[0]
        current    = dispatcher
        for case in cases[1:]:
            current.orelse = [case]
            current = case
        while_loop = ast.While(
            test=ast.Constant(value=True),
            body=[dispatcher],
            orelse=[],
        )
        node.body = [init, while_loop]
        ast.fix_missing_locations(node)
        return node

def FlattenControlFlow(tree):
    tree = ControlFlowFlattener().visit(tree)
    ast.fix_missing_locations(tree)
    return tree

class LambdaWrapper(ast.NodeTransformer):
    def __init__(self, intensity=0.2):
        self.intensity = intensity

    def visit_FunctionDef(self, node):
        self.generic_visit(node)
        if random.random() > self.intensity:
            return node
        if any(isinstance(s, (ast.Return, ast.Yield, ast.YieldFrom)) for s in ast.walk(node)):
            return node
        if node.decorator_list:
            return node
        if any(isinstance(a, ast.arg) and a.annotation for a in node.args.args):
            return node
        wrapper_name = RandomName(8)
        original     = ast.FunctionDef(
            name=wrapper_name,
            args=node.args,
            body=node.body,
            decorator_list=[],
            returns=None,
        )
        assign = ast.Assign(
            targets=[ast.Name(id=node.name, ctx=ast.Store())],
            value=ast.Name(id=wrapper_name, ctx=ast.Load()),
        )
        return [original, assign]

def WrapLambdas(tree):
    wrapper  = LambdaWrapper()
    new_body = []
    for node in tree.body:
        result = wrapper.visit(node)
        if isinstance(result, list):
            new_body.extend(result)
        else:
            new_body.append(result)
    tree.body = new_body
    ast.fix_missing_locations(tree)
    return tree

def BuildJunkStmt():
    kind = random.choice(["assign", "dead_if", "false_cmp", "dead_loop", "dead_try", "opaque_assign"])
    if kind == "assign":
        return ast.Assign(
            targets=[ast.Name(id=RandomName(), ctx=ast.Store())],
            value=ast.Constant(value=random.randint(0, 99999)),
        )
    elif kind == "dead_if":
        name = RandomName()
        return ast.If(
            test=ast.Constant(value=False),
            body=[
                ast.Assign(targets=[ast.Name(id=name, ctx=ast.Store())], value=ast.Constant(value=random.randint(1, 100))),
                ast.AugAssign(target=ast.Name(id=name, ctx=ast.Store()), op=ast.Mult(), value=ast.Constant(value=random.randint(2, 9))),
            ],
            orelse=[],
        )
    elif kind == "false_cmp":
        return ast.If(
            test=ast.Compare(
                left=ast.Constant(value=random.randint(1, 100)),
                ops=[ast.Eq()],
                comparators=[ast.Constant(value=random.randint(101, 200))],
            ),
            body=[ast.Pass()],
            orelse=[],
        )
    elif kind == "dead_loop":
        return ast.If(
            test=ast.Constant(value=False),
            body=[
                ast.For(
                    target=ast.Name(id=RandomName(), ctx=ast.Store()),
                    iter=ast.Call(func=ast.Name(id="range", ctx=ast.Load()), args=[ast.Constant(value=0)], keywords=[]),
                    body=[ast.Pass()], orelse=[],
                )
            ],
            orelse=[],
        )
    elif kind == "dead_try":
        return ast.If(
            test=ast.Constant(value=False),
            body=[
                ast.Try(
                    body=[ast.Pass()],
                    handlers=[ast.ExceptHandler(type=None, name=None, body=[ast.Pass()])],
                    orelse=[], finalbody=[],
                )
            ],
            orelse=[],
        )
    else:
        n    = RandomName()
        val  = random.randint(1, 9999)
        pred = BuildOpaquePredicate()
        return ast.If(
            test=ast.UnaryOp(op=ast.Not(), operand=pred),
            body=[ast.Assign(targets=[ast.Name(id=n, ctx=ast.Store())], value=ast.Constant(value=val))],
            orelse=[],
        )

class JunkInjector(ast.NodeTransformer):
    def __init__(self, intensity=0.4):
        self.intensity = intensity

    def Inject(self, body):
        if not body:
            return body
        new_body = []
        for stmt in body:
            if random.random() < self.intensity:
                junk = BuildJunkStmt()
                ast.fix_missing_locations(junk)
                new_body.append(junk)
            new_body.append(stmt)
            if random.random() < 0.15:
                junk = BuildJunkStmt()
                ast.fix_missing_locations(junk)
                new_body.append(junk)
        return new_body

    def visit_FunctionDef(self, node):
        self.generic_visit(node)
        node.body = self.Inject(node.body)
        return node

    def visit_AsyncFunctionDef(self, node):
        return self.visit_FunctionDef(node)

    def visit_Module(self, node):
        self.generic_visit(node)
        import_end = 0
        for i, stmt in enumerate(node.body):
            if isinstance(stmt, (ast.Import, ast.ImportFrom, ast.Assign)):
                if isinstance(stmt, ast.Assign) and any(
                    isinstance(t, ast.Name) and t.id.startswith("_") for t in stmt.targets
                ):
                    import_end = i + 1
                elif isinstance(stmt, (ast.Import, ast.ImportFrom)):
                    import_end = i + 1
            else:
                break
        header    = node.body[:import_end]
        body      = node.body[import_end:]
        node.body = header + self.Inject(body)
        return node

def InjectJunkCode(tree):
    tree = JunkInjector().visit(tree)
    ast.fix_missing_locations(tree)
    return tree

def WrapLayerMarshal(source):
    try:
        code_obj   = compile(source, "<module>", "exec")
        payload    = marshal.dumps(code_obj)
        compressed = zlib.compress(payload, level=9)
        encoded    = base64.b64encode(compressed).decode("ascii")
        b, z, m    = RandVar(), RandVar(), RandVar()
        return (
            f"{b}=__import__('base64');"
            f"{z}=__import__('zlib');"
            f"{m}=__import__('marshal');"
            f"exec({m}.loads({z}.decompress({b}.b64decode('{encoded}'))))"
        )
    except:
        return WrapLayerZlib(source)

def WrapLayerZlib(source):
    compressed = zlib.compress(source.encode("utf-8"), level=9)
    encoded    = base64.b64encode(compressed).decode("ascii")
    b, z       = RandVar(), RandVar()
    return (
        f"{b}=__import__('base64');"
        f"{z}=__import__('zlib');"
        f"exec({z}.decompress({b}.b64decode('{encoded}')).decode())"
    )

def WrapLayerXor(source):
    key        = random.randint(1, 255)
    xored      = bytes([b ^ key for b in source.encode("utf-8")])
    compressed = zlib.compress(xored, level=9)
    encoded    = base64.b64encode(compressed).decode("ascii")
    b, z       = RandVar(), RandVar()
    return (
        f"{b}=__import__('base64');"
        f"{z}=__import__('zlib');"
        f"exec(bytes(c^{key} for c in {z}.decompress({b}.b64decode('{encoded}'))).decode())"
    )

def WrapLayerHex(source):
    compressed = zlib.compress(source.encode("utf-8"), level=9)
    hex_str    = compressed.hex()
    z          = RandVar()
    return (
        f"{z}=__import__('zlib');"
        f"exec({z}.decompress(bytes.fromhex('{hex_str}')).decode())"
    )

def WrapMultiLayer(source, layers=4):
    current    = source
    wrap_funcs = [WrapLayerMarshal, WrapLayerZlib, WrapLayerXor, WrapLayerHex]
    current    = WrapLayerMarshal(current)
    for i in range(1, layers):
        func    = random.choice(wrap_funcs[1:])
        current = func(current)
    return current

def Obfuscate(source):
    source = RemoveComments(source)
    tree   = ast.parse(source)
    tree   = RemoveDocstrings(tree)
    tree   = RenameIdentifiers(tree)
    tree   = HideImports(tree)
    tree   = ObfuscateLiterals(tree)
    tree   = FlattenControlFlow(tree)
    tree   = InjectOpaquePredicates(tree)
    tree   = WrapLambdas(tree)
    tree   = InjectJunkCode(tree)
    code   = ast.unparse(tree)
    code   = WrapMultiLayer(code, layers=4)
    code   = anti_debug_code + "\n" + code
    return code

try:
    print(f"{INPUT} Select Python File {red}->{reset} ", reset)

    filepath = BrowseFile("Select Python File", [("Python Files", "*.py"), ("All Files", "*.*")])

    if not filepath:
        print(f"{ERROR} No file selected!", reset)
        Continue()
        Reset()

    print(f"{SUCCESS} File:{red} {os.path.basename(filepath)}", reset)

    if not os.path.isfile(filepath):
        print(f"{ERROR} File not found!", reset)
        Continue()
        Reset()

    with open(filepath, "r", encoding="utf-8") as f:
        source = f.read()

    if not source.strip():
        ErrorInput()

    print(f"{LOADING} Obfuscating..", reset)

    try:
        obfuscated = Obfuscate(source)
    except SyntaxError:
        print(f"{ERROR} Invalid Python syntax!", reset)
        Continue()
        Reset()

    output_dir  = os.path.join(tool_path, "Programs", "Output", "AdvancedPythonObfuscator")
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, os.path.basename(filepath))

    header = (
        f"# Copyright (c) 2025-2026 v4lkyr0 — Buildware-Tools\n"
        f"# Obfuscated with Advanced Python Obfuscator.\n\n"
    )

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(header + obfuscated)

    print(f"{SUCCESS} Saved:{red} {output_path}", reset)

    if platform_pc == "Windows":
        os.startfile(output_dir)
    else:
        subprocess.Popen(["xdg-open", output_dir])

    Continue()
    Reset()

except Exception as e:
    Error(e)