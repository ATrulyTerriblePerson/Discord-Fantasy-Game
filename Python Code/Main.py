import discord
from discord.ext import commands
from discord.ui import Button, View, Select, TextInput, Modal
from discord import app_commands
import json
import os
import asyncio
import random
import glob
import traceback



def initialize_items_file():
    # Define the path for the items.json file
    items_path = r'C:\Users\docto\PycharmProjects\Discord-Fantasy-Game\DnD\items.json'

    # Check if the items.json file already exists
    if not os.path.exists(items_path):
        # Define the base items to be added
        base_items = {
            "materials": [
                {"name": "Iron", "base_price": 10},
                {"name": "Coal", "base_price": 5},
                {"name": "Sturdy Stick", "base_price": 3}
            ],
            "potions": [
                {"name": "Lower Potion of Restoration", "quantity": 1, "base_price": 20}
            ]
        }

        # Write the base items to the file
        with open(items_path, 'w') as file:
            json.dump(base_items, file, indent=4)

        print("items.json created with base items.")
    else:
        print("items.json already exists.")


# Call the function to ensure items.json is initialized
initialize_items_file()



# Define the path for the Armour.json file
armour_file_path = r'C:\Users\docto\PycharmProjects\Discord-Fantasy-Game\DnD\Armour.json'

# Define the default level 0 armor
default_armour = {
    "Leather Helmet": {
        "level": 0,
        "defense": "1d4",
        "cost": 10,
        "description": "A basic leather helmet, offering minimal protection.",
        "durability": 50,
        "debuffs": []
    },
    "Rusty Shield": {
        "level": 0,
        "defense": "1d6",
        "cost": 15,
        "description": "An old shield, rusted but still functional.",
        "durability": 30,
        "debuffs": ["rusty"]
    },
    "Scrap Chestplate": {
        "level": 0,
        "defense": "1d8",
        "cost": 20,
        "description": "A chestplate made from scrap metal, not very reliable.",
        "durability": 40,
        "debuffs": ["heavy"]
    },
    "Worn Gauntlets": {
        "level": 0,
        "defense": "1d2",
        "cost": 5,
        "description": "Gauntlets showing signs of heavy use.",
        "durability": 20,
        "debuffs": ["tetanus"]
    },
    "Old Boots": {
        "level": 0,
        "defense": "1d3",
        "cost": 8,
        "description": "Boots with worn-out soles, providing minimal protection.",
        "durability": 25,
        "debuffs": []
    },
    "Patchwork Leggings": {
        "level": 0,
        "defense": "1d5",
        "cost": 12,
        "description": "Leggings patched together from various scraps.",
        "durability": 30,
        "debuffs": []
    }
}

# Check if the file exists
if not os.path.exists(armour_file_path):
    # Create the file with the default armor
    with open(armour_file_path, 'w') as file:
        json.dump(default_armour, file, indent=4)
    print("Armour.json file created with default level 0 armor.")
else:
    print("Armour.json file already exists.")

# Correct file paths for abilities
mana_abilities_path = r'C:\Users\docto\PycharmProjects\Discord-Fantasy-Game\DnD\Mana_Abilities.json'
stamina_abilities_path = r'C:\Users\docto\PycharmProjects\Discord-Fantasy-Game\DnD\Stamina_Abilities.json'

# Load the abilities from the correct paths
with open(mana_abilities_path, 'r') as mana_file:
    mana_abilities = json.load(mana_file)

with open(stamina_abilities_path, 'r') as stamina_file:
    stamina_abilities = json.load(stamina_file)


# Check and create role.json if it doesn't exist
def check_and_create_role_file():
    role_file_path = r'C:\Users\docto\PycharmProjects\Discord-Fantasy-Game\DnD\role.json'
    if not os.path.exists(role_file_path):
        default_role = {
            "Paladin": {
                "description": "A noble warrior with a funny sense of humor.",
                "benefits": "Can only use Axe, Sword & Shield."
            }
        }
        with open(role_file_path, 'w') as f:
            json.dump(default_role, f, indent=4)

# Check and create weapons.json if it doesn't exist
def check_and_create_weapons_file():
    weapons_file_path = r'C:\Users\docto\PycharmProjects\Discord-Fantasy-Game\DnD\weapons.json'
    if not os.path.exists(weapons_file_path):
        default_weapons = {
            "Rusty Iron Sword": {
                "level": 0,
                "damage": "1d4",
                "description": "An old and rusty sword, barely sharp."
            },
            "Grandfather's Hunting Bow": {
                "level": 0,
                "damage": "1d6",
                "description": "A bow passed down through generations, still functional."
            },
            "Woodcutting Axe": {
                "level": 0,
                "damage": "1d6",
                "description": "An axe used for chopping wood, now repurposed for battle."
            },
            "Bendy Spear": {
                "level": 0,
                "damage": "1d4",
                "description": "A spear that bends slightly, not very reliable."
            }
        }
        with open(weapons_file_path, 'w') as f:
            json.dump(default_weapons, f, indent=4)

# Load roles from role.json
def load_roles():
    role_file_path = r'C:\Users\docto\PycharmProjects\Discord-Fantasy-Game\DnD\role.json'
    with open(role_file_path, 'r') as f:
        roles = json.load(f)
    return list(roles.keys())

# Load weapons from weapons.json
def load_weapons():
    weapons_file_path = r'C:\Users\docto\PycharmProjects\Discord-Fantasy-Game\DnD\weapons.json'
    with open(weapons_file_path, 'r') as f:
        weapons = json.load(f)
    return list(weapons.keys())

# Load base height from races.json
def load_base_height(race):
    races_file_path = r'C:\Users\docto\PycharmProjects\Discord-Fantasy-Game\DnD\races.json'
    with open(races_file_path, 'r') as f:
        races = json.load(f)
    return races[race]['base_height']

# Generate random height
def generate_random_height(base_height):
    return base_height + random.randint(-10, 10)


def add_item_to_inventory(character, item_name, quantity=1):
    # Define the path for the items.json file
    items_path = r'C:\Users\docto\PycharmProjects\Discord-Fantasy-Game\DnD\items.json'

    # Load the items data
    with open(items_path, 'r') as file:
        items_data = json.load(file)

    # Determine where to add the item
    item_added = False
    for category in ['materials', 'potions']:
        for item in items_data[category]:
            if item['name'] == item_name:
                if category not in character['inventory']:
                    character['inventory'][category] = []

                # Check if the item already exists in the inventory
                existing_item = next((i for i in character['inventory'][category] if i['name'] == item_name), None)
                if existing_item:
                    existing_item['quantity'] += quantity
                else:
                    character['inventory'][category].append({"name": item_name, "quantity": quantity})

                item_added = True
                break

        if item_added:
            break

    return item_added





















# Ensure the JSON files exist
check_and_create_role_file()
check_and_create_weapons_file()


# Default race data
default_race = {
    "name": "Human",
    "description": "Just a regular human with no special abilities, but a great sense of humor!",
    "attributes": {
        "base_health": 100,
        "base_damage": 10,
        "base_height": 170,
        "weaknesses": [],
        "strengths": []
    }
}

# Path to the races JSON file
races_file_path = r'C:\Users\docto\PycharmProjects\Discord-Fantasy-Game\DnD\races.json'

# Check if the races file exists, if not create it with the default race
if not os.path.exists(races_file_path):
    with open(races_file_path, 'w') as f:
        json.dump([default_race], f, indent=4)
else:
    # Ensure the file is not empty or corrupted
    try:
        with open(races_file_path, 'r') as f:
            races = json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        with open(races_file_path, 'w') as f:
            json.dump([default_race], f, indent=4)

class RaceSelect(Select):
    def __init__(self):
        options = [discord.SelectOption(label=race['name'], description=race['description']) for race in races]
        super().__init__(placeholder='Choose your race...', min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        selected_race = self.values[0]
        await interaction.response.send_message(f'You selected: {selected_race}')




















def save_character(user_id, character_data):
    file_path = f'{user_id}_character_file.json'
    with open(file_path, 'w') as f:
        json.dump(character_data, f)

# Example usage
character_data = {
    'name': 'Aragorn',
    'race': 'Human',
    'role': 'Ranger',
    # Add other attributes here
}
save_character(user_id='123456789', character_data=character_data)



# Initialize bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)
intents = discord.Intents.default()
intents.members = True  # Enable member intents
intents.presences = True  # Enable presence intents

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    update_character_map()
    print("Bot is ready and character map is updated.")





async def is_in_town(ctx):
    # Check if the command is used in the correct category and channel
    if ctx.channel.category and ctx.channel.category.name == 'D&D Adventure' and ctx.channel.name == 'town-of-beginnings':
        return True
    await ctx.send('This command can only be used in the "town-of-beginnings" channel within the "D&D Adventure" category.')
    return False


#Creates roles, channels and etc for the Dungeons and Dragons game.
@bot.command()
async def DnD(ctx):
    guild = ctx.guild
    category_name = "D&D Adventure"
    channel_name = "town-of-beginnings"
    player_role_name = "D&D Player"
    gm_role_name = "Game Master"
    channel_ch_name = "character-channel"

    # Check if the category already exists
    category = discord.utils.get(guild.categories, name=category_name)
    if not category:
        category = await guild.create_category(category_name)
        await ctx.send(f'Category created: {category.name}')
    else:
        await ctx.send(f'Category already exists: {category.name}')

    # Check if the channel already exists within the category
    channel = discord.utils.get(category.text_channels, name=channel_name)
    if not channel:
        channel = await guild.create_text_channel(channel_name, category=category)
        await ctx.send(f'Channel created: {channel.name}')
    else:
        await ctx.send(f'Channel already exists: {channel.name}')

    # Check if the channel already exists within the category
    channel = discord.utils.get(category.text_channels, name=channel_ch_name)
    if not channel:
        channel = await guild.create_text_channel(channel_ch_name, category=category)
        await ctx.send(f'Channel created: {channel_ch_name}')
    else:
        await ctx.send(f'Channel already exists: {channel_ch_name}')

    # Check if the roles already exist
    player_role = discord.utils.get(guild.roles, name=player_role_name)
    if not player_role:
        player_role = await guild.create_role(name=player_role_name)
        await ctx.send(f'Role created: {player_role.name}')
    else:
        await ctx.send(f'Role already exists: {player_role.name}')

    gm_role = discord.utils.get(guild.roles, name=gm_role_name)
    if not gm_role:
        gm_role = await guild.create_role(name=gm_role_name)
        await ctx.send(f'Role created: {gm_role.name}')
    else:
        await ctx.send(f'Role already exists: {gm_role.name}')

    # Set permissions for the category
    overwrite = {
        guild.default_role: discord.PermissionOverwrite(read_messages=False),
        player_role: discord.PermissionOverwrite(read_messages=True),
        gm_role: discord.PermissionOverwrite(read_messages=True, manage_channels=True, manage_roles=True)
    }
    await category.edit(overwrites=overwrite)
    await ctx.send(f'Permissions set for category: {category.name}')


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

# Check if the command is in the correct category and channel
def is_in_dnd_channel(ctx):
    return ctx.channel.name == 'character-channel' and ctx.channel.category.name == 'D&D Adventure'







# Load JSON data
def load_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

weapons = load_json(r'C:\Users\docto\PycharmProjects\Discord-Fantasy-Game\DnD\weapons.json')
races = load_json(r'C:\Users\docto\PycharmProjects\Discord-Fantasy-Game\DnD\races.json')
roles = load_json(r'C:\Users\docto\PycharmProjects\Discord-Fantasy-Game\DnD\role.json')


# Assume the following global variables are set correctly
weapons = load_json(r'C:\Users\docto\PycharmProjects\Discord-Fantasy-Game\DnD\weapons.json')
races = load_json(r'C:\Users\docto\PycharmProjects\Discord-Fantasy-Game\DnD\races.json')


@bot.command()
async def character(ctx, action=None):
    if not is_in_dnd_channel(ctx):
        await ctx.send("This command can only be used in the 'D&D Adventure' category and 'character-channel'.")
        return

    if action is None:
        # Show options using buttons
        actions = ['Create', 'Edit', 'Delete', 'List']
        buttons = [discord.ui.Button(label=action, style=discord.ButtonStyle.primary, custom_id=action.lower()) for action in actions]

        async def action_callback(interaction):
            selected_action = interaction.data['custom_id']
            print(f'Button clicked by user: {interaction.user.id}, selected action: {selected_action}')
            await interaction.response.defer()
            if selected_action == "create":
                await create_character(ctx)
            elif selected_action == "edit":
                await edit_character(ctx)
            elif selected_action == "delete":
                await delete_character(ctx)
            elif selected_action == "list":
                await list_characters(ctx)

        view = discord.ui.View(timeout=None)
        for button in buttons:
            button.callback = action_callback
            view.add_item(button)

        await ctx.send("Choose an action:", view=view)
        return

async def create_character(ctx):
    await ctx.send("Please enter the name of your character:")

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    try:
        msg = await bot.wait_for('message', check=check, timeout=60)
        character_name = msg.content
        print(f"Character name provided: {character_name}")

        # Check if character already exists for this user
        user_id = ctx.author.id
        file_path = r'C:\Users\docto\PycharmProjects\Discord-Fantasy-Game\DnD\{user_id}_character_{character_name}.json'

        if os.path.exists(file_path):
            await ctx.send(f"A character with the name '{character_name}' already exists. Do you want to overwrite it? (yes/no)")
            confirmation = await bot.wait_for('message', check=check, timeout=60)
            print(f"Overwrite confirmation: {confirmation.content.lower()}")
            if confirmation.content.lower() != 'yes':
                await ctx.send("Character creation cancelled.")
                return

        await ctx.send(f"Character name: {character_name}. Are you sure? (yes/no)")

        confirmation = await bot.wait_for('message', check=check, timeout=60)
        print(f"Final confirmation: {confirmation.content.lower()}")
        if confirmation.content.lower() != 'yes':
            await ctx.send("Character creation cancelled.")
            return

        # Prepare options from dictionaries
        race_options = [discord.SelectOption(label=race['name'], value=race['name']) for race in races]
        role_options = [discord.SelectOption(label=role, value=role) for role in roles]
        weapon_options = [discord.SelectOption(label=weapon, value=weapon) for weapon, details in weapons.items() if details['level'] == 0]
        gender_options = [
            discord.SelectOption(label="Male", value="Male"),
            discord.SelectOption(label="Female", value="Female"),
            discord.SelectOption(label="Other", value="Other"),
        ]

        # Create dropdown menus for Race, Role, Weapon, and Gender
        race_select = discord.ui.Select(placeholder="Choose your race", options=race_options)
        role_select = discord.ui.Select(placeholder="Choose your role", options=role_options)
        weapon_select = discord.ui.Select(placeholder="Choose your weapon", options=weapon_options)
        gender_select = discord.ui.Select(placeholder="Choose your gender", options=gender_options)

        # Initialize selections
        selected_race = None
        selected_role = None
        selected_weapon = None
        selected_gender = None

        async def race_callback(interaction):
            nonlocal selected_race
            selected_race = interaction.data['values'][0]
            print(f"Race selected: {selected_race}")
            await interaction.response.send_message(f"Selected race: {selected_race}")

        async def role_callback(interaction):
            nonlocal selected_role
            selected_role = interaction.data['values'][0]
            print(f"Role selected: {selected_role}")
            await interaction.response.send_message(f"Selected role: {selected_role}")

        async def weapon_callback(interaction):
            nonlocal selected_weapon
            selected_weapon = interaction.data['values'][0]
            print(f"Weapon selected: {selected_weapon}")
            await interaction.response.send_message(f"Selected weapon: {selected_weapon}")

        async def gender_callback(interaction):
            nonlocal selected_gender
            selected_gender = interaction.data['values'][0]
            print(f"Gender selected: {selected_gender}")
            await interaction.response.send_message(f"Selected gender: {selected_gender}")

        # Set callbacks
        race_select.callback = race_callback
        role_select.callback = role_callback
        weapon_select.callback = weapon_callback
        gender_select.callback = gender_callback

        # Create and send view
        view = discord.ui.View(timeout=None)
        view.add_item(race_select)
        view.add_item(role_select)
        view.add_item(weapon_select)
        view.add_item(gender_select)

        await ctx.send("Choose your character's race, role, weapon, and gender:", view=view)

        # Wait for all selections
        while not (selected_race and selected_role and selected_weapon and selected_gender):
            await asyncio.sleep(1)  # Check every second

        # Get race attributes
        race_data = next(race for race in races if race['name'] == selected_race)
        base_health = race_data['attributes']['base_health']
        base_height = race_data['attributes']['base_height']
        height = random.randint(base_height - 10, base_height + 10)
        manamax = race_data['attributes']['manamax']
        mana = random.randint(0, manamax)
        stamina = race_data['attributes']['stamina']
        undead = race_data['attributes']['undead']
        baseability = race_data['attributes']['baseability']

        # Determine ability
        selected_ability = None
        if random.random() < baseability:
            if random.choice(["mana", "stamina"]) == "mana":
                # Choose a random mana ability
                selected_ability = random.choice(list(mana_abilities.keys()))
                print(f"Mana ability selected: {selected_ability}")
            else:
                # Choose a random stamina ability, ensuring it's compatible with the race
                compatible_stamina_abilities = [
                    ability for ability, details in stamina_abilities.items()
                    if 'race' not in details or details['race'] == selected_race
                ]
                if compatible_stamina_abilities:
                    selected_ability = random.choice(compatible_stamina_abilities)
                    print(f"Stamina ability selected: {selected_ability}")

        # Save character details after all selections are made
        character_details = {
            "name": character_name,
            "level": 0,
            "race": selected_race,
            "role": selected_role,
            "equipped": {
                "helmet": None,
                "shield": None,
                "chestplate": None,
                "gauntlets": None,
                "boots": None,
                "leggings": None,
                "weapon": selected_weapon
            },
            "inventory": {
                "helmet": [],
                "shield": [],
                "chestplate": [],
                "gauntlets": [],
                "boots": [],
                "leggings": [],
                "weapon": [],
                "potions": [
                    {"name": "Lower Potion of Restoration", "quantity": 1}
                ],
                "materials": [],
                "misc": []
            },
            "health": base_health,
            "height": height,
            "gender": selected_gender,
            "mana": mana,
            "stamina": stamina,
            "undead": undead,
            "abilities": {},
            "gold": 100,
            "wanted": False,
            "xp": 0,
            "kills": 0
        }

        try:
            with open(file_path, 'w') as file:
                json.dump(character_details, file, indent=4)
            print(f"Character saved to {file_path}")
        except Exception as e:
            print(f"Error saving character: {e}")
            await ctx.send("There was an error saving your character. Please try again.")

        embed = discord.Embed(title=character_name, description="Character Details")
        embed.add_field(name="Level", value=character_details["level"])
        embed.add_field(name="Race", value=character_details["race"])
        embed.add_field(name="Role", value=character_details["role"])
        embed.add_field(name="Weapon", value=character_details["equipped"]["weapon"])
        embed.add_field(name="Health", value=character_details["health"])
        embed.add_field(name="Height", value=character_details["height"])
        embed.add_field(name="Gender", value=character_details["gender"])
        embed.add_field(name="Mana", value=character_details["mana"])
        embed.add_field(name="Stamina", value=character_details["stamina"])
        embed.add_field(name="Abilities", value=", ".join(character_details["abilities"].keys()) or "None")
        embed.add_field(name="Gold", value=character_details["gold"])
        embed.add_field(name="XP", value=character_details["xp"])
        embed.add_field(name="Kills", value=character_details["kills"])

        await ctx.send(embed=embed)

    except asyncio.TimeoutError:
        print("Character creation timed out.")
        await ctx.send("Character creation timed out. Please try again.")
    except Exception as e:
        print(f"Unexpected error during character creation: {e}")
        await ctx.send("An unexpected error occurred. Please try again.")







async def edit_character(ctx):
    await ctx.send("Character editing not yet implemented.")

async def delete_character(ctx):
    await ctx.send("Character deletion not yet implemented.")

async def list_characters(ctx):
    await ctx.send("Character listing not yet implemented.")



# Load weapon data
with open(r'C:\Users\docto\PycharmProjects\Discord-Fantasy-Game\DnD\weapons.json', 'r') as file:
    weapons_data = json.load(file)


# Command to access the shop
@bot.command(name='shop', aliases=['store'])
@commands.check(is_in_town)
async def shop(ctx):
    user_id = ctx.author.id
    character_files = glob.glob(r'C:\Users\docto\PycharmProjects\Discord-Fantasy-Game\DnD{user_id}_character_*.json')

    if not character_files:
        await ctx.send("You don't have any characters. Create one first.")
        return

    if len(character_files) == 1:
        selected_character_file = character_files[0]
        await show_store_options(ctx, selected_character_file)
    else:
        character_options = []
        for file in character_files:
            with open(file, 'r') as f:
                char = json.load(f)
            character_options.append(
                discord.SelectOption(
                    label=char['name'],
                    value=file,
                    description=f"Gold: {char['gold']}"
                )
            )

        select = discord.ui.Select(
            placeholder="Select your character",
            options=character_options
        )

        async def select_callback(interaction: discord.Interaction):
            selected_character_file = interaction.data['values'][0]
            await interaction.response.defer()
            await show_store_options(interaction, selected_character_file)

        select.callback = select_callback
        view = discord.ui.View()
        view.add_item(select)
        await ctx.send("Select a character to use:", view=view)

async def show_store_options(interaction: discord.Interaction, character_file):
    print("show_store_options called")

    # Load character file
    with open(character_file, 'r') as file:
        character = json.load(file)

    print("Character loaded:", character)

    # Define buttons
    buttons = [
        discord.ui.Button(label="Armor Store", style=discord.ButtonStyle.primary, custom_id="armor_store"),
        discord.ui.Button(label="Weapons Store", style=discord.ButtonStyle.primary, custom_id="weapons_store"),
        discord.ui.Button(label="Misc Store", style=discord.ButtonStyle.primary, custom_id="misc_store")
    ]

    async def button_callback(interaction: discord.Interaction):
        print("Button callback called")
        store_type = interaction.data['custom_id']
        print(f"Store type selected: {store_type}")

        if store_type == 'armor_store':
            await handle_armor_store(interaction, character, character_file)
        elif store_type == 'weapons_store':
            await handle_weapons_store(interaction, character, character_file)
        elif store_type == 'misc_store':
            await handle_misc_store(interaction, character, character_file)

    # Add button callbacks
    for button in buttons:
        button.callback = button_callback

    # Create and populate view
    view = discord.ui.View()
    for button in buttons:
        view.add_item(button)

    # Defer the interaction response if needed
    if not interaction.response.is_done():
        try:
            await interaction.response.defer()
        except Exception as e:
            print(f"Error deferring response: {e}")

    # Send message with buttons
    try:
        await interaction.followup.send("Choose a store to visit:", view=view)
        print("Message sent with buttons")
    except Exception as e:
        print(f"Error sending message with buttons: {e}")
# Update `select_callback` to ensure it handles interactions correctly
async def select_callback(interaction: discord.Interaction):
    selected_character_file = interaction.data['values'][0]

    # Ensure interaction is not already responded to
    if interaction.response.is_done():
        print("Interaction response already done")
        return

    # Call the function to show store options
    await show_store_options(interaction, selected_character_file)
async def handle_armor_store(interaction: discord.Interaction, character, character_file):
    armor_path = r'C:\Users\docto\PycharmProjects\Discord-Fantasy-Game\DnD\Armour.json'
    if not os.path.exists(armor_path):
        initialize_armour_file()

    with open(armor_path, 'r') as file:
        armor_data = json.load(file)

    available_armor = {
        name: details
        for name, details in armor_data.items()
        if details['level'] in [character['level'], character['level'] + 1, character['level'] - 1]
    }

    if not available_armor:
        await interaction.response.send_message("No armor available for your level.")
        return

    armor_options = [
        discord.SelectOption(label=name, value=name, description=f"Cost: {details.get('cost', 100)} gold")
        for name, details in available_armor.items()
    ]

    select = discord.ui.Select(
        placeholder="Choose an armor piece to buy",
        options=armor_options
    )

    async def select_callback(interaction: discord.Interaction):
        armor_name = interaction.data['values'][0]
        armor_details = available_armor[armor_name]
        price = armor_details.get('cost', 100)

        await interaction.response.send_message(f"Do you want to buy {armor_name} for {price} gold? Reply with 'yes' or 'no'.")

        def check(m):
            return m.author == interaction.user and m.channel == interaction.channel

        try:
            msg = await bot.wait_for('message', check=check, timeout=60)
            if msg.content.lower() == 'yes':
                if character['gold'] >= price:
                    character['gold'] -= price
                    armor_type = armor_details['type']
                    if armor_type in character['inventory']:
                        character['inventory'][armor_type].append({"name": armor_name, "quantity": 1})
                    else:
                        character['inventory'][armor_type] = [{"name": armor_name, "quantity": 1}]
                    with open(character_file, 'w') as file:
                        json.dump(character, file, indent=4)
                    await interaction.followup.send(f"You bought {armor_name} for {price} gold!")
                else:
                    await interaction.followup.send("You don't have enough gold.")
            else:
                await interaction.followup.send("Purchase cancelled.")
        except asyncio.TimeoutError:
            await interaction.followup.send("Purchase timed out.")

    select.callback = select_callback
    view = discord.ui.View()
    view.add_item(select)
    await interaction.response.send_message("Select an armor piece to purchase:", view=view)
async def handle_weapons_store(interaction: discord.Interaction, character, character_file):
    weapons_path = r'C:\Users\docto\PycharmProjects\Discord-Fantasy-Game\DnD\weapons.json'
    if not os.path.exists(weapons_path):
        await interaction.response.send_message("Weapons store data not found.")
        return

    with open(weapons_path, 'r') as file:
        weapons_data = json.load(file)

    available_weapons = {
        name: details
        for name, details in weapons_data.items()
        if details['level'] <= character['level'] + 1 and details['level'] >= character['level'] - 1
    }

    if not available_weapons:
        await interaction.response.send_message("No weapons available for your level.")
        return

    weapon_options = [
        discord.SelectOption(label=name, value=name, description=f"Price: {details.get('cost', 100)} gold")
        for name, details in available_weapons.items()
    ]

    select = discord.ui.Select(
        placeholder="Choose a weapon to buy",
        options=weapon_options
    )

    async def select_callback(interaction: discord.Interaction):
        weapon_name = interaction.data['values'][0]
        weapon_details = available_weapons[weapon_name]
        price = weapon_details.get('cost', 100)

        await interaction.response.send_message(f"Do you want to buy {weapon_name} for {price} gold? Reply with 'yes' or 'no'.")

        def check(m):
            return m.author == interaction.user and m.channel == interaction.channel

        try:
            msg = await bot.wait_for('message', check=check, timeout=60)
            if msg.content.lower() == 'yes':
                if character['gold'] >= price:
                    character['gold'] -= price
                    if 'inventory' not in character:
                        character['inventory'] = {category: [] for category in ['helmet', 'shield', 'chestplate', 'gauntlets', 'boots', 'leggings', 'weapon']}
                    character['inventory']['weapon'].append({"name": weapon_name, "quantity": 1})
                    with open(character_file, 'w') as file:
                        json.dump(character, file, indent=4)
                    await interaction.followup.send(f"You bought {weapon_name} for {price} gold!")
                else:
                    await interaction.followup.send("You don't have enough gold.")
            else:
                await interaction.followup.send("Purchase cancelled.")
        except asyncio.TimeoutError:
            await interaction.followup.send("Purchase timed out.")

    select.callback = select_callback
    view = discord.ui.View()
    view.add_item(select)
    await interaction.response.send_message("Select a weapon to purchase:", view=view)
async def handle_misc_store(interaction: discord.Interaction, character, character_file):
    items_path = r'C:\Users\docto\PycharmProjects\Discord-Fantasy-Game\DnD\items.json'
    if not os.path.exists(items_path):
        initialize_items_file()

    # Load items data
    with open(items_path, 'r') as file:
        items_data = json.load(file)

    # Debug: Print the loaded items data
    print("Loaded items data:")
    for category, items in items_data.items():
        print(f"Category: {category}")
        for item in items:
            print(
                f"  Item: {item['name']}, Base Price: {item.get('base_price', 'N/A')}, Quantity: {item.get('quantity', 'N/A')}")

    # Prepare available items for the Misc store
    available_items = {}
    for category, items in items_data.items():
        for item in items:
            if item.get('base_price') is not None:
                available_items[item['name']] = {
                    'category': category,
                    'base_price': item['base_price']
                }

    # Debug: Print available items for the store
    print("Available items for store:")
    for name, details in available_items.items():
        print(f"  Item: {name}, Base Price: {details.get('base_price', 'N/A')}")

    if not available_items:
        await interaction.response.send_message("No items available in the Misc store.")
        return

    # Create select options for items
    item_options = [
        discord.SelectOption(label=name, value=name, description=f"Price: {details.get('base_price', 10)} gold")
        for name, details in available_items.items()
    ]

    # Define select menu
    select = discord.ui.Select(
        placeholder="Choose an item to buy",
        options=item_options
    )

    async def select_callback(interaction: discord.Interaction):
        item_name = interaction.data['values'][0]
        item_details = available_items.get(item_name)
        if item_details is None:
            await interaction.response.send_message("Item not found.")
            return

        category = item_details['category']
        price = item_details['base_price']

        # Confirm purchase
        await interaction.response.send_message(
            f"Do you want to buy {item_name} for {price} gold? Reply with 'yes' or 'no' within 60 seconds.")

        def check(m):
            return m.author == interaction.user and m.channel == interaction.channel

        try:
            msg = await bot.wait_for('message', check=check, timeout=60)
            if msg.content.lower() == 'yes':
                if character['gold'] >= price:
                    character['gold'] -= price
                    if 'inventory' not in character:
                        character['inventory'] = {category: [] for category in
                                                  ['helmet', 'shield', 'chestplate', 'gauntlets', 'boots', 'leggings',
                                                   'weapon', 'potions', 'materials', 'misc']}

                    # Check if the item is already in the inventory
                    item_found = False
                    for item in character['inventory'][category]:
                        if item['name'] == item_name:
                            item['quantity'] += 1
                            item_found = True
                            break

                    if not item_found:
                        # Add new item if not found
                        character['inventory'][category].append({"name": item_name, "quantity": 1})

                    with open(character_file, 'w') as file:
                        json.dump(character, file, indent=4)
                    await interaction.followup.send(f"You bought {item_name} for {price} gold!")
                else:
                    await interaction.followup.send("You don't have enough gold.")
            else:
                await interaction.followup.send("Purchase cancelled.")
        except asyncio.TimeoutError:
            await interaction.followup.send("Purchase timed out.")

    select.callback = select_callback

    # Create and send view with the select menu
    view = discord.ui.View()
    view.add_item(select)
    await interaction.response.send_message("Select an item to purchase:", view=view)



@bot.command(name='inventory')
async def inventory(ctx):
    user_id = ctx.author.id
    character_files = glob.glob(r'C:\Users\docto\PycharmProjects\Discord-Fantasy-Game\DnD\{user_id}_character_*.json')

    if not character_files:
        await ctx.send("No characters found for this user.")
        return

    async def create_inventory_embed(character):
        embed = discord.Embed(
            title=character['name'],
            color=0x00ff00
        )
        embed.add_field(name="Level", value=character['level'], inline=True)
        embed.add_field(name="Gold", value=f"{character['gold']} gold", inline=True)
        embed.add_field(name="Gender", value=character['gender'], inline=True)
        embed.add_field(name="Race", value=character['race'], inline=True)
        embed.add_field(name="Kills", value=character['kills'], inline=True)

        return embed

    async def show_equipped_inventory(interaction, character):
        equipped = character.get('equipped', {})
        equipped_items = "\n".join(
            [f"{key.capitalize()}: {value if value else 'None'}" for key, value in equipped.items()])

        embed = await create_inventory_embed(character)
        embed.add_field(name="Equipped Items", value=equipped_items, inline=False)

        await interaction.response.edit_message(embed=embed)

    async def show_unequipped_inventory(interaction, character):
        inventory = character.get('inventory', {})
        unequipped_items = []

        # Loop through each category in the inventory
        for category, items in inventory.items():
            if isinstance(items, list) and items:
                if isinstance(items[0], dict):
                    item_list = ', '.join([f"{item['name']} (x{item['quantity']})" for item in items])
                else:
                    item_list = ', '.join(items)
            else:
                item_list = 'None'

            unequipped_items.append(f"{category.capitalize()}: {item_list}")

        unequipped_items_display = "\n".join(unequipped_items)

        embed = await create_inventory_embed(character)
        embed.add_field(name="Unequipped Items", value=unequipped_items_display, inline=False)

        await interaction.response.edit_message(embed=embed)

    for character_file in character_files:
        with open(character_file, 'r') as file:
            character = json.load(file)

        embed = await create_inventory_embed(character)

        # Create buttons for equipped and unequipped inventory views
        equipped_button = discord.ui.Button(label="Equipped Inventory", style=discord.ButtonStyle.primary)
        unequipped_button = discord.ui.Button(label="Unequipped Inventory", style=discord.ButtonStyle.secondary)

        async def equipped_callback(interaction):
            await show_equipped_inventory(interaction, character)

        async def unequipped_callback(interaction):
            await show_unequipped_inventory(interaction, character)

        equipped_button.callback = equipped_callback
        unequipped_button.callback = unequipped_callback

        view = discord.ui.View()
        view.add_item(equipped_button)
        view.add_item(unequipped_button)

        await ctx.send(embed=embed, view=view)





bot.run('TOKEN')
