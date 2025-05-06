import math

# ------------------- 配置 -------------------
VIP_LEVELS = {
    "PC": {"stake": 100, "power_direct": 0, "power_indirect": 0, "dividend": 0},
    "VIP1": {"stake": 500, "power_direct": 0.08, "power_indirect": 0, "dividend": 0},
    "VIP2": {"stake": 2000, "power_direct": 0.13, "power_indirect": 0.06, "dividend": 0},
    "VIP3": {"stake": 10000, "power_direct": 0.16, "power_indirect": 0.10, "dividend": 0},
    "VIP4": {"stake": 25000, "power_direct": 0.20, "power_indirect": 0.14, "dividend": 0.01},
    "VIP5": {"stake": 50000, "power_direct": 0.26, "power_indirect": 0.17, "dividend": 0.03},
    "VIP6": {"stake": 150000, "power_direct": 0.35, "power_indirect": 0.20, "dividend": 0.05},
}

PARTNER_LEVELS = {
    "机构合伙人": 0.10,
    "一级合伙人": 0.08,
    "二级合伙人": 0.05,
    "无": 0.00
}

HASHBANK_APY = {
    30: 1.83,
    90: 7.5,
    180: 17.5,
    360: 40.0,
    720: 90.0
}

# ------------------- 输入参数 -------------------
vip_level = "VIP6"
direct_count = 4
member_stake = 10000
member_days = 720
mbc_price = 0.02
burned_nuts = 1_000_000
partner_level = "机构合伙人"
global_profit = 3_000_000
total_agents = 10

# ------------------- 计算参数 -------------------
indirect_count = direct_count * direct_count
team_count = (direct_count + indirect_count) * 10
stake_per_member = member_stake

# 获取 VIP 配置
vip_config = VIP_LEVELS[vip_level]
mine_stake = vip_config["stake"]
direct_reward_rate = vip_config["power_direct"]
indirect_reward_rate = vip_config["power_indirect"]
dividend_rate = vip_config["dividend"]
partner_service_rate = PARTNER_LEVELS[partner_level]

# 每位会员每日收益（按年收益率 / 365）
member_apy = HASHBANK_APY[member_days]
member_period_return = member_apy / 100
member_total_reward = stake_per_member * member_period_return
member_daily_reward = member_total_reward / member_days

# 直推和间推总收益
total_direct_reward_u = direct_count * member_daily_reward * direct_reward_rate
total_indirect_reward_u = indirect_count * member_daily_reward * indirect_reward_rate
total_promotion_u = total_direct_reward_u + total_indirect_reward_u

# nuts -> MBC -> USDT
nuts_reward = total_promotion_u * 1000
mbc_from_nuts = nuts_reward / burned_nuts * 800_000  # 每日释放 80 万 MBC
nuts_to_mbc_rate = mbc_from_nuts / nuts_reward if nuts_reward > 0 else 0
promotion_value_u = mbc_from_nuts * mbc_price

# hashbank 收益
my_hashbank_return = mine_stake * (HASHBANK_APY[member_days] / 100)
my_hashbank_daily = my_hashbank_return / member_days

# 合伙人服务费收益
team_daily_total_reward = team_count * member_daily_reward
partner_fee_u = team_daily_total_reward * partner_service_rate

# 季度分红
quarter_bonus = global_profit * dividend_rate / total_agents
quarter_bonus_daily = quarter_bonus / 90

# 年度汇总
annual_reward = (promotion_value_u + my_hashbank_daily + partner_fee_u + quarter_bonus_daily) * 360
months_to_roi = mine_stake / annual_reward * 12 if annual_reward > 0 else float('inf')

# ------------------- 输出 -------------------
print("\n📊 每日收益模拟：")
print(f"您的VIP等级: {vip_level}")
print(f"直推人数: {direct_count}, 间推人数: {indirect_count}")
print(f"直推/间推比例: 1:{indirect_count / direct_count:.1f}")
print(f"全团队人数: {team_count}")
print(f"每位会员每日收益: ${member_daily_reward:.2f}")

print("--- 推广奖励 ---")
print(f"直推奖励U: {total_direct_reward_u:.2f}")
print(f"间推奖励U: {total_indirect_reward_u:.2f}")
print(f"推广奖励总U: {total_promotion_u:.2f}")

print("--- nuts / mbc 奖励 ---")
print(f"奖励对应nuts: {nuts_reward:.0f}")
print(f"奖励对应mbc: {mbc_from_nuts:.2f}")
print(f"奖励usdt价值: {promotion_value_u:.2f}")
print(f"nuts/MBC兑换比: {nuts_to_mbc_rate:.2f}")

print("--- hashbank收益 ---")
print(f"自己质押周期收益: ${my_hashbank_return:.2f}")
print(f"折合每日收益: ${my_hashbank_daily:.2f}")

print("--- 合伙人服务费 ---")
print(f"团队每日服务费收益: ${partner_fee_u:.2f}")

print("--- 季度分红 ---")
print(f"季度红利奖励: ${quarter_bonus:.2f}")
print(f"季度红利每日平均: ${quarter_bonus_daily:.2f}")

print("--- 综合年化回报 ---")
print(f"年度奖励总计: ${annual_reward:.2f}")
print(f"ROI 回本月数: {months_to_roi:.1f}")

print("--- 每日综合收益汇总 ---")
print(f"每日综合收益: ${(promotion_value_u + my_hashbank_daily + partner_fee_u + quarter_bonus_daily):.2f}")
