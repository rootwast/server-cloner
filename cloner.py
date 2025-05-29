import requests
import json
import time

API = "https://discord.com/api/v10"

def headers(token):
    return {
        "Authorization": token,
        "Content-Type": "application/json"
    }

def get_roles(guild_id, token):
    url = f"{API}/guilds/{guild_id}/roles"
    r = requests.get(url, headers=headers(token))
    if r.status_code == 200:
        roles = r.json()
        return sorted(roles, key=lambda r: r['position'])
    else:
        print(f"Rol alma hatası: {r.status_code} {r.text}")
        return None

def create_role(guild_id, token, role_data):
    url = f"{API}/guilds/{guild_id}/roles"
    r = requests.post(url, headers=headers(token), data=json.dumps(role_data))
    if r.status_code in (200, 201):
        return r.json()
    else:
        print(f"Rol oluşturma hatası: {r.status_code} {r.text}")
        return None

def get_channels(guild_id, token):
    url = f"{API}/guilds/{guild_id}/channels"
    r = requests.get(url, headers=headers(token))
    if r.status_code == 200:
        return r.json()
    else:
        print(f"Kanal alma hatası: {r.status_code} {r.text}")
        return None

def create_channel(guild_id, token, channel_data):
    url = f"{API}/guilds/{guild_id}/channels"
    r = requests.post(url, headers=headers(token), data=json.dumps(channel_data))
    if r.status_code in (200, 201):
        return r.json()
    else:
        print(f"Kanal oluşturma hatası: {r.status_code} {r.text}")
        return None

def copy_roles(token, source_guild_id, target_guild_id):
    print("Roller kopyalanıyor...")
    roles = get_roles(source_guild_id, token)
    if roles is None:
        print("Rol alma başarısız!")
        return None

    role_map = {}
    for role in roles:
        if role['name'] == "@everyone":
            continue  # Everyone rolünü atla
        role_data = {
            "name": role['name'],
            "permissions": role['permissions'],
            "color": role['color'],
            "hoist": role['hoist'],
            "mentionable": role['mentionable']
        }
        created_role = create_role(target_guild_id, token, role_data)
        if created_role:
            role_map[role['id']] = created_role['id']
            print(f"Rol oluşturuldu: {role['name']}")
        else:
            print(f"Rol oluşturulamadı: {role['name']}")
        time.sleep(3)
    return role_map

def copy_channels(token, source_guild_id, target_guild_id, role_map):
    print("Kanallar kopyalanıyor...")
    channels = get_channels(source_guild_id, token)
    if channels is None:
        print("Kanal alma başarısız!")
        return

    categories = [c for c in channels if c['type'] == 4]
    others = [c for c in channels if c['type'] != 4]

    category_map = {}

    for cat in categories:
        cat_data = {
            "name": cat['name'],
            "type": 4,
            "permission_overwrites": []
        }
        created_cat = create_channel(target_guild_id, token, cat_data)
        if created_cat:
            category_map[cat['id']] = created_cat['id']
            print(f"Kategori oluşturuldu: {cat['name']}")
        else:
            print(f"Kategori oluşturulamadı: {cat['name']}")
        time.sleep(3)
      
    for ch in others:
        ch_data = {
            "name": ch['name'],
            "type": ch['type'],
            "topic": ch.get('topic'),
            "bitrate": ch.get('bitrate'),
            "user_limit": ch.get('user_limit'),
            "rate_limit_per_user": ch.get('rate_limit_per_user', 0),
            "permission_overwrites": [],
            "parent_id": category_map.get(ch.get('parent_id'))
        }
        created_ch = create_channel(target_guild_id, token, ch_data)
        if created_ch:
            print(f"Kanal oluşturuldu: {ch['name']}")
        else:
            print(f"Kanal oluşturulamadı: {ch['name']}")
        time.sleep(3)

def main():
    print("Discord Kullanıcı Tokeninizi Girin:")
    token = input("> ").strip()
    print("Kopyalanacak (Kaynak) Sunucu ID'sini Girin:")
    source = input("> ").strip()
    print("Yapıştırılacak (Hedef) Sunucu ID'sini Girin:")
    target = input("> ").strip()

    role_map = copy_roles(token, source, target)
    if role_map is None:
        print("Rol kopyalama başarısız, işlem durduruldu.")
        return

    copy_channels(token, source, target, role_map)

    print("\033[38;2;255;0;255m★ Made by Wast ★\033[0m")

if __name__ == "__main__":
    main()
