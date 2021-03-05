# Entity id and Hit Detection System

## General 
This is a utility made to identify entities, and run functions when a player hits an entity or when an entity hits a player.

## IDs
This system assigns an id to every entity not in the entity tag `#entityid:id_skip`. IDs are stored in the scoreboard `entityid` as well as bit by bit in scoreboards `entityid.<0..15>` and in the entities `Tags`, where it is scored in tags in the format `entityid.<0..15>.[0|1]`. 

Projectiles gain the ID of their owner, projectiles are determined with the #entityid:projectile tag. 

## Use

### Enabling/Disabling listening
For performance reasons, this system does not run unless it is enabled. 

To enable listening for `entity_hurt_player` you add 1 to the score `ehp_listen`, and to stop listening, remove 1 from the score `ehp_listen`

To enable listening for `player_hurt_entity` you add 1 to the score `phe_listen`, and to stop listening, remove 1 from the score `phe_listen`

The reason for this is to allow multiple systems to easily enable/disable listening without having to know if it was listening previously. 

### Using the triggers
If the system is currently listening some function tags will be called when triggered. These function tags are listed below. (these function tags are in the minecraft namespace)

> `#player_hurt_entity/as_entity`	| runs as the entity that was hit by the player before any player handling happens

> `#player_hurt_entity/as_attacker`	| runs as the player when they attack an entity

> `#player_hurt_entity/as_receiver`	| runs as the entity that was hit by the player

> `#entity_hurt_player/as_entity`	| runs as the entity that hit the player before any player handling happens

> `#entity_hurt_player/as_receiver`	| runs as the player when hit by an entity

> `#entity_hurt_player/as_attacker`	| runs as the entity that hit the player

Before these function tags are run, the attacker and receiver are tagged with `entityid.[attacker|receiver]`. If the trigger is `entity_hurt_player` and the damage type is `is_projectile`, all projectiles within 8 blocks that are owned by the attacker will receive the tag `entityid.attacker.projectile`

When the tags are run, it will run everything in the tags, so you need something in your system that tracks if it is listening.

### Detecting damage types

This system also tracks the type of damage that the player received, you can check for damage type with a selector.

`[advancements={entityid:[entity_hurt_player|player_hurt_entity]={<type>=true}}]`

The Types of damage you can detect are 

> `typeless` | true if none other are

> `bypasses_armor` | damage types that ignore armor
  
> `is_explosion` | explosive damage
  
> `is_fire` | fire damage
  
> `is_magic` | magic damage, effects mostly
  
> `is_projectile` | projectiles 
  
> `is_lightning` | lightning
  
> `bypasses_invulnerability` | void
  
> `bypasses_magic` | starvation
