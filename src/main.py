import json
import random
import requests
import os
from datetime import datetime

def fetch_ips():
    try:
        response = requests.get('https://raw.githubusercontent.com/ircfspace/endpoint/refs/heads/main/ip.json')
        data = response.json()
        return data
    except Exception as e:
        # اگر دریافت IP با خطا مواجه شد، از IP های پیش‌فرض استفاده می‌کنیم
        return {
            "ipv4": ["162.159.192.23:859", "162.159.192.178:4500"],
            "ipv6": ["[2606:4700:d1::9f62:b405:88e4:858e]:7152"]
        }

def generate_config(ip_port, index, ip_version):
    base = f"warp://{ip_port}/?ifp=50-100&ifps=50-100&ifpd=3-6&ifpm=m4&&detour=warp://{ip_port}/?ifp=50-100&ifps=50-100&ifpd=3-6&ifpm=m4#Anon-WoW-{ip_version}🇩🇪-{index}"
    return base

def update_config_file():
    # خواندن قالب از فایل
    with open('src/templates/config_template.txt', 'r', encoding='utf-8') as f:
        template = f.read()

    # دریافت IP ها
    ips = fetch_ips()
    
    # انتخاب تصادفی IP ها
    ipv4_list = random.sample(ips['ipv4'], 2)
    ipv6 = random.choice(ips['ipv6'])
    
    # ساخت کانفیگ‌ها
    configs = []
    configs.append(generate_config(ipv4_list[0], 1, "IPv4"))
    configs.append(generate_config(ipv4_list[1], 2, "IPv4"))
    configs.append(generate_config(ipv6, 3, "IPv6"))
    
    # ترکیب قالب و کانفیگ‌ها
    final_config = template + "\n\n" + "\n\n".join(configs)
    
    # ذخیره در فایل
    with open('config.txt', 'w', encoding='utf-8') as f:
        f.write(final_config)

if __name__ == "__main__":
    update_config_file()
