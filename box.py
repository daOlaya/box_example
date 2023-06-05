import pyteal as pt
from typing import Literal
import beaker


# # Our custom Struct
# class Order(pt.abi.NamedTuple):
#     a1: pt.abi.Field[pt.abi.Uint64]
#     a2: pt.abi.Field[pt.abi.Uint64]
#     a3: pt.abi.Field[pt.abi.Uint64]
#     a4: pt.abi.Field[pt.abi.Uint64]
#     a5: pt.abi.Field[pt.abi.Uint64]
#     # item: pt.abi.Field[pt.abi.String]
#     # quantity: pt.abi.Field[pt.abi.Uint16]

a1 = pt.Bytes("1")
a2 = pt.Bytes("2")
a3 = pt.Bytes("3")
a4 = pt.Bytes("4")
a5 = pt.Bytes("5")

arr_order = [a1, a2, a3, a4, a5]
# Assume you have a StaticArray of integers
# static_array = pt.abi.StaticArray[pt.abi.Uint64, 5]
Order = pt.abi.StaticArray[pt.TealType.bytes, 5]
# Order = pt.abi.StaticArray.new_instance(pt.TealType.uint64)
# Order = pt.abi.DynamicArray[pt.abi.Uint64]
# Order = pt.abi.StaticArray[a1, a2, a3, a4, a5]
    # item: pt.abi.Field[pt.abi.String]
    # quantity: pt.abi.Field[pt.abi.Uint16]


class StructerState:
    orders = beaker.ReservedLocalStateValue(
        stack_type=pt.TealType.bytes,
        max_keys=16,
        prefix="",
    )
# 

app = (
    beaker.Application("Structer", state=StructerState())
    # allow opt-in and initialise local/account state
    .apply(beaker.unconditional_opt_in_approval, initialize_local_state=True)
)


@app.external
def place_order(order_number: pt.abi.Uint8) -> pt.Expr:
    return app.state.orders[order_number].set(arr_order)


# @app.external(read_only=True)
# def read_item(order_number: pt.abi.Uint8, *, output: Order) -> pt.Expr:
#     # return pt.Seq(
#     #     (arr := Order()).decode(get_item(order_number)),
#     #     output.set(arr)
#     # )
#     return output.set(get_item(order_number))
    # return output.decode(get_item(order_number))
    # return output.decode(app.state.orders[order_number])


# @app.external(read_only=True)
# def read_item_1(order_number: pt.abi.Uint8, *, output: pt.abi.Uint64) -> pt.Expr:
#     return output.decode(app.state.orders[order_number][1])

@app.external#(read_only=True)
def read_item_2(order_number: pt.abi.Uint8, *, output: pt.abi.Uint64) -> pt.Expr:
    # return output.decode(get_item(order_number))
    return pt.Seq(
        (new_order := Order()).decode(app.state.orders[order_number]),
        (quant := pt.abi.Uint64()).set(new_order[1]),
        output.set(quant.get() + pt.Int(1))
    )

# @app.external
# def calc_st(order_number: pt.abi.Uint8, *, output: pt.abi.Uint64) -> pt.Expr:
#     total_sum = pt.ScratchVar(pt.TealType.uint64)
#     l = pt.ScratchVar(pt.TealType.uint64)
#     j = pt.ScratchVar(pt.TealType.uint64)
#     x = pt.abi.make(pt.abi.Uint64)

#     return pt.Seq(
#         total_sum.store(pt.Int(0)),
#         l.store(pt.Int(5)),
#         (order := Order()).decode(app.state.orders[order_number]),
#         pt.For(
#             j.store(pt.Int(0)),
#             j.load() < l.load(), 
#             j.store(j.load() + pt.Int(1)),
#         ).Do(
#             (x.set(j.load())),
#             # total_sum.store(j.load() + pt.Int(10))
#             (element := pt.abi.Uint64()).set(order[pt.Bytes("a1")]),
#             total_sum.store(total_sum.load() +  element.get()),
#         ),
#         output.set(total_sum.load())
#     )

@pt.Subroutine(pt.TealType.bytes)
def get_item(order_number: pt.abi.Uint8) -> pt.Expr:
    # return Order().decode(app.state.orders[order_number]),
    return pt.Seq(
        (new_order := Order()).decode(app.state.orders[order_number]),
        (quant := pt.abi.Uint64()).set(new_order[1]),
        quant.encode()
    )
    # return app.state.orders[order_number]

# @app.external(read_only=True)
# def read_item_len(order_number: pt.abi.Uint8, *, output: Order) -> pt.Expr:
#     return pt.Seq(
#         arr := app.state.orders[order_number],

#     )


# @app.external
# def increase_quantity(order_number: pt.abi.Uint8, *, output: Order) -> pt.Expr:
#     return pt.Seq(
#         # Read the order from state
#         (new_order := Order()).decode(app.state.orders[order_number]),
#         # Select out in the quantity attribute, its a TupleElement type
#         # so needs to be stored somewhere
#         (quant := pt.abi.Uint16()).set(new_order.quantity),
#         # Add 1 to quantity
#         quant.set(quant.get() + pt.Int(1)),
#         (item := pt.abi.String()).set(new_order.item),
#         # We've gotta set all of the fields at the same time, but we can
#         # borrow the item we already know about
#         new_order.set(item, quant),
#         # Write the new order to state
#         app.state.orders[order_number].set(new_order.encode()),
#         # Write new order to caller
#         output.decode(new_order.encode()),
#     )