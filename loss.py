def minimize(price_list):
    min_loss = float('inf')
    buy_year = sell_year = -1
    for buy in range(len(price_list)):
        for sell in range(buy + 1, len(price_list)):
            if price_list[sell] < price_list[buy]:
                loss = price_list[buy] - price_list[sell]
                if loss < min_loss:
                    min_loss = loss
                    buy_year, sell_year = buy + 1, sell + 1
    return buy_year, sell_year, min_loss

years = int(input())
prices = list(map(int, input().split()))
yb, ys, loss = minimize(prices)
print(yb, ys, loss)
