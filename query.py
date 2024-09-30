import requests


STEAM_API_KEY = 'YOUR_STEAM_API_KEY'

def get_server_info(server_ip, server_port):
    # 查询服务器信息的URL
    url = f"https://api.steampowered.com/IGameServersService/GetServerList/v1/?key={STEAM_API_KEY}&filter=\\addr\\{server_ip}:{server_port}"

    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            servers = data.get('response', {}).get('servers', [])
            if servers:
                server_info = servers[0]
                print(f"服务器名称: {server_info.get('name')}")
                print(f"玩家人数: {server_info.get('players')}/{server_info.get('max_players')}")服务器 = data.get('响应', {}).get('服务器', [])
                print(f"地图: {server_info.get('map')}")
                print(f"游戏模式: {server_info.get('game_descr')}")
            else:
                print("未找到该服务器信息。请检查IP和端口。")
        else:
            print("请求失败，错误代码:", response.status_code)
    except Exception as e:
        print("发生错误:", str(e))

if __name__ == "__main__":
    # 提示用户输入服务器IP和端口
    server_ip = input("请输入服务器IP: ")
    server_port = input("请输入服务器端口: ")
    
    get_server_info(server_ip, server_port)
