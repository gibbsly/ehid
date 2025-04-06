import json
from os import path
from pathlib import Path

script = Path(__file__)
name, ext = path.splitext(path.basename(script))

ehid_dir = script.parents[1].absolute()
advancements_dir = path.join(ehid_dir, "entity_hit_detection/data/entityid/advancement")

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
    "mace_smash",
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
    "oak_boat",
    "spruce_boat",
    "birch_boat",
    "jungle_boat",
    "acacia_boat",
    "cherry_boat",
    "dark_oak_boat",
    "pale_oak_boat",
    "mangrove_boat",
    "bamboo_raft",
    "bogged",
    "breeze",
    "breeze_wind_charge",
    "camel",
    "cat",
    "cave_spider",
    "oak_chest_boat",
    "spruce_chest_boat",
    "birch_chest_boat",
    "jungle_chest_boat",
    "acacia_chest_boat",
    "cherry_chest_boat",
    "dark_oak_chest_boat",
    "pale_oak_chest_boat",
    "mangrove_chest_boat",
    "bamboo_chest_raft",
    "chest_minecart",
    "chicken",
    "cod",
    "command_block_minecart",
    "cow",
    "creaking",
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
    "splash_potion",
    "lingering_potion",
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


def player_killed_entity(entity):
    structure = {
        "trigger": "minecraft:player_killed_entity",
        "conditions": {
            "entity": [{"condition": "minecraft:entity_properties", "entity": "this", "predicate": {"type": entity}}]
        }
    }

    return structure


def ehid_advancement(id):
    structure = {
        "criteria": {
            "entity": {"trigger": "minecraft:" + id},
            "tagless": {
                "trigger": "minecraft:" + id,
                "conditions": {},
            }
        },
        "requirements": [
            ["entity"],
        ],
        "rewards": {"function": "entityid:" + id},
    }

    return structure


advancement_types = [
    "entity_hurt_player",
    "entity_killed_player",
    "player_hurt_entity",
    "player_killed_entity"
]

for advancement in advancement_types:
    with open(path.join(advancements_dir, advancement + ".json"), "w") as loaded_advancement:
        current_advancement = ehid_advancement(advancement)

        tagless_conditions = []
        tag_requirements = ["tagless"]
        for damage_type in damage_tags:
            tagless_conditions.append({"expected": False, "id": damage_type})
            current_advancement["criteria"][damage_type] = {
                    "trigger": "minecraft:" + advancement,
                    "conditions": {}
                }
            tag_requirements.append(damage_type)
        current_advancement["requirements"].append(tag_requirements)

        if (advancement == "entity_hurt_player") or (advancement == "player_hurt_entity"):
            for damage_type in damage_tags:
                current_advancement["criteria"][damage_type]["conditions"] = {"damage": {"type": {"tags": [{"expected": True, "id": damage_type}]}}}
            current_advancement["criteria"]["tagless"]["conditions"] = {"damage": {"type": {"tags": tagless_conditions}}}
        elif (advancement == "entity_killed_player") or (advancement == "player_killed_entity"):
            for damage_type in damage_tags:
                current_advancement["criteria"][damage_type]["conditions"] = {"killing_blow": {"tags": [{"expected": True, "id": damage_type}]}}
            current_advancement["criteria"]["tagless"]["conditions"] = {"killing_blow": {"tags": tagless_conditions}}

        if (advancement == "player_killed_entity"):
            entity_requirements = []
            for entity in entities:
                current_advancement["criteria"][entity] = player_killed_entity(entity)
                entity_requirements.append(entity)
            current_advancement["requirements"].append(entity_requirements)

        for bit in range(num_bits):
            if (advancement == "entity_hurt_player"):
                current_advancement["criteria"]["bit" + str(bit)] = {
                    "trigger": "minecraft:" + advancement,
                    "conditions": {
                        "damage": {"source_entity": {"nbt": "{Tags:[entityid." + str(bit) + ".1]}"}}
                    }
                }
                current_advancement["criteria"]["!bit" + str(bit)] = {
                    "trigger": "minecraft:" + advancement,
                    "conditions": {
                        "damage": {"source_entity": {"nbt": "{Tags:[entityid." + str(bit) + ".0]}"}}
                    }
                }
            elif (advancement == "entity_killed_player"):
                current_advancement["criteria"]["bit" + str(bit)] = {
                    "trigger": "minecraft:" + advancement,
                    "conditions": {
                        "killing_blow": {"source_entity": {"nbt": "{Tags:[entityid." + str(bit) + ".1]}"}}
                    }
                }
                current_advancement["criteria"]["!bit" + str(bit)] = {
                    "trigger": "minecraft:" + advancement,
                    "conditions": {
                        "killing_blow": {"source_entity": {"nbt": "{Tags:[entityid." + str(bit) + ".0]}"}}
                    }
                }
            elif (advancement == "player_hurt_entity") or (advancement == "player_killed_entity"):
                current_advancement["criteria"]["bit" + str(bit)] = {
                    "trigger": "minecraft:" + advancement,
                    "conditions": {
                        "entity": {"nbt": "{Tags:[entityid." + str(bit) + ".1]}"}
                    }
                }
                current_advancement["criteria"]["!bit" + str(bit)] = {
                    "trigger": "minecraft:" + advancement,
                    "conditions": {
                        "entity": {"nbt": "{Tags:[entityid." + str(bit) + ".0]}"}
                    }
                }
            current_advancement["requirements"].append(["bit" + str(bit), "!bit" + str(bit)])

        json_structure = json.dumps(current_advancement, indent=4)
        loaded_advancement.write(json_structure)