import configparser
import os
import color_analyzer


def create_config(path, section, setting, value):
    """
    Create a config file
    """
    config = configparser.ConfigParser()
    config.add_section(section)
    config.set(section, "color", "colorAnalysis(imagepath)")
    config.set(section, "lab", "10")
    config.set(section, "name", "Normal")
    config.set(section, "delta", "Normal")
    with open(path, "a") as config_file:
        config.write(config_file)


def get_config(path):
    """
    Returns the config object
    """
    if not os.path.exists(path):
        create_config(path, '0', '0', '0')

    config = configparser.ConfigParser()
    config.read(path, encoding="utf8")
    return config


def get_setting(path, section, setting):
    """
    Print out a setting
    """
    config = get_config(path)
    value = config.get(section, setting)
    msg = "{section} {setting} is {value}".format(
        section=section, setting=setting, value=value
    )

    return value


def update_setting(path, section, setting, value):
    """
    Update a setting
    """
    config = get_config(path)
    try:
        config.set(section, setting, value)
        with open(path, "w", encoding='utf-8') as config_file:
            config.write(config_file)
        return
    except configparser.NoSectionError as identifier:
        create_config(path, section, setting, value)
        update_setting(path, section, setting, value)


def delete_setting(path, section):
    """
    Delete a setting
    """
    config = get_config(path)
    config.remove_section(section)
    with open(path, "w", encoding="utf8") as config_file:
        config.write(config_file)


if __name__ == "__main__":
    path = 'settings.ini'
    img = 'src\\images.jpg'
    strStand = get_setting(path, "core", "stand")
    stand = []
    for i in range(3):
        intStand = strStand.split(" ")[i]
        stand.append(int(intStand))
    names = get_setting(path, "core", "names")
    names_of_section = names.split(",")
    print(names_of_section)
    reference_mass = []
    reference_delta_mass = []
    for name in names_of_section:
        if name == '':
            continue
        str_reference = get_setting(path, name, 'lab')
        str_delta = get_setting(path, name, 'delta')
        int_reference = []
        for i in range(3):
            for_int_reference = str_reference.split(" ")[i]
            int_reference.append(int(for_int_reference))
        int_delta = int(str_delta)
        reference_mass.append(int_reference)
        reference_delta_mass.append(int_delta)
    print(color_analyzer.colorAnalysis(
        reference_mass, reference_delta_mass, stand, img))
