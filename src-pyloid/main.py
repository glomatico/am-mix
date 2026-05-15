from pyloid.utils import (
    get_production_path,
    is_production,
)
from pyloid.serve import pyloid_serve
from pyloid import Pyloid
from server import CustomRpc

custom_rpc = CustomRpc()

app = Pyloid(
    app_name="am-mix",
    single_instance=True,
    server=custom_rpc,
)

app.set_icon(get_production_path("src-pyloid/icons/icon.ico"))
app.set_tray_icon(get_production_path("src-pyloid/icons/icon.ico"))

if is_production():
    url = pyloid_serve(directory=get_production_path("dist-front"))
    window = app.create_window(title=app.app.app_name)
    window.load_url(url)
else:
    window = app.create_window(title=app.app.app_name, dev_tools=True)
    window.load_url("http://localhost:5173")

window.show_and_focus()

custom_rpc.window = window

app.run()
