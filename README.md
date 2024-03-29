# Entity id and Hit Detection System

## General 
This is a utility made to identify entities, and run functions when a player hits/kills an entity or when an entity hits/kills a player.

## IDs
This system assigns an id to every entity not in the entity tag [`#entityid:id_skip`](https://github.com/gibbsly/ehid/blob/main/entity_hit_detection/data/entityid/tags/entity_types/id_skip.json). IDs are stored in the scoreboard `entityid` and in the entities `Tags`, where it is scored in tags bit by bit in the format `entityid.<0..15>.[0|1]`. 

Projectiles gain the ID of their owner, projectiles are determined with the [`#entityid:projectile`](https://github.com/gibbsly/ehid/blob/main/entity_hit_detection/data/entityid/tags/entity_types/projectile.json) tag. 

## Use
### Enabling/Disabling listening
For performance reasons, this system does not run unless it is enabled. 

To enable listening for `entity_hurt_player` you **add** 1 to the score `ehp_listen`, and to stop listening, **remove** 1 from the score `ehp_listen`

To enable listening for `player_hurt_entity` you **add** 1 to the score `phe_listen`, and to stop listening, **remove** 1 from the score `phe_listen`

To enable listening for `entity_killed_player` you **add** 1 to the score `ekp_listen`, and to stop listening, **remove** 1 from the score `ekp_listen`

To enable listening for `player_killed_entity` you **add** 1 to the score `pke_listen`, and to stop listening, **remove** 1 from the score `pke_listen`

### If you are enabling or disabling the listen, please **ADD** or **REMOVE** 1 from the score, do ***NOT*** **SET**. The reason for this is to allow multiple systems to easily enable/disable listening without having to know if it was listening previously. If you set the score something can go wrong, the **INTENDED** use is for you to **ADD** and **REMOVE**.

### Using the triggers
If the system is currently listening some function tags will be called when triggered. These function tags are listed below. (these function tags are in the minecraft namespace)

> `#player_hurt_entity/as_entity`	| runs as the entity that was hit by the player before any player handling happens
>
> `#player_hurt_entity/as_attacker`	| runs as the player when they attack an entity
>
> `#player_hurt_entity/as_receiver`	| runs as the entity that was hit by the player

> `#entity_hurt_player/as_entity`	| runs as the entity that hit the player before any player handling happens
>
> `#entity_hurt_player/as_receiver`	| runs as the player when hit by an entity
>
> `#entity_hurt_player/as_attacker`	| runs as the entity that hit the player

> `#player_killed_entity/as_attacker`[*](https://github.com/gibbsly/ehid#player_killed_entity-usage)	| runs as the player when they kill an entity, there is no way to execute something as a dead entity so there are no other tags

> `#entity_killed_player/as_entity`		| runs as the entity that hit killed player before any player handling happens
>
> `#entity_killed_player/as_receiver`	| runs as the player when killed by an entity
>
> `#entity_killed_player/as_attacker`	| runs as the entity that killed the player

Before these function tags are run, the attacker and receiver are tagged with `entityid.[attacker|receiver]`. If the trigger is `entity_hurt_player` and the damage type is `is_projectile`, all projectiles within 8 blocks that are owned by the attacker will receive the tag `entityid.attacker.projectile`.

When the tags are run, it will run everything in the tags, so you need something in your system that tracks if it is listening.

### Detecting damage types
This system also tracks the type of damage that the player received, you can check for damage type with a selector.

`[advancements={entityid:[entity_hurt_player|player_hurt_entity|entity_killed_player|player_killed_entity]={<type>=true}}]`

The Types of damage you can detect are 

> `tagless` | true if none other are
>
> `<all vanilla damage type tags>` | `always_hurts_ender_dragons, always_most_significant_fall, always_triggers_silverfish, avoids_guardian_thorns, burns_armor_stands, bypasses_armor, bypasses_effects, bypasses_enchantments, bypasses_invulnerability, bypasses_resistance, bypasses_shield, damages_helmet, ignites_armor_stands, is_drowning, is_explosion, is_fall, is_fire, is_freezing, is_lightning, is_projectile, no_anger, no_impact, witch_resistant_to, wither_immune_to`

### `player_killed_entity` usage
If a player kills an entity and listening for "player_killed_entity" is enabled, the only thing this system can do is tell you the ID of the entity that the player killed was, as well as telling you the type of entity. 

The system currently checks 73 entity types, these types are listed in the tag ["#entityid:checked_by_player_killed_entity"](https://github.com/gibbsly/ehid/blob/main/entity_hit_detection/data/entityid/tags/entity_types/checked_by_player_killed_entity.json). This tag is purely informational, and is not used by the advancement. Detecting the type of entity that was killed uses an identical check to checking the damage type.

`[advancements={entityid:player_killed_entity={<type>=true}}]`

## Examples
I have provided an example in the [`example`](https://github.com/gibbsly/ehid/tree/main/entity_hit_detection/data/example) namespace. You can safely remove it. 

## Packaging 
The function `entityid:package` removes all IDs currently listed, and prevents the system from assigning new IDs until the next reload.

## Footnote
If you need this system to start listening in the same tick that you add to the listen score, I recommend enabling this datapack last. If you don't know what that means, you probably don't need to worry about it.
