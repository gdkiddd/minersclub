import requests
import json

# BscScan API 设置
BSC_API_KEY = "KIUQKQCQH7F3JZ9IS3SSYRV6DK2TU6B4WP"
ADDRESS = "0x197c60276D9D6342E887Fa15ad2aFf943FAC917C"  # 钱包地址
MBC_CONTRACT = "0x7D28276933D6aA0Ef1513F8B5e18dC492befeFea"  # MBC 代币合约地址
MBCUSDT_CONTRACT = "0x2d7c6794ef5a5234b26ba620c659c0913f4b0609"  # MBC/USDT 交易对合约地址
BSC_USD_CONTRACT = "0x55d398326f99059fF775485246999027B3197955"  # USDT 合约地址
API_URL = f"https://api.bscscan.com/api?module=account&action=tokentx&address={ADDRESS}&startblock=0&endblock=99999999&sort=asc&apikey={BSC_API_KEY}"
DEXSCREENER_URL = f"https://api.dexscreener.com/latest/dex/pairs/bsc/{MBCUSDT_CONTRACT}"

# 获取交易记录
def get_transactions():
    response = requests.get(API_URL)
    if response.status_code == 200:
        data = response.json()
        return data.get("result", [])
    return []

# 获取最新 MBC 价格（来自 DexScreener）
def get_latest_mbc_price():
    response = requests.get(DEXSCREENER_URL)
    if response.status_code == 200:
        data = response.json()
        pairs = data.get("pairs", [])
        if pairs:
            return float(pairs[0].get("priceUsd", 0))
    return -1

# 分析交易记录
def analyze_trades(transactions):
    total_buy_cost = 0  # 买入总花费
    total_buy_quantity = 0  # 买入总数量
    total_sell_revenue = 0  # 卖出总收入
    total_sell_quantity = 0  # 卖出总数量
    holding_quantity = 0  # 当前持仓数量
    buy_count = 0  # 买入次数
    sell_count = 0  # 卖出次数
    realized_profit = 0  # 已实现利润

    for tx in transactions:
        value = int(tx["value"]) / (10 ** int(tx["tokenDecimal"]))  # 将代币数量转换为实际数值
        if tx["contractAddress"].lower() == MBC_CONTRACT.lower():  # 只处理 MBC 的交易
            if tx["to"].lower() == ADDRESS.lower():  # 买入交易
                # 查找相同哈希中 USDT 的交易记录
                corresponding_tx = next((t for t in transactions if t["hash"] == tx["hash"] and t["contractAddress"].lower() == BSC_USD_CONTRACT.lower()), None)
                if corresponding_tx:
                    cost = int(corresponding_tx["value"]) / (10 ** int(corresponding_tx["tokenDecimal"]))
                    price = cost / value  # 买入价格
                    total_buy_cost += cost
                    total_buy_quantity += value
                    holding_quantity += value
                    buy_count += 1
                    print(f"buy MBC: {price:.4f} {value:.1f}/{holding_quantity:.1f}")
            elif tx["from"].lower() == ADDRESS.lower():  # 卖出交易
                # 查找相同哈希中 USDT 的交易记录
                corresponding_tx = next((t for t in transactions if t["hash"] == tx["hash"] and t["contractAddress"].lower() == BSC_USD_CONTRACT.lower()), None)
                if corresponding_tx:
                    revenue = int(corresponding_tx["value"]) / (10 ** int(corresponding_tx["tokenDecimal"]))
                    price = revenue / value  # 卖出价格
                    total_sell_revenue += revenue
                    total_sell_quantity += value
                    holding_quantity -= value
                    sell_count += 1
                    # 计算已实现利润
                    realized_profit += (price * value) - (total_buy_cost / total_buy_quantity * value)
                    print(f"sell MBC: {price:.4f} {value:.1f}/{holding_quantity:.1f}")

    # 平均买入/卖出价格
    avg_buy_price = round(total_buy_cost / total_buy_quantity, 4) if total_buy_quantity else 0
    avg_sell_price = round(total_sell_revenue / total_sell_quantity, 4) if total_sell_quantity else 0
    pnl = round(total_sell_revenue - total_buy_cost, 1)  # 总盈亏
    latest_price = get_latest_mbc_price()  # 当前 MBC 价格
    unrealized_pnl = round(holding_quantity * latest_price, 1)  # 持仓市值
    current_average_price = round(total_buy_cost / holding_quantity, 4) if holding_quantity else 0  # 当前平均成本
    unrealized_profit = round(holding_quantity * latest_price - total_buy_cost, 1) if latest_price != -1 else 0  # 未实现利润

    trade_result = {
        "mbc price": latest_price,
        "average_buy_price": avg_buy_price,
        "average_sell_price": avg_sell_price,
        "pnl": pnl,
        "holding_quantity": holding_quantity,
        "unrealized_pnl": unrealized_pnl,
        "buy_count": buy_count,
        "sell_count": sell_count,
        "current_average_price": current_average_price,
        "realized_profit": round(realized_profit, 1) ,
        "unrealized_profit": unrealized_profit
    }
    print(f"{trade_result}")
    return trade_result

# 主程序入口
if __name__ == "__main__":
    transactions = get_transactions()
    results = analyze_trades(transactions)
    print(json.dumps(results, indent=4))
