from beaker import Application, GlobalStateValue, unconditional_create_approval
from pyteal import Bytes, Expr, Int, TealType, abi


class GlobalState:
    TotalVaccines = GlobalStateValue(
        stack_type=TealType.uint64,
        default=Int(0),
        static=False,
        descr="An integer global state value"

    )

    AdminAddress = GlobalStateValue(
        stack_type=TealType.bytes,
        default=Bytes(""),
        static=False,
        descr="A Address which is a global state value"

    )

    AppVersion = GlobalStateValue(
        stack_type=TealType.bytes,
        default=Bytes("1.0.0"),
        static=True,
        descr="An global state value which stores the version of the contract running"

    )

    TotalStores = GlobalStateValue(
        stack_type=TealType.uint64,
        default=Int(1),
        static=False,
        descr="an integer value that stores the total number of stores that exist"

    )
app = Application("VaccineDistribution", state=GlobalState()).apply(
    unconditional_create_approval, initialize_global_state=True
)


@app.external
def set_app_state_val(v: abi.Uint32) -> Expr:
    return app.state.TotalVaccines.set(v.get())


@app.external(read_only=True)
def get_app_state_val(*, output: abi.Uint32) -> Expr:
    return output.set(app.state.TotalVaccines)


@app.external
def set_admin(new_admin: abi.Address):
    return app.state.AdminAddress.set(new_admin.get())

@app.external(read_only=True)
def get_admin(*, output: abi.Address) -> Expr:
    return output.set(app.state.AdminAddress.get())


@app.external
def set_total_stores(v: abi.Uint32) -> Expr:
    return app.state.TotalStores.set(v.get())


@app.external(read_only=True)
def get_total_stores(*, output: abi.Uint32) -> Expr:
    return output.set(app.state.TotalStores)

