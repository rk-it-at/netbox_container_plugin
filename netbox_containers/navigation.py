# netbox_containers/navigation.py
from netbox.plugins import PluginMenu, PluginMenuItem, PluginMenuButton
from netbox.choices import ButtonColorChoices

pods = PluginMenuItem(
    link="plugins:netbox_containers:pod_list",
    link_text="Pods",
    permissions=["netbox_containers.view_pod"],
    buttons=(
        PluginMenuButton(
            link="plugins:netbox_containers:pod_add",
            title="Add",
            icon_class="mdi mdi-plus",
            color=ButtonColorChoices.GREEN,
            permissions=["netbox_containers.add_pod"],
        ),
    ),
)

networks = PluginMenuItem(
    link="plugins:netbox_containers:network_list",
    link_text="Networks",
    permissions=["netbox_containers.view_network"],
    buttons=(
        PluginMenuButton(
            link="plugins:netbox_containers:network_add",
            title="Add",
            icon_class="mdi mdi-plus",
            color=ButtonColorChoices.GREEN,
            permissions=["netbox_containers.add_network"],
        ),
    ),
)

menu = PluginMenu(
    label="Containers",
    groups=(
        ("Inventory", (pods, networks)),
    ),
    icon_class="mdi mdi-docker",
)
