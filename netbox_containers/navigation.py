from netbox.plugins import PluginMenu, PluginMenuItem, PluginMenuButton
from netbox.choices import ButtonColorChoices

containers = PluginMenuItem(
    link="plugins:netbox_containers:container_list",
    link_text="Containers",
    permissions=["netbox_containers.view_container"],
    buttons=(
        PluginMenuButton(
            link="plugins:netbox_containers:container_add",
            title="Add",
            icon_class="mdi mdi-plus",
            color=ButtonColorChoices.GREEN,
            permissions=["netbox_containers.add_container"],
        ),
    ),
)

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

volumes = PluginMenuItem(
    link="plugins:netbox_containers:volume_list",
    link_text="Volumes",
    permissions=["netbox_containers.view_volume"],
    buttons=(
        PluginMenuButton(
            link="plugins:netbox_containers:volume_add",
            title="Add",
            icon_class="mdi mdi-plus",
            color=ButtonColorChoices.GREEN,
            permissions=["netbox_containers.add_volume"],
        ),
    ),
)

menu = PluginMenu(
    label="Containers",
    groups=(
        ("Inventory", (containers, pods, networks, images, imagetags, volumes)),
    ),
    icon_class="mdi mdi-docker",
)
