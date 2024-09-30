import requests
import time
import sys
import os


STEAM_API_KEY = 'YOUR_STEAM_API_KEY'

# 包装
def print_separator(char='-', length=50):
    print(char * length)


def fancy_input(prompt):
    print_separator()
    user_input = input(f"{prompt} > ").strip()
    print_separator()
    return user_input

# 输出
def fancy_print(label, value, label_width=10):
    print(f"{label.ljust(label_width)}: {value}")

def get_server_info(server_ip, server_port, proxies=None):
    # 查询服务器信息的URL
    url = f"https://api.steampowered.com/IGameServersService/GetServerList/v1/?key={STEAM_API_KEY}&filter=\\addr\\{server_ip}:{server_port}"

    try:
        response = requests.get(url, timeout=10, proxies=proxies)  # 设置代理
        if response.status_code == 200:
            data = response.json()
            servers = data.get('response', {}).get('servers', [])
            if servers:
                server_info = servers[0]
                print("\n服务器信息查询成功！\n")
                print_separator('=')
                fancy_print("服务器名称", server_info.get('name'))
                fancy_print("玩家人数", f"{server_info.get('players')}/{server_info.get('max_players')}")
                fancy_print("地图", server_info.get('map'))
                fancy_print("游戏模式", server_info.get('game_descr'))
                print_separator('=')
            else:
                print("\n未找到该服务器信息，请检查IP和端口是否正确。\n")
        else:
            print(f"\n请求失败，错误代码: {response.status_code}\n")
    except requests.exceptions.Timeout:
        print("\n请求超时，请检查网络连接或稍后重试。\n")
    except requests.exceptions.RequestException as e:
        print(f"\n发生请求错误: {str(e)}\n")
    except Exception as e:
        print(f"\n发生未知错误: {str(e)}\n")

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

if __name__ == "__main__":
    clear_console()
    print_separator('=')
    print(" 欢迎使用测试查询工具 ")
    print_separator('=')

    # 提示用户输入服务器IP和端口
    server_ip = fancy_input("输入服务器IP")
    server_port = fancy_input("输入服务器端口")

    if not server_ip or not server_port:
        print("\n输入无效，程序将退出。")
        sys.exit(1)

    # 输入查询间隔
    while True:
        try:
            query_interval = float(fancy_input("请输入查询间隔时间（秒）"))
            if query_interval <= 0:
                print("\n查询间隔必须为正数，请重新输入。")
            else:
                break
        except ValueError:
            print("\n输入无效，请输入一个数字。")

    # 输入代理
    proxy_ip = fancy_input("请输入代理IP地址（留空则不使用代理）")
    proxy_port = fancy_input("请输入代理端口（留空则不使用代理）")

    # 检查代理输入
    if proxy_ip and proxy_port:
        proxies = {
            "http": f"http://{proxy_ip}:{proxy_port}",
            "https": f"http://{proxy_ip}:{proxy_port}"
        }
        print("\n已启用代理设置。\n")
    else:
        proxies = None
        print("\n未启用代理，将使用本地IP进行查询。\n")

    # 循环查询服务器信息
    try:
        while True:
            get_server_info(server_ip, server_port, proxies=proxies)
            print(f"\n将在 {query_interval} 秒后再次查询...")
            time.sleep(query_interval)
    except KeyboardInterrupt:
        print("\n查询已停止！")
        print_separator('=')
