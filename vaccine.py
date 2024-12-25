from beaker import Application, GlobalStateValue, unconditional_create_approval
from pyteal import Bytes, Expr, Int, TealType, abi


class GlobalState:
    TotalVaccines = GlobalStateValue(
        stack_type=TealType.uint64,
        default=Int(0),
        static=False,
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
