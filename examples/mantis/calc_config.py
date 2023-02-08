LISTBOX_MIMETYPE = "application/x-item"
OP_NODE_INPUT = 1
OP_NODE_OUTPUT = 2
OP_NODE_ADD = 3
OP_NODE_SUB = 4
OP_NODE_MUL = 5
OP_NODE_DIV = 6
OP_NODE_TEST = 7
OP_NODE_S_MVX_FILE = 8
OP_NODE_T_MVX_FILE = 9
OP_NODE_S_UUID = 10
OP_NODE_O_HARVEST = 11
OP_NODE_O_JOIN = 12
OP_NODE_O_UPLOAD = 13
OP_NODE_O_TSDF = 14

CALC_NODES = {
}


class ConfException(Exception):
    pass


class InvalidNodeRegistration(ConfException):
    pass


class OpCodeNotRegistered(ConfException):
    pass


def register_nodes_now(op_code, class_reference):
    if op_code in CALC_NODES:
        raise InvalidNodeRegistration(f"Duplication of registration at {op_code}. Node {CALC_NODES[op_code]} already exists.")
    CALC_NODES[op_code] = class_reference


def register_nodes(op_code):
    def decorator(original_class):
        register_nodes_now(op_code, original_class)
        return original_class
    return decorator


def get_class_from_op_code(op_code):
    if op_code not in CALC_NODES:
        raise OpCodeNotRegistered(f"op_code {op_code} is not registered.")

    return CALC_NODES[op_code]


from examples.mantis.nodes import * # noqa
