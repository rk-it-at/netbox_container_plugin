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

images = PluginMenuItem(
    link="plugins:netbox_containers:image_list",
    link_text="Images",
    permissions=["netbox_containers.view_image"],
    buttons=(
        PluginMenuButton(
            link="plugins:netbox_containers:image_add",
            title="Add",
            icon_class="mdi mdi-plus",
            color=ButtonColorChoices.GREEN,
            permissions=["netbox_containers.add_image"],
        ),
    ),
)

imagetags = PluginMenuItem(
    link="plugins:netbox_containers:imagetag_list",
    link_text="Image Tags",
    permissions=["netbox_containers.view_imagetags"],
    buttons=(
        PluginMenuButton(
            link="plugins:netbox_containers:imagetag_add",
            title="Add",
            icon_class="mdi mdi-plus",
            color=ButtonColorChoices.GREEN,
            permissions=["netbox_containers.add_imagetag"],
        ),
    ),
)

menu = PluginMenu(
    label="Containers",
    groups=(
        ("Inventory", (pods, networks, images, imagetags)),
    ),
    icon_class="mdi mdi-docker",
)
