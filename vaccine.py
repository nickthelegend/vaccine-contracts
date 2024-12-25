from beaker import Application, GlobalStateValue, unconditional_create_approval , LocalStateValue, unconditional_opt_in_approval
from pyteal import Bytes, Expr, Int, Seq, TealType, abi,Txn, Concat
from beaker.lib.storage import BoxMapping

class VaccineItem(abi.NamedTuple):
    name : abi.Field[abi.String]
    manufacturer: abi.Field[abi.String]
    desc: abi.Field[abi.String]


# class StoreInventory:
#     inventory = BoxMapping(abi.Uint64, VaccineItem)



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

    GlobalVaccineAvailability = GlobalStateValue(
        stack_type=TealType.uint64,
        default=Int(1),
        static=False,
        descr="an integer value that stores the total number of stores that exist"

    )


    

class LocalState:
    Role = LocalStateValue(
        stack_type=TealType.bytes,
        default=Bytes("User"),
        descr="User's role"
    )


class CombinedState(GlobalState, LocalState):
    inventory = BoxMapping(abi.String, VaccineItem)

    pass

app = Application("VaccineDistribution", state=CombinedState()).apply(
    unconditional_opt_in_approval, initialize_local_state=True
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



@app.external
def set_total_global_vaccine(v: abi.Uint32) -> Expr:
    return app.state.GlobalVaccineAvailability.set(v.get())


@app.external(read_only=True)
def get_total_global_vaccine(*, output: abi.Uint32) -> Expr:
    return output.set(app.state.GlobalVaccineAvailability)

@app.external
def set_local_role(v:abi.String) -> Expr:
    return app.state.Role[Txn.sender()].set(v.get())

@app.external(read_only=True)
def get_local_role(*, output: abi.String) -> Expr:
    return output.set(app.state.Role[Txn.sender()])
    
@app.external
def set_vaccine_quantity(store_id: abi.String,vaccine_name: abi.String,vaccineManufacturer: abi.String, desc: abi.String,vaccine_id: abi.Uint64, quantity: abi.Uint64) -> Expr:
    vaccineTuple = VaccineItem()
    

    return Seq(
        vaccineTuple.set(vaccine_name,vaccineManufacturer,desc),
    app.state.inventory[store_id.get()].set(vaccineTuple)
        
    )



@app.external
def readItem(store_id: abi.String, *, output: VaccineItem) -> Expr:
    return app.state.inventory[store_id.get()].store_into(output)
