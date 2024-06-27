import json
from pathlib import Path
from os import path

script = Path(__file__)
name, ext = path.splitext(path.basename(script))

ehid_dir = script.parents[1].absolute()
advancements_dir = path.join(ehid_dir, "entity_hit_detection/data/entityid/advancement")

advancement_types = [
    {"id": "entity_hurt_player", "check": "damage"},
    {"id": "entity_killed_player", "check": "killing_blow"},
    {"id": "player_hurt_entity", "check": "damage"},
    {"id": "player_killed_entity", "check": "killing_blow"}
]

damage_tags = [
    "always_hurts_ender_dragons",
    "always_kills_armor_stands",
    "always_most_significant_fall",
    "always_triggers_silverfish",
    "avoids_guardian_thorns",
    "burn_from_stepping",
    "burns_armor_stands",
    "bypasses_armor",
    "bypasses_effects",
    "bypasses_enchantments",
    "bypasses_invulnerability",
    "bypasses_resistance",
    "bypasses_shield",
    "bypasses_wolf_armor",
    "can_break_armor_stand",
    "damages_helmet",
    "ignites_armor_stands",
    "is_drowning",
    "is_explosion",
    "is_fall",
    "is_fire",
    "is_freezing",
    "is_lightning",
    "is_player_attack",
    "is_projectile",
    "no_anger",
    "no_impact",
    "no_knockback",
    "panic_causes",
    "panic_environmental_causes",
    "witch_resistant_to",
    "wither_immune_to"
]

entities = [
    "allay",
    "area_effect_cloud",
    "armadillo",
    "armor_stand",
    "arrow",
    "axolotl",
    "bat",
    "bee",
    "blaze",
    "block_display",
    "boat",
    "bogged",
    "breeze",
    "breeze_wind_charge",
    "camel",
    "cat",
    "cave_spider",
    "chest_boat",
    "chest_minecart",
    "chicken",
    "cod",
    "command_block_minecart",
    "cow",
    "creeper",
    "dolphin",
    "donkey",
    "dragon_fireball",
    "drowned",
    "egg",
    "elder_guardian",
    "end_crystal",
    "ender_dragon",
    "ender_pearl",
    "enderman",
    "endermite",
    "evoker",
    "evoker_fangs",
    "experience_bottle",
    "experience_orb",
    "eye_of_ender",
    "falling_block",
    "fireball",
    "firework_rocket",
    "fishing_bobber",
    "fox",
    "frog",
    "furnace_minecart",
    "ghast",
    "giant",
    "glow_item_frame",
    "glow_squid",
    "goat",
    "guardian",
    "hoglin",
    "hopper_minecart",
    "horse",
    "husk",
    "illusioner",
    "interaction",
    "iron_golem",
    "item",
    "item_display",
    "item_frame",
    "leash_knot",
    "lightning_bolt",
    "llama",
    "llama_spit",
    "magma_cube",
    "marker",
    "minecart",
    "mooshroom",
    "mule",
    "ocelot",
    "ominous_item_spawner",
    "painting",
    "panda",
    "parrot",
    "phantom",
    "pig",
    "piglin",
    "piglin_brute",
    "pillager",
    "player",
    "polar_bear",
    "potion",
    "pufferfish",
    "rabbit",
    "ravager",
    "salmon",
    "sheep",
    "shulker",
    "shulker_bullet",
    "silverfish",
    "skeleton",
    "skeleton_horse",
    "slime",
    "small_fireball",
    "sniffer",
    "snow_golem",
    "snowball",
    "spawner_minecart",
    "spectral_arrow",
    "spider",
    "squid",
    "stray",
    "strider",
    "tadpole",
    "text_display",
    "tnt",
    "tnt_minecart",
    "trader_llama",
    "trident",
    "tropical_fish",
    "turtle",
    "vex",
    "villager",
    "vindicator",
    "wandering_trader",
    "warden",
    "wind_charge",
    "witch",
    "wither",
    "wither_skeleton",
    "wither_skull",
    "wolf",
    "zoglin",
    "zombie",
    "zombie_horse",
    "zombie_villager",
    "zombified_piglin"
]

num_bits = 16


def tagless_template(damage_type):
    structure = {"expected": False, "id": damage_type}

    return structure


def tag_template(id, damage_type):
    structure = {
        "trigger": "minecraft:" + id,
        "conditions": {
            "damage": {"type": {"tags": [{"expected": True, "id": damage_type}]}}
        },
    }

    return structure


def bit_template_true(id, bit):
    structure = {
        "trigger": "minecraft:" + id,
        "conditions": {
            "damage": {"source_entity": {"nbt": "{Tags:[entityid." + bit + ".1]}"}}
        }
    }

    return structure


def bit_template_false(id, bit):
    structure = {
        "trigger": "minecraft:" + id,
        "conditions": {
            "damage": {"source_entity": {"nbt": "{Tags:[entityid." + bit + ".0]}"}}
        }
    }

    return structure


def player_killed_entity(entity):
    structure = {
        "trigger": "minecraft:player_killed_entity",
        "conditions": {
            "entity": [{"condition": "minecraft:entity_properties", "entity": "this", "predicate": {"type": entity}}]
        }
    }

    return structure


def ehid_advancement(id, check):
    structure = {
        "criteria": {
            "entity": {"trigger": "minecraft:" + id},
            "tagless": {
                "trigger": "minecraft:" + id,
                "conditions": {check: {"type": {"tags": []}}},
            }
        },
        "requirements": [
            ["entity"],
        ],
        "rewards": {"function": "entityid:" + id},
    }

    return structure


for advancement in advancement_types:
    with open(path.join(advancements_dir, advancement["id"] + ".json"), "w") as loaded_advancement:
        current_advancement = ehid_advancement(advancement["id"], advancement["check"])

        tag_requirements = ["tagless"]
        for damage_type in damage_tags:
            current_advancement["criteria"]["tagless"]["conditions"][advancement["check"]]["type"]["tags"].append(tagless_template(damage_type))
            current_advancement["criteria"][damage_type] = tag_template(advancement["id"], damage_type)
            tag_requirements.append(damage_type)
        current_advancement["requirements"].append(tag_requirements)

        if advancement["id"] == "player_killed_entity":
            entity_requirements = []
            for entity in entities:
                current_advancement["criteria"][entity] = player_killed_entity(entity)
                entity_requirements.append(entity)
            current_advancement["requirements"].append(entity_requirements)

        for bit in range(num_bits):
            current_advancement["criteria"]["bit" + str(bit)] = bit_template_true(advancement["id"], str(bit))
            current_advancement["criteria"]["!bit" + str(bit)] = bit_template_false(advancement["id"], str(bit))
            current_advancement["requirements"].append(["bit" + str(bit), "!bit" + str(bit)])

        json_structure = json.dumps(current_advancement, indent=4)
        loaded_advancement.write(json_structure)